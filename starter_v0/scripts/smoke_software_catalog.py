"""Offline smoke test for the software_catalog bonus tool (mock data only, no API key)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.software_catalog.tool import lookup_software

FAILURES: list[str] = []


def check(label: str, cond: bool, detail: str = "") -> None:
    print(f"{'PASS' if cond else 'FAIL'}  {label}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(label)


def main() -> None:
    both = lookup_software(asset_id="LT-204", software_name="Outlook")
    check("asset+software returns current", both.get("status") == "current" and both.get("approval") == "approved", str(both))

    outdated = lookup_software(asset_id="LT-240", software_name="Wi-Fi driver")
    check("outdated detected", outdated.get("status") == "outdated", str(outdated))

    by_asset = lookup_software(asset_id="LT-204")
    names = {row["software_name"] for row in by_asset.get("installed", [])}
    check("asset inventory lists installs", {"Outlook", "VPN client", "Edge"} <= names, str(names))

    by_sw = lookup_software(software_name="TeamViewer")
    check("restricted approval surfaced", by_sw.get("approval") == "restricted" and by_sw.get("installed_on") == [], str(by_sw))

    banned = lookup_software(software_name="uTorrent")
    check("banned approval surfaced", banned.get("approval") == "banned", str(banned))

    missing_asset = lookup_software(asset_id="LT-9999")
    check("unknown asset errors", missing_asset.get("error") == "asset_not_found", str(missing_asset))

    missing_sw = lookup_software(software_name="Photoshop CS2")
    check("unknown software errors with hints", missing_sw.get("error") == "software_not_found" and bool(missing_sw.get("known_software")), str(missing_sw))

    not_installed = lookup_software(asset_id="LT-204", software_name="TeamViewer")
    check("known software absent on asset", not_installed.get("error") == "not_installed", str(not_installed))

    neither = lookup_software()
    check("empty args error", neither.get("error") == "missing_argument", str(neither))

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURES: {FAILURES}")
        raise SystemExit(1)
    print("software_catalog smoke test: all 9 checks passed.")


if __name__ == "__main__":
    main()
