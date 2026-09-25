# bell-ha.github.io

이종하 포트폴리오 — https://bell-ha.github.io

정적 사이트입니다. 빌드 스크립트가 원고에서 HTML을 만들어 이 저장소에 써 넣고,
결과물을 그대로 커밋합니다. **빌드 없이 HTML을 직접 고쳐도 됩니다.**

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

원고와 빌더는 **이 저장소 밖**에 있습니다 — `../_portfolio-redesign/`.

```bash
cd ../_portfolio-redesign
python3 build.py            # 전체
python3 build.py nav-robot  # 한 페이지만
```

| 무엇을 고칠 때 | 어디를 |
|---|---|
| 프로젝트 본문 | `_portfolio-redesign/content/<slug>.md` |
| 제목 · 기간 · Impact · 도판 지정 | `_portfolio-redesign/overrides.yaml` |
| 프로필 · Skills · 경력 · 수상 | `_portfolio-redesign/site.yaml` |
| 문체 · 조판 규칙 | `_portfolio-redesign/STYLE.md` — **고치기 전에 읽을 것** |
| 이력서 | `resume.html` 직접 (빌더를 타지 않습니다) |

`index.html`·`projects/*/index.html`·`sitemap.xml`·`robots.txt`는 생성물입니다.
직접 고쳐도 되지만 다음 빌드에서 덮어써집니다.

## 이력서

A4로 자동 분할됩니다. 화면에 보이는 그대로 인쇄됩니다.
항목 설명은 한 줄을 넘지 않게 35자 내외로 유지하세요.
