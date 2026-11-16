// Renderiza os HTML gerados por gerar.py em PNG (Playwright pré-instalado).
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch();
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 1 });
    await p.goto('file://' + j.html, { waitUntil: 'networkidle' }).catch(() => {});
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({ path: j.png });
    await p.close();
    console.log('ok', j.png.split('/').pop());
  }
  await b.close();
})();
