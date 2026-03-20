#!/usr/bin/env python3
"""Generate station.cfg from station.cfg.example and environment variables."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


SECTION_RE = re.compile(r"^\[(?P<section>[^\]]+)\]\s*$")
SETTING_RE = re.compile(
    r"^(?P<indent>\s*)(?P<key>[A-Za-z0-9_]+)(?P<sep>\s*=\s*)(?P<value>.*?)(?P<newline>\r?\n?)$"
)


def env_names(prefix: str, section: str, key: str) -> list[str]:
    section_name = re.sub(r"[^A-Za-z0-9]+", "_", section).upper()
    key_name = re.sub(r"[^A-Za-z0-9]+", "_", key).upper()
    return [
        f"{prefix}_{section_name}__{key_name}",
        f"{prefix}_{section_name}_{key_name}",
    ]


def generate(source: Path, destination: Path, prefix: str) -> None:
    active_section: str | None = None
    rendered_lines: list[str] = []

    for line in source.read_text(encoding="utf-8").splitlines(keepends=True):
        section_match = SECTION_RE.match(line.strip())
        if section_match:
            active_section = section_match.group("section")
            rendered_lines.append(line)
            continue

        setting_match = SETTING_RE.match(line)
        if setting_match and active_section:
            key = setting_match.group("key")
            replacement = None

            for name in env_names(prefix, active_section, key):
                if name in os.environ:
                    replacement = os.environ[name]
                    break

            if replacement is not None:
                rendered_lines.append(
                    f"{setting_match.group('indent')}{key}{setting_match.group('sep')}"
                    f"{replacement}{setting_match.group('newline')}"
                )
                continue

        rendered_lines.append(line)

    destination.write_text("".join(rendered_lines), encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: generate_station_cfg.py <source> <destination>", file=sys.stderr)
        return 1

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    prefix = os.environ.get("AUTORX_ENV_PREFIX", "AUTORX")

    if not source.is_file():
        print(f"template not found: {source}", file=sys.stderr)
        return 1

    destination.parent.mkdir(parents=True, exist_ok=True)
    generate(source, destination, prefix)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
