from datetime import datetime, timezone


def formated_datetime(ref_datetime: datetime | None = None) -> str:
    if ref_datetime is None:
        ref_datetime = datetime.now(timezone.utc)
    return ref_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
