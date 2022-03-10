import {
  readJSONFile,
  validateConfig,
  handleError,
  createNoteList,
  sendMails,
} from "./utils.js";

export default function main(config_path) {
  const config = readJSONFile(config_path);

  try {
    validateConfig(config);
  } catch (error) {
    handleError({ error });
  }

  let cache = readJSONFile(config.cache_file) || {};

  let note_list = createNoteList(config, cache);

  sendMails(note_list, config, cache);
}
