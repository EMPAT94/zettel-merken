import test from "ava";

import {
  readJSONFile,
  validateConfig,
  createNoteList,
  sendMails,
} from "../src/utils.js";

console.log("readJSONFile tests:");

test("Should return undefined if file doesn't exist", (t) => {
  t.is(readJSONFile("noFileFound"), undefined);
});
