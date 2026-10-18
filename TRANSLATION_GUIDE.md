# 번역 가이드

이 저장소는 Matheus Facure의 [Causal Inference for The Brave and True](https://github.com/matheusfacure/python-causality-handbook)를 옮긴 것입니다. 용어는 같은 저자의 책을 번역한 『실무로 통하는 인과추론 with 파이썬』(한빛미디어, 2024)을 기준으로 맞췄습니다. 번역을 고치거나 새 장을 옮길 때 아래 원칙을 따라 주세요.

## 1. 원문과 맞추는 방법

- 노트북 구조(셀 순서, 코드 셀, 출력, 이미지)는 원문 저장소의 최신 버전을 그대로 따릅니다. 번역은 마크다운 셀에만 합니다.
- 원문 문장을 빼거나 요약하지 않습니다. 저자의 농담이나 밈 설명도 옮깁니다.
- 원문에 없는 설명이 꼭 필요하면 `> 옮긴이:`로 시작하는 인용문으로 따로 표시합니다. 본문에 섞지 않습니다.
- 수식(`$...$`, `$$...$$`), 이미지 경로, 링크 주소, 인라인 코드(`` `price` ``)는 손대지 않습니다.
- 참고 문헌 목록은 원문 그대로 둡니다.
- 원문 자체에 오류가 있을 때: 오타나 지칭 실수처럼 뜻이 분명한 것은 뜻대로 옮기고 `> 옮긴이:`로 밝힙니다. 논리·수치 오류는 본문을 원문대로 옮기고 옮긴이 주로 짚습니다. 수식은 어떤 경우에도 고치지 않습니다.

## 2. 문체

- 기본은 `-습니다`체입니다. 한 장 안에서 `-해요`체와 섞지 않습니다.
- 원문의 `we`, `you`를 매번 `우리는`, `여러분은`으로 옮기지 않습니다. 주어가 없어도 뜻이 통하면 뺍니다.
- 번역투를 피합니다.
  - `~하는 것이 가능합니다` → `~할 수 있습니다`
  - `~에 의해 ~되어집니다` → 능동으로 바꿉니다.
  - `그것은`, `이것은`을 문장마다 쓰지 않습니다.
  - `~에 대해서`, `~를 통해서`가 한 문장에 두 번 이상 나오면 다시 씁니다.
- 영어 단어를 한글 문장 사이에 그대로 남기지 않습니다(`counterfactual을 추정`, `bias가 생깁니다` 등). 아래 용어표의 한국어를 씁니다.
- 핵심 용어는 장마다 처음 나올 때 `한국어(English)`로 한 번 병기하고, 그 뒤로는 한국어만 씁니다.
- ATE, CATE, DID, OLS 같은 약어는 처음에 `평균 처치효과(ATE)`처럼 풀어 쓰고 이후에는 약어를 써도 됩니다.
- 장 제목(H1)은 원문 영어 제목을 유지하고, 그 아래 절 제목은 한국어로 옮깁니다. `Key Ideas`는 `핵심 요약`, `References`는 `참고 자료`, `Contribute`는 `기여하기`로 통일합니다.
- 브라질 화폐는 `5헤알`처럼 쓰고, 장마다 처음 나올 때만 `5헤알(BRL)`로 병기합니다.
- 인명은 원어 표기를 기본으로 합니다(예: Joshua Angrist). 본문 흐름상 한글 표기가 자연스러우면 『실무로 통하는 인과추론』의 표기(조슈아 앵그리스트, 알베르토 아바디, 주데아 펄)를 따릅니다.

## 3. 용어표

『실무로 통하는 인과추론 with 파이썬』 찾아보기와 본문에서 쓴 번역어입니다. 띄어쓰기도 표기대로 맞춥니다.

### 기본 개념

| 원어 | 번역어 | 비고 |
|---|---|---|
| causal inference | 인과추론 | |
| causality / causation | 인과관계 | |
| association | 연관관계 | correlation은 상관관계 |
| treatment | 처치 | |
| intervention | 개입 | |
| treated, treatment group | 실험군 | `처치군`, `처치 그룹` 쓰지 않음 |
| control group, untreated | 대조군 | `통제군`, `통제 그룹` 쓰지 않음 |
| outcome | 결과 | 변수를 가리킬 때는 결과변수 |
| potential outcome | 잠재적 결과 | |
| counterfactual | 반사실 / 반사실적 결과 | |
| factual outcome | 사실적 결과 | |
| treatment effect | 처치효과 | 붙여 씀 |
| individual treatment effect (ITE) | 개별 처치효과(ITE) | |
| average treatment effect (ATE) | 평균 처치효과(ATE) | |
| average treatment effect on the treated (ATT) | 실험군에 대한 평균 처치효과(ATT) | |
| conditional average treatment effect (CATE) | 조건부 평균 처치효과(CATE) | |
| heterogeneous treatment effect | 이질적 처치효과 | |
| treatment assignment | 처치 배정 | |
| randomized controlled trial (RCT) | 무작위 통제 실험(RCT) | |
| randomized experiment | 무작위 실험 | |
| randomization | 랜덤화 / 무작위 배정 | |
| observational data | 관측 데이터 | |
| unit | 분석단위 / 대상 | 문맥에 맞게 |
| covariate | 공변량 | |
| identification | 식별 | |
| estimand / causal quantity | 인과 추정량 | |
| estimator | 추정량 | |
| parameter | 매개변수 | `모수`, `파라미터` 쓰지 않음. nuisance parameter는 장애모수, parametric은 모수적 |
| estimate (명사) | 추정값 | `추정치` 쓰지 않음 |
| SUTVA | SUTVA | |
| spillover | 파급 효과 | |

### 편향과 그래프

| 원어 | 번역어 | 비고 |
|---|---|---|
| bias | 편향 | |
| selection bias | 선택편향 | |
| confounding | 교란 | |
| confounder | 교란 요인 | `교란변수` 쓰지 않음 |
| confounding bias | 교란편향 | |
| collider | 충돌부 | |
| collider bias | 충돌부 편향 | |
| mediator | 매개자 | |
| omitted variable bias (OVB) | 누락 변수 편향(OVB) | |
| upward / downward bias | 상향 편향 / 하향 편향 | |
| graphical (causal) model | 그래프 (인과) 모델 | |
| directed acyclic graph (DAG) | 유향 비순환 그래프(DAG) | |
| node / edge | 노드 / 엣지 | |
| chain / fork | 사슬 / 분기 | |
| parent / child / descendant | 부모 / 자식 / 자손 | |
| backdoor path / adjustment | 뒷문 경로 / 뒷문 보정 | |
| front door | 앞문 | |
| d-separation | d-분리 | |
| conditional independence assumption (CIA) | 조건부 독립성 가정(CIA) | |
| independence assumption | 독립성 가정 | |
| unconfoundedness | 비교란성 | |
| ignorability | 무시가능성 | |
| exchangeability | 교환 가능성 | |
| positivity | 양수성 | |
| overlap / common support | 중첩 / 공통 지지 | |
| extrapolation / interpolation | 외삽 / 내삽 | |
| sensitivity analysis | 민감도 분석 | |

### 통계와 회귀분석

| 원어 | 번역어 | 비고 |
|---|---|---|
| regression | 회귀분석 / 회귀 | `회귀 분석` 쓰지 않음 |
| linear regression | 선형회귀 | |
| ordinary least squares (OLS) | 최소제곱법(OLS) | |
| regressor | 설명변수 | |
| intercept | 절편 | |
| residual | 잔차 | |
| dummy variable | 더미변수 | |
| interaction | 상호작용 | |
| saturated model | 포화모델 | |
| Frisch-Waugh-Lovell theorem (FWL) | 프리슈-워-로벨 정리(FWL) | |
| orthogonalization | 직교화 | |
| de-meaning | 평균 제거 | |
| standard error | 표준오차 | 붙여 씀 |
| consistency | 일치성 | |
| partialling out | 부분 제거 | |
| standard deviation | 표준편차 | |
| confidence interval | 신뢰구간 | 붙여 씀 |
| hypothesis test | 가설검정 | |
| null hypothesis | 귀무가설 | |
| test statistic | 검정통계량 | |
| p-value | p 값 | |
| significance level | 유의수준 | |
| statistically significant | 통계적으로 유의 | |
| central limit theorem (CLT) | 중심극한정리(CLT) | |
| normal distribution | 정규분포 | |
| sample size | 표본 크기 | |
| power | 검정력 | |
| bootstrap / block bootstrap | 부트스트랩 / 블록 부트스트랩 | |
| heteroskedasticity | 이분산성 | |
| mean squared error (MSE) | 평균제곱오차(MSE) | |

### 식별 전략

| 원어 | 번역어 | 비고 |
|---|---|---|
| instrumental variable (IV) | 도구변수 | 붙여 씀 |
| first stage / second stage | 1단계 / 2단계 | |
| reduced form | 축약형 | |
| two-stage least squares (2SLS) | 2단계 최소제곱법(2SLS) | |
| exclusion restriction | 배제 제약 | |
| relevance | 연관성 | |
| monotonicity | 단조성 | |
| non-compliance | 불응 | |
| compliers | 순응자 | |
| always-takers | 항시 참여자 | |
| never-takers | 항시 불참자 | |
| defiers | 반항자 | |
| local average treatment effect (LATE) | 국지적 평균 처치효과(LATE) | |
| intention-to-treat effect (ITT) | 처치 의도 효과(ITTE) | |
| matching / matching estimator | 매칭 / 매칭 추정량 | |
| propensity score | 성향점수 | 붙여 씀 |
| propensity weighting | 성향점수 가중치 | |
| inverse probability weighting (IPW) | 역확률 가중치(IPW) | |
| doubly robust estimation | 이중 강건 추정 | |
| doubly robust | 이중 강건 | |
| difference-in-differences (DID) | 이중차분법(DID) | `DiD` 대신 `DID` |
| parallel trends | 평행 추세 | |
| no anticipation | 비기대 가정 | |
| panel data | 패널데이터 | |
| cross-sectional data | 횡단면 데이터 | |
| fixed effects | 고정효과 | 붙여 씀 |
| two-way fixed effects (TWFE) | 이원고정효과(TWFE) | |
| staggered adoption | 시차 도입 (설계) | |
| strict exogeneity | 강외생성 | |
| synthetic control (method) | 통제집단합성법 | 방법론 |
| synthetic control (unit) | 가상의 대조군 | 합성된 대조 단위 |
| synthetic difference-in-differences (SDID) | 합성 이중차분법(SDID) | |
| conformal inference | 컨포멀 추론 | |
| regression discontinuity design (RDD) | 회귀 불연속 설계(RDD) | |
| running variable | 배정변수 | `실행 변수` 쓰지 않음 |
| threshold, cutoff | 임곗값 | `임계값` 쓰지 않음 |
| placebo test | 위약 검정 | |
| sharp / fuzzy RD | 계단형 RD / 경사형 RD | |
| subclassification estimator | 층화 추정량 | |
| event study | 이벤트 스터디 | |

### 머신러닝과 CATE

| 원어 | 번역어 | 비고 |
|---|---|---|
| feature / feature engineering | 특성 / 특성 엔지니어링 | |
| overfitting | 과적합 | |
| cross-validation | 교차 검증 | |
| cross prediction / cross-fitting | 교차 예측 | |
| out of fold (OOF) | 아웃 오브 폴드(OOF) | |
| hold-out | 홀드아웃 | |
| regularization (bias) | 정규화 (편향) | |
| nuisance parameter | 장애모수 | |
| meta-learner | 메타러너 | |
| S-learner / T-learner / X-learner | S 러너 / T 러너 / X 러너 | |
| R-loss / R-learner | R 손실 / R 러너 | |
| double / debiased machine learning (DML) | 이중 머신러닝 / 편향 제거 머신러닝 | |
| debiasing | 편향 제거 | |
| target transformation | 목표 변환 | |
| cumulative gain curve | 누적 이득 곡선 | |
| cumulative effect curve | 누적 효과 곡선 | |
| cumulative sensitivity curve | 누적 민감도 곡선 | |
| treatment sensitivity | 처치 민감도 | 원문 개정으로 elasticity를 대부분 sensitivity로 바꿈 |
| elasticity | 탄력성 | 원문이 elasticity로 남긴 곳만 |
| uplift modeling | 업리프트 모델링 | |
| personalization | 개인화 | |
| calibrated probability | 보정된 확률 | |
| importance sampling | 중요도 샘플링 | |
| curse of dimensionality | 차원의 저주 | |
| nudge | 넛지 | |
| latent outcome | 잠재 결과 | potential outcome(잠재적 결과)과 구분 |
| noise | 잡음 | `노이즈` 쓰지 않음 |
| ground truth | 참값 | |
| training / test set | 훈련 셋 / 테스트 셋 | |
| band (예측값 구간) | 구간 | 신뢰구간과 헷갈리지 않게 문맥 표현 |
| conversion | 전환 | |

## 4. 작업 순서

1. 원문 저장소의 해당 노트북을 내려받아 코드 셀과 출력은 그대로 둡니다.
2. 마크다운 셀을 위 원칙대로 옮깁니다.
3. 수식, 이미지, 링크 개수가 원문과 같은지 확인합니다.
4. Jupyter Book으로 빌드해 렌더링을 확인합니다.
5. PR에는 원문 커밋과 바뀐 셀을 적어 주세요.
