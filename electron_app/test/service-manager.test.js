"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const test = require("node:test");
const {
  assertRuntimeLayout,
  getFreePort,
  resolveLayout,
} = require("../src/service-manager");

test("getFreePort returns a valid loopback port", async () => {
  const port = await getFreePort(39100);
  assert.ok(port >= 39100 && port <= 39149);
});

test("development layout resolves all paths relative to the project", () => {
  const project = path.join("C:\\", "example", "dietaryindex_py");
  const layout = resolveLayout({
    appPath: path.join(project, "electron_app"),
    resourcesPath: "unused",
    isPackaged: false,
    projectRootOverride: project,
  });
  assert.equal(layout.backendCwd, path.resolve(project));
  assert.equal(layout.siteRoot, path.join(path.resolve(project), "desktop_runtime", "site"));
  assert.ok(layout.backendArgs[0].endsWith("backend_server.py"));
});

test("runtime validation lists missing files without modifying the filesystem", () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "dietaryindex-electron-test-"));
  const layout = {
    backendCommand: path.join(tempRoot, "backend.exe"),
    nodeCommand: path.join(tempRoot, "node.exe"),
    siteRoot: path.join(tempRoot, "site"),
  };
  assert.throws(() => assertRuntimeLayout(layout), /Missing desktop runtime files/);
});
