import {
  readFileSync,
  existsSync,
  accessSync,
  readdirSync,
  constants,
} from "fs";

import { extname, resolve } from "path";

import { createTransport } from "nodemailer";

const CONFIG_FILE = "./config.json";
const CACHE_FILE = "./.cache.json";
const UTF = { encoding: "utf-8" };

async function main() {
  const config = validateConfig(readConfig());
  const cache = readCache();
  const notes_list = createNoteList(config, cache);
  const mail_list = createMailList(notes_list);
  await sendMails(mail_list, config);
}

function readConfig() {
  try {
    return JSON.parse(readFileSync(CONFIG_FILE, UTF));
  } catch (error) {
    handleError({ error });
  }
}

function readCache() {
  try {
    if (existsSync(CACHE_FILE)) {
      return JSON.parse(readFileSync(CACHE_FILE, UTF));
    }
  } catch (e) {
    handleError({ error });
  }
}

function validateConfig(config) {
  return config;
}

function createNoteList(config, cache) {
  let note_list = [];

  config.note_folders.forEach(
    ({
      path,
      count = 10,
      priority = 0,
      include_ext = config.include_ext || [],
    }) => {
      try {
        accessSync(path, constants.R_OK);

        const note_files = readdirSync(path, UTF).filter((f) =>
          include_ext.includes(extname(f))
        );

        const notes_obj = {
          path,
          priority,
          raw_strings: [],
        };

        while (count--)
          // TODO Check against cache
          notes_obj.raw_strings.push(
            readFileSync(resolve(path, note_files.pop()), UTF)
          );

        // TODO Additional transformation as necessary
        note_list.push(notes_obj);
      } catch (e) {
        handleError({ error, shouldExit: false });
      }
    }
  );

  return note_list;
}

function createMailList(note_list) {
  return [{ subject: "", html: "" }];
}

async function sendMails(mail_list, config) {
  const TRANSPORTER = createTransport({
    service: config.host.service,
    auth: {
      user: config.host.email,
      pass: config.host.password,
    },
  });

  for (const mail of mail_list) {
    const info = await TRANSPORTER.sendMail({
      from: config.host.email,
      to: config.recipients,
      subject: mail.subject,
      text: "",
      html: mail.html,
    });

    // TODO Handle rejections
  }
}

function handleError({ error, shouldExit = true }) {
  if (shouldExit) {
    console.error(error.name, error.message);
    process.exit();
  } else {
    console.warn(error.name, error.message);
  }
}

main();
