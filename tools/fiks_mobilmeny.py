"""
Egen mobilmeny på alle sider.

Elementors mobilmeny lar seg ikke åpne i en statisk kopi. CSS-en kollapser
beholderen med max-height:0, transform:scaleY(0) og CSS-variabelen
--menu-height, som Elementors JS normalt fyller ut ved å måle innholdet. Den
JS-en initialiseres aldri uten WordPress, så variabelen forblir tom og menyen
står klemt flat. Ingen på mobil kommer inn i menyen.

Å overstyre Elementors regler tapte på spesifisitet hver gang. Løsningen er å
bygge et eget panel av lenkene som allerede finnes, og la Elementors egen
ligge urørt.

To ting som kostet tid, og som ikke må «forbedres» tilbake:

1. Panelet er et <nav>, ikke en <ul>. Sidens egen CSS kollapser <ul> her.
2. Åpning skjer med display, ikke med en max-height-overgang. En overgang som
   går fra 0 til en calc()-verdi med vh interpolerer ikke pålitelig, og menyen
   blir stående på null høyde.
"""
from pathlib import Path

ROT = Path(r"Z:\nettside-Roar\Idebolig")
MERKE = "ib-mobilmeny"

BLOKK = """<script>
/* Egen mobilmeny. Elementors egen lar seg ikke åpne i en statisk kopi — den
   kollapses av CSS som venter på en variabel Elementors JS aldri setter.
   Panelet bygges av lenkene som allerede ligger i menyen, så det holder seg
   i synk hvis menypunktene endres.
   NB: <nav>, ikke <ul> — sidens CSS kollapser <ul> her. Og åpning med
   display, ikke max-height-overgang, som ikke interpolerer pålitelig. */
(function(){
 var knapp=document.querySelector('.elementor-menu-toggle');
 if(!knapp)return;
 var beholder=knapp.nextElementSibling;
 if(!beholder)return;
 var kilde=beholder.querySelector('ul.elementor-nav-menu');
 if(!kilde)return;

 var stil=document.createElement('style');
 stil.textContent=
  '#ib-mobilmeny{position:fixed;left:0;right:0;z-index:9998;display:none;'
 +'background:#fff;box-shadow:0 14px 34px rgba(38,35,31,.20);'
 +'overflow-y:auto;-webkit-overflow-scrolling:touch;font-family:Poppins,sans-serif}'
 +'#ib-mobilmeny.ib-apen{display:block}'
 +'#ib-mobilmeny a{display:block;padding:16px 22px;color:#26231F;'
 +'text-decoration:none;font-size:16px;line-height:1.3;border-top:1px solid #efece7}'
 +'#ib-mobilmeny a:first-child{border-top:0}'
 +'#ib-mobilmeny a:hover,#ib-mobilmeny a:focus{background:#faf7f2;color:#C99C55}'
 +'#ib-mobilskygge{position:fixed;top:0;right:0;bottom:0;left:0;z-index:9997;'
 +'display:none;background:rgba(38,35,31,.42)}'
 +'#ib-mobilskygge.ib-apen{display:block}';
 document.head.appendChild(stil);

 var skygge=document.createElement('div');
 skygge.id='ib-mobilskygge';
 document.body.appendChild(skygge);

 var panel=document.createElement('nav');
 panel.id='ib-mobilmeny';
 panel.setAttribute('aria-label','Hovedmeny');
 [].forEach.call(kilde.querySelectorAll(':scope > li > a'),function(a){
  var l=document.createElement('a');
  l.href=a.getAttribute('href')||'#';
  l.textContent=(a.textContent||'').trim();
  panel.appendChild(l);
 });
 if(!panel.children.length)return;
 document.body.appendChild(panel);

 knapp.setAttribute('aria-expanded','false');
 knapp.setAttribute('aria-controls','ib-mobilmeny');

 function sett(apen){
  if(apen){
   var h=document.querySelector('.elementor-location-header');
   var topp=Math.round(h?h.getBoundingClientRect().bottom:64);
   panel.style.top=topp+'px';
   panel.style.maxHeight=Math.max(160,window.innerHeight-topp-12)+'px';
  }
  panel.classList.toggle('ib-apen',apen);
  skygge.classList.toggle('ib-apen',apen);
  knapp.classList.toggle('elementor-active',apen);
  knapp.setAttribute('aria-expanded',apen?'true':'false');
 }

 knapp.addEventListener('click',function(e){
  e.preventDefault();e.stopPropagation();
  sett(!panel.classList.contains('ib-apen'));
 });
 panel.addEventListener('click',function(e){ if(e.target.tagName==='A')sett(false); });
 skygge.addEventListener('click',function(){sett(false);});
 document.addEventListener('keydown',function(e){
  if(e.key==='Escape'&&panel.classList.contains('ib-apen')){sett(false);knapp.focus();}
 });
 window.addEventListener('resize',function(){
  if(window.innerWidth>921)sett(false);
  else if(panel.classList.contains('ib-apen'))sett(true);
 });
})();
</script>
</body>"""

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
