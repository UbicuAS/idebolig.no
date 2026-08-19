"""
Informasjonskapsel-banner på alle sider.

Siden setter ingen sporingskapsler: analyse/Site Kit ble fjernet i IB3.4, og
det eneste som kan sette en kapsel er Cloudflare Turnstile (botvern) på
kontaktskjemaet. Banneren sier derfor ærlig at kun nødvendige kapsler brukes,
med en «Les mer»-tekst i selve banneren (siden har ingen personvernside).
Ett valg («Godta») huskes i localStorage — banneren setter altså ingen kapsel
selv, og vises ikke igjen etter lukking.

Utseende: kort nede til venstre på skrivebord (maks 420 px), fullbredde bånd
nederst på mobil (<= 640 px), i sidens stilspråk (Poppins, #26231F på hvitt,
gull #C99C55). z-index 9996 — bevisst UNDER mobilmenyens skygge/panel
(9997/9998), så et åpent menypanel legger seg over banneren.

Blokken settes inn som ÉN linje rett før </body> (binærtrygt, linjeskiftstil
i filene røres ikke). Skriptet er idempotent: sider som allerede har merket
ib-cookiebanner hoppes over. Endres banneren, fjern gammel blokk først.
"""
from pathlib import Path

ROT = Path(r"Z:\nettside-Roar\Idebolig")
MERKE = "ib-cookiebanner"

JS = (
    "(function(){"
    "try{if(localStorage.getItem('ib-cookievalg'))return;}catch(e){return;}"
    "var stil=document.createElement('style');"
    "stil.textContent='"
    "#ib-cookiebanner{position:fixed;left:18px;bottom:18px;z-index:9996;max-width:420px;"
    "background:#fff;color:#26231F;font-family:Poppins,sans-serif;border-radius:14px;"
    "box-shadow:0 14px 34px rgba(38,35,31,.22);padding:20px 22px;line-height:1.5;font-size:14px}"
    "#ib-cookiebanner h2{margin:0 0 6px;font-size:16px;font-weight:700;color:#26231F}"
    "#ib-cookiebanner p{margin:0 0 12px}"
    "#ib-cookiebanner .ib-ck-detalj{display:none;margin:0 0 12px;color:#5c564d;font-size:13px}"
    "#ib-cookiebanner.ib-ck-apen .ib-ck-detalj{display:block}"
    "#ib-cookiebanner .ib-ck-rad{display:flex;gap:14px;align-items:center;flex-wrap:wrap}"
    "#ib-cookiebanner button{font-family:Poppins,sans-serif;cursor:pointer}"
    "#ib-cookiebanner .ib-ck-ok{background:#C99C55;color:#fff;border:0;border-radius:8px;"
    "padding:12px 26px;min-height:44px;font-size:14px;font-weight:700}"
    "#ib-cookiebanner .ib-ck-ok:hover,#ib-cookiebanner .ib-ck-ok:focus{background:#b3873f}"
    "#ib-cookiebanner .ib-ck-mer{background:none;border:0;padding:12px 2px;min-height:44px;color:#8a7147;"
    "font-size:14px;text-decoration:underline}"
    "#ib-cookiebanner .ib-ck-mer:hover,#ib-cookiebanner .ib-ck-mer:focus{color:#C99C55}"
    "@media(max-width:640px){#ib-cookiebanner{left:0;right:0;bottom:0;max-width:none;"
    "border-radius:14px 14px 0 0;padding:18px 18px calc(18px + env(safe-area-inset-bottom));"
    "box-shadow:0 -10px 30px rgba(38,35,31,.25)}"
    "#ib-cookiebanner .ib-ck-ok{flex:1 1 auto}}"
    "';document.head.appendChild(stil);"
    "var b=document.createElement('div');"
    "b.id='ib-cookiebanner';"
    "b.setAttribute('role','dialog');"
    "b.setAttribute('aria-modal','false');"
    "b.setAttribute('aria-label','Informasjonskapsler');"
    "b.innerHTML='<h2>Informasjonskapsler<\\/h2>'"
    "+'<p>Vi bruker kun n\\u00f8dvendige informasjonskapsler \\u2014 ingen sporing og ingen analyse.<\\/p>'"
    "+'<p class=\"ib-ck-detalj\">Den eneste kapselen kommer fra Cloudflare Turnstile p\\u00e5 kontaktsiden og "
    "brukes bare til \\u00e5 skille folk fra roboter n\\u00e5r du sender skjemaet. Valget ditt her lagres kun "
    "lokalt i din egen nettleser og sendes ikke til noen.<\\/p>'"
    "+'<div class=\"ib-ck-rad\">"
    "<button type=\"button\" class=\"ib-ck-ok\">Godta<\\/button>"
    "<button type=\"button\" class=\"ib-ck-mer\" aria-expanded=\"false\">Les mer<\\/button><\\/div>';"
    "document.body.appendChild(b);"
    "b.querySelector('.ib-ck-ok').addEventListener('click',function(){"
    "try{localStorage.setItem('ib-cookievalg','1');}catch(e){}"
    "b.parentNode.removeChild(b);});"
    "var mer=b.querySelector('.ib-ck-mer');"
    "mer.addEventListener('click',function(){"
    "var apen=!b.classList.contains('ib-ck-apen');"
    "b.classList.toggle('ib-ck-apen',apen);"
    "mer.setAttribute('aria-expanded',apen?'true':'false');"
    "mer.textContent=apen?'Skjul':'Les mer';});"
    "})();"
)

BLOKK = "<script>/* ib-cookiebanner: kun nodvendige kapsler, se tools/legg_inn_cookiebanner.py */" + JS + "</script></body>"

endret, hoppet = 0, 0
for fil in sorted(ROT.rglob("*.html")):
    if ".git" in fil.parts or fil.name.startswith("._"):
        continue
    data = fil.read_bytes()
    if MERKE.encode() in data:
        hoppet += 1
        continue
    if b"</body>" not in data:
        continue
    fil.write_bytes(data.replace(b"</body>", BLOKK.encode("utf-8"), 1))
    endret += 1

print(f"{endret} sider fikk banner" + (f", {hoppet} hoppet over" if hoppet else ""))
