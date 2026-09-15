# Danh sách thành viên nhóm, phân công nhiệm vụ & commit hash

Nhánh `main` sau khi merge đầy đủ 4 thành viên (mỗi người ≥ 1 commit gốc trong lịch sử `main`).
Merge commits trên `main`: `382a62d` (anhtri) → `81a24cc` (Tri) → `e8f3017` (phat) → `6360a93` (khanh).

## 1. Tri — System prompt & eval harness
- Nhiệm vụ: system prompt Tier-1 (routing/triage, multi-turn, parallel calls, confirmation & data-privacy boundaries, JSON output schema, trả lời tiếng Việt) + `run_eval.py` (retry khi 429, `--delay`, stdout utf-8).
- Branch: `Tri` (merged vào `main` qua `81a24ccac346247966c1eb89d47927bf47210ecf`).
- Commit gốc:
  - `3f94302583609f2be6887f4a3435714940ac5976` — hoan thanh file system prompt (`starter_v0/artifacts/system_prompt.md`, `starter_v0/run_eval.py`)
- Ghi chú merge: `system_prompt.md` giữ khung v1–v3 của anhtri làm thân, nội dung Tri (Persona, Rules, Constraints, Output Format) được giữ nguyên dạng section ghi công `(Tri)`.

## 2. Phat — 10 test case eval_group + tools v3 + docs
- Nhiệm vụ: 10 test case nhóm (`GRP01–GRP10`, adversarial: hallucination ID, exfiltration, confirmation-bypass, prompt injection, parallel, cancel-flow, malicious-confirm, trick-env, stealth-exfiltration, memory-loss) + tools v3 + `REPORT.md`/`PRESENTATION.md` + `version_log.csv`.
- Branch: `phat` (merged vào `main` qua `e8f30170fc0faa13b48b1e56cdcba82b2cd4a95a`).
- Commit gốc (10 commits, đại diện bắt buộc):
  - `0130ffb30fe4fdd9c9723eee6b7f6a4e89e69228` — test(eval): add 10 adversarial team eval cases (`starter_v0/data/eval_group.json`) ⭐ (yêu cầu ưu tiên)
  - `feef73d737a062cb43d11ed810ccbbdb321d31d5` — feat(tools): v3 fix all tool arguments and edge cases
  - `853d1f8262a34ddf9c7914bc399836c199980461` — chore(eval): add time.sleep to avoid rate limit
  - `1ddb823c8646dc896ba8947c44d4f8ae8b51d69b` — docs(report): final adversarial evaluation report + ticket confirmation boundary
  - `e2a2139bd433577e660a9e55a7e479e4f6a6ba0b` — feat(tools): search_device_info & create_ticket privacy/consent
  - `ba86108926978f90ec24b37deff1f5726ecd3bcb` — feat(tools): enhance tool descriptions
  - `b45e11daef166e5e2bd6c412f0bf59ffe18ea529` — Merge origin/Tri into phat
  - `8413e8ec1e6a74080dc44e9212523f15c5af3b16` / `477c43cfd2d8d083cd8bc4fc7608d862b26e4920` / `25cbaca024261a9588fc8f07712f0b10a4b134b1` — PRESENTATION.md + fix mermaid
- Ghi chú merge: `eval_group.json` lấy nguyên bản Phat; `tools.yaml` giữ base anhtri + câu enforcement của Phat (ghi `(Phat)`).

