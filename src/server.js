import { readFileSync, existsSync, constants } from "fs";
import { access } from "fs/promises";

const CONFIG_FILE = "./config.json";
const CACHE_FILE = "./cache.json";

let config;
try {
  config = JSON.parse(readFileSync(CONFIG_FILE, { encoding: "utf-8" }));
} catch (e) {
  handleError(e);
}

// TODO: Basic validation of config

// 2. Fetch and parse cache.json

let cache;
try {
  if (existsSync(CACHE_FILE)) {
    cache = JSON.parse(readFileSync(CACHE_FILE, { encoding: "utf-8" }));
  }
} catch (e) {
  handleError(e);
}

// 3. Check if "note-folders" exist and readable

config.note_folders.forEach(async ({ path }) => {
  try {
    await access(path, constants.R_OK);
    console.log("Folder access works, requires full path!");
  } catch (e) {
    handleError(e);
  }
});

// 4. Select notes to be sent based on config
// 5. Additional transformation as necessary
// 6. Send mail to each receiver email
// 7. Update cache.json

function handleError(e) {
  console.error(e.name + ": " + e.message);
  process.exit();
}
