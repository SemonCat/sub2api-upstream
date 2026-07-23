import importlib.util
from pathlib import Path


PLUGIN_PATH = Path(__file__).with_name("__init__.py")
SPEC = importlib.util.spec_from_file_location("session_header", PLUGIN_PATH)
PLUGIN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLUGIN)


def test_adds_session_header_for_any_provider():
    result = PLUGIN.add_session_header(
        provider="custom",
        session_id="session-123",
        request={"extra_headers": {"x-existing": "kept"}},
    )

    assert result["request"]["extra_headers"] == {
        "x-existing": "kept",
        "x-session-id": "session-123",
    }


def test_sanitizes_and_bounds_session_header():
    result = PLUGIN.add_session_header(
        session_id=("a" * 210) + "\r\ninjected",
        request={},
    )

    assert result["request"]["extra_headers"]["x-session-id"] == "a" * 200


def test_preserves_existing_header_case_insensitively():
    result = PLUGIN.add_session_header(
        session_id="new",
        request={"extra_headers": {"X-Session-ID": "existing"}},
    )

    assert result["request"]["extra_headers"] == {"X-Session-ID": "existing"}


def test_ignores_empty_session_id():
    assert PLUGIN.add_session_header(session_id="", request={}) is None
