// Vyrenderuje návrhy loga a bannerů do PNG.
// Použití: node render.js  (ze složky videa/branding)
const { chromium } = require("playwright");
const path = require("path");

const DIR = __dirname;
const F = path.resolve(DIR, "../remotion/node_modules/@fontsource/oswald/files");
const IMG = path.resolve(DIR, "../01-praha-1926/flow");
const fs = require("fs");
const MIME = { ".png": "image/png", ".woff2": "font/woff2", ".jpg": "image/jpeg" };
const url = (p) => `data:${MIME[path.extname(p)]};base64,${fs.readFileSync(p).toString("base64")}`;

const css = `
@font-face{font-family:Oswald;font-weight:500;src:url(${url(F + "/oswald-latin-500-normal.woff2")})}
@font-face{font-family:Oswald;font-weight:500;src:url(${url(F + "/oswald-latin-ext-500-normal.woff2")});unicode-range:U+0100-024F}
@font-face{font-family:Oswald;font-weight:700;src:url(${url(F + "/oswald-latin-700-normal.woff2")})}
@font-face{font-family:Oswald;font-weight:700;src:url(${url(F + "/oswald-latin-ext-700-normal.woff2")});unicode-range:U+0100-024F}
*{margin:0;box-sizing:border-box}
body{font-family:Oswald,sans-serif}
:root{--ink:#2a221a;--paper:#f3e9d6;--orange:#ff7a1a}
`;
const bust = url(path.join(DIR, "hlava.png"));

// profilovka 800×800 (YouTube ji ořízne do kruhu)
const profile = (ring, inner) => `
<div style="width:800px;height:800px;background:${ring};display:flex;align-items:center;justify-content:center">
  <div style="width:700px;height:700px;border-radius:50%;overflow:hidden;border:14px solid ${inner};background:#efe6d6">
    <img src="${bust}" style="width:100%;height:100%;object-fit:cover;transform:translateY(40px) scale(1.08)">
  </div>
</div>`;

// banner 2560×1440, bezpečná zóna pro všechna zařízení je 1546×423 uprostřed
const banner = ({ bg, title, sub, foot, filter, size = 150 }) => `
<div style="position:relative;width:2560px;height:1440px;overflow:hidden;background:var(--ink)">
  <img src="${url(path.join(IMG, bg))}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:${filter}">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse 70% 45% at 50% 50%, rgba(42,34,26,.82), rgba(42,34,26,.35) 70%, rgba(42,34,26,.15))"></div>
  <div style="position:absolute;left:507px;top:508px;width:1546px;height:423px;display:flex;align-items:center;gap:56px;padding:0 40px">
    <div style="flex:0 0 330px;height:330px;border-radius:50%;overflow:hidden;border:12px solid var(--orange);background:#efe6d6">
      <img src="${bust}" style="width:100%;height:100%;object-fit:cover;transform:translateY(26px) scale(1.08)">
    </div>
    <div style="color:var(--paper)">
      <div style="font-weight:700;font-size:${size}px;line-height:1;letter-spacing:4px;white-space:nowrap;text-shadow:7px 7px 0 var(--orange)">${title}</div>
      <div style="font-weight:500;font-size:50px;margin-top:22px">${sub}</div>
      <div style="display:inline-block;margin-top:22px;font-weight:500;font-size:36px;color:var(--ink);background:var(--orange);padding:6px 22px;border-radius:6px">${foot}</div>
    </div>
  </div>
</div>`;


// náhledovka videa 1280×720
const thumb = ({ bg, big, badge }) => `
<div style="position:relative;width:1280px;height:720px;overflow:hidden;background:var(--ink)">
  <img src="${url(path.join(DIR, bg))}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.12);transform-origin:38% 62%;filter:saturate(1.15) contrast(1.05)">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(42,34,26,.85) 0%, rgba(42,34,26,.35) 32%, rgba(42,34,26,0) 50%)"></div>
  <div style="position:absolute;top:22px;left:0;right:0;text-align:center;font-weight:700;font-size:150px;line-height:1;color:#fff;letter-spacing:2px;-webkit-text-stroke:6px var(--ink);paint-order:stroke fill;text-shadow:8px 8px 0 var(--orange)">${big}</div>
  <div style="position:absolute;right:28px;bottom:28px;font-weight:700;font-size:92px;line-height:1;color:var(--ink);background:var(--orange);padding:6px 26px 10px;border-radius:12px;border:6px solid var(--ink);transform:rotate(-4deg)">${badge}</div>
</div>`;


