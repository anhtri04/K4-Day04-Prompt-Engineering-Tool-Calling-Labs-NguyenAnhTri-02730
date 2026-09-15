---
name: software_catalog
track: bonus
kind: local_inventory
provider: mock_software_catalog
requires_env: []
inputs: [asset_id, software_name]
outputs: [installed, installed_version, latest_approved_version, status, approval, license]
side_effect: false
---
# software_catalog

Looks up the fictional software catalog under
`helpdesk_data/software_catalog.json`. It answers three questions from mock
data only: which software is installed on an asset, what the latest approved
version / license / approval status of a software is, and whether a specific
software on a specific asset is current, outdated, restricted or unapproved.

Give `asset_id`, `software_name`, or both. At least one is required.
Unknown assets return `asset_not_found`; unknown software returns
`software_not_found`; a known software missing on an asset returns
`not_installed`. Statuses are computed, never guessed.
