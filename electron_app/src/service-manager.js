"use strict";

const crypto = require("node:crypto");
const fs = require("node:fs");
const http = require("node:http");
const net = require("node:net");
const path = require("node:path");
const { spawn, spawnSync } = require("node:child_process");
const { EventEmitter } = require("node:events");

const SITE_PORT_START = 3210;
const API_PORT_START = 8210;

function getFreePort(preferredPort, host = "127.0.0.1") {
  return new Promise((resolve, reject) => {
    const tryPort = (port) => {
      if (port > preferredPort + 49) {
        reject(new Error(`No local port is available near ${preferredPort}.`));
        return;
      }
      const server = net.createServer();
      server.unref();
      server.once("error", () => tryPort(port + 1));
      server.listen({ host, port, exclusive: true }, () => {
        const assigned = server.address().port;
        server.close((error) => (error ? reject(error) : resolve(assigned)));
      });
    };
    tryPort(preferredPort);
  });
}

function requestStatus(url, headers = {}, timeoutMs = 1500) {
  return new Promise((resolve) => {
    const request = http.get(url, { headers, timeout: timeoutMs }, (response) => {
      response.resume();
      resolve(response.statusCode ?? 0);
    });
    request.once("timeout", () => request.destroy());
    request.once("error", () => resolve(0));
  });
}

async function waitForUrl(url, timeoutMs, headers = {}) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const status = await requestStatus(url, headers);
    if (status >= 200 && status < 400) return;
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  throw new Error(`Timed out waiting for local service: ${url}`);
}

function resolveLayout({ appPath, resourcesPath, isPackaged, projectRootOverride }) {
  const projectRoot = projectRootOverride
    ? path.resolve(projectRootOverride)
    : path.resolve(appPath, "..");
  if (isPackaged) {
    return {
      backendCommand: path.join(resourcesPath, "DietaryIndexBackend.exe"),
      backendArgs: [],
      backendCwd: resourcesPath,
      nodeCommand: path.join(resourcesPath, "desktop_runtime", "node", "node.exe"),
      siteRoot: path.join(resourcesPath, "desktop_runtime", "site"),
    };
  }

  const venvPython = path.join(projectRoot, ".venv", "Scripts", "python.exe");
  return {
    backendCommand: fs.existsSync(venvPython) ? venvPython : "python",
    backendArgs: [path.join(projectRoot, "backend_server.py")],
    backendCwd: projectRoot,
    nodeCommand: path.join(projectRoot, "desktop_runtime", "node", "node.exe"),
    siteRoot: path.join(projectRoot, "desktop_runtime", "site"),
  };
}

function assertRuntimeLayout(layout) {
  const required = [
    layout.backendCommand,
    layout.nodeCommand,
    path.join(layout.siteRoot, "server.js"),
  ];
  const missing = required.filter((item) => item !== "python" && !fs.existsSync(item));
  if (missing.length) {
    throw new Error(`Missing desktop runtime files:\n${missing.join("\n")}`);
  }
}

function terminateProcessTree(child) {
  if (!child || child.exitCode !== null || !child.pid) return;
  if (process.platform === "win32") {
    spawnSync("taskkill.exe", ["/pid", String(child.pid), "/t", "/f"], {
      windowsHide: true,
      stdio: "ignore",
    });
    return;
  }
  try {
    child.kill("SIGTERM");
  } catch {
    // The process may have exited between the status check and termination.
  }
}

class ServiceManager extends EventEmitter {
  constructor({ layout, userDataDir }) {
    super();
    this.layout = layout;
    this.userDataDir = userDataDir;
    this.logDir = path.join(userDataDir, "logs");
    this.runtimeDir = path.join(userDataDir, "runtime_data");
    this.children = new Map();
    this.stopping = false;
    this.runtime = null;
  }

  spawnService(name, command, args, options) {
    const stdoutPath = path.join(this.logDir, `${name}.log`);
    const stderrPath = path.join(this.logDir, `${name}.err.log`);
    const stdout = fs.openSync(stdoutPath, "a");
    const stderr = fs.openSync(stderrPath, "a");
    const child = spawn(command, args, {
      ...options,
      windowsHide: true,
      stdio: ["ignore", stdout, stderr],
    });
    fs.closeSync(stdout);
    fs.closeSync(stderr);
    child.once("exit", (code, signal) => {
      this.children.delete(name);
      if (!this.stopping) {
        this.emit("unexpected-exit", { name, code, signal, stderrPath });
      }
    });
    child.once("error", (error) => this.emit("spawn-error", { name, error, stderrPath }));
    this.children.set(name, child);
    return child;
  }

  async start() {
    assertRuntimeLayout(this.layout);
    fs.mkdirSync(this.logDir, { recursive: true });
    fs.mkdirSync(this.runtimeDir, { recursive: true });

    const [apiPort, sitePort] = await Promise.all([
      getFreePort(API_PORT_START),
      getFreePort(SITE_PORT_START),
    ]);
    const apiToken = crypto.randomBytes(32).toString("hex");
    const apiUrl = `http://127.0.0.1:${apiPort}`;
    const siteUrl = `http://127.0.0.1:${sitePort}`;
    const commonEnvironment = {
      ...process.env,
      NO_PROXY: "127.0.0.1,localhost",
      no_proxy: "127.0.0.1,localhost",
    };

    this.spawnService(
      "api",
      this.layout.backendCommand,
      [...this.layout.backendArgs, "--port", String(apiPort)],
      {
        cwd: this.layout.backendCwd,
        env: {
          ...commonEnvironment,
          DIETARYINDEX_RUNTIME_DIR: this.runtimeDir,
          DIETARYINDEX_DESKTOP_MODE: "1",
          DIETARYINDEX_API_KEY: apiToken,
          DIETARYINDEX_REQUIRE_API_KEY: "true",
        },
      },
    );
    await waitForUrl(`${apiUrl}/healthz`, 45000);

    this.spawnService("site", this.layout.nodeCommand, ["server.js"], {
      cwd: this.layout.siteRoot,
      env: {
        ...commonEnvironment,
        NODE_ENV: "production",
        NEXT_TELEMETRY_DISABLED: "1",
        HOSTNAME: "127.0.0.1",
        PORT: String(sitePort),
        DIETARYINDEX_API_INTERNAL_URL: apiUrl,
        DIETARYINDEX_API_KEY: apiToken,
        DIETARYINDEX_DESKTOP_MODE: "1",
      },
    });
    await waitForUrl(siteUrl, 45000);
    await waitForUrl(`${siteUrl}/api/dietary/v1/indices`, 15000);

    this.runtime = { apiUrl, siteUrl, apiPort, sitePort };
    return this.runtime;
  }

  stop() {
    this.stopping = true;
    for (const child of [...this.children.values()].reverse()) terminateProcessTree(child);
    this.children.clear();
    this.runtime = null;
  }
}

module.exports = {
  ServiceManager,
  assertRuntimeLayout,
  getFreePort,
  requestStatus,
  resolveLayout,
  waitForUrl,
};