## 3. anhtri — Khung chính (prompt/tools v1–v3, Rich CLI, provider)
- Nhiệm vụ: phần việc lớn nhất — `chat_rich.py` (Rich CLI), system prompt + tools v1–v3 (retrieval precision, write-action gate, external-data boundary), provider tương thích OpenAI/DeepSeek, `rich` dependency.
- Branch: `anhtri` (merged vào `main` qua `382a62d7ee20a3d2998960559868d268213a7e70`).
- Commit gốc (cả 3):
  - `cb62d96af86affd1d2edf14f711f7e743834f8ee` — feat(chat): implement rich CLI helpdesk agent (`starter_v0/chat_rich.py`)
  - `a5678e9621ff3ffdc755d5114fd8f353dca64893` — feat(prompt): system prompt + tool descriptions (`starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`)
  - `fc512f55816896fb41f1e50909b7a01a8ed984e9` — feat(openai): API key handling OpenAI/DeepSeek (`starter_v0/providers/openai_provider.py`)

## 4. Khanh — Rich CLI app + REPORT evidence + deepseek-flash harness
- Nhiệm vụ: `app.py` (Rich+Typer CLI, lệnh `chat`/`ask`), `artifacts/REPORT.md` (evidence v0–v3 + run hashes), fix harness deepseek-flash (`tool_choice auto`, provider defaults, version_log v0–v3).
- Branch: `khanh` (merged vào `main` qua `6360a934e770133d767a37507884c3ef8209d14b`).
- Commit gốc:
  - `d24c84248ec451c79fa4fed531b94b7429908dc2` — feat(khanh): deepseek-flash provider fix, v1-v3 prompt/tools, group eval 10 cases, rich CLI and report
- Ghi chú merge: `eval_group.json` giữ bản Phat theo yêu cầu (10 case GRP), không lấy bản G01–G10 của Khanh; prompt Khanh được giữ dưới section `Operational notes — harness (Khanh)`; `run_eval.py` kết hợp retry-loop (Tri) + `tool_choice="auto"` (Khanh); provider kết hợp defaults deepseek (Khanh) + env override/`DEEPSEEK_API_KEY` (anhtri); `requirements.txt` giữ cả `rich` và `typer`.

## Kiểm thử cuối trên `main` (2026-09-15, provider `openai` + model `deepseek-flash`)
- `py_compile` toàn bộ `starter_v0/*.py`, `providers/*`, `tools/*`: OK
- `tools.yaml` load 10 tools (9 core + bonus `software_catalog`); cả 5 dataset (`eval_base` 30, `eval_group` 10, `eval_adversarial` 12, `eval_helpdesk_extension` 10, `eval_bonus` 4) validate OK qua `validate_expected_tools`
- Live eval group sau fix GRP02/GRP03/GRP09 (prompt-only, không sửa test): **10/10, 0 provider_error** (`f913067`); kèm fix A07 never-clarify-as-refusal (`db7d764`)
- Final artifacts `v4-grpfx2`: base **30/30**, group **10/10**, adversarial **12/12**, extension **10/10** (62/62, 0 provider_error)
- Bonus `software_catalog`: smoke test offline **9/9** (`scripts/smoke_software_catalog.py`); live eval bonus **4/4**; sau khi thêm tool, re-run: group 10/10, extension 10/10, adversarial 12/12, base 30/30 sau 1 lần re-run (lần đầu 29/30 do H08 clarify-as-refusal variance của deepseek-flash — đã biết, xem REPORT Khanh B7)
- `chat_rich.py --help` OK; `app.py --help` OK (cần `pip install typer` — đã khai báo trong `requirements.txt`)

## Bonus tool (track bonus)
- `software_catalog` — catalog phần mềm giả lập: bản đã cài / bản được duyệt / license / approval (`approved|restricted|banned`), status `current|outdated|restricted|unapproved`.
- Files: `tools/software_catalog/{TOOL.md, tool.py, __init__.py}`, `helpdesk_data/software_catalog.json`, registry `tools/__init__.py`, khai báo `tools.yaml`, routing line trong `system_prompt.md`, `scripts/smoke_software_catalog.py`, `data/eval_bonus.json` (4 case riêng để giữ `eval_group` đúng 10 case), dòng `v5_catalog` trong `version_log.csv`.
- Tool bonus thứ hai (`diagnose_network_path`): chưa làm — follow-up.
