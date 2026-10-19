"""렌더링 뒤처리: 웹북 검색 색인(search-index.json)을 만든다.

렌더링된 각 장의 본문을 절(h2/h3) 단위로 나눠 평문으로 모은다. 코드 셀과 출력은 빼고,
수식은 `\\(Y_1 \\perp T\\)` 대신 `Y_1 ⊥ T`처럼 읽히는 평문으로 바꾼다.
검색 화면(book/site-search.html)이 이 파일을 읽어 띄어쓰기와 상관없이 찾는다.
"""
import html
import json
import os
import re
from html.parser import HTMLParser
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
    tex = re.sub(r"\\(?:hat|bar|tilde|mathbb|mathcal|mathrm|text|operatorname|underbrace|overbrace|left|right|big|Big|frac|dfrac|tfrac|displaystyle|mathbf|boldsymbol)\b", "", tex)
    tex = re.sub(r"\\([A-Za-z]+)", lambda m: SYMBOLS.get(m.group(1), m.group(1)), tex)
    tex = re.sub(r"⊥(\s*⊥)+", "⊥", tex)
    tex = tex.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"\s{2,}", " ", tex).strip()


def clean(text):
    """\\( \\)와 \\[ \\] 안의 수식만 평문으로 바꾼다."""
    return re.sub(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", lambda m: tex_to_plain(m.group(1) or m.group(2) or ""), text, flags=re.S)


SKIP_TAGS = {"script", "style", "svg", "pre", "nav", "button", "noscript", "header"}
SKIP_CLASSES = ("cell", "code-copy-outer-scaffold", "sourceCode", "inline-toc", "hero-actions", "hero-links", "term-link", "screen-reader-only")
TEXT_BREAK = {"p", "li", "td", "th", "dt", "dd", "figcaption", "blockquote", "h4", "h5", "div", "tr"}
VOID = {"br", "img", "hr", "meta", "link", "input", "source", "wbr"}


class PageParser(HTMLParser):
    """main#quarto-document-content 안의 글을 절 단위로 모은다."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.skip = 0
        self.stack = []
        self.heading = None
        self.sections = [{"id": "", "title": "", "text": []}]

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            if tag == "br" and self.in_main and not self.skip:
                self.sections[-1]["text"].append(" ")
            return
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        mark = None
        if tag == "main" and a.get("id") == "quarto-document-content":
            self.in_main = True
            mark = "main"
        elif self.in_main:
            if self.skip or tag in SKIP_TAGS or any(c in cls for c in SKIP_CLASSES):
                self.skip += 1
                mark = "skip"
            elif tag == "section" and a.get("id") and ("level2" in cls or "level3" in cls):
                self.sections.append({"id": a["id"], "title": "", "text": []})
            elif tag in ("h2", "h3"):
                self.heading = []
                mark = "heading"
        self.stack.append((tag, mark))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack:
            t, mark = self.stack.pop()
            if mark == "skip":
                self.skip -= 1
            elif mark == "heading" and self.heading is not None:
                title = " ".join("".join(self.heading).split())
                if not self.sections[-1]["title"]:
                    self.sections[-1]["title"] = title
                self.heading = None
            elif mark == "main":
                self.in_main = False
            if t == tag:
                break
        if self.in_main and not self.skip and tag in TEXT_BREAK:
            self.sections[-1]["text"].append(" ")

    def handle_data(self, data):
        if not self.in_main or self.skip:
            return
        (self.heading if self.heading is not None else self.sections[-1]["text"]).append(data)


def page_title(raw):
    m = re.search(r"<title>(.*?)</title>", raw, re.S)
    title = html.unescape(m.group(1)) if m else ""
    title = re.sub(r"\s+[–|]\s+Python으로 하는 인과추론\s*$", "", title)
    return " ".join(title.replace("\u00a0", " ").split())


def build_index():
    entries = []
    for path in sorted(OUT.glob("*.html")):
        if path.name in ("404.html", "search.html", "landing-page.html"):
            continue
        raw = path.read_text(encoding="utf-8")
        if "quarto-document-content" not in raw:
            continue
        parser = PageParser()
        parser.feed(raw)
        title = page_title(raw)
        for sec in parser.sections:
            text = clean(" ".join("".join(sec["text"]).split()))
            text = re.sub(r"\s+([.,)])", r"\1", text)
            if not text and not sec["title"]:
                continue
            if sec["title"] == "기여하기":
                continue  # 모든 장에 같은 문단이라 검색 결과만 어지럽힌다
            entries.append({
                "u": path.name + (f"#{sec['id']}" if sec["id"] else ""),
                "p": title,
                "s": clean(sec["title"]),
                "t": text,
            })
    (OUT / "search-index.json").write_text(json.dumps(entries, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return len(entries)


def main():
    print(f"search index: {build_index()} sections")
    # Quarto 기본 검색은 쓰지 않으므로 그 색인은 지운다.
    (OUT / "search.json").unlink(missing_ok=True)


if __name__ == "__main__":
    main()
