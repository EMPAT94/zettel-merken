import {
  readJSONFile,
  validateConfig,
  handleError,
  createNoteList,
  sendMails,
  CONFIG,
  CACHE,
} from "utils.js";

export function main() {
  let config = readJSONFile(CONFIG);

  try {
    validateConfig(config);
  } catch (error) {
    handleError({ error });
  }

  let cache = readJSONFile(CACHE) || {};
  let note_list = createNoteList(config, cache);

  sendMails(note_list, config, cache);
}
