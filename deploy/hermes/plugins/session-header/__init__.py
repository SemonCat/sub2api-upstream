from __future__ import annotations


_MAX_SESSION_ID_LENGTH = 200


def register(ctx):
    ctx.register_middleware("llm_request", add_session_header)


def _clean_session_id(value):
    text = str(value or "").replace("\r", " ").replace("\n", " ").strip()
    return text[:_MAX_SESSION_ID_LENGTH]


def add_session_header(**kwargs):
    session_id = _clean_session_id(kwargs.get("session_id"))
    if not session_id:
        return None

    request = dict(kwargs.get("request") or {})
    headers = dict(request.get("extra_headers") or {})

    if not any(str(key).lower() == "x-session-id" for key in headers):
        headers["x-session-id"] = session_id

    request["extra_headers"] = headers
    return {
        "request": request,
        "source": "session-header",
        "reason": "attach Hermes session id for provider correlation",
    }
