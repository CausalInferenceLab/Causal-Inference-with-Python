"""Quarto 빌드용 원고를 만든다.

원본 노트북(causal-inference-for-the-brave-and-true/*.ipynb)은 원서와 같은 구조를 유지해야 하므로
직접 고치지 않고, book/ 아래에 빌드 전용 사본을 만들어 다음만 바꾼다.

- 장 제목: 원문 영어 H1을 지우고 한국어 장 제목을 front matter로 넣는다.
- 수식: 한 줄에 `$`만 있는 블록 수식을 `$$`로 바꾼다(Pandoc은 단일 `$` 블록을 수식으로 읽지 않는다).
- `hide-input` 태그: 코드를 접어 두는 Quarto 옵션(code-fold)으로 바꾼다.
- 대체 텍스트가 `img`뿐인 이미지: 그림 캡션으로 찍히지 않게 비운다.
- `{note}` 지시문과 `> 옮긴이:` 인용문: Quarto 콜아웃으로 바꾼다.

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


def fix_markdown(text):
    # 대체 텍스트가 "img"뿐인 이미지는 캡션으로 찍히지 않게 비운다
    text = re.sub(r"!\[img\]\(", "![](", text)
    # 한 줄짜리 `$` 블록 수식 → `$$`
    text = re.sub(r"(?m)^[ \t]*\$[ \t]*$", "$$", text)
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
    front = {"cell_type": "raw", "metadata": {}, "source": [f'---\ntitle: "{title}"\n---']}
    nb["cells"] = [front] + [c for c in cells if not (c["cell_type"] == "markdown" and not src_text(c).strip())]
    (OUT / f"{key}.ipynb").write_text(json.dumps(nb, ensure_ascii=False), encoding="utf-8")


def main():
    for key, title in CHAPTERS.items():
        prepare_notebook(key, title)
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
