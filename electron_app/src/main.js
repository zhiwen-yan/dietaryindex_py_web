"use strict";

const fs = require("node:fs");
const path = require("node:path");
const { app, BrowserWindow, dialog, Menu, session, shell } = require("electron");
const {
  ServiceManager,
  requestStatus,
  resolveLayout,
} = require("./service-manager");

let mainWindow = null;
let splashWindow = null;
let services = null;
let quitting = false;

function argumentValue(prefix) {
  const item = process.argv.find((argument) => argument.startsWith(`${prefix}=`));
  return item ? item.slice(prefix.length + 1) : null;
}

function isTrustedNavigation(target, siteUrl) {
  try {
    return new URL(target).origin === new URL(siteUrl).origin;
  } catch {
    return false;
  }
}

function installSecurityPolicy(siteUrl) {
  const trustedOrigin = new URL(siteUrl).origin;
  session.defaultSession.setPermissionRequestHandler((_webContents, _permission, callback) => callback(false));
  session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
    let headers = details.responseHeaders ?? {};
    try {
      if (new URL(details.url).origin === trustedOrigin) {
        headers = {
          ...headers,
          "Content-Security-Policy": [
            "default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; " +
            "script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; " +
            "img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self'; " +
            "form-action 'self'",
          ],
        };
      }
    } catch {
      // Leave non-URL responses unchanged.
    }
    callback({ responseHeaders: headers });
  });
}

function createSplash() {
  splashWindow = new BrowserWindow({
    width: 500,
    height: 260,
    frame: false,
    resizable: false,
    show: false,
    backgroundColor: "#fefcf8",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });
  splashWindow.loadFile(path.join(__dirname, "splash.html"));
  splashWindow.once("ready-to-show", () => splashWindow?.show());
}

function createApplicationMenu(logDir) {
  const template = [
    {
      label: "File",
      submenu: [
        { label: "Open logs folder", click: () => shell.openPath(logDir) },
        { type: "separator" },
        { role: "quit" },
      ],
    },
    {
      label: "View",
      submenu: [{ role: "resetZoom" }, { role: "zoomIn" }, { role: "zoomOut" }, { role: "togglefullscreen" }],
    },
    {
      label: "Help",
      submenu: [
        {
          label: "About DietaryIndex",
          click: () => dialog.showMessageBox({
            type: "info",
            title: "About DietaryIndex",
            message: `DietaryIndex ${app.getVersion()}`,
            detail: "Electron desktop host with the validated Python compute engine, Next.js interface, FastAPI, and local MCP integration.",
          }),
        },
      ],
    },
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

function createMainWindow(siteUrl, logDir) {
  installSecurityPolicy(siteUrl);
  createApplicationMenu(logDir);
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 920,
    minWidth: 1024,
    minHeight: 700,
    show: false,
    backgroundColor: "#fefcf8",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webviewTag: false,
    },
  });
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    try {
      const parsed = new URL(url);
      if (parsed.protocol === "https:") shell.openExternal(parsed.toString());
    } catch {
      // Invalid and non-HTTPS links remain blocked.
    }
    return { action: "deny" };
  });
  mainWindow.webContents.on("will-navigate", (event, url) => {
    if (!isTrustedNavigation(url, siteUrl)) event.preventDefault();
  });
  mainWindow.once("ready-to-show", () => {
    splashWindow?.destroy();
    splashWindow = null;
    mainWindow?.show();
  });
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
  mainWindow.loadURL(siteUrl);
}

async function runSmokeTest(runtime, outputPath) {
  const checks = {
    site: await requestStatus(runtime.siteUrl, {}, 5000),
    calculator: await requestStatus(`${runtime.siteUrl}/calculator?index=DII`, {}, 5000),
    apiProxy: await requestStatus(`${runtime.siteUrl}/api/dietary/v1/indices`, {}, 5000),
  };
  let consistency = null;
  let consistencyError = null;
  const consistencyFixture = argumentValue("--consistency-fixture");
  if (consistencyFixture) {
    try {
      consistency = await computeConsistency(runtime.siteUrl, {
        fixturePath: consistencyFixture,
        mappingPath: argumentValue("--consistency-mapping"),
        indexKey: argumentValue("--consistency-index") || "HEI2020",
      });
    } catch (error) {
      consistencyError = error instanceof Error ? error.stack ?? error.message : String(error);
    }
  }
  const passed = Object.values(checks).every((status) => status >= 200 && status < 400)
    && !consistencyError;
  const report = {
    passed,
    version: app.getVersion(),
    electron: process.versions.electron,
    node: process.versions.node,
    checks,
    consistency,
    consistencyError,
  };
  writeSmokeReport(outputPath, report);
  return passed;
}

