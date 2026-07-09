import json
from datetime import datetime, timezone
from pathlib import Path


FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "tinymux" / "log_events" / "v0"

REQUIRED_FIELDS = {
    "schema_version",
    "event_id",
    "timestamp",
    "source",
    "world",
    "room",
    "actor",
    "event_type",
    "text",
    "visibility",
}

EVENT_TYPES = {
    "say",
    "pose",
    "emit",
    "enter",
    "leave",
    "page",
    "ooc",
    "system",
    "custom",
}

VISIBILITY_SCOPES = {
    "room",
    "private",
    "system",
    "custom",
}

EMPTY_TEXT_EVENT_TYPES = {
    "enter",
    "leave",
    "system",
    "custom",
}


def _load_jsonl_records():
    paths = sorted(FIXTURE_DIR.glob("*.jsonl"))
    assert paths, f"no JSONL fixtures found under {FIXTURE_DIR}"

    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        assert lines, f"{path}: fixture file is empty"

        for line_number, line in enumerate(lines, start=1):
            assert line.strip(), f"{path}:{line_number}: empty JSONL line"
            record = json.loads(line)
            assert isinstance(record, dict), f"{path}:{line_number}: JSONL line is not an object"
            yield path, line_number, record


def _assert_utc_iso8601_like(value, location):
    assert isinstance(value, str), f"{location}: timestamp must be a string"
    normalized = value.removesuffix("Z") + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    assert parsed.tzinfo is not None, f"{location}: timestamp must include UTC timezone"
    assert parsed.utcoffset() == timezone.utc.utcoffset(parsed), f"{location}: timestamp must be UTC"


def _assert_identity_object(value, location, require_type=False):
    assert isinstance(value, dict), f"{location}: identity must be an object"

    # v0 fixtures currently use TinyMUX dbrefs; accept id for a future normalized shape.
    stable_id = value.get("id", value.get("dbref"))
    assert isinstance(stable_id, str) and stable_id, f"{location}: identity must include id or dbref"
    assert isinstance(value.get("name"), str) and value["name"], f"{location}: identity must include name"

    if require_type or "type" in value:
        assert isinstance(value.get("type"), str) and value["type"], f"{location}: identity type must be non-empty"


def test_tinymux_log_event_v0_fixtures_match_documented_shape():
    seen_records = 0

    for path, line_number, record in _load_jsonl_records():
        location = f"{path}:{line_number}"
        missing = REQUIRED_FIELDS - set(record)
        assert not missing, f"{location}: missing required fields {sorted(missing)}"

        assert record["schema_version"] == "tinymux.log_event.v0", f"{location}: schema_version mismatch"
        assert record["source"] == "tinymux", f"{location}: source mismatch"
        assert record["event_type"] in EVENT_TYPES, f"{location}: unsupported event_type"

        assert isinstance(record["event_id"], str) and record["event_id"], f"{location}: event_id must be non-empty"
        _assert_utc_iso8601_like(record["timestamp"], location)

        _assert_identity_object(record["room"], f"{location}: room")

        if record["actor"] is None:
            assert record["event_type"] in {"system", "custom"}, f"{location}: only system/custom may omit actor"
        else:
            _assert_identity_object(record["actor"], f"{location}: actor")

        assert isinstance(record["visibility"], dict), f"{location}: visibility must be an object"
        assert record["visibility"].get("scope") in VISIBILITY_SCOPES, f"{location}: unsupported visibility scope"

        assert isinstance(record["text"], str), f"{location}: text must be a string"
        if record["event_type"] not in EMPTY_TEXT_EVENT_TYPES:
            assert record["text"], f"{location}: text must be non-empty"

        if "raw" in record:
            assert isinstance(record["raw"], dict), f"{location}: raw must be an object when present"

        seen_records += 1

    assert seen_records > 0


if __name__ == "__main__":
    test_tinymux_log_event_v0_fixtures_match_documented_shape()
