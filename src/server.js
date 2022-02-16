import { readFileSync } from "fs";

const FILE = readFileSync("config.json", { encoding: "utf-8" });
let CONFIG;
try {
  CONFIG = JSON.parse(FILE);
} catch (e) {
  throw e;
}

// TODO:
// 1. Basic validation of config
// 2. Fetch and parse cache.json
// 3. Check if "note-folders" exist and readable
// 4. Select notes to be sent based on config
// 5. Additional transformation as necessary
// 6. Send mail to each receiver email
// 7. Update cache.json
