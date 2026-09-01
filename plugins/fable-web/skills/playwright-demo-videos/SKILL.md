---
name: playwright-demo-videos
description: Use when recording a polished UI demo/walkthrough video of a web app with Playwright. Covers cursor and subtitle overlay injection, moveAndClick/typeSlowly helpers, pacing values, video output handling, and recording gotchas.
---

# Playwright Demo Videos

Playwright's `recordVideo` context option captures WebM video, but raw automation looks robotic: no visible cursor, instant fills, teleporting clicks. These helpers fix that.

## Recording Setup

```javascript
const context = await browser.newContext({
  recordVideo: { dir: VIDEO_DIR, size: { width: 1280, height: 720 } },
  viewport: { width: 1280, height: 720 },
});
```

Playwright writes the video to a random filename inside `dir`; copy it to a stable name after `context.close()`:

```javascript
await context.close();
const video = page.video();
if (video) {
  fs.copyFileSync(await video.path(), path.join(VIDEO_DIR, 'demo-feature.webm'));
}
```

Popup windows record to separate video files; capture popup pages explicitly and merge afterwards if needed.

## Cursor Overlay

Headless recordings have no visible cursor. Inject an SVG arrow that follows `mousemove`:

```javascript
async function injectCursor(page) {
  await page.evaluate(() => {
    if (document.getElementById('demo-cursor')) return;
    const cursor = document.createElement('div');
    cursor.id = 'demo-cursor';
    cursor.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M5 3L19 12L12 13L9 20L5 3Z" fill="white" stroke="black" stroke-width="1.5" stroke-linejoin="round"/>
    </svg>`;
    cursor.style.cssText = `
      position: fixed; z-index: 999999; pointer-events: none;
      width: 24px; height: 24px;
      transition: left 0.1s, top 0.1s;
      filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.3));
    `;
    cursor.style.left = '0px';
    cursor.style.top = '0px';
    document.body.appendChild(cursor);
    document.addEventListener('mousemove', (e) => {
      cursor.style.left = e.clientX + 'px';
      cursor.style.top = e.clientY + 'px';
    });
  });
}
```

The overlay lives in the DOM, so navigation destroys it - re-inject after every `page.goto` (same for the subtitle bar below).

## Click and Type Helpers

Move the mouse to the target with intermediate steps before clicking; never teleport:

```javascript
async function moveAndClick(page, locator, label, opts = {}) {
  const { postClickDelay = 800, ...clickOpts } = opts;
  const el = typeof locator === 'string' ? page.locator(locator).first() : locator;
  const visible = await el.isVisible().catch(() => false);
  if (!visible) {
    console.error(`WARNING: moveAndClick skipped - "${label}" not visible`);
    return false;
  }
  try {
    await el.scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    const box = await el.boundingBox();
    if (box) {
      await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 10 });
      await page.waitForTimeout(400);
    }
    await el.click(clickOpts);
  } catch (e) {
    console.error(`WARNING: moveAndClick failed on "${label}": ${e.message}`);
    return false;
  }
  await page.waitForTimeout(postClickDelay);
  return true;
}

async function typeSlowly(page, locator, text, label, charDelay = 35) {
  const el = typeof locator === 'string' ? page.locator(locator).first() : locator;
  const visible = await el.isVisible().catch(() => false);
  if (!visible) {
    console.error(`WARNING: typeSlowly skipped - "${label}" not visible`);
    return false;
  }
  await moveAndClick(page, el, label);
  await el.fill('');
  await el.pressSequentially(text, { delay: charDelay });
  await page.waitForTimeout(500);
  return true;
}
```

Pass a descriptive `label` on every call so failures are traceable in the log; the helpers warn instead of throwing so one broken selector does not abort the recording, but silent `catch {}` blocks are what make recordings fail mysteriously.

## Pacing

Values that feel natural to a human viewer:

| Moment | Pause |
|--------|-------|
| After login | 4 s |
| After navigation | 3 s |
| After clicking a button | 2 s |
| Between major steps | 1.5-2 s |
| After the final action | 3 s |
| Typing delay | 25-40 ms per character |

Smooth scrolling instead of jumps:

```javascript
await page.evaluate(() => window.scrollTo({ top: 400, behavior: 'smooth' }));
await page.waitForTimeout(1500);
```

## Subtitle Bar

```javascript
async function injectSubtitleBar(page) {
  await page.evaluate(() => {
    if (document.getElementById('demo-subtitle')) return;
    const bar = document.createElement('div');
    bar.id = 'demo-subtitle';
    bar.style.cssText = `
      position: fixed; bottom: 0; left: 0; right: 0; z-index: 999998;
      text-align: center; padding: 12px 24px;
      background: rgba(0, 0, 0, 0.75);
      color: white; font-family: -apple-system, "Segoe UI", sans-serif;
      font-size: 16px; font-weight: 500; letter-spacing: 0.3px;
      transition: opacity 0.3s; pointer-events: none;
    `;
    bar.style.opacity = '0';
    document.body.appendChild(bar);
  });
}

async function showSubtitle(page, text) {
  await page.evaluate((t) => {
    const bar = document.getElementById('demo-subtitle');
    if (!bar) return;
    bar.textContent = t || '';
    bar.style.opacity = t ? '1' : '0';
  }, text);
  if (text) await page.waitForTimeout(800);
}
```

Keep subtitles under 60 characters, `Step N - Action` format; clear with `showSubtitle(page, '')` when the UI speaks for itself.

## Gotchas

- Overlays (cursor, subtitle bar) vanish on navigation - re-inject after every `goto`.
- The recorded file has a random name; copy it via `page.video().path()` to a stable output.
- Native `<select>` placeholder options often have `value="0"` or `value=""` and text like "Select..."; dump `Array.from(el.options).map(o => ({ value: o.value, text: o.text }))` and skip placeholders before picking.
- Field types differ from assumptions: inputs vs textareas, custom dropdowns vs `<select>`, contenteditable comment boxes with `@mention`/`#tag` support. Dump visible `input, select, textarea, button, [contenteditable]` elements per page before scripting selectors.
- In table-driven forms, map each `input[type="number"]` to its column header instead of assuming all numeric inputs mean the same thing.
- Modals feel abrupt without a read pause before confirming.
- Send buttons are often disabled until the input has content - type first, then click.
