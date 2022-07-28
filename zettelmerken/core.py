from .db import Db, ScheduleNotFound, ScheduleExhausted
from .config import Config, ConfigNotFound
from .helpers import get_notes_list, get_app_path, get_mail_content
from .mail import send_mail


def main() -> None:
    app_path = get_app_path()

    try:
        config = Config.load_from_file(app_path / "config.json")
    except ConfigNotFound:
        print(
            f"config.json not found at {app_path}, "
            "Please see README for more details!"
        )
        exit()

    db = Db((app_path / "zettel_merken.db"), config)

    db.create_schema()

    scheduled_notes = []

    for note in get_notes_list(config):
        if len(scheduled_notes) >= config.MAX_NOTES_PER_MAIL:
            break

        try:
            if db.is_note_scheduled(note):
                scheduled_notes.append(note)

        except ScheduleNotFound:
            db.create_note_schedule(note)

        except ScheduleExhausted:
            continue

    if scheduled_notes:
        mail_content = get_mail_content(scheduled_notes)
        send_mail(mail_content, config)
        db.update_note_schedule(scheduled_notes)
