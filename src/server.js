import {
  readFileSync,
  writeFileSync,
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

// CONFIG DEFAULTS
const DEFAULT_COUNT = 1;
const DEFAULT_PRIORITY = 0;
const DEFAULT_INCLUDE_EXT = [".md", ".txt", ".org", ".norg"];
const DEFAULT_EXCLUDE_FILES = [];

function readJSONFile(file) {
  try {
    if (existsSync(file)) return JSON.parse(readFileSync(file, ENCODING));
  } catch (error) {
    handleError({ error });
  }
}

function validateConfig(config) {
  const {
    host: { service, email, password },
    recipients,
    note_folders,
  } = config;

  const err = (prop) => {
    throw "Missing or invalid property: " + prop;
  };

  if (!service) err("host.service");
  if (!email) err("host.email");
  if (!password) err("host.password");
  if (!recipients || !recipients.length) err("recipients");
  if (!note_folders || !note_folders.length) err("note_folders");
  for (const { path } of note_folders) {
    if (!path) err("note_folders.path");
  }
}

function createNoteList(config, cache) {
  let note_list = [];

  config.note_folders.forEach(
    ({
      path,
      count = DEFAULT_COUNT,
      priority = DEFAULT_PRIORITY,
      include_ext = DEFAULT_INCLUDE_EXT,
      exclude_files = DEFAULT_EXCLUDE_FILES,
    }) => {
      try {
        accessSync(path, constants.R_OK);

        const note_files = readdirSync(path, ENCODING).filter((f) =>
          include_ext.includes(extname(f))
        );

        for (const note_file of note_files) {
          if (exclude_files.includes(note_file)) continue;

          const note_obj = {
            path,
            priority,
            dir: path.split(sep).pop(),
            file: note_file,
            raw_strings: [],
          };

          if (cache[note_file]) {
            if (!isScheduled(cache[note_file].schedule)) continue;
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

  function isScheduled({ dates, day }) {
    return dates[day - 1] <= Date.now();
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
    const folder_mail = mail_list.find((m) => m.text === note.dir);

    if (folder_mail) {
      folder_mail.html.push("\n\n", note.raw_strings);
      folder_mail.notes.push(note);
    } else {
      mail_list.push({
        from: config.host.email,
        to: config.recipients,
        subject: "Review: " + note.dir,
        text: note.dir,
        html: note.raw_strings,
        notes: [note],
      });
    }
  }

  for await (const mail of mail_list) {
    mail.html = mail.html.join("\n\n");

    console.log(
      "SENDING MAIL: ",
      mail.subject,
      mail.notes.map((n) => n.file)
    );

    const info = await TRANSPORTER.sendMail(mail);

    for (const note of mail.notes) {
      if (!cache[note.file]) {
        cache[note.file] = {
          dir: note.dir,
          schedule: note.schedule,
        };
      }

      if (info.messageId) {
        // Assuming message was sent
        cache[note.file].schedule.day += 1;
      } else {
        handleError({ error: "Error while sending mail" });
      }
    }
  }

  try {
    writeFileSync(CACHE_FILE, JSON.stringify(cache));
  } catch (error) {
    handleError({ error });
  }
}

function handleError({ error, shouldExit = true }) {
  console.error(error.message || error);
  if (shouldExit) process.exit();
}

(function main() {
  let config = readJSONFile(CONFIG_FILE);

  try {
    validateConfig(config);
  } catch (error) {
    handleError({ error });
  }

  let cache = readJSONFile(CACHE_FILE) || {};
  let note_list = createNoteList(config, cache);

  sendMails(note_list, config, cache);
})();
