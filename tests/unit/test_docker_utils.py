import requests

from app.utils import docker_utils


class FakeResponse:
    def __init__(
        self,
        status_code=200,
        content_type="text/event-stream",
        lines=None
    ):
        self.status_code = status_code
        self.headers = {"Content-Type": content_type}
        self.closed = False
        self.lines = lines or [
            "event: endpoint",
            "data: /messages/?session_id=test-session",
            ""
        ]

    def iter_lines(self, **kwargs):
        return iter(self.lines)

    def close(self):
        self.closed = True


def test_wait_for_mcp_sse_ready_accepts_event_stream(monkeypatch):
    response = FakeResponse()
    monkeypatch.setattr(docker_utils.requests, "get", lambda *args, **kwargs: response)

    ready, message = docker_utils.wait_for_mcp_sse_ready(
        "http://127.0.0.1:27001/sse",
        timeout=1
    )

    assert ready is True
    assert "MCP SSE端点已就绪" in message
    assert response.closed is True


def test_wait_for_mcp_sse_ready_reports_timeout(monkeypatch):
    times = iter([0.0, 2.0])
    monkeypatch.setattr(docker_utils.time, "monotonic", lambda: next(times))

    def fail_request(*args, **kwargs):
        raise requests.ConnectionError("connection refused")

    monkeypatch.setattr(docker_utils.requests, "get", fail_request)

    ready, message = docker_utils.wait_for_mcp_sse_ready(
        "http://127.0.0.1:27001/sse",
        timeout=1,
        interval=0
    )

    assert ready is False
    assert "等待MCP SSE端点超时" in message
    assert "connection refused" in message


def test_wait_for_mcp_sse_ready_rejects_plain_http_response(monkeypatch):
    times = iter([0.0, 2.0])
    response = FakeResponse(content_type="application/json")
    monkeypatch.setattr(docker_utils.time, "monotonic", lambda: next(times))
    monkeypatch.setattr(docker_utils.requests, "get", lambda *args, **kwargs: response)

    ready, message = docker_utils.wait_for_mcp_sse_ready(
        "http://127.0.0.1:27001/sse",
        timeout=1,
        interval=0
    )

    assert ready is False
    assert "Content-Type=application/json" in message


def test_wait_for_mcp_sse_ready_requires_endpoint_event(monkeypatch):
    times = iter([0.0, 2.0])
    response = FakeResponse(lines=["event: ping", "data: ok", ""])
    monkeypatch.setattr(docker_utils.time, "monotonic", lambda: next(times))
    monkeypatch.setattr(docker_utils.requests, "get", lambda *args, **kwargs: response)

    ready, message = docker_utils.wait_for_mcp_sse_ready(
        "http://127.0.0.1:27001/sse",
        timeout=1,
        interval=0
    )

    assert ready is False
    assert "未收到MCP endpoint事件" in message
