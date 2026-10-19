"""렌더링 뒤처리: 검색 색인(search.json)의 수식 기호를 읽기 쉽게 바꾼다.

검색 결과 미리보기는 수식을 그리지 않으므로 `\\(Y_1 \\perp T\\)` 같은 TeX 원문이 그대로 보인다.
구분 기호를 지우고 자주 쓰는 기호만 유니코드로 바꾼다. 검색 대상 문자열에만 적용되고 본문은 그대로다.
"""
import json
import os
import re
from pathlib import Path

OUT = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", Path(__file__).parent / "_book"))
SYMBOLS = {
    "perp": "⊥", "mid": "|", "times": "×", "cdot": "·", "leq": "≤", "geq": "≥", "neq": "≠",
    "approx": "≈", "sum": "Σ", "infty": "∞", "alpha": "α", "beta": "β", "gamma": "γ",
    "delta": "δ", "epsilon": "ε", "varepsilon": "ε", "theta": "θ", "lambda": "λ", "mu": "μ",
    "pi": "π", "sigma": "σ", "tau": "τ", "phi": "φ", "rightarrow": "→", "to": "→",
}


def tex_to_plain(tex):
    tex = re.sub(r"\\[!,;: ]", "", tex)
    tex = re.sub(r"\\(?:hat|bar|tilde|mathbb|mathcal|mathrm|text|operatorname|underbrace|overbrace|left|right|big|Big|frac|displaystyle)\b", "", tex)
    tex = re.sub(r"\\([A-Za-z]+)", lambda m: SYMBOLS.get(m.group(1), m.group(1)), tex)
    tex = re.sub(r"⊥(\s*⊥)+", "⊥", tex)
    tex = tex.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"\s{2,}", " ", tex).strip()


def clean(text):
    """\\( \\)와 \\[ \\] 안의 수식만 평문으로 바꾼다."""
    return re.sub(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", lambda m: tex_to_plain(m.group(1) or m.group(2) or ""), text, flags=re.S)


def main():
    path = OUT / "search.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    for item in data:
        for key in ("text", "section", "title"):
            if isinstance(item.get(key), str):
                item[key] = clean(item[key])
        # 검색 결과의 경로 표시(crumbs)에 장 번호 HTML이 그대로 찍히는 문제
        if isinstance(item.get("crumbs"), list):
            item["crumbs"] = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip() for c in item["crumbs"]]
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
