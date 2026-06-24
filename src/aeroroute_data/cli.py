"""Explicit local data-bundle commands; no automatic downloads."""

from __future__ import annotations

import argparse
from pathlib import Path

from aeroroute_data.bundles.airports import build_airport_bundle


def main() -> None:
    parser = argparse.ArgumentParser(prog="aeroroute-data")
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build-airports")
    build.add_argument("--source", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--version", required=True)
    arguments = parser.parse_args()
    if arguments.command == "build-airports":
        manifest = build_airport_bundle(
            arguments.source, arguments.output, arguments.version
        )
        print(f"bundle_sha256={manifest.bundle_sha256}")
