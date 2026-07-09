import json
from datetime import datetime, timezone
from pathlib import Path


FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "telemetry" / "v0"

REQUIRED_TOP_LEVEL_FIELDS = {
    "schema_version",
    "event_id",
    "ts_utc",
    "run_id",
    "seq",
    "event_type",
    "event_phase",
    "producer",
    "actor",
    "location",
    "raw",
}

REQUIRED_PRODUCER_FIELDS = {
    "kind",
    "source",
    "authoritative",
}

REQUIRED_RAW_FIELDS = {
    "command_raw",
    "content_raw",
    "verb_raw",
    "from_dbref",
    "to_dbref",
    "realm_tx_raw",
    "realm_rx_raw",
    "realm_context_raw",
    "perception_context_raw",
    "target_raw",
    "error_raw",
}

SUPPORTED_EVENT_TYPES = {
    "SAY_ATTEMPT",
    "MOVE_ATTEMPT",
    "POSE_ATTEMPT",
    "ROOM_EMIT",
    "REFUSAL",
    "ERROR",
}

EXPECTED_FIXTURE_EVENT_TYPES = {
    "SAY_ATTEMPT",
    "MOVE_ATTEMPT",
    "REFUSAL",
    "ERROR",
}

SUPPORTED_PHASES = {
    "attempt",
    "fact",
    "refusal",
    "error",
    "emit",
}

EXPECTED_FIXTURE_PHASES = {
    "attempt",
    "refusal",
    "error",
}


def _load_jsonl_records():
    paths = sorted(FIXTURE_DIR.glob("*.jsonl"))
    assert paths, f"no telemetry JSONL fixtures found under {FIXTURE_DIR}"

    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        assert lines, f"{path}: fixture file is empty"

        for line_number, line in enumerate(lines, start=1):
            assert line.strip(), f"{path}:{line_number}: empty JSONL line"
            record = json.loads(line)
            assert isinstance(record, dict), f"{path}:{line_number}: JSONL line is not an object"
            yield path, line_number, record


def _assert_utc_iso8601_like(value, location):
    assert isinstance(value, str), f"{location}: ts_utc must be a string"
    normalized = value.removesuffix("Z") + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    assert parsed.tzinfo is not None, f"{location}: ts_utc must include UTC timezone"
    assert parsed.utcoffset() == timezone.utc.utcoffset(parsed), f"{location}: ts_utc must be UTC"


def _assert_identity_or_null(value, location):
    if value is None:
        return

    assert isinstance(value, dict), f"{location}: identity must be an object or null"
    assert isinstance(value.get("dbref"), str) and value["dbref"], f"{location}: missing dbref"
    assert isinstance(value.get("name_raw"), str) and value["name_raw"], f"{location}: missing name_raw"


def test_telemetry_v0_fixtures_match_documented_contract():
    seen_event_types = set()
    seen_phases = set()
    seen_records = 0

    for path, line_number, record in _load_jsonl_records():
        location = f"{path}:{line_number}"
        missing = REQUIRED_TOP_LEVEL_FIELDS - set(record)
        assert not missing, f"{location}: missing required fields {sorted(missing)}"

        assert record["schema_version"] == "noesis.telemetry.v0", f"{location}: schema_version mismatch"
        assert isinstance(record["event_id"], str) and record["event_id"], f"{location}: empty event_id"
        assert isinstance(record["run_id"], str) and record["run_id"], f"{location}: empty run_id"
        assert isinstance(record["seq"], int), f"{location}: seq must be an integer"
        _assert_utc_iso8601_like(record["ts_utc"], location)

        assert record["event_type"] in SUPPORTED_EVENT_TYPES, f"{location}: unsupported event_type"
        assert record["event_phase"] in SUPPORTED_PHASES, f"{location}: unsupported event_phase"
        assert isinstance(record["event_phase"], str) and record["event_phase"], f"{location}: empty event_phase"

        producer = record["producer"]
        assert isinstance(producer, dict), f"{location}: producer must be an object"
        missing_producer = REQUIRED_PRODUCER_FIELDS - set(producer)
        assert not missing_producer, f"{location}: missing producer fields {sorted(missing_producer)}"
        assert isinstance(producer["kind"], str) and producer["kind"], f"{location}: empty producer.kind"
        assert isinstance(producer["source"], str) and producer["source"], f"{location}: empty producer.source"
        assert isinstance(producer["authoritative"], bool), f"{location}: producer.authoritative must be boolean"

        _assert_identity_or_null(record["actor"], f"{location}: actor")
        _assert_identity_or_null(record["location"], f"{location}: location")

        raw = record["raw"]
        assert isinstance(raw, dict), f"{location}: raw must be an object"
        missing_raw = REQUIRED_RAW_FIELDS - set(raw)
        assert not missing_raw, f"{location}: missing raw fields {sorted(missing_raw)}"

        seen_event_types.add(record["event_type"])
        seen_phases.add(record["event_phase"])
        seen_records += 1

    assert seen_records > 0
    assert EXPECTED_FIXTURE_EVENT_TYPES <= seen_event_types
    assert EXPECTED_FIXTURE_PHASES <= seen_phases


if __name__ == "__main__":
    test_telemetry_v0_fixtures_match_documented_contract()
