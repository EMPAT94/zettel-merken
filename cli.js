#!/usr/bin/env node

import { dirname, resolve } from "path";
import { fileURLToPath } from "url";

import main from "./src/core.js";

const [, , ...args] = process.argv;

if (args.length) {
  if (args[0] === "--config" || args[0] === "-c") {
    main(args[1]);
  } else {
    console.error("Zettel Merken v0.0.1");
    console.error("Usage: zettel-merken --config [-c] '/path/to/config.js'");
    process.exit();
  }
} else {
  const config_path = resolve(
    dirname(fileURLToPath(import.meta.url)),
    "config.json"
  );
  main(config_path);
}
