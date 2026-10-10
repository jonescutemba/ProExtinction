// Share picture (site/og.png, 1200x630) and square logo (site/logo.png, 512x512) from logo.svg and the design tokens.
// Run after changing the logo or colours: NODE_PATH=$(npm root -g) node tools/og.js
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const root = path.resolve(__dirname, '..');
const logo = 'data:image/svg+xml,' + encodeURIComponent(fs.readFileSync(path.join(__dirname, 'assets/logo.svg'), 'utf8').replace(/currentColor/g, '#000'));
const font = 'file://' + path.join(root, 'site/fonts/anton-latin-400-normal.woff2');
const page = (w, h, body) => `<!doctype html><html><head><style>
@font-face{font-family:Anton;src:url(${font})}
html,body{margin:0;width:${w}px;height:${h}px;background:#0b0708;color:#e9e4e4;font-family:Anton,sans-serif;overflow:hidden}
.logo{-webkit-mask:url("${logo}") center/contain no-repeat;background:#e8484d}
</style></head><body>${body}</body></html>`;
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
  const p = await b.newPage();
  await p.setViewportSize({ width: 1200, height: 630 });
  await p.setContent(page(1200, 630, `<div style="display:flex;align-items:center;gap:56px;height:100%;padding:0 90px;box-sizing:border-box">
    <div class="logo" style="width:300px;height:300px;flex:none"></div>
    <div><div style="font-size:112px;line-height:.95;letter-spacing:2px">PRO<br>EXTINCTION</div>
    <div style="margin-top:28px;font:500 34px/1.3 sans-serif;color:#b9b0b0">Together, we end suffering.</div>
    <div style="margin-top:34px;height:6px;width:160px;background:#e8484d"></div></div></div>`), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(root, 'site/og.png') });
  await p.setViewportSize({ width: 512, height: 512 });
  await p.setContent(page(512, 512, '<div class="logo" style="width:400px;height:400px;margin:56px"></div>'), { waitUntil: 'load' });
  await p.screenshot({ path: path.join(root, 'site/logo.png') });
  await b.close();
})();
