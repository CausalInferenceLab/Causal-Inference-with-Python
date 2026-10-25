# 기여 안내

번역을 고치거나 웹북을 손보려는 분을 위한 안내입니다. 읽기만 하신다면 [웹북](https://causalinferencelab.github.io/Causal-Inference-with-Python/)으로 가시면 됩니다.

## 번역 고치기

1. [번역 가이드](TRANSLATION_GUIDE.md)의 원칙과 용어표를 먼저 읽습니다.
2. 원고는 `causal-inference-for-the-brave-and-true/` 폴더의 노트북입니다. 마크다운 셀만 고치고, 코드 셀·출력·수식·링크 주소는 그대로 둡니다.
3. PR을 올리면 GitHub Actions가 웹북을 빌드해 확인합니다. 메인테이너 검토 뒤 머지되면 웹북에 반영됩니다.

용어를 바꾸거나 더하고 싶다면 [용어 제안 이슈](https://github.com/CausalInferenceLab/Causal-Inference-with-Python/issues/new?template=term-proposal.yml)로 먼저 의견을 나눠 주세요.

## 웹북 빌드와 미리 보기

웹북은 [Quarto](https://quarto.org/) Book으로 만듭니다. `main`에 머지되면 GitHub Actions(`.github/workflows/book.yml`)가 빌드해 GitHub Pages에 배포합니다. PR에서는 빌드만 확인하며, 결과물은 Actions의 `book-preview` 아티팩트로 내려받아 볼 수 있습니다.

로컬에서 미리 보려면 Quarto를 설치한 뒤 다음을 실행하세요. 노트북은 다시 실행하지 않고 저장된 출력을 그대로 씁니다.

```bash
pip install jupyter
python book/prepare.py
cd book && quarto preview
```

`book/prepare.py`는 빌드할 때 [번역 가이드](TRANSLATION_GUIDE.md)의 용어표로 웹북의 '용어집' 페이지를 만들고, `book/postrender.py`는 렌더링이 끝난 뒤 웹북 검색 색인(`search-index.json`)을 만듭니다. `book/prepare.py`는 빌드할 때만 장 제목, 수식 표기, 접힌 코드, 옮긴이 주 상자를 책 형식으로 바꿉니다. 그래서 노트북은 원서와 같은 구조로 두면 됩니다.

읽기 기능(읽은 장 기록, 이어 읽기, 장 끝 평가, 허브로 가는 링크)은 `book/reader.html`, GA4 설정은 `book/analytics.html`에 있습니다. 읽은 장 기록은 독자의 브라우저(`localStorage`의 `cil-book-*`)에만 남고, 같은 도메인의 [Causal Inference Hub](https://causalinferencelab.github.io/)가 이 기록으로 진도와 활동 여권 스탬프를 보여 줍니다.

## 원서 변경 반영 (메인테이너)

원서가 바뀌면 GitHub Actions(`Upstream watch`)가 매월 1일 확인해 바뀐 장과 본문 변경을 정리한 이슈를 메인테이너에게 배정합니다. 번역을 고친 PR이 메인테이너 검토를 거쳐 머지되면 웹북에 반영되고 이슈는 자동으로 닫힙니다. 자세한 절차는 [번역 가이드](TRANSLATION_GUIDE.md#5-원서-변경-반영)에 있습니다.
