# bell-ha.github.io

이종하 포트폴리오 — https://bell-ha.github.io

정적 사이트입니다. HTML을 직접 고쳐서 커밋합니다.

## 구성

```
index.html            메인 (About · Skills · Education · Experience · Awards · Projects)
resume.html           이력서. 브라우저에서 열어 [PDF 저장 / 인쇄]
projects/<slug>/      프로젝트 상세 17개
assets/
  css/  js/  data/
  img/common/         프로필 · og 이미지
  img/<slug>/         프로젝트별 이미지
papers/               학사학위 논문 PDF (경로 고정 — 지원서에 인용됨)
```

## 고치는 방법

HTML을 직접 고칩니다. 예전에는 저장소 밖의 원고 폴더(`_portfolio-redesign/`)에서
빌드 스크립트로 HTML을 만들었지만, 그 폴더는 더 이상 쓰지 않습니다(2026-10).

| 무엇을 고칠 때 | 어디를 |
|---|---|
| 메인 (About · Skills · 경력 · 수상 · 프로젝트 카드) | `index.html` |
| 프로젝트 상세 | `projects/<slug>/index.html` |
| 이력서 | `resume.html` |
| 문체 · 조판 규칙 | `projects/STYLE.md` — **고치기 전에 읽을 것** |

프로젝트 제목을 바꾸면 메인 카드, 이력서, 앞뒤 프로젝트 페이지의 하단 링크(pager)도 같이 바꿉니다.

## 이력서

A4로 자동 분할됩니다. 화면에 보이는 그대로 인쇄됩니다.
항목 설명은 한 줄을 넘지 않게 35자 내외로 유지하세요.
