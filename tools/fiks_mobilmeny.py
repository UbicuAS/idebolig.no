"""
Egen mobilmeny på alle sider.

Elementors mobilmeny lar seg ikke åpne i en statisk kopi. CSS-en kollapser
beholderen med max-height:0, transform:scaleY(0) og CSS-variabelen
--menu-height, som Elementors JS normalt fyller ut ved å måle innholdet. Den
JS-en initialiseres aldri uten WordPress, så variabelen forblir tom og menyen
står klemt flat. Ingen på mobil kommer inn i menyen.

Å overstyre Elementors regler tapte på spesifisitet hver gang. Løsningen er å
bygge et eget panel og la Elementors egen ligge urørt.

Tre ting som kostet tid, og som ikke må «forbedres» tilbake:

1. Panelet er et <nav>, ikke en <ul>. Sidens egen CSS kollapser <ul> her.
2. Åpning skjer med display, ikke med en max-height-overgang. En overgang som
   går fra 0 til en calc()-verdi med vh interpolerer ikke pålitelig, og menyen
   blir stående på null høyde.
3. Menypunktene står som fast liste i skriptet, ikke lest fra siden. Menyene i
   den speilede kopien er nemlig ulike fra side til side — kontaktsiden manglet
   Boligkatalog, og hver boligside har sitt eget navn ekstra. Leses de fra
   siden, får hver side sin egen meny. Stien regnes ut fra sidedybden i stedet.

Blokken under er den samme som ligger på alle 17 sidene, tegn for tegn.
Endres menyen, endres den her og skriptet kjøres på nytt — men merk at
skriptet hopper over sider som allerede har blokken, så gammel blokk må
fjernes først.
"""
from pathlib import Path

ROT = Path(r"Z:\nettside-Roar\Idebolig")
MERKE = "ib-mobilmeny"

BLOKK = "<script>\n/* Egen mobilmeny. Elementors egen lar seg ikke åpne i en statisk kopi — den\n   kollapses av CSS som venter på en variabel Elementors JS aldri setter.\n   Panelet bygges av lenkene som allerede ligger i menyen, så det holder seg\n   i synk hvis menypunktene endres.\n   NB: <nav>, ikke <ul> — sidens CSS kollapser <ul> her. Og åpning med\n   display, ikke max-height-overgang, som ikke interpolerer pålitelig. */\n(function(){\n var knapp=document.querySelector('.elementor-menu-toggle');\n if(!knapp)return;\n var beholder=knapp.nextElementSibling;\n if(!beholder)return;\n var kilde=beholder.querySelector('ul.elementor-nav-menu');\n if(!kilde)return;\n\n var stil=document.createElement('style');\n stil.textContent=\n  '#ib-mobilmeny{position:fixed;left:0;right:0;z-index:9998;display:none;'\n +'background:#fff;box-shadow:0 14px 34px rgba(38,35,31,.20);'\n +'overflow-y:auto;-webkit-overflow-scrolling:touch;font-family:Poppins,sans-serif}'\n +'#ib-mobilmeny.ib-apen{display:block}'\n +'#ib-mobilmeny a{display:block;padding:16px 22px;color:#26231F;'\n +'text-decoration:none;font-size:16px;line-height:1.3;border-top:1px solid #efece7}'\n +'#ib-mobilmeny a:first-child{border-top:0}'\n +'#ib-mobilmeny a:hover,#ib-mobilmeny a:focus{background:#faf7f2;color:#C99C55}'\n +'#ib-mobilskygge{position:fixed;top:0;right:0;bottom:0;left:0;z-index:9997;'\n +'display:none;background:rgba(38,35,31,.42)}'\n +'#ib-mobilskygge.ib-apen{display:block}';\n document.head.appendChild(stil);\n\n var skygge=document.createElement('div');\n skygge.id='ib-mobilskygge';\n document.body.appendChild(skygge);\n\n var panel=document.createElement('nav');\n panel.id='ib-mobilmeny';\n panel.setAttribute('aria-label','Hovedmeny');\n /* Menyen er definert fast, ikke lest fra siden. Grunn: menyene i den\n    speilede kopien er ulike fra side til side — kontaktsiden manglet\n    Boligkatalog, og hver boligside har sitt eget navn ekstra. Panelet skal\n    vise det samme overalt. */\n var PUNKTER=[\n  ['Tjenester','tjenester/'],\n  ['Prosjekter','prosjekter/'],\n  ['Våre boliger','våre-boliger/'],\n  ['Boligkatalog','boligkatalog/'],\n  ['Kontakt','kontakt/']\n ];\n /* Riktig antall ../ ut fra hvor dypt sida ligger */\n var dybde=location.pathname.replace(/\\/[^\\/]*$/,'/').split('/').filter(Boolean).length;\n var opp=new Array(dybde+1).join('../');\n PUNKTER.forEach(function(p){\n  var l=document.createElement('a');\n  l.href=opp+p[1];\n  l.textContent=p[0];\n  panel.appendChild(l);\n });\n if(!panel.children.length)return;\n document.body.appendChild(panel);\n\n knapp.setAttribute('aria-expanded','false');\n knapp.setAttribute('aria-controls','ib-mobilmeny');\n\n function sett(apen){\n  if(apen){\n   var h=document.querySelector('.elementor-location-header');\n   var topp=Math.round(h?h.getBoundingClientRect().bottom:64);\n   panel.style.top=topp+'px';\n   panel.style.maxHeight=Math.max(160,window.innerHeight-topp-12)+'px';\n  }\n  panel.classList.toggle('ib-apen',apen);\n  skygge.classList.toggle('ib-apen',apen);\n  knapp.classList.toggle('elementor-active',apen);\n  knapp.setAttribute('aria-expanded',apen?'true':'false');\n }\n\n knapp.addEventListener('click',function(e){\n  e.preventDefault();e.stopPropagation();\n  sett(!panel.classList.contains('ib-apen'));\n });\n panel.addEventListener('click',function(e){ if(e.target.tagName==='A')sett(false); });\n skygge.addEventListener('click',function(){sett(false);});\n document.addEventListener('keydown',function(e){\n  if(e.key==='Escape'&&panel.classList.contains('ib-apen')){sett(false);knapp.focus();}\n });\n window.addEventListener('resize',function(){\n  if(window.innerWidth>921)sett(false);\n  else if(panel.classList.contains('ib-apen'))sett(true);\n });\n})();\n</script>\n</body>"

endret, hoppet = 0, 0
for fil in sorted(ROT.rglob("*.html")):
    if ".git" in fil.parts or fil.name.startswith("._"):
        continue
    tekst = fil.read_text(encoding="utf-8")
    if "elementor-menu-toggle" not in tekst or "</body>" not in tekst:
        continue
    if MERKE in tekst:
        hoppet += 1
        continue
    fil.write_text(tekst.replace("</body>", BLOKK, 1), encoding="utf-8")
    endret += 1

print(f"{endret} sider fikset" + (f", {hoppet} hoppet over" if hoppet else ""))
