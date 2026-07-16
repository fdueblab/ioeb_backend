import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

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


def test_read_default_gateway_from_linux_route_table(tmp_path):
    route_file = tmp_path / "route"
    route_file.write_text(
        "Iface Destination Gateway Flags RefCnt Use Metric Mask MTU Window IRTT\n"
        "eth0 00000000 010012AC 0003 0 0 0 00000000 0 0 0\n",
        encoding="utf-8"
    )

    assert docker_utils._read_default_gateway(str(route_file)) == "172.18.0.1"


def test_build_readiness_urls_supports_host_and_container_networks(monkeypatch):
    monkeypatch.setenv("DOCKER_HOST_GATEWAY", "10.10.0.1")
    monkeypatch.setattr(
        docker_utils.socket,
        "getaddrinfo",
        lambda *args, **kwargs: [(None, None, None, None, None)]
    )
    monkeypatch.setattr(
        docker_utils,
        "_read_default_gateway",
        lambda: "172.18.0.1"
    )

    urls = docker_utils.build_mcp_readiness_urls("27001", "/sse")

    assert urls == [
        "http://10.10.0.1:27001/sse",
        "http://127.0.0.1:27001/sse",
        "http://host.docker.internal:27001/sse",
        "http://172.18.0.1:27001/sse"
    ]


def test_build_readiness_urls_discovers_linux_bridge_gateway(monkeypatch):
    monkeypatch.delenv("DOCKER_HOST_GATEWAY", raising=False)

    def missing_host_alias(*args, **kwargs):
        raise docker_utils.socket.gaierror("not found")

    monkeypatch.setattr(docker_utils.socket, "getaddrinfo", missing_host_alias)
    monkeypatch.setattr(
        docker_utils,
        "_read_default_gateway",
        lambda: "172.30.0.1"
    )

    urls = docker_utils.build_mcp_readiness_urls("27001", "/sse")

    assert urls == [
        "http://127.0.0.1:27001/sse",
        "http://172.30.0.1:27001/sse"
    ]


def test_wait_for_mcp_sse_ready_falls_back_to_docker_gateway(monkeypatch):
    response = FakeResponse()
    requested_urls = []

    def request(candidate_url, **kwargs):
        requested_urls.append(candidate_url)
        if candidate_url.startswith("http://127.0.0.1"):
            raise requests.ConnectionError("connection refused")
        return response

    monkeypatch.setattr(docker_utils.requests, "get", request)

    ready, message = docker_utils.wait_for_mcp_sse_ready(
        [
            "http://127.0.0.1:27001/sse",
            "http://172.18.0.1:27001/sse"
        ],
        timeout=1
    )

    assert ready is True
    assert requested_urls == [
        "http://127.0.0.1:27001/sse",
        "http://172.18.0.1:27001/sse"
    ]
    assert "http://172.18.0.1:27001/sse" in message


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


def test_wait_for_mcp_sse_ready_accepts_real_idle_event_stream(monkeypatch):
    class IdleSseHandler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "keep-alive")
            self.send_header("X-Accel-Buffering", "no")
            self.end_headers()
            self.wfile.flush()
            time.sleep(0.2)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), IdleSseHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    monkeypatch.setattr(docker_utils, "MCP_SSE_READ_TIMEOUT", 0.05)

    try:
        ready, message = docker_utils.wait_for_mcp_sse_ready(
            f"http://127.0.0.1:{server.server_port}/sse",
            timeout=1,
            interval=0,
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1)

    assert ready is True
    assert "HTTP事件流保持连接" in message


def test_wait_for_mcp_sse_ready_rejects_non_timeout_stream_error(monkeypatch):
    times = iter([0.0, 2.0])
    response = FakeResponse()
    response.headers.update({
        "Cache-Control": "no-store",
        "X-Accel-Buffering": "no",
    })

    def broken_stream(**kwargs):
        raise requests.ConnectionError("connection reset by peer")

    response.iter_lines = broken_stream
    monkeypatch.setattr(docker_utils.time, "monotonic", lambda: next(times))
    monkeypatch.setattr(docker_utils.requests, "get", lambda *args, **kwargs: response)

    ready, message = docker_utils.wait_for_mcp_sse_ready(
        "http://127.0.0.1:27001/sse",
        timeout=1,
        interval=0,
    )

    assert ready is False
    assert "connection reset by peer" in message


def test_wait_for_mcp_sse_ready_rejects_idle_stream_without_keepalive_headers(monkeypatch):
    times = iter([0.0, 2.0])
    response = FakeResponse()

    def idle_stream(**kwargs):
        raise requests.ConnectionError("HTTPConnectionPool: Read timed out.")

    response.iter_lines = idle_stream
    monkeypatch.setattr(docker_utils.time, "monotonic", lambda: next(times))
    monkeypatch.setattr(docker_utils.requests, "get", lambda *args, **kwargs: response)

    ready, message = docker_utils.wait_for_mcp_sse_ready(
        "http://127.0.0.1:27001/sse",
        timeout=1,
        interval=0,
    )

    assert ready is False
    assert "Read timed out" in message
