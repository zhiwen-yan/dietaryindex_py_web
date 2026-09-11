import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { packager } from "@electron/packager";
import {
  flipFuses,
  FuseState,
  FuseV1Options,
  FuseVersion,
  getCurrentFuseWire,
} from "@electron/fuses";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const electronRoot = path.resolve(scriptDir, "..");
const projectRoot = path.resolve(electronRoot, "..");
const packageMetadata = JSON.parse(
  fs.readFileSync(path.join(electronRoot, "package.json"), "utf8"),
);
const electronVersion = packageMetadata.devDependencies.electron;
const stagingRoot = path.join(
  projectRoot,
  ".desktop_build_cache",
  "electron-package-staging",
);
const finalRoot = path.join(electronRoot, "out");
const appDirectoryName = "DietaryIndex-win32-x64";

function assertDirectChild(candidate, parent, label) {
  const relative = path.relative(parent, candidate);
  if (!relative || relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error(`Refusing to modify unexpected ${label}: ${candidate}`);
  }
}

function findCachedElectronZipDir(version) {
  const expected = `electron-v${version}-win32-x64.zip`;
  const cacheRoot = path.join(
    process.env.LOCALAPPDATA || path.join(os.homedir(), "AppData", "Local"),
    "electron",
    "Cache",
  );
  if (!fs.existsSync(cacheRoot)) return undefined;

  for (const entry of fs.readdirSync(cacheRoot, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const candidateDirectory = path.join(cacheRoot, entry.name);
    if (fs.existsSync(path.join(candidateDirectory, expected))) {
      return candidateDirectory;
    }
  }
  return undefined;
}

async function main() {
  assertDirectChild(stagingRoot, path.join(projectRoot, ".desktop_build_cache"), "staging directory");
  assertDirectChild(finalRoot, electronRoot, "release directory");
  fs.mkdirSync(path.dirname(stagingRoot), { recursive: true });
  fs.rmSync(stagingRoot, { recursive: true, force: true });
  fs.rmSync(finalRoot, { recursive: true, force: true });

  const electronZipDir = findCachedElectronZipDir(electronVersion);
  if (electronZipDir) {
    console.log(`Using cached Electron ${electronVersion}: ${electronZipDir}`);
  } else {
    console.log(`Electron ${electronVersion} is not cached; the packager may download it.`);
  }

  const outputPaths = await packager({
    dir: electronRoot,
    name: "DietaryIndex",
    executableName: "DietaryIndex",
    appVersion: packageMetadata.version,
    platform: "win32",
    arch: "x64",
    electronVersion,
    electronZipDir,
    out: stagingRoot,
    overwrite: true,
    tmpdir: false,
    asar: true,
    ignore: [/^\/node_modules(?:\/|$)/, /^\/out(?:\/|$)/],
    extraResource: [
      path.join(projectRoot, "desktop_runtime"),
      path.join(projectRoot, "dist", "DietaryIndexBackend.exe"),
      path.join(projectRoot, "LICENSE"),
      path.join(projectRoot, "NOTICE"),
      path.join(projectRoot, "CITATION.cff"),
    ],
  });

  if (outputPaths.length !== 1) {
    throw new Error(`Expected one Electron output, received ${outputPaths.length}.`);
  }
  const packagedRoot = outputPaths[0];
  const executable = path.join(packagedRoot, "DietaryIndex.exe");

  const expectedFuses = {
    [FuseV1Options.RunAsNode]: false,
    [FuseV1Options.EnableCookieEncryption]: true,
    [FuseV1Options.EnableNodeOptionsEnvironmentVariable]: false,
    [FuseV1Options.EnableNodeCliInspectArguments]: false,
    [FuseV1Options.EnableEmbeddedAsarIntegrityValidation]: true,
    [FuseV1Options.OnlyLoadAppFromAsar]: true,
    [FuseV1Options.LoadBrowserProcessSpecificV8Snapshot]: false,
    [FuseV1Options.GrantFileProtocolExtraPrivileges]: false,
    [FuseV1Options.WasmTrapHandlers]: true,
  };
  await flipFuses(executable, {
    version: FuseVersion.V1,
    strictlyRequireAllFuses: true,
    ...expectedFuses,
  });

  const actualFuses = await getCurrentFuseWire(executable);
  for (const [option, expected] of Object.entries(expectedFuses)) {
    const expectedState = expected ? FuseState.ENABLE : FuseState.DISABLE;
    if (actualFuses[option] !== expectedState) {
      throw new Error(`Electron fuse ${option} was not written as expected.`);
    }
  }

  if (path.basename(packagedRoot) !== appDirectoryName) {
    throw new Error(`Unexpected packaged directory: ${packagedRoot}`);
  }
  fs.renameSync(stagingRoot, finalRoot);
  console.log(`Packaged Electron application: ${path.join(finalRoot, appDirectoryName)}`);
  console.log("All nine Electron v1 fuses were explicitly configured and verified.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
