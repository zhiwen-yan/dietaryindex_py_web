"use strict";

const { contextBridge } = require("electron");

// Expose no filesystem, process-spawning, shell, or raw IPC capability to the
// renderer. The existing Next.js application communicates only with its
// same-origin proxy, which forwards authenticated calls to the loopback API.
contextBridge.exposeInMainWorld("dietaryindexDesktop", Object.freeze({
  isDesktop: true,
  platform: process.platform,
}));
