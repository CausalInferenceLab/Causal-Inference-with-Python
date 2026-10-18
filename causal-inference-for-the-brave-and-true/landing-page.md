# Causal Inference for The Brave and True

![img](./data/img/brave-and-true.png)

안녕하세요. [가짜연구소](https://pseudo-lab.com/) 빌더 [신진수](https://www.linkedin.com/in/jinsoo-shin-436060162/)입니다. 가짜연구소 인과추론팀은 한국어 자료가 많지 않은 인과추론을 더 많은 분들이 쉽게 접할 수 있도록 이 책을 옮겼습니다.

## 책 소개

이 책은 Matheus Facure(Nubank 데이터 과학자)의 [Causal Inference for The Brave and True](https://matheusfacure.github.io/python-causality-handbook/landing-page.html)를 한국어로 옮긴 것입니다. 저자는 이 책을 이렇게 소개합니다.

> 가볍지만 엄밀하게 효과 추정과 민감도 분석을 배우는 책입니다. 모든 실습은 파이썬으로 하고, 찾을 수 있는 밈은 최대한 넣었습니다.
>
> Part I에서는 인과추론의 핵심 개념과 모델을 다룹니다. 인과적 질문을 잠재적 결과 표기법으로 나타내는 방법, 인과 그래프, 편향이 무엇이고 어떻게 다루는지를 배웁니다. 여기 담긴 내용은 대부분 학계에서 자리를 잡은 것들로, 책과 대학 강의, 온라인 강좌에서 찾은 자료를 엮은 것입니다. Part I은 인과적 질문을 탐구할 때 기댈 수 있는 튼튼하고 안전한 토대라고 생각하면 됩니다.
>
> Part II에서는 인과추론이 (주로 IT) 산업에서 최근 어떻게 발전하고 쓰이는지를 다룹니다. Part I이 주로 평균 처치효과를 식별하는 데 집중한다면, Part II는 개인화와 CATE 모델을 이용한 이질적 효과 추정으로 넘어갑니다. 이 부분은 대부분 저의 실무 경험에서 나온 것이라 아직 확립된 과학이라고 할 수는 없습니다. 훨씬 실험적이고 앞으로 바뀔 수도 있습니다. 저 역시 아직 배우는 중이니까요.

용어는 같은 저자의 책을 옮긴 『실무로 통하는 인과추론 with 파이썬』(한빛미디어)과 맞췄습니다. 번역 원칙과 용어표는 저장소의 [번역 가이드](https://github.com/CausalInferenceLab/Causal-Inference-with-Python/blob/main/TRANSLATION_GUIDE.md)에 정리해 두었습니다.

가짜연구소 인과추론팀은 전문 번역가가 아니라 데이터 분석가, 데이터 과학자, 연구자로 이루어져 있습니다. 어색하거나 틀린 부분이 보이면 언제든 알려 주세요. 도움이 되었다면 GitHub 스타로 응원해 주시면 큰 힘이 됩니다.

한국어 번역에 흔쾌히 동의해 준 Matheus Facure와, 번역과 실습 자료를 함께 만든 인과추론팀 멤버들에게 감사드립니다.

## 감사의 말 (원저자)

> 이 시리즈 전체를 Joshua Angrist, Alberto Abadie, Christopher Walters의 훌륭한 계량경제학 강의에 바치는 헌사로 생각합니다. Part I의 아이디어는 대부분 이들이 미국경제학회(American Economic Association)에서 한 강의에서 가져왔습니다. 2020년이라는 힘든 해를 버틸 수 있었던 것도 이 강의 덕분이었습니다.

* [Cross-Section Econometrics](https://www.aeaweb.org/conference/cont-ed/2017-webcasts)
* [Mastering Mostly Harmless Econometrics](https://www.aeaweb.org/conference/cont-ed/2020-webcasts)

> Angrist의 책들도 꼭 소개하고 싶습니다. 계량경제학, 그들 말로 'Metrics가 아주 유용할 뿐 아니라 무척 재미있다는 것을 이 책들에서 배웠습니다.

* [Mostly Harmless Econometrics](https://www.mostlyharmlesseconometrics.com/)
* [Mastering 'Metrics](https://www.masteringmetrics.com/)

> 마지막은 Miguel Hernan과 Jamie Robins의 책입니다. 가장 까다로운 인과적 질문에 답해야 했을 때 늘 믿고 기댄 동반자였습니다.

* [Causal Inference Book](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/)

## 기여하기

번역 오류나 어색한 문장은 [이슈 페이지](https://github.com/CausalInferenceLab/Causal-Inference-with-Python/issues)에 남겨 주세요. 관련 질문은 메인테이너 [신진수](https://github.com/jsshin2022)에게 부탁드립니다.

원서는 누구나 무료로 볼 수 있는 오픈소스 자료입니다. 원서가 도움이 되었다면 저자의 [Patreon](https://www.patreon.com/causal_inference_for_the_brave_and_true)을 후원하거나 [원서 저장소에 스타](https://github.com/matheusfacure/python-causality-handbook/stargazers)를 남겨 주세요.
