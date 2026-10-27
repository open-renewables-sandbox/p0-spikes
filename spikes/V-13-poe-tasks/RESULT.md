# V-13 poethepoet tasks and local pre-commit hooks: result

Date: 2026-10-27. Labels: **[Test]**. Project: this folder, a throwaway `pyproject.toml` with `[tool.poe.tasks]` mirroring I-16 (`install`, `check`, `test`, plus a `shell` probe), ruff, mypy `--strict`, pytest and `repo: local` pre-commit hooks that run `uv run`. Driver: `../V-13-run.sh` (fresh `git clone` of a seeded repository, then each step with its exit code). Runs: GitHub Actions run [40451497123](https://github.com/open-renewables-sandbox/p0-spikes/actions/runs/40451497123) (ubuntu, macOS arm64, Windows × Python 3.11 and 3.14) and this Windows machine under Python 3.11 and 3.14 in Git Bash, plus `check`, `shell-probe` and `test` from PowerShell. Tools: poethepoet 0.49.0, uv 0.11.x on the runners, pre-commit 4.x.

## Outcome

**Every step passed on all three systems and both Python versions**, except two behaviours to note. `uv run poe install` worked on every fresh clone (it ran `uv sync --all-groups` then `pre-commit install`), `uv run poe check` (lock check, ruff check and format, mypy strict, a script) and `uv run poe test` passed, and the `repo: local` hooks ran through `uv run` on commit on all of them (two hooks "Passed" on each of the eight runs).

| Step | ubuntu | macOS | Windows hosted | Windows local (Git Bash) | Windows local (PowerShell) |
| --- | --- | --- | --- | --- | --- |
| `poe install` on a fresh clone | pass | pass | pass | pass | not run |
| `poe check` | pass | pass | pass | pass | ran; failed only on a line-ending artefact of my test edit (below) |
| `poe test` | pass | pass | pass | pass | pass |
| `poe shell-probe` (`echo one && echo two`) | pass | pass | pass | pass | pass |
| pre-commit `repo: local` hooks on commit | pass | pass | pass | pass | not run |

## Behaviours to note

- `uv run poe` with no task prints the task list but **exits 1** (poethepoet reports "No task specified"). I-16 says it lists the tasks, which is true; CI must not call it bare.
- Without a `.python-version`, `uv` picked the highest installed interpreter (3.13.16 locally), not 3.12. The template's `.python-version` (AD-03) is needed for that reason.
- My PowerShell `check` failed at `ruff format --check` because the test appended an LF line to a file that Git for Windows had checked out as CRLF (`core.autocrlf=true` is set globally on this machine), leaving mixed line endings. The V-13 project, like the fixture, sits under a `.gitattributes` of `* text=auto eol=lf`. **SDD §6 has no `.gitattributes` in the layout**; a checkout on Windows without one is exposed to this. Recorded as a P1 input, not a decision.
- A `shell` task with `&&` worked on Windows because Git for Windows' shell was found; a `cmd` task has no such dependency. The `shell` form is better avoided in the template's tasks.

## Not tested

macOS or Linux hardware (hosted runners only); Windows without Git for Windows; pre-commit's own hook environments (not used: all hooks are `language: system`); `gitleaks` and `lychee` hooks; real project size.

## Feeds

I-16, I-17, AD-20, FR2.11 confirmed on three systems. **P-12 is not triggered.** The `.gitattributes` and `.python-version` points go to P1 planning.
