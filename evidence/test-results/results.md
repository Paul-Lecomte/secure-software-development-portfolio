# Security test results — Python routing backend

**Repository:** `fastest_path_backend`
**Commit:** `90a50769c4c2013f8e2f7d0241d883cc7b3befd2` (origin/main)
**Date audited:** 21 October 2026 (test runs captured 22 October 2026)
**Environment:** Python 3.12.10 (win32), pytest 9.1.1
**Installed dependencies:** grpcio 1.78.0, grpcio-tools 1.78.0, neo4j 6.1.0, numba 0.64.0, numpy 2.4.3, pandas 3.0.1, protobuf 6.33.6, python-dotenv 1.2.2

## 1. Baseline (before the fix)

Command: `python -m pytest tests/test_smoke.py -q`

Result: **26 passed** in 2.84s

All existing algorithm smoke tests (RAPTOR, Dijkstra, A*, HTTP origin/destination resolution, transfer caps, adaptive expansion) passed.

## 2. After the fix (request-body size ceiling)

Command: `python -m pytest tests/test_smoke.py tests/test_request_limits.py -q`

Result: **32 passed** in 2.79s
- 26 existing smoke tests: pass (no regression)
- 6 new request-limit tests: pass

Both runs above are captured verbatim in `pytest-results.txt`; the timings quoted here are taken from that file.

## 3. New regression tests (`tests/test_request_limits.py`)

| Test | What it verifies | Result |
|---|---|---|
| `test_normal_payload_accepted` | Well-formed `/path` body not rejected for size | PASSED |
| `test_missing_content_length_rejected` | Missing `Content-Length` → 400 `missing_content_length` | PASSED |
| `test_oversized_body_rejected_413` | Body above limit → 413 `request_entity_too_large` | PASSED |
| `test_body_at_limit_accepted` | Body exactly at the limit accepted | PASSED |
| `test_negative_content_length_rejected` | Negative `Content-Length` → 400 `invalid_content_length` | PASSED |
| `test_invalid_content_length_rejected` | Non-numeric `Content-Length` → 400 `invalid_content_length` | PASSED |

## 4. Before-and-after comparison

| Behaviour | Before | After |
|---|---|---|
| Oversized `Content-Length` body | Attempted `self.rfile.read(length)` — potential memory exhaustion / DoS | HTTP 413 `request_entity_too_large` before any allocation |
| Negative `Content-Length` | Passed to `read()` (undefined/undesirable) | HTTP 400 `invalid_content_length` |
| Normal request | Processed normally | Processed normally (no change) |
| Test suite | 26 passed | 32 passed (no regression) |

## 5. Static analysis / dependency checks

No dedicated SAST (e.g., `bandit`) or dependency-audit tool (e.g., `pip-audit`, `safety`) was installed in the audit environment, so no scanner output is claimed. Dependency versions were recorded. Adding `bandit` and `pip-audit` to CI is listed as future work.

## 6. Evidence location

The change and tests live in the local audit clone
`C:\Users\lecom\audit-work\backend` (files `src/http_server.py` and
`tests/test_request_limits.py`). They have **not** been pushed to the origin
repository, per the requirement not to modify the student's repositories
without authorisation.

Raw pytest output: `pytest-results.txt`