async function responseJson(response, operation) {
  const text = await response.text();
  let payload = null;
  try {
    payload = text ? JSON.parse(text) : null;
  } catch {
    throw new Error(`${operation} returned non-JSON data (HTTP ${response.status}).`);
  }
  if (!response.ok) {
    throw new Error(`${operation} failed (HTTP ${response.status}): ${JSON.stringify(payload)}`);
  }
  return payload;
}

async function computeConsistency(siteUrl, { fixturePath, mappingPath, indexKey }) {
  const fixture = path.resolve(fixturePath);
  if (!fs.statSync(fixture).isFile()) throw new Error(`Consistency fixture is not a file: ${fixture}`);
  const mapping = mappingPath
    ? JSON.parse(fs.readFileSync(path.resolve(mappingPath), "utf8"))
    : {};
  const apiBase = `${siteUrl}/api/dietary/v1`;
  const form = new FormData();
  form.append(
    "file",
    new Blob([fs.readFileSync(fixture)], { type: "text/csv" }),
    path.basename(fixture),
  );
  const upload = await responseJson(
    await fetch(`${apiBase}/uploads`, { method: "POST", body: form }),
    "Electron consistency upload",
  );
  let job = await responseJson(
    await fetch(`${apiBase}/compute`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        index_key: indexKey,
        mode: "general",
        upload_id: upload.upload_id,
        mapping,
        options: {},
      }),
    }),
    "Electron consistency compute",
  );
  const deadline = Date.now() + 60000;
  while (["queued", "running"].includes(job.status) && Date.now() < deadline) {
    await new Promise((resolve) => setTimeout(resolve, 100));
    job = await responseJson(
      await fetch(`${apiBase}/jobs/${encodeURIComponent(job.job_id)}`),
      "Electron consistency job poll",
    );
  }
  if (job.status !== "succeeded") {
    throw new Error(`Electron consistency job ended with status ${job.status}: ${JSON.stringify(job.error)}`);
  }
  return job.result;
}

function writeSmokeReport(outputPath, report) {
  if (!outputPath) return;
  const resolved = path.resolve(outputPath);
  fs.mkdirSync(path.dirname(resolved), { recursive: true });
  fs.writeFileSync(resolved, JSON.stringify(report, null, 2), "utf8");
}

async function startApplication() {
  const projectRootOverride = process.env.DIETARYINDEX_PROJECT_ROOT || null;
  const layout = resolveLayout({
    appPath: app.getAppPath(),
    resourcesPath: process.resourcesPath,
    isPackaged: app.isPackaged,
    projectRootOverride,
  });
  services = new ServiceManager({ layout, userDataDir: app.getPath("userData") });
  services.on("unexpected-exit", ({ name, code, stderrPath }) => {
    if (quitting) return;
    dialog.showErrorBox(
      "DietaryIndex local service stopped",
      `${name} exited unexpectedly (code ${code}).\nLog: ${stderrPath}`,
    );
    app.quit();
  });
  const runtime = await services.start();
  if (process.argv.includes("--smoke-test")) {
    const passed = await runSmokeTest(runtime, argumentValue("--smoke-output"));
    quitting = true;
    services.stop();
    app.exit(passed ? 0 : 1);
    return;
  }
  createMainWindow(runtime.siteUrl, services.logDir);
}

const smokeMode = process.argv.includes("--smoke-test");
const hasSingleInstanceLock = smokeMode || app.requestSingleInstanceLock();
if (!hasSingleInstanceLock) {
  app.quit();
} else {
  app.on("second-instance", () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
  app.whenReady().then(async () => {
    app.setAppUserModelId("org.dietaryindex.desktop");
    if (!smokeMode) createSplash();
    try {
      await startApplication();
    } catch (error) {
      splashWindow?.destroy();
      const message = error instanceof Error ? error.stack ?? error.message : String(error);
      if (smokeMode) {
        const output = argumentValue("--smoke-output");
        try {
          writeSmokeReport(output, { passed: false, error: message });
        } catch (reportError) {
          process.stderr.write(`Unable to write smoke-test report: ${reportError}\n`);
        }
      } else {
        dialog.showErrorBox("DietaryIndex failed to start", message);
      }
      quitting = true;
      services?.stop();
      app.exit(1);
    }
  });
  app.on("window-all-closed", () => app.quit());
  app.on("before-quit", () => {
    quitting = true;
    services?.stop();
  });
}

module.exports = { isTrustedNavigation };
