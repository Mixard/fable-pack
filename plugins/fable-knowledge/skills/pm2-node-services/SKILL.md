---
name: pm2-node-services
description: Use when running dev servers or Python services under PM2, especially on Windows. Covers the .cjs config requirement, exact framework bin paths for Vite/Next/Nuxt, the Python child-process wrapper, and process-list persistence.
---

# PM2 Service Configs

## Config file

PM2 config in an ESM project ("type": "module") needs the `.cjs` extension: `ecosystem.config.cjs`, CommonJS `module.exports`.

```javascript
module.exports = {
  apps: [
    {
      name: 'web-3000',
      cwd: './packages/web',
      script: 'node_modules/vite/bin/vite.js',
      args: '--port 3000',
      env: { NODE_ENV: 'development' }
    },
    {
      name: 'api-8000',
      cwd: './backend',
      script: 'start.cjs',
      env: { PYTHONUNBUFFERED: '1' }
    }
  ]
}
```

On Windows, add `interpreter: 'C:/Program Files/nodejs/node.exe'` to each app — PM2's default interpreter resolution is unreliable there.

## Framework entry points

Pointing `script` at the framework's real bin file (not an npm script) keeps PM2 in control of the actual process:

| Framework | script | args | Default port |
|-----------|--------|------|--------------|
| Vite | `node_modules/vite/bin/vite.js` | `--port {port}` | 5173 |
| Next.js | `node_modules/next/dist/bin/next` | `dev -p {port}` | 3000 |
| Nuxt | `node_modules/nuxt/bin/nuxt.mjs` | `dev --port {port}` | 3000 |
| Express/Node | `src/index.js` or `server.js` | — | 3000 |
| FastAPI (via wrapper) | `start.cjs` | — | 8000 |

## Python under PM2

Running Python directly via PM2 `interpreter` is flaky on Windows; a Node wrapper script is the reliable route:

```javascript
// backend/start.cjs
const { spawn } = require('child_process');
const proc = spawn('python', ['-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000', '--reload'], {
  cwd: __dirname, stdio: 'inherit', windowsHide: true
});
proc.on('close', (code) => process.exit(code));
```

`windowsHide: true` prevents a console window flashing per restart.

## Operations

```bash
pm2 start ecosystem.config.cjs && pm2 save   # first run; save enables `pm2 start all` later
pm2 start ecosystem.config.cjs --only web-3000
pm2 stop all / pm2 restart all / pm2 logs {name} / pm2 monit / pm2 status
pm2 resurrect                                # restore saved process list after reboot
```

Opening a separate Windows Terminal window for logs/monitor:

```bash
start wt.exe -d "C:/path/to/project" pwsh -NoExit -c "pm2 logs web-3000"
```
