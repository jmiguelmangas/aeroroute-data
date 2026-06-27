"""Explicit local data-bundle commands; no automatic downloads."""

from __future__ import annotations

import argparse
from pathlib import Path

from aeroroute_data.bundles.airports import build_airport_bundle
from aeroroute_data.mvp_airports import write_mvp_airports_csv


def main() -> None:
    parser = argparse.ArgumentParser(prog="aeroroute-data")
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build-airports")
    build.add_argument("--source", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--version", required=True)
    mvp = commands.add_parser("build-mvp-airports")
    mvp.add_argument("--source", type=Path, required=True)
    mvp.add_argument("--output", type=Path, required=True)
    mvp.add_argument("--version", required=True)
    arguments = parser.parse_args()
    if arguments.command == "build-airports":
        manifest = build_airport_bundle(
            arguments.source, arguments.output, arguments.version
        )
        print(f"bundle_sha256={manifest.bundle_sha256}")
    if arguments.command == "build-mvp-airports":
        selected_csv = arguments.output / "airports.source.csv"
        write_mvp_airports_csv(arguments.source, selected_csv)
        manifest = build_airport_bundle(
            selected_csv, arguments.output, arguments.version
        )
        print(
            f"accepted={manifest.accepted_rows} "
            f"bundle_sha256={manifest.bundle_sha256}"
        )
