import grp
import os
import stat
from pathlib import Path
from types import SimpleNamespace

import pytest

import container_entrypoint


def test_prepare_services_directory_creates_and_chowns_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    services_path = tmp_path / "nested" / "services"
    chown_calls = []
    monkeypatch.setattr(
        os,
        "chown",
        lambda path, uid, gid: chown_calls.append((path, uid, gid)),
    )

    container_entrypoint.prepare_services_directory(services_path, 1000, 1000)

    assert services_path.is_dir()
    assert chown_calls == [(services_path, 1000, 1000)]


def test_supplementary_groups_include_socket_group(
    monkeypatch: pytest.MonkeyPatch,
):
    socket_gid = 4321
    monkeypatch.setattr(
        Path,
        "stat",
        lambda _: SimpleNamespace(st_mode=stat.S_IFSOCK, st_gid=socket_gid),
    )
    monkeypatch.setattr(
        grp,
        "getgrall",
        lambda: [SimpleNamespace(gr_gid=1234, gr_mem=["appuser"])],
    )

    group_ids = container_entrypoint.supplementary_group_ids(
        "appuser", 1000, Path("/var/run/docker.sock")
    )

    assert set(group_ids) == {1000, 1234, socket_gid}


def test_drop_privileges_before_exec(monkeypatch: pytest.MonkeyPatch):
    calls = []
    user = SimpleNamespace(pw_uid=1000, pw_gid=1000)
    monkeypatch.setattr(container_entrypoint.pwd, "getpwnam", lambda _: user)
    monkeypatch.setattr(os, "geteuid", lambda: 0)
    monkeypatch.setattr(
        container_entrypoint,
        "prepare_services_directory",
        lambda path, uid, gid: calls.append(("prepare", path, uid, gid)),
    )
    monkeypatch.setattr(
        container_entrypoint,
        "supplementary_group_ids",
        lambda username, gid, socket_path: [998, 1000],
    )
    monkeypatch.setattr(
        os,
        "setgroups",
        lambda groups: calls.append(("groups", groups)),
    )
    monkeypatch.setattr(os, "setgid", lambda gid: calls.append(("gid", gid)))
    monkeypatch.setattr(os, "setuid", lambda uid: calls.append(("uid", uid)))

    def fake_execvp(executable, command):
        calls.append(("exec", executable, command))
        raise RuntimeError("exec reached")

    monkeypatch.setattr(os, "execvp", fake_execvp)

    with pytest.raises(RuntimeError, match="exec reached"):
        container_entrypoint.drop_privileges_and_exec(["python", "-V"])

    assert [call[0] for call in calls] == [
        "prepare",
        "groups",
        "gid",
        "uid",
        "exec",
    ]
