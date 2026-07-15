#!/usr/bin/env python3
"""Prepare mounted runtime paths and launch the backend as the application user."""

from __future__ import annotations

import grp
import os
import pwd
import stat
import sys
from pathlib import Path
from typing import Sequence


DEFAULT_SERVICES_PATH = "/app/data/services"
DEFAULT_DOCKER_SOCKET = "/var/run/docker.sock"
DEFAULT_APP_USER = "appuser"


def prepare_services_directory(path: Path, uid: int, gid: int) -> None:
    """Create the services directory and make its root writable by appuser."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        os.chown(path, uid, gid)
    except OSError as exc:
        raise RuntimeError(
            f"cannot initialize services directory {path}: {exc}"
        ) from exc


def supplementary_group_ids(
    username: str,
    primary_gid: int,
    docker_socket: Path,
) -> list[int]:
    """Return app groups plus the mounted Docker socket's actual group id."""
    group_ids = {primary_gid}
    group_ids.update(
        group.gr_gid for group in grp.getgrall() if username in group.gr_mem
    )

    try:
        socket_stat = docker_socket.stat()
    except FileNotFoundError:
        pass
    else:
        if stat.S_ISSOCK(socket_stat.st_mode):
            group_ids.add(socket_stat.st_gid)

    return sorted(group_ids)


def drop_privileges_and_exec(
    command: Sequence[str],
    username: str = DEFAULT_APP_USER,
) -> None:
    """Drop root privileges while retaining access to the mounted Docker socket."""
    if not command:
        raise RuntimeError("no command was provided to the container entrypoint")

    user = pwd.getpwnam(username)
    services_path = Path(os.environ.get("SERVICES_BASE_PATH", DEFAULT_SERVICES_PATH))

    if os.geteuid() == 0:
        prepare_services_directory(services_path, user.pw_uid, user.pw_gid)
        groups = supplementary_group_ids(
            username,
            user.pw_gid,
            Path(DEFAULT_DOCKER_SOCKET),
        )
        os.setgroups(groups)
        os.setgid(user.pw_gid)
        os.setuid(user.pw_uid)
    else:
        services_path.mkdir(parents=True, exist_ok=True)
        if not os.access(services_path, os.W_OK | os.X_OK):
            raise RuntimeError(
                f"services directory is not writable by uid {os.geteuid()}: "
                f"{services_path}"
            )

    os.execvp(command[0], list(command))


def main(argv: Sequence[str] | None = None) -> int:
    command = list(sys.argv[1:] if argv is None else argv)
    try:
        drop_privileges_and_exec(command)
    except (KeyError, OSError, RuntimeError) as exc:
        print(f"Container startup failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
