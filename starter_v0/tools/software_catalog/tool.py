from __future__ import annotations

import json
from typing import Any

from tools._shared import ROOT, err, fold_text


CATALOG_FILE = ROOT / "helpdesk_data" / "software_catalog.json"


def _norm(value: str) -> str:
    return fold_text(value or "").strip()


def _load() -> dict[str, Any]:
    return json.loads(CATALOG_FILE.read_text(encoding="utf-8"))


def _status(installed: str, latest: str, approval: str) -> str:
    if approval == "banned":
        return "unapproved"
    if approval == "restricted":
        return "restricted"
    if not latest:
        return "unknown"
    return "current" if installed.strip() == latest.strip() else "outdated"


def lookup_software(asset_id: str = "", software_name: str = "") -> dict[str, Any]:
    """Tra cứu catalog phần mềm giả lập: bản đã cài / bản được duyệt / license / approval."""
    try:
        data = _load()
        catalog = {_norm(item["name"]): item for item in data["catalog"]}
        asset = (asset_id or "").strip().upper()
        wanted = _norm(software_name)

        if not asset and not wanted:
            return {"tool": "software_catalog", "error": "missing_argument"}

        if asset and not wanted:
            known_assets = sorted({r["asset_id"] for r in data["installs"]})
            if asset not in known_assets:
                return {"tool": "software_catalog", "asset_id": asset, "error": "asset_not_found"}
            rows = [r for r in data["installs"] if r["asset_id"] == asset]
            installed = []
            for row in rows:
                entry = catalog.get(_norm(row["software_name"]), {})
                installed.append({
                    "software_name": row["software_name"],
                    "installed_version": row["installed_version"],
                    "latest_approved_version": entry.get("latest_approved_version", ""),
                    "status": _status(row["installed_version"], entry.get("latest_approved_version", ""), entry.get("approval", "")),
                    "approval": entry.get("approval", "unknown"),
                    "license": entry.get("license", "unknown"),
                })
            return {"tool": "software_catalog", "asset_id": asset, "installed": installed}

        if wanted and not asset:
            entry = catalog.get(wanted)
            if entry is None:
                return {
                    "tool": "software_catalog",
                    "software_name": (software_name or "").strip(),
                    "error": "software_not_found",
                    "known_software": sorted(item["name"] for item in data["catalog"]),
                }
            on_assets = []
            for row in data["installs"]:
                if _norm(row["software_name"]) == wanted:
                    on_assets.append({
                        "asset_id": row["asset_id"],
                        "installed_version": row["installed_version"],
                        "status": _status(row["installed_version"], entry.get("latest_approved_version", ""), entry.get("approval", "")),
                    })
            return {
                "tool": "software_catalog",
                "software_name": entry["name"],
                "vendor": entry.get("vendor", ""),
                "latest_approved_version": entry.get("latest_approved_version", ""),
                "license": entry.get("license", "unknown"),
                "approval": entry.get("approval", "unknown"),
                "note": entry.get("note", ""),
                "installed_on": on_assets,
            }

        entry = catalog.get(wanted)
        if entry is None:
            return {
                "tool": "software_catalog",
                "asset_id": asset,
                "software_name": (software_name or "").strip(),
                "error": "software_not_found",
            }
        row = next((r for r in data["installs"] if r["asset_id"] == asset and _norm(r["software_name"]) == wanted), None)
        if row is None:
            return {
                "tool": "software_catalog",
                "asset_id": asset,
                "software_name": entry["name"],
                "error": "not_installed",
                "latest_approved_version": entry.get("latest_approved_version", ""),
                "approval": entry.get("approval", "unknown"),
            }
        return {
            "tool": "software_catalog",
            "asset_id": asset,
            "software_name": entry["name"],
            "installed_version": row["installed_version"],
            "latest_approved_version": entry.get("latest_approved_version", ""),
            "status": _status(row["installed_version"], entry.get("latest_approved_version", ""), entry.get("approval", "")),
            "approval": entry.get("approval", "unknown"),
            "license": entry.get("license", "unknown"),
        }
    except Exception as exc:
        return err("software_catalog", exc)