// varianta B: rozmazané a ztlumené okolí, ostrá postava s autem, sytější barvy
const thumbB = ({ bg, big, badge }) => `
<div style="position:relative;width:1280px;height:720px;overflow:hidden;background:var(--ink)">
  <img src="${url(path.join(DIR, bg))}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.12);transform-origin:38% 62%;filter:blur(9px) saturate(.45) brightness(.6)">
  <img src="${url(path.join(DIR, bg))}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.12);transform-origin:38% 62%;filter:saturate(1.45) contrast(1.12);-webkit-mask-image:radial-gradient(ellipse 46% 52% at 52% 62%, #000 62%, transparent 100%)">
  <div style="position:absolute;top:22px;left:0;right:0;text-align:center;font-weight:700;font-size:150px;line-height:1;color:#fff;letter-spacing:2px;-webkit-text-stroke:6px var(--ink);paint-order:stroke fill;text-shadow:8px 8px 0 var(--orange)">${big}</div>
  <div style="position:absolute;right:28px;bottom:28px;font-weight:700;font-size:92px;line-height:1;color:var(--ink);background:var(--orange);padding:6px 26px 10px;border-radius:12px;border:6px solid var(--ink);transform:rotate(-4deg)">${badge}</div>
</div>`;


// náhledovka shortu 1080×1920: velká scéna uprostřed, text v bezpečné střední části
const shortThumb = ({ bg, top, bottom, shift = -230, size = 150 }) => `
<div style="position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--ink)">
  <img src="${url(path.join(DIR, bg))}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:blur(30px) brightness(.45) saturate(.6);transform:scale(1.2)">
  <div style="position:absolute;left:0;top:520px;width:1080px;height:1000px;overflow:hidden;border-top:10px solid var(--orange);border-bottom:10px solid var(--orange)">
    <img src="${url(path.join(DIR, bg))}" style="position:absolute;height:1000px;left:${shift}px;filter:saturate(1.35) contrast(1.1)">
  </div>
  <div style="position:absolute;top:185px;left:40px;right:40px;text-align:center;font-weight:700;font-size:${size}px;line-height:1;color:#fff;-webkit-text-stroke:7px var(--ink);paint-order:stroke fill;text-shadow:9px 9px 0 var(--orange)">${top}</div>
  <div style="position:absolute;top:1560px;left:0;right:0;display:flex;justify-content:center">
    <div style="font-weight:700;font-size:100px;line-height:1;color:var(--ink);background:var(--orange);padding:10px 36px 16px;border-radius:14px;border:7px solid var(--ink);transform:rotate(-3deg)">${bottom}</div>
  </div>
</div>`;

// náhled bezpečné zóny (jen pro kontrolu)
const safe = (inner) => inner.replace('<div style="position:absolute;left:507px', '<div style="position:absolute;left:507px;top:508px;width:1546px;height:423px;outline:6px dashed #0f0;z-index:9"></div><div style="position:absolute;left:507px');

const jobs = [
  ["nahled-short-4-bacily.png", 1080, 1920, shortThumb({ bg: "nahled-zaklad-S23.png", top: "NEVIDITELNÝ<br>ZABIJÁK", bottom: "PRAHA 1926", shift: -349, size: 140 })],
  ["nahled-short-2-karta.png", 1080, 1920, shortThumb({ bg: "nahled-zaklad-S11.png", top: "ZAPLATÍŠ<br>KARTOU?", bottom: "PRAHA 1926", shift: -250 })],
  ["nahled-short-5-mlcet.png", 1080, 1920, shortThumb({ bg: "nahled-zaklad-S34.png", top: "DOKÁZAL BYS<br>MLČET?", bottom: "PRAHA 1926", shift: -356, size: 140 })],
  ["nahled-short-1-auto.png", 1080, 1920, shortThumb({ bg: "nahled-zaklad-S04.png", top: "SRAZÍ TĚ<br>ZPRAVA!", bottom: "PRAHA 1926" })],
  ["nahled-praha-1926-B.png", 1280, 720, thumbB({ bg: "nahled-zaklad-S04.png", big: "PŘEŽIL BYS?", badge: "1926" })],
  ["nahled-praha-1926.png", 1280, 720, thumb({ bg: "nahled-zaklad-S04.png", big: "PŘEŽIL BYS?", badge: "1926" })],
  ["logo-a-oranzovy-kruh.png", 800, 800, profile("#ff7a1a", "#2a221a")],
  ["logo-b-tmavy-kruh.png", 800, 800, profile("#2a221a", "#ff7a1a")],
  ["banner-tenkrat.png", 2560, 1440, banner({
    bg: "last/S33.png", filter: "sepia(.35) brightness(.9)",
    title: "TENKRÁT", sub: "Jak by ses měl, kdyby ses narodil o 100 let dřív?",
    foot: "Animovaná historie Česka a Slovenska" })],
  ["banner-oranzova-mikina.png", 2560, 1440, banner({
    bg: "S05.png", filter: "sepia(.2) brightness(.95)",
    title: "ORANŽOVÁ MIKINA", size: 118, sub: "Kluk z budoucnosti uprostřed dějin",
    foot: "Přežil bys? · Animovaná historie" })],
];

(async () => {
  const browser = await chromium.launch();
  for (const [name, w, h, html] of jobs) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.setContent(`<style>${css}</style>${html}`, { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(DIR, name) });
    if (name.startsWith("banner")) {
      await page.setContent(`<style>${css}</style>${safe(html)}`, { waitUntil: "load" });
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({ path: path.join(DIR, "_kontrola-" + name) });
    }
    await page.close();
    console.log("hotovo", name);
  }
  await browser.close();
})();
