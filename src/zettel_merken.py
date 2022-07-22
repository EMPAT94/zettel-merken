#!/usr/bin/env python

from db import Db
import mail
import helpers as hlp
import config as cfg


def main() -> None:
    app_path = hlp.get_app_path()

    try:
        config = cfg.get_config(app_path / "config.json")
    except cfg.ConfigNotFound as err:
        print(err)
        exit()

    db = Db((app_path / "zettel_merken.db"), config)

    db.create_schema()

    scheduled_notes = []

    for note in hlp.notes_list(config):
        if len(scheduled_notes) > config.MAX_NOTES_PER_MAIL:
            break

        try:
            if db.is_note_scheduled(note):
                scheduled_notes.append(note)

        except db.ScheduleNotFound:
            db.create_note_schedule(note)

        except db.ScheduleExhausted:
            continue

    if scheduled_notes:
        mail_content = "\n\n".join(
            str(note) + "\n\n" + open(note).read() for note in scheduled_notes
        )
        mail.send_mail(mail_content, config)
        db.update_note_schedule(scheduled_notes)


if __name__ == "__main__":
    main()
