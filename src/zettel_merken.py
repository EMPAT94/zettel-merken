#!/usr/bin/env python

import db
import mail
import helpers
import config as cnf


def main() -> None:
    app_path = cnf.get_app_path()

    config = cnf.get_config(app_path)

    db.create_schema(config)

    scheduled_notes = []

    for note in helpers.notes_list(config):
        if len(scheduled_notes) > config.MAX_NOTES_PER_MAIL:
            break

        try:
            if db.is_note_scheduled(note, config):
                scheduled_notes.append(note)

        except db.ScheduleNotFound:
            db.create_note_schedule(note, config)

        except db.ScheduleExhausted:
            continue

    if scheduled_notes:
        mail_content = mail.build_mail_content(scheduled_notes)
        mail.send_mail(mail_content, config)
        db.update_note_schedule(scheduled_notes, config)


if __name__ == "__main__":
    main()
