"""Quarto 빌드용 원고를 만든다.

원본 노트북(causal-inference-for-the-brave-and-true/*.ipynb)은 원서와 같은 구조를 유지해야 하므로
직접 고치지 않고, book/ 아래에 빌드 전용 사본을 만들어 다음만 바꾼다.

- 장 제목: 원문 영어 H1을 지우고 한국어 장 제목을 front matter로 넣는다.
- 수식: 한 줄에 `$`만 있는 블록 수식을 `$$`로 바꾸고, 인라인 수식 안쪽 공백(`$ x $`)을 지운다(Pandoc은 둘 다 수식으로 읽지 않는다).
- `hide-input` 태그: 코드를 접어 두는 Quarto 옵션(code-fold)으로 바꾼다.
- 대체 텍스트가 `img`뿐인 이미지: 그림 캡션으로 찍히지 않게 비운다.
- `{note}` 지시문과 `> 옮긴이:` 인용문: Quarto 콜아웃으로 바꾼다.
- 장 설명: 첫 문단을 front matter `description`으로 넣어 검색엔진과 공유 카드에 쓴다.
- 용어 찾아보기: TRANSLATION_GUIDE.md 용어표로 glossary.qmd를 만들고, 용어가 많이 나오는 장을 잇는다.

실행: python book/prepare.py
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "causal-inference-for-the-brave-and-true"
OUT = ROOT / "book"

CHAPTERS = {
    "01-Introduction-To-Causality": "인과추론 소개",
    "02-Randomised-Experiments": "무작위 실험",
    "03-Stats-Review-The-Most-Dangerous-Equation": "통계 복습: 가장 위험한 수식",
    "04-Graphical-Causal-Models": "그래프 인과 모델",
    "05-The-Unreasonable-Effectiveness-of-Linear-Regression": "선형회귀의 터무니없는 효과",
    "06-Grouped-and-Dummy-Regression": "그룹 회귀와 더미 회귀",
    "07-Beyond-Confounders": "교란 요인을 넘어서",
    "08-Instrumental-Variables": "도구변수",
    "09-Non-Compliance-and-LATE": "불응과 LATE",
    "10-Matching": "매칭",
    "11-Propensity-Score": "성향점수",
    "12-Doubly-Robust-Estimation": "이중 강건 추정",
    "13-Difference-in-Differences": "이중차분법",
    "14-Panel-Data-and-Fixed-Effects": "패널데이터와 고정효과",
    "15-Synthetic-Control": "통제집단합성법",
    "16-Regression-Discontinuity-Design": "회귀 불연속 설계",
    "17-Predictive-Models-101": "예측 모델 101",
    "18-Heterogeneous-Treatment-Effects-and-Personalization": "이질적 처치효과와 개인화",
    "19-Evaluating-Causal-Models": "인과 모델 평가",
    "20-Plug-and-Play-Estimators": "플러그 앤 플레이 추정량",
    "21-Meta-Learners": "메타러너",
    "22-Debiased-Orthogonal-Machine-Learning": "편향 제거/직교화 머신러닝",
    "23-Challenges-with-Effect-Heterogeneity-and-Nonlinearity": "효과 이질성과 비선형성",
    "24-The-Diff-in-Diff-Saga": "이중차분법 사가",
    "25-Synthetic-Diff-in-Diff": "합성 이중차분법",
    "Debiasing-with-Orthogonalization": "직교화로 편향 제거하기",
    "Debiasing-with-Propensity-Score": "성향점수로 편향 제거하기",
    "When-Prediction-Fails": "예측이 실패할 때",
    "Prediction-Metrics-For-Causal-Models": "예측 지표가 인과 모델에 위험한 이유",
    "Conformal-Inference-for-Synthetic-Control": "통제집단합성법의 컨포멀 추론",
}


def src_text(cell):
    s = cell["source"]
    return "".join(s) if isinstance(s, list) else s


def set_text(cell, text):
    lines = text.split("\n")
    cell["source"] = [line + "\n" for line in lines[:-1]] + [lines[-1]]


PROTECT = re.compile(r"(```.*?```|`[^`\n]*`|\$\$.*?\$\$)", re.S)
INLINE = re.compile(r"(?<![\\$])\$(?!\$)([^$\n]+?)(?<![\\$])\$(?!\$)")


def fix_inline_math(text):
    parts = PROTECT.split(text)
    for i in range(0, len(parts), 2):
        parts[i] = INLINE.sub(lambda m: "$" + m.group(1).strip() + "$", parts[i])
    return "".join(parts)


def fix_markdown(text):
    # 대체 텍스트가 "img"뿐인 이미지는 캡션으로 찍히지 않게 비운다
    text = re.sub(r"!\[img\]\(", "![](", text)
    # 한 줄짜리 `$` 블록 수식 → `$$`
    text = re.sub(r"(?m)^[ \t]*\$[ \t]*$", "$$", text)
    # 인라인 수식 `$ x $`처럼 안쪽에 공백이 있으면 Pandoc이 수식으로 읽지 않으므로 공백을 지운다
    text = fix_inline_math(text)
    # MyST {note} → Quarto 콜아웃
    text = re.sub(r"```\{note\}\n(.*?)\n```", r"::: {.callout-note}\n\1\n:::", text, flags=re.S)
    # 원문의 잘못된 note 펜스(```note)도 같은 콜아웃으로
    text = re.sub(r"```note\n(.*?)\n```", r"::: {.callout-note}\n\1\n:::", text, flags=re.S)

    # > 옮긴이: ... 인용문(여러 줄 포함) → 옮긴이 콜아웃
    def translator_note(m):
        body = re.sub(r"(?m)^> ?", "", m.group(0))
        body = re.sub(r"^옮긴이:\s*", "", body.strip())
        return '::: {.callout-tip appearance="simple" title="옮긴이"}\n' + body + "\n:::"

    text = re.sub(r"(?m)^> 옮긴이:.*(?:\n>.*)*", translator_note, text)
    return text


TEXTS = {}


def describe(md, limit=150):
    """첫 문단을 평문으로 줄여 장 설명으로 쓴다."""
    for para in re.split(r"\n\s*\n", md):
        p = para.strip()
        if not p or p.startswith(("#", "!", "<", "|", "```", ":::", ">", "$")):
            continue
        p = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", p)
        p = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", p)
        p = re.sub(r"\$[^$]*\$", "", p)
        p = re.sub(r"[*_`]", "", p)
        p = re.sub(r"\s+", " ", p).strip()
        if len(p) < 40:
            continue
        return p if len(p) <= limit else p[:limit].rsplit(" ", 1)[0] + "…"
    return ""


def label(key):
    keys = list(CHAPTERS)
    i = keys.index(key)
    if i < 25:
        return f"{i + 1}장 {CHAPTERS[key]}"
    return f"부록 {chr(65 + i - 25)} {CHAPTERS[key]}"


# 검색할 때 띄어 쓰는 경우가 많은 용어. 용어 찾아보기에 함께 적어 두면 띄어 써서 검색해도 찾힌다.
SPACED = {
    "도구변수": "도구 변수", "성향점수": "성향 점수", "처치효과": "처치 효과", "패널데이터": "패널 데이터",
    "이중차분법": "이중 차분법", "통제집단합성법": "통제 집단 합성법", "회귀분석": "회귀 분석",
    "선택편향": "선택 편향", "교란편향": "교란 편향", "고정효과": "고정 효과", "메타러너": "메타 러너",
    "더미변수": "더미 변수", "결과변수": "결과 변수", "처치변수": "처치 변수", "인과추론": "인과 추론",
    "인과관계": "인과 관계", "역확률": "역 확률", "표준오차": "표준 오차", "신뢰구간": "신뢰 구간",
}


def build_glossary():
    """번역 가이드 용어표로 용어 찾아보기 페이지를 만든다."""
    guide = (ROOT / "TRANSLATION_GUIDE.md").read_text(encoding="utf-8")
    body = guide.split("## 3. 용어표", 1)[1].split("\n## ", 1)[0]
    out = [
        "---",
        'description: "이 책에서 쓴 인과추론 용어의 번역어와 원어, 그 용어를 주로 다루는 장을 모았습니다."',
        "---",
        "",
        "# 용어 찾아보기 {.unnumbered}",
        "",
        "이 책에서 쓴 번역어와 원어, 그 용어가 많이 나오는 장을 모았습니다. "
        "번역어는 『실무로 통하는 인과추론 with 파이썬』과 같습니다. "
        "다른 책이나 자료에서 본 표기(예: 처치군, 통제군)로 검색해도 이 페이지에서 찾을 수 있습니다.",
        "",
    ]
    order = list(CHAPTERS)
    for section in re.split(r"(?m)^### ", body)[1:]:
        heading, _, rest = section.partition("\n")
        items = []
        for line in rest.splitlines():
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) < 2 or cols[0] in ("원어", "---") or set(cols[0]) <= {"-"}:
                continue
            en, ko = cols[0], cols[1]
            note = cols[2] if len(cols) > 2 else ""
            variants = [re.sub(r"\s*\([^)]*\)", "", v).strip() for v in ko.split("/")]
            variants = [v[:-1] if v.endswith("다") and len(v) > 2 else v for v in variants if len(v) >= 2]

            def score(k):
                text = TEXTS.get(k, "")
                n = sum(text.count(v) for v in variants)
                if not n:
                    return 0
                # 긴 장이 무조건 앞서지 않도록 길이로 나누고, 원어를 병기해 처음 소개하는 장에 가산점
                intro = any(re.search(re.escape(v) + r"\s*\([A-Za-z]", text) for v in variants)
                return n / max(len(text), 1) * 10000 + (5 if intro else 0)

            scores = {k: score(k) for k in order}
            top = sorted((k for k in order if scores[k]), key=lambda k: -scores[k])[:3]
            top.sort(key=order.index)
            others = [a for a in re.findall(r"`([^`]+)`", note) if "쓰지" in note]
            line_out = f"- **{ko}** · {en}"
            for w, spaced in SPACED.items():
                if w in ko:
                    alias = re.sub(r"\s*\([^)]*\)", "", ko.replace(w, spaced)).strip()
                    if alias not in others:
                        others.append(alias)
            if others:
                line_out += f" · 다른 표기: {', '.join(others)}"
            if top:
                line_out += " · " + ", ".join(f"[{label(k)}]({k}.html)" for k in top)
            items.append(line_out)
        if items:
            out += [f"## {heading.strip()}", ""] + items + [""]
    (OUT / "glossary.qmd").write_text("\n".join(out), encoding="utf-8")


def prepare_notebook(key, title):
    nb = json.loads((SRC / f"{key}.ipynb").read_text(encoding="utf-8"))
    cells = nb["cells"]
    for cell in cells:
        if cell["cell_type"] == "markdown":
            set_text(cell, fix_markdown(src_text(cell)))
        elif cell["cell_type"] == "code":
            tags = cell.get("metadata", {}).get("tags", [])
            if "hide-input" in tags and src_text(cell).strip():
                set_text(cell, "#| code-fold: true\n" + src_text(cell))

    # 원문 영어 H1을 지우고 한국어 제목을 front matter로
    for cell in cells:
        if cell["cell_type"] == "markdown":
            text = src_text(cell)
            stripped = re.sub(r"\A\s*# [^\n]*\n?", "", text, count=1)
            if stripped != text:
                set_text(cell, stripped.lstrip("\n"))
            break
    md = "\n\n".join(src_text(c) for c in cells if c["cell_type"] == "markdown")
    TEXTS[key] = md
    desc = describe(md)
    front_lines = [f'title: "{title}"'] + ([f"description: {json.dumps(desc, ensure_ascii=False)}"] if desc else [])
    front = {"cell_type": "raw", "metadata": {}, "source": ["---\n" + "\n".join(front_lines) + "\n---"]}
    nb["cells"] = [front] + [c for c in cells if not (c["cell_type"] == "markdown" and not src_text(c).strip())]
    (OUT / f"{key}.ipynb").write_text(json.dumps(nb, ensure_ascii=False), encoding="utf-8")


def main():
    for key, title in CHAPTERS.items():
        prepare_notebook(key, title)
    build_glossary()
    # 이미지·데이터와 노트북이 import하는 보조 모듈
    data = OUT / "data"
    if data.is_symlink() or data.exists():
        data.unlink() if data.is_symlink() else shutil.rmtree(data)
    shutil.copytree(SRC / "data" / "img", data / "img")
    for helper in SRC.glob("*.py"):
        shutil.copy(helper, OUT / helper.name)
    print(f"prepared {len(CHAPTERS)} notebooks into {OUT}")


if __name__ == "__main__":
    main()
