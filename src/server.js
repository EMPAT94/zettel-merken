import {
  readFileSync,
  existsSync,
  accessSync,
  readdirSync,
  constants,
} from "fs";

import { extname, resolve, sep } from "path";

import { createTransport } from "nodemailer";

const CONFIG_FILE = "./config.json";
const CACHE_FILE = "./.cache.json";
const ENCODING = { encoding: "utf-8" };

const DEFAULT_COUNT = 1;
const DEFAULT_PRIORITY = 0;
const DEFAULT_EXTENSIONS = [".md", ".txt", ".org", ".norg"];
const DEFAULT_VERBOSITY = 3; // 0 = debug, 1 = info, 2 = warn, 3 = error

async function main() {
  const config = validateConfig(readConfig());
  const cache = readCache();
  const note_list = createNoteList(config, cache);
  await sendMails(note_list, config, cache);
}

function readConfig() {
  try {
    return JSON.parse(readFileSync(CONFIG_FILE, ENCODING));
  } catch (error) {
    handleError({ error });
  }
}

function readCache() {
  try {
    if (existsSync(CACHE_FILE)) {
      return JSON.parse(readFileSync(CACHE_FILE, ENCODING));
    } else {
      return {};
    }
  } catch (error) {
    handleError({ error });
  }
}

function validateConfig(config) {
  return config;
}

function generateSchedule() {
  const getFutureDate = (d) => new Date().setDate(new Date().getDate() + d);

  const schedule = {
    day: 1,
    dates: [
      getFutureDate(1),
      getFutureDate(3),
      getFutureDate(6),
      getFutureDate(14),
      getFutureDate(30),
      getFutureDate(60),
    ],
  };

  return schedule;
}

function isScheduled({ dates, day }) {
  return dates[day - 1] <= Date.now();
}

function createNoteList(config, cache) {
  let note_list = [];

  config.note_folders.forEach(
    ({
      path,
      count = DEFAULT_COUNT,
      priority = DEFAULT_PRIORITY,
      include_ext = DEFAULT_EXTENSIONS,
      exclude_files = [],
    }) => {
      try {
        accessSync(path, constants.R_OK);

        const note_files = readdirSync(path, ENCODING).filter((f) =>
          include_ext.includes(extname(f))
        );

        for (const note_file of note_files) {
          console.log("READING: ", note_file);

          if (exclude_files.includes(note_file)) continue;

          const note_obj = {
            path,
            priority,
            dir: path.split(sep).pop(),
            file: note_file,
            raw_strings: [],
          };

          if (cache.note_file) {
            if (!isScheduled(cache.note_file.schedule)) continue;
          } else {
            note_obj.schedule = generateSchedule();
          }

          note_obj.raw_strings.push(
            readFileSync(resolve(path, note_file), ENCODING)
          );

          note_list.push(note_obj);

          if (--count <= 0) break;
        }
      } catch (error) {
        handleError({ error, shouldExit: false });
      }
    }
  );

  return note_list;
}

async function sendMails(note_list, config, cache) {
  const TRANSPORTER = createTransport({
    service: config.host.service,
    auth: {
      user: config.host.email,
      pass: config.host.password,
    },
  });

  const mail_list = [];

  for (const note of note_list) {
    const folder_mail = mail_list.find((m) => (m.text === note.dir));

    if (folder_mail) folder_mail.html.push("\n\n", note.raw_strings);
    else {
      mail_list.push({
        from: config.host.email,
        to: config.recipients,
        subject: "Review: " + note.dir,
        text: note.dir,
        html: note.raw_strings,
      });
    }
  }

  for (const mail of mail_list) {
    mail.html = mail.html.join("");

    console.log("SENDING MAIL: ", mail);
    // const info = await TRANSPORTER.sendMail(mail);
  }

  // const info = await TRANSPORTER.sendMail(mail);
  // TODO Update cache
  // TODO Handle rejections
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
