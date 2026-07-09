import json
from pathlib import Path


FIXTURE_DIR = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "mapping"
    / "tinymux_log_to_telemetry"
    / "v0"
)

REQUIRED_TOP_LEVEL_FIELDS = {
    "case_id",
    "status",
    "input",
    "expected_output",
    "notes",
}

VALID_STATUSES = {
    "expected",
    "open_question",
}

REQUIRED_INPUT_FIELDS = {
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

EXPECTED_OUTPUT_COVERAGE = {
    "SAY_ATTEMPT",
    "POSE_ATTEMPT",
    "MOVE_ATTEMPT",
}


def _load_mapping_fixtures():
    paths = sorted(FIXTURE_DIR.glob("*.json"))
    assert paths, f"no mapping fixtures found under {FIXTURE_DIR}"

    for path in paths:
        fixture = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(fixture, dict), f"{path}: root must be a JSON object"
        yield path, fixture


def _contains_key(value, key):
    if isinstance(value, dict):
        if key in value:
            return True
        return any(_contains_key(child, key) for child in value.values())

    if isinstance(value, list):
        return any(_contains_key(child, key) for child in value)

    return False


def _assert_notes(value, location):
    assert isinstance(value, list), f"{location}: notes must be a list"
    assert value, f"{location}: notes must not be empty"
    for note in value:
        assert isinstance(note, str) and note, f"{location}: each note must be a non-empty string"


def _assert_input_shape(value, location):
    assert isinstance(value, dict), f"{location}: input must be an object"
    missing = REQUIRED_INPUT_FIELDS - set(value)
    assert not missing, f"{location}: missing input fields {sorted(missing)}"
    assert value["schema_version"] == "tinymux.log_event.v0", f"{location}: input schema mismatch"
    assert value["source"] == "tinymux", f"{location}: input source mismatch"
    assert isinstance(value["event_type"], str) and value["event_type"], f"{location}: empty event_type"


def _assert_expected_output_shape(value, location):
    assert isinstance(value, dict), f"{location}: expected_output must be an object"
    assert value.get("schema_version") == "noesis.telemetry.v0", f"{location}: output schema mismatch"
    assert isinstance(value.get("event_type"), str) and value["event_type"], f"{location}: empty output event_type"
    assert isinstance(value.get("event_phase"), str) and value["event_phase"], f"{location}: empty output event_phase"
    assert isinstance(value.get("producer"), dict), f"{location}: producer must be an object"
    assert isinstance(value.get("raw"), dict), f"{location}: raw must be an object"
    assert "realm_tx_raw" in value["raw"], f"{location}: raw.realm_tx_raw missing"
    assert "perception_context_raw" in value["raw"], f"{location}: raw.perception_context_raw missing"
    assert not _contains_key(value, "perceived_by"), f"{location}: perceived_by is not allowed in mapping output"


def test_tinymux_to_telemetry_mapping_fixtures_have_expected_shape():
    seen_expected_event_types = set()
    seen_open_question_inputs = set()

    for path, fixture in _load_mapping_fixtures():
        location = str(path)
        missing = REQUIRED_TOP_LEVEL_FIELDS - set(fixture)
        assert not missing, f"{location}: missing top-level fields {sorted(missing)}"

        assert isinstance(fixture["case_id"], str) and fixture["case_id"], f"{location}: empty case_id"
        assert fixture["status"] in VALID_STATUSES, f"{location}: invalid status"
        _assert_input_shape(fixture["input"], location)
        _assert_notes(fixture["notes"], location)

        if fixture["status"] == "expected":
            _assert_expected_output_shape(fixture["expected_output"], location)
            seen_expected_event_types.add(fixture["expected_output"]["event_type"])
        else:
            assert fixture["expected_output"] is None, f"{location}: open_question expected_output must be null"
            joined_notes = " ".join(fixture["notes"]).lower()
            assert "unresolved" in joined_notes, f"{location}: open_question notes must explain unresolved status"
            seen_open_question_inputs.add(fixture["input"]["event_type"])

    assert EXPECTED_OUTPUT_COVERAGE <= seen_expected_event_types
    assert "page" in seen_open_question_inputs


if __name__ == "__main__":
    test_tinymux_to_telemetry_mapping_fixtures_have_expected_shape()
