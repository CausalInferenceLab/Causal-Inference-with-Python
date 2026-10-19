"""원서 저장소의 변경을 확인해 한국어판 검토 이슈를 만들거나 갱신한다.

`.github/upstream.json`의 synced_sha(한국어판이 마지막으로 맞춘 원서 커밋)와 원서 브랜치 최신 커밋을 비교한다.

- 새 커밋이 있으면: 바뀐 장과 본문(마크다운 셀) 변경 요약을 담은 이슈를 만들고 검토자에게 배정한다.
  이미 열린 이슈가 있으면 본문을 최신으로 바꾸고, 새 커밋이 생겼을 때만 댓글로 알린다.
- 새 커밋이 없는데 열린 이슈가 있으면(번역 반영 PR에서 synced_sha를 올린 경우) 이슈를 닫는다.

GitHub Actions에서는 GITHUB_TOKEN과 GITHUB_REPOSITORY를 쓴다.
로컬 점검: python .github/scripts/check_upstream.py --git-dir <원서 clone> --dry-run
"""
import argparse
import difflib
import importlib.util
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT / ".github" / "upstream.json").read_text(encoding="utf-8"))
MARKER = "<!-- upstream-sync -->"
SITE = "https://causalinferencelab.github.io/Causal-Inference-with-Python"
MAX_SNIPPET = 260


def chapter_titles():
    spec = importlib.util.spec_from_file_location("prepare", ROOT / "book" / "prepare.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CHAPTERS


# ---------- 원서 정보 가져오기 (API 또는 로컬 clone) ----------

class Api:
    def __init__(self, token):
        self.token = token

    def request(self, method, url, data=None):
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "upstream-sync"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        body = json.dumps(data).encode() if data is not None else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        with urllib.request.urlopen(req) as res:
            text = res.read().decode()
            return json.loads(text) if text else None

    def get(self, url):
        return self.request("GET", url)


class Upstream:
    """원서 저장소에서 비교 결과와 파일 내용을 읽는다."""

    def __init__(self, api=None, git_dir=None):
        self.api, self.git_dir = api, git_dir
        self.repo = CONFIG["repo"]

    def head(self):
        if self.git_dir:
            return self._git("rev-parse", f"origin/{CONFIG['branch']}")
        return self.api.get(f"https://api.github.com/repos/{self.repo}/commits/{CONFIG['branch']}")["sha"]

    def compare(self, base, head):
        if self.git_dir:
            log = self._git("log", "--reverse", "--format=%H%x1f%an%x1f%ad%x1f%s", "--date=short", f"{base}..{head}")
            commits = [dict(zip(("sha", "author", "date", "message"), l.split("\x1f"))) for l in log.splitlines() if l]
            files = []
            for line in self._git("diff", "--name-status", base, head).splitlines():
                status, *paths = line.split("\t")
                files.append({"filename": paths[-1], "status": {"A": "added", "D": "removed"}.get(status[0], "modified")})
            return commits, files
        data = self.api.get(f"https://api.github.com/repos/{self.repo}/compare/{base}...{head}")
        commits = [{"sha": c["sha"], "author": c["commit"]["author"]["name"], "date": c["commit"]["author"]["date"][:10],
                    "message": c["commit"]["message"].splitlines()[0]} for c in data["commits"]]
        files = [{"filename": f["filename"], "status": f["status"]} for f in data.get("files", [])]
        return commits, files

    def read(self, sha, path):
        try:
            if self.git_dir:
                return self._git("show", f"{sha}:{path}")
            url = f"https://raw.githubusercontent.com/{self.repo}/{sha}/{path}"
            with urllib.request.urlopen(url) as res:
                return res.read().decode()
        except Exception:
            return None

    def _git(self, *args):
        return subprocess.run(["git", "-C", self.git_dir, *args], check=True, capture_output=True, text=True).stdout.strip()


# ---------- 노트북 본문 비교 ----------

def cells(text, kind):
    if not text:
        return []
    nb = json.loads(text)
    out = []
    for c in nb.get("cells", []):
        if c.get("cell_type") == kind:
            src = c.get("source", "")
            out.append("".join(src) if isinstance(src, list) else src)
    return out


def short(text):
    one = " ".join(text.split())
    return one if len(one) <= MAX_SNIPPET else one[:MAX_SNIPPET] + "…"


def word_diff(old, new, limit=3, ctx=6):
    """두 문단에서 바뀐 부분만 앞뒤 몇 단어와 함께 `기존 → 변경`으로 보여 준다."""
    a, b = old.split(), new.split()
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        before = " ".join(a[max(0, i1 - ctx):i1])
        after = " ".join(a[i2:i2 + ctx])
        removed, added = " ".join(a[i1:i2]), " ".join(b[j1:j2])
        out.append(f"…{before} ~~{removed or '∅'}~~ **{added or '∅'}** {after}…")
        if len(out) >= limit:
            break
    return out


def notebook_changes(old, new):
    """마크다운 셀 변경을 (셀 번호, 설명 줄 목록)으로, 코드 셀은 바뀐 개수만 돌려준다."""
    a, b = cells(old, "markdown"), cells(new, "markdown")
    changes = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        pairs = min(i2 - i1, j2 - j1) if tag == "replace" else 0
        for k in range(pairs):
            changes.append((j1 + k, word_diff(a[i1 + k], b[j1 + k])))
        for i in range(i1 + pairs, i2):
            changes.append((i, [f"삭제된 셀: {short(a[i])}"]))
        for j in range(j1 + pairs, j2):
            changes.append((j, [f"추가된 셀: {short(b[j])}"]))
    ca, cb = cells(old, "code"), cells(new, "code")
    code_changed = sum(max(i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in
                       difflib.SequenceMatcher(a=ca, b=cb, autojunk=False).get_opcodes() if t != "equal")
    return changes, code_changed


# ---------- 보고서 ----------

def report(base, head, commits, files, upstream, titles):
    repo, path = CONFIG["repo"], CONFIG["path"]
    lines = [
        MARKER,
        f"원서 저장소 [{repo}](https://github.com/{repo})에 한국어판이 아직 반영하지 않은 변경이 있습니다.",
        "",
        f"- 한국어판 기준 커밋: [`{base[:7]}`](https://github.com/{repo}/commit/{base}) ({CONFIG.get('synced_at', '')})",
        f"- 원서 최신 커밋: [`{head[:7]}`](https://github.com/{repo}/commit/{head})",
        f"- 전체 비교: https://github.com/{repo}/compare/{base[:12]}...{head[:12]}",
        "",
        f"### 새 커밋 {len(commits)}개",
        "",
    ]
    lines += [f"- [`{c['sha'][:7]}`](https://github.com/{repo}/commit/{c['sha']}) {c['date']} {c['message']} ({c['author']})" for c in commits]

    book_files = [f for f in files if f["filename"].startswith(path + "/") and f["filename"].endswith(".ipynb")]
    other = [f for f in files if f not in book_files]
    lines += ["", f"### 바뀐 장 {len(book_files)}개", ""]
    if not book_files:
        lines.append("책 본문 노트북은 바뀌지 않았습니다. 아래 기타 파일만 확인하면 됩니다.")
    details = []
    for f in book_files:
        key = Path(f["filename"]).stem
        title = titles.get(key, key)
        old = upstream.read(base, f["filename"]) if f["status"] != "added" else None
        new = upstream.read(head, f["filename"]) if f["status"] != "removed" else None
        changes, code_changed = notebook_changes(old, new)
        diff_url = f"https://github.com/{repo}/compare/{base[:12]}...{head[:12]}"
        summary = f"본문 셀 {len(changes)}곳, 코드 셀 {code_changed}곳"
        if f["status"] == "added":
            summary = "새로 추가된 장"
        elif f["status"] == "removed":
            summary = "원서에서 삭제됨"
        lines.append(f"- [ ] **{title}** (`{key}`): {summary} · [웹북]({SITE}/{key}.html) · [원서 변경]({diff_url})")
        if changes:
            details += ["", f"<details><summary>{title}: 본문 변경</summary>", ""]
            for i, parts in changes[:20]:
                details.append(f"- 셀 {i}")
                details += [f"  - {short(x)}" for x in parts]
            if len(changes) > 20:
                details.append(f"- …외 {len(changes) - 20}곳")
            details += ["", "</details>"]
    lines += details
    if other:
        lines += ["", "### 기타 파일", ""] + [f"- `{f['filename']}` ({f['status']})" for f in other[:50]]
    lines += [
        "",
        "### 반영 절차",
        "",
        "1. 위 목록에서 장별 변경을 확인하고, 번역에 반영할지 정합니다(오탈자·링크만 바뀐 경우는 건너뛰어도 됩니다).",
        "2. 반영할 장은 번역 가이드에 따라 고친 뒤 PR을 엽니다. PR에서 `.github/upstream.json`의 `synced_sha`를 이 이슈의 원서 최신 커밋으로, `synced_at`을 날짜로 바꿉니다.",
        "3. 메인테이너가 PR을 검토하고 머지하면 웹북에 배포되고, 다음 점검 때 이 이슈가 자동으로 닫힙니다.",
        "",
        "이 이슈는 `Upstream watch` 워크플로가 매일 자동으로 갱신합니다.",
    ]
    body = "\n".join(lines)
    return body[:60000]


# ---------- 이슈 관리 ----------

def sync_issue(api, repo, body, head, ahead):
    label = CONFIG["label"]
    base_url = f"https://api.github.com/repos/{repo}"
    try:
        api.request("POST", f"{base_url}/labels", {"name": label, "color": "a996d6", "description": "원서 변경 반영 검토"})
    except Exception:
        pass  # 이미 있음
    issues = api.get(f"{base_url}/issues?state=open&labels={label}&per_page=10")
    issue = next((i for i in issues if MARKER in (i.get("body") or "")), None)
    if not ahead:
        if issue:
            api.request("POST", f"{base_url}/issues/{issue['number']}/comments",
                        {"body": "한국어판 기준 커밋이 원서 최신 커밋과 같아져서 이 이슈를 닫습니다."})
            api.request("PATCH", f"{base_url}/issues/{issue['number']}", {"state": "closed", "state_reason": "completed"})
            print(f"closed #{issue['number']}")
        return
    title = f"[원서 변경] 반영 검토 필요 ({head[:7]})"
    if issue:
        known = issue.get("title", "").endswith(f"({head[:7]})")
        api.request("PATCH", f"{base_url}/issues/{issue['number']}", {"title": title, "body": body})
        if not known:
            mention = " ".join(f"@{r}" for r in CONFIG.get("reviewers", []))
            api.request("POST", f"{base_url}/issues/{issue['number']}/comments",
                        {"body": f"{mention} 원서에 새 커밋이 추가되어 이슈 내용을 갱신했습니다. 최신 커밋: `{head[:7]}`"})
        print(f"updated #{issue['number']}")
    else:
        new = api.request("POST", f"{base_url}/issues", {"title": title, "body": body, "labels": [label],
                                                       "assignees": CONFIG.get("reviewers", [])})
        print(f"opened #{new['number']}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--git-dir", help="원서 저장소 로컬 clone (API 대신 사용)")
    parser.add_argument("--base", help="비교 기준 커밋 (기본: upstream.json의 synced_sha)")
    parser.add_argument("--dry-run", action="store_true", help="이슈를 만들지 않고 보고서만 출력")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")
    api = Api(token)
    upstream = Upstream(api=None if args.git_dir else api, git_dir=args.git_dir)
    base = args.base or CONFIG["synced_sha"]
    head = upstream.head()
    commits, files = ([], []) if head == base else upstream.compare(base, head)
    body = report(base, head, commits, files, upstream, chapter_titles()) if commits else ""

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        Path(summary).write_text(body or f"원서 변경 없음 (기준 `{base[:7]}` = 최신 `{head[:7]}`)", encoding="utf-8")
    if args.dry_run:
        print(body or f"no upstream changes since {base[:7]}")
        return
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        sys.exit("GITHUB_REPOSITORY가 없습니다. 로컬에서는 --dry-run으로 실행하세요.")
    sync_issue(api, repo, body, head, bool(commits))


if __name__ == "__main__":
    main()
