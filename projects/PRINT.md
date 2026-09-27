# A4 인쇄 · PDF 저장 — 조판 기준표

이 사이트를 `Cmd+P` 로 뽑을 때 쓰는 근거다. 값은 전부 이 저장소에서
계산으로 확정했거나 명세에서 유도한 것이고, 추측은 넣지 않았다.
`assets/css/print.css` 를 고치기 전에 여기부터 읽는다.

원문은 인쇄 조판을 검증하며 만든 기준표다(2026-09-27). 아래 본문은 그대로다.

---

이 표는 **49의 수정 내용을 보기 전에 명세·저장소 사실에서 먼저 유도**했다. 수정본을 역으로 설명하는
문서가 아니다. (49의 1차 수정이 들어온 시각: `print.css` mtime **2026-09-27 15:32:14**, 7,589 bytes.
검증 전 원본은 2026-09-26 01:47:09, 5,914 bytes.)

**검증 환경 실측**
- Google Chrome **154.0.8037.57**
- poppler `pdftoppm` **26.09.0**
- 대상: `projects/nav-robot/index.html` (16,635 bytes)

---

## 0. 먼저 — 이 저장소에서 계산으로 확정된 값

### 0-1. A4 본문 상자

`@page { size: A4; margin: 16mm 14mm }` 기준 (현행 print.css):

| 값 | mm | CSS px (96dpi) |
|---|---|---|
| 용지 | 210 × 297 | 793.7 × 1122.5 |
| 좌우 여백 | 14 × 2 = 28 | 105.8 |
| 상하 여백 | 16 × 2 = 32 | 120.9 |
| **본문 폭** | **182mm** | **687.9px** |
| **본문 높이** | **265mm** | **1001.6px** |

계산: `182 ÷ 25.4 × 96 = 687.87`

### 0-2. ⚠️ 가장 중요한 귀결 — 인쇄 폭 687.9px 에서 **화면용 미디어쿼리가 켜진다**

인쇄에서 `min-width` 미디어쿼리는 **페이지 본문 상자 폭**으로 평가된다. 이 저장소의
브레이크포인트를 실측해 대조한 결과:

| 브레이크포인트 | 파일 | 인쇄(687.9px)에서 |
|---|---|---|
| `min-width: 560px` | detail.css | **ON** |
| `min-width: 640px` | detail.css | **ON** ← `.contrib-side` 2단 그리드 + **`img { position: absolute }`** |
| `min-width: 680px` | components.css | **ON** |
| `min-width: 720px` | components.css | off |
| `min-width: 920px` | components.css | off |

**→ `.contrib-side .figure img { position: absolute; inset: 0; block-size: 100% }` (detail.css:331-342)
가 인쇄에서도 살아 있다.** 이게 이 페이지 인쇄의 핵심 위험원이다. 아래 3-2 참조.

> 687.9px는 640과 720 **사이**다. 여백을 조금만 바꿔도 브레이크포인트를 넘나든다.
> `@page margin` 좌우를 **11.5mm 이하**로 줄이면 폭이 720px를 넘어 `min-width:720px` 규칙까지 켜진다
> (187 ÷ 25.4 × 96 = 706.8 → 여전히 off; 720px를 넘기려면 좌우 ≤ 9.7mm).
> **여백을 건드리는 수정은 반드시 이 표를 다시 계산해야 한다.**

### 0-3. 이 저장소에 **없는** 것 — 확인함

b5가 조사 항목으로 준 **화면용 breakout(`margin-inline-start:50%` + `translateX(-50%)`)
패턴은 이 저장소에 존재하지 않는다.** 빌드 결과(`bell-ha.github.io/assets/css/*.css`)와
소스(`_portfolio-redesign/`) 양쪽을 `margin-inline-start:50%` / `margin-left:50%` /
`translateX(-50%)` / `100vw` 로 전수 검색해 **0건**이다.

→ 이 항목은 **일반 위험으로만 기록**한다(7절). 없는 문제를 고치는 수정이 들어오면 그게 오히려 회귀다.

---

## 1. `break-inside` / `break-before` / `break-after`

### 1-1. 적용 대상 — 명세

> **"Applies to: block-level elements"**
> — MDN, https://developer.mozilla.org/en-US/docs/Web/CSS/break-inside

> "If there is no generated box, the property is ignored."
> — 같은 문서

즉 `display: none`, `display: contents` 인 요소에는 듣지 않는다.

### 1-2. ⚠️ **avoid 는 "지킬 수 있으면 지킨다"는 뜻이다 — 보장이 아니다**

이게 인쇄 조판에서 가장 많이 틀리는 지점이다. 명세 원문:

> "If that still does not lead to sufficient break points, then rules 1, 2 and 4 are **dropped**
> in order to find additional breakpoints. In this case the UA may use the avoids that are in
> effect at those points to weigh the appropriateness of the new breakpoints; however, this
> specification does not suggest a precise algorithm."
> — CSS Fragmentation Level 3, https://drafts.csswg.org/css-break/

**→ 요소가 한 쪽보다 크면 `break-inside: avoid` 는 무시되고 그냥 잘린다.**
"avoid 를 걸었으니 안 잘린다"는 판정 근거가 될 수 없다. **PDF 를 눈으로 봐야 한다.**

**검증 기준 A**: 한 쪽(265mm)보다 큰 요소에 `avoid` 가 걸려 있으면, 그건 효과가 없는 선언이다.
잘림 여부는 렌더로만 판정한다. 큰 요소는 avoid 가 아니라 **크기 상한**으로 해결해야 한다.

### 1-3. 강제 break 가 avoid 를 이긴다

> "If any of the three concerned values is a forced break value (`always`, `left`, `right`,
> `page`, `column`, or `region`), it has precedence. … the `break-before` value has precedence
> over the `break-after` value, which in turn has precedence over the `break-inside` value."
> — MDN, 위 문서

**검증 기준 B**: 같은 경계에 `break-before: page` 와 `break-inside: avoid` 가 만나면 page 가 이긴다.
`break-after: avoid`(제목 뒤 안 끊기)는 다음 형제의 `break-before` 와 충돌하지 않는지 본다.

### 1-4. grid · flex 자식 — **옛 조언은 이제 틀렸다**

Chrome 은 LayoutNG 로 fragmentation 을 다시 구현했고 버전별 도입 시점이 명확하다:

> "core fragmentation in Chrome 102, flex/grid in Chrome 103, tables in Chrome 106,
> and **printing in Chrome 108**."
> — Chrome for Developers, https://developer.chrome.com/docs/chromium/renderingng-fragmentation

**검증 환경 Chrome 이 154 이므로 flex·grid·표 fragmentation 이 전부 정상 동작한다.**
"grid/flex 자식에는 break-inside 가 안 듣는다"는 인터넷 조언은 **Chrome 103 이전 이야기**다.

**검증 기준 C**: `.contrib-side`(grid), `.impact-grid`(grid), `.figure--pair`(grid) 의 자식에 건
`break-inside: avoid` 는 이 Chrome 에서 **들어야 정상**이다. 안 들으면 1-2(크기 초과)를 의심한다.

### 1-5. ⚠️ 컨테이너와 자식 중 어디에 걸 것인가

한 줄짜리 그리드(`.impact-grid` 4칸)는 **칸마다 avoid 를 걸어도 줄 자체가 쪽 경계에서 갈린다.**
칸 하나하나는 안 잘리지만 1·2번 칸이 앞 쪽, 3·4번 칸이 뒤 쪽에 놓인다.
**줄 전체를 한 쪽에 두려면 컨테이너에 걸어야 한다.**

**검증 기준 D**: 수치 카드 4칸이 **같은 쪽에** 있는지 본다. 칸이 안 잘렸다는 것만으로 통과시키지 않는다.

---

## 2. `orphans` / `widows`

> "Applies to: **block containers**" / "Initial value: **2**"
> **Firefox**: 지원하지 않음(`orphans: 1` 처럼 동작) / **Chrome**: 지원
> — MDN, https://developer.mozilla.org/en-US/docs/Web/CSS/orphans

- `orphans` = 쪽 **아래**에 남겨야 하는 최소 줄 수
- `widows` = 쪽 **위**로 넘어갈 때 최소 줄 수

**검증 기준 E**: Chrome 초기값이 이미 2 이므로 `orphans: 2; widows: 2` 를 명시해도 **렌더는 안 바뀐다.**
이건 "동작이 바뀌는 수정"이 아니라 "의도를 기록하는 수정"이다.
→ 이 선언이 추가됐다고 해서 낱줄이 사라졌다고 보고하면 **인과를 잘못 말하는 것**이다.
값을 3 이상으로 올린 게 아니면 효과 없음으로 판정한다.

**검증 기준 F**: `orphans`/`widows` 는 **block container** 에만 듣는다.
`display: grid`/`flex` 인 요소에 걸면 그 요소의 직계 줄에는 의미가 없다.

---

## 3. `position: absolute` 와 인쇄

### 3-1. 명세 — 절대 배치도 조각난다

> "Absolute positioning affects layout and thus interacts with fragmentation. Both the coordinate
> system and absolutely-positioned boxes belonging to a containing block will fragment across
> fragmentainers in the same fragmentation flow as the containing block."
> "**UAs are not required to correctly position boxes that span a fragmentation break** and whose
> block-start edge position depends on where the box's content fragments."
> — CSS Fragmentation Level 3, https://drafts.csswg.org/css-break/

Chrome 구현 쪽 설명:

> "It can be even more complicated when there's an out-of-flow positioned element inside
> fragmentation, because then the **out-of-flow fragments become direct children of the
> fragmentainer** (and not a child of what CSS thinks is the containing block)."
> — https://developer.chrome.com/docs/chromium/renderingng-fragmentation

### 3-2. ⚠️ 이 저장소의 실제 위험 — `.contrib-side .figure img`

`detail.css:331-342`, `@media (min-width: 640px)` 안:

```css
.contrib-side .figure { position: relative; }
.contrib-side .figure img {
  position: absolute; inset: 0;
  inline-size: 100%; block-size: 100%;
  max-inline-size: none; max-block-size: none;   /* ← 상한을 명시적으로 푼다 */
  object-fit: contain;
}
```

0-2 에서 보았듯 **이 블록은 인쇄(687.9px)에서 켜진다.** 결과적으로:

1. **이미지가 행 높이를 만들지 않는다.** 높이는 옆 글이 정한다 — 화면에서는 의도된 동작이지만,
   인쇄에서는 글이 짧으면 사진이 그 높이로 납작해진다.
2. **`max-block-size: none` 이 print.css 의 `.figure img { max-block-size: 150mm }` 를 무력화한다.**
   선택자 특정성이 `.contrib-side .figure img`(0,2,1) > `.figure img`(0,1,1) 이라 **detail.css 가 이긴다.**
   → print.css 에서 `.figure img` 에만 상한을 걸면 `.contrib-side` 안의 사진에는 **안 듣는다.**
3. 쪽 경계를 넘는 absolute 박스의 위치는 **명세상 UA 보장 대상이 아니다**(위 인용).

**검증 기준 G (최우선)**: `.contrib-side` 절의 사진이 PDF 에서
(a) 찌그러지지 않았는지(가로세로비 유지), (b) 쪽 경계에서 어긋나거나 사라지지 않았는지,
(c) 글과 같은 쪽에 있는지 — **세 가지를 눈으로 본다.**
`nav-robot` 페이지에 `.contrib-side` 가 **6개**(`contrib-side--wide` 5개 포함) 있으므로 전부 확인.

**검증 기준 H**: 이 문제를 `position: static` 으로 되돌려 푸는 수정이라면,
되돌린 뒤 **높이 상한이 실제로 먹는지**를 본다(특정성 때문에 같은 급 선택자로 덮어야 한다).

---

## 4. 대체 요소 — `img` · `iframe` · `video` (monolithic)

### 4-1. 명세 — 쪼갤 수 없는 내용

> "Some content is not fragmentable, for example many types of **replaced elements (such as images
> or video)**, scrollable elements, or a single line of text content. Such content is considered
> **monolithic**: it contains no possible break points."
> — CSS Fragmentation Level 3, https://drafts.csswg.org/css-break/

한 쪽보다 클 때:

> "the UA may fragment such boxes or it may treat them as monolithic … the UA may break anywhere
> in order to avoid losing content off the edge of the fragmentainer. In such cases, the UA may
> also fragment the contents of monolithic elements by **slicing the element's graphical representation**."
> — 같은 문서

Chrome 의 실제 선택:

> "Content is monolithic if it is not eligible for breaking into multiple fragments. …
> **Rather than letting it overflow** the first column (as it does with LayoutNG block fragmentation)"
> — https://developer.chrome.com/docs/chromium/renderingng-fragmentation

**검증 기준 I**: 한 쪽보다 큰 이미지는 `break-inside: avoid` 로 못 막는다(1-2). **`max-block-size` 로
쪽 안에 들어가게 만드는 것이 유일한 해법이다.** 본문 높이가 265mm 이므로, 제목·여백을 감안하면
도판 상한은 그보다 작아야 한다.

### 4-2. ⚠️ `iframe` — nav-robot 에 2개 있다

`.video-embed iframe` 은 `position: absolute; inset: 0` 이고 부모가 `aspect-ratio: 16/9` +
`overflow: hidden` + `background: #000` 이다 (components.css:726-741).

인쇄 시 실제 동작:
- **YouTube 임베드(교차 출처)는 인쇄에서 영상 프레임이 나오지 않는다.** 재생 화면이 아니라
  보통 **검은 상자**로 찍힌다 — 부모 `background: #000` 때문에 비어 있어도 검게 나온다.
- `overflow: hidden` 인 스크롤 컨테이너는 명세상 **monolithic** 이다(4-1 인용).
- 헤드리스 인쇄에서는 외부 프레임 로드가 완료되지 않을 수 있다 (`--virtual-time-budget` 으로 대기).

**검증 기준 J**: 영상 자리가 **검은 직사각형 2개**로 찍히는지 확인한다. 검은 상자가 나왔다면
그건 "깨진 것"이 아니라 예상된 동작이지만, **A4 에서 16:9 검은 상자 2개는 지면 낭비**다.
잉크 관점에서도 나쁘다(182mm × 102mm 검정 면적).
→ 인쇄에서 `.figure--video` 를 숨기고 링크 주소만 남기는 편이 문서로서 낫다. **(제안이지 결격은 아님)**

**검증 기준 K**: `<video>` 1개(`coex-demo.mp4`, `autoplay loop muted`)는 인쇄에서
**포스터 프레임 또는 빈 상자**로 나온다. `preload="metadata"` 라 첫 프레임조차 없을 수 있다.
`.figure--pair` 안에서 `object-fit: cover` + `aspect-ratio: 4/3` 이므로, 옆 사진과 높이는 맞되
**내용이 비면 빈 칸**이 된다. 이 경우 사진 1장 + 빈 칸 1개가 나란히 찍힌다.

### 4-3. ⚠️ 헤드리스 인쇄에서 `loading="lazy"`

`nav-robot` 에 `loading="lazy"` 가 **10개** 있다. 헤드리스로 스크롤 없이 인쇄하면
뷰포트 밖 이미지가 로드되지 않아 **빈 칸으로 찍힐 수 있다.**

**검증 기준 L**: 이미지가 비어 있을 때 **원인을 print.css 로 돌리기 전에 lazy 로딩을 의심한다.**
판별법: `--virtual-time-budget` 을 크게 늘려 다시 뽑아 같은 칸이 채워지면 로딩 문제,
그대로 비면 CSS 문제다. **이 구분을 안 하고 보고하면 49 에게 없는 버그를 떠넘기게 된다.**

---

## 5. `@page` 여백과 본문 폭

- `@page { margin }` 은 **용지 가장자리에서 본문 상자까지**다. `body` 의 `margin`/`padding` 은 그 **안쪽**에 더해진다.
- print.css 는 `.container { margin: 0; padding: 0 }` 로 화면 폭 제한을 푼다 → 본문이 182mm 를 다 쓴다.
- `@page` 안에서는 **`vw`/`vh` 를 쓰지 않는다.** 인쇄 시 뷰포트 단위는 페이지 상자 기준으로 해석되지만
  값이 직관과 어긋난다. mm/pt 로 쓴다.

**검증 기준 M**: 본문이 좌우 여백(14mm)을 침범하지 않는지, 오른쪽에서 글자가 잘리지 않는지 본다.
`word-break: break-all` 이 걸린 링크 주소(`.detail-links a::after`)가 특히 여백을 넘기 쉽다.

**검증 기준 N**: 0-2 에 따라 **여백이 바뀌면 미디어쿼리 매칭이 바뀐다.** `@page margin` 이 수정됐다면
0-1 표를 다시 계산하고, 켜지는 브레이크포인트가 달라졌는지 확인한다.

---

## 6. 색 · 배경

- Chrome 은 기본적으로 배경을 인쇄하지 않는다. 배경이 필요하면 `print-color-adjust: exact`
  (구 `-webkit-print-color-adjust`) 가 필요하다.
- print.css 는 반대 전략을 쓴다 — **토큰을 흰 바닥/검은 글자로 덮어** 배경 자체를 없앤다. 잉크 관점에서 옳다.
- `.figure img { filter: none !important }` 는 **다크모드로 보다 인쇄할 때 음화가 찍히는 것**을 막는다.
  `!important` 가 필요한 이유는 화면 CSS 의 `--invert` 필터를 이겨야 하기 때문이다.

**검증 기준 O**: 다크모드 상태에서 뽑아도 흰 바닥·검은 글자인지, 도판이 음화가 아닌지 본다.
(헤드리스는 기본 light 이므로 이 항목은 **이번 렌더로는 검증되지 않는다** — 별도 확인 필요.
`--force-dark-mode` 또는 `data-theme="dark"` 를 주입해야 한다.)

---

## 7. 일반 함정 — 이 저장소에는 없지만 기록

**화면용 breakout**(`margin-inline-start: 50%; transform: translateX(-50%); width: 100vw`)은
인쇄에서 다음을 일으킨다:
- `100vw` 가 페이지 상자 기준으로 해석돼 **본문보다 넓어지고 여백을 침범**한다.
- `transform` 이 걸린 요소는 **자체 포함 블록**을 만들어 fragmentation 동작이 달라진다.
- 인쇄에서는 `transform` 이 적용된 채로 잘리면 **내용이 종이 밖으로 나간다**(복구 불가).

**0-3 에서 확인했듯 이 저장소에는 해당 패턴이 없다.** print.css 에 이걸 되돌리는 규칙이
새로 들어왔다면 **불필요한 수정**이므로 지적 대상이다.

---

## 8. 판정 체크리스트 (PDF 를 눈으로 보며 채운다)

| # | 기준 | 근거 |
|---|---|---|
| A | 한 쪽보다 큰 요소의 `avoid` 는 무효 — 잘림은 렌더로만 판정 | 1-2 |
| B | 강제 break 가 avoid 를 이김 | 1-3 |
| C | grid/flex 자식 avoid 는 Chrome 154 에서 **들어야** 정상 | 1-4 |
| D | `.impact-grid` 4칸이 **같은 쪽**에 | 1-5 |
| E | `orphans/widows: 2` 는 Chrome 기본값 — 렌더 변화 없음. 효과 주장 금지 | 2 |
| F | `orphans/widows` 는 block container 에만 | 2 |
| **G** | **`.contrib-side` 사진 6곳: 비율·쪽경계·글과 동일 쪽** | **3-2** |
| H | static 으로 되돌렸다면 높이 상한이 **실제로** 먹는지(특정성) | 3-2 |
| I | 큰 도판은 `max-block-size` 로만 해결 가능 | 4-1 |
| J | iframe 2개 = 검은 상자 예상. 지면 낭비 여부 | 4-2 |
| K | video 1개 = 빈 칸 가능 | 4-2 |
| **L** | **빈 이미지는 lazy 로딩부터 의심** — budget 늘려 재현 | **4-3** |
| M | 본문이 14mm 여백 침범 안 함 (특히 링크 주소) | 5 |
| N | `@page margin` 이 바뀌었으면 0-1 재계산 | 5 |
| O | 다크모드 인쇄는 **이번 렌더로 검증 안 됨** | 6 |
| P | breakout 관련 규칙이 새로 들어왔으면 불필요한 수정 | 7 |

### 검증 절차에 대한 자기 규율
- **49 의 보고를 읽고 그에 맞춰 보지 않는다.** PDF 를 먼저 보고 소견을 적은 뒤 대조한다.
- **PNG 는 전 장을 연다.** 표본만 보고 "됐다"고 하지 않는다.
- **내가 재지 않은 것을 결과에 명시한다**(예: 기준 O 다크모드).
- 판정 시각과 `print.css` mtime 을 결과에 적는다 — 검증 중 파일이 바뀔 수 있다.

---

## 출처

- MDN `break-inside` — https://developer.mozilla.org/en-US/docs/Web/CSS/break-inside
- MDN `orphans` — https://developer.mozilla.org/en-US/docs/Web/CSS/orphans
- CSS Fragmentation Module Level 3 (W3C 편집안) — https://drafts.csswg.org/css-break/
- Chrome RenderingNG: LayoutNG block fragmentation — https://developer.chrome.com/docs/chromium/renderingng-fragmentation

**(추측) 표시 항목**
- 4-2 의 "YouTube 교차출처 iframe 이 검은 상자로 찍힌다" 는 `background: #000` + 교차출처 제약에서
  유도한 **예측**이다. 명세 인용이 아니므로 **PDF 로 확인해야 확정된다.**
- 0-2 의 "인쇄 미디어쿼리는 페이지 본문 상자 폭으로 평가된다" 는 계산과 통상 구현에 근거한
  **예측**이다. PDF 에서 `.contrib-side` 가 2단으로 찍히면 확정, 1단이면 예측이 틀린 것이다.
  **이 한 가지가 3-2 위험 전체의 전제이므로 렌더에서 가장 먼저 확인한다.**

---

# 9. 계산으로 미리 확정한 값 (렌더 전 예측)

추가: 2026-09-27, github-3c. b5 의 "90mm 가 죽은 규칙일 수 있다" 지적을 계산으로 확인한 결과와,
다크모드 항목을 준비하다 **정적 분석만으로 잡힌 결함 1건**.

## 9-0. ⚠️ 먼저 — 인쇄에서 `1rem` 이 달라진다

`print.css:49` 가 `html { font-size: 10.5pt }` 를 준다. `rem` 은 루트 글자 크기 기준이므로
**인쇄에서 `1rem = 10.5pt = 14px = 3.70mm`** 다 (화면 16px 이 아니다).
→ `--sp-5: 1.25rem` 은 화면 20px 이지만 **인쇄에서는 17.5px = 4.63mm**.
간격 토큰을 쓰는 모든 계산은 이 값으로 해야 한다.

## 9-1. `.contrib-side` 실제 칸 폭

```
본문 182.0mm − .contrib{padding-inline-start:--sp-5} 4.63mm = 그리드 폭 177.37mm
gap = --sp-5 = 4.63mm
기본(32%)  →  글칸 116.0mm / 사진칸 56.8mm
--wide(42%) →  글칸  98.2mm / 사진칸 74.5mm
```

## 9-2. **`max-block-size: 90mm` 은 2단에서 한 번도 걸리지 않는다** — b5 지적 확인

`block-size:auto` + `inline-size:100%` 이므로 높이 = 칸폭 × (원본 h/w).

| 이미지 | 원본 | h/w | 2단 높이 | 90mm |
|---|---|---|---|---|
| robot-handle.png | 522×484 | 0.927 | 칸 56.8 → **52.6mm** | 안 걸림 |
| elevator-align.jpg | 1100×612 | 0.556 | 칸 74.5 → **41.4mm** | 안 걸림 |
| people-fov-diagram.png | 1168×600 | 0.514 | 칸 74.5 → **38.3mm** | 안 걸림 |
| gpt-gate-diagram.svg | 640×330 | 0.516 | 칸 74.5 → **38.4mm** | 안 걸림 |

**→ 2단으로 찍히면 90mm 선언은 inert 하다. 실제로 문제를 푸는 건 `position: static` 쪽이다.**
"90mm 를 넣어서 사진이 안 넘쳤다"로 보고하면 인과가 틀린다(기준 E 와 같은 종류의 오류).

**그런데 죽은 규칙은 아니다 — 1단으로 떨어지면 전부 걸린다:**

| 이미지 | 1단(177.4mm) 높이 | 90mm |
|---|---|---|
| robot-handle.png | **164.4mm** | 걸림 |
| elevator-align.jpg | **98.6mm** | 걸림 |
| people-fov-diagram.png | **91.2mm** | 걸림 |
| gpt-gate-diagram.svg | **91.5mm** | 걸림 |

**→ 90mm 는 "1단 낙하 시 보험"이다.** 0-2 의 687.9px 예측이 틀려 1단으로 찍히는 경우를 막는다.
판정: **2단이면 inert(정상), 1단이면 load-bearing.** 어느 쪽인지 렌더에서 먼저 확인한다.

> ⚠️ 1단으로 떨어져 90mm 가 걸리면 **새 문제가 생긴다.** `object-fit: contain` 이라
> robot-handle(0.927)은 90mm 높이에 맞추면 폭이 **97.1mm** 로 줄어, 177.4mm 칸 안에서
> **좌우 80mm 가 흰 여백**이 된다. 1단 렌더가 나오면 이 여백을 반드시 확인할 것.

## 9-3. iframe · video 지면 점유 — 판단 자료

| 요소 | 크기 | 면적 | A4 본문 한 쪽 대비 |
|---|---|---|---|
| YouTube iframe (16:9, --wide 칸) | 74.5 × 41.9mm | 3,122mm² | **6.5%** × 2개 |
| `.figure--pair` 칸 (4:3) | 87.1 × 65.3mm | 5,689mm² | **11.8%** (video 1칸) |
| **합계(최악)** | | **11,933mm²** | **0.25쪽분** |

계산: `.figure--pair` 는 `repeat(auto-fit, minmax(min(100%,200px),1fr))` + gap 12px →
177.37mm 에 2칸이 들어가 칸당 87.1mm, `aspect-ratio: 4/3` 이라 높이 65.3mm.

**소견**: 네 쪽 안팎 문서에서 **0.25쪽**이 빈/검은 상자다. 치명적이진 않다.
다만 `.figure--pair` 칸(11.8%)이 가장 크고, **사진 1장 옆에 빈 칸 1개**가 나란히 놓이는 모양이라
눈에 띄는 손실이다. iframe 2개는 각 6.5% 로 상대적으로 작다.
→ 권고 순위: ① `.figure--pair` 의 `video` 를 인쇄에서 `display:none` (옆 사진이 칸을 다 쓰게)
② iframe 은 검은 상자 대신 제목+URL 텍스트로 대체. **둘 다 개선 제안이지 결격은 아니다.**

## 9-4. 🚨 다크모드 인쇄 — **정적 분석으로 잡힌 결함** (렌더 없이 확정)

기준 O 를 "검증 범위 밖"으로만 두려 했으나, 특정성을 따져 보니 **실제 결함이 있다.**

```
tokens.css:159   @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --text-muted: #a3a3a3; … } }
print.css:22     :root,                      ← 이 줄이 문제
print.css:23     :root[data-theme="dark"],
print.css:24     :root[data-theme="light"]   { --text-muted: #1a1a1a; … }
```

| 선택자 | 특정성 |
|---|---|
| `:root:not([data-theme="light"])` (tokens.css) | **(0,2,0)** — `:not()` 은 인자의 특정성을 더한다 |
| `:root` (print.css) | **(0,1,0)** |
| `:root[data-theme="dark"]` (print.css) | (0,2,0) |

**→ `data-theme` 속성이 없는 상태에서 tokens.css(0,2,0) 가 print.css(0,1,0) 를 이긴다.**
소스 순서는 특정성이 같을 때만 보므로 print.css 가 뒤에 링크돼 있어도 소용없다.

**언제 터지나**: `theme.js` 는 사용자가 토글을 **누른 적이 있을 때만** `data-theme` 을 심는다
(누르기 전에는 `prefers-color-scheme` 로만 판정). 따라서
**"시스템이 다크인 사람이 토글을 안 누르고 Ctrl+P"** 라는 가장 흔한 경로에서 재현된다.

**증상**: `html,body{background:#fff!important; color:#000}` 은 `!important`/소스순서로 이기므로
바탕과 본문 글자는 정상이다. 그러나 **`var(--text-muted)` 를 쓰는 곳은 `#a3a3a3` 으로 남는다**
— 흰 종이에 명도대비 약 2.3:1 로, 캡션·메타·보조 문구가 거의 안 보인다.
`var(--surface)`·`var(--border)` 도 다크값으로 남는다(배경은 Chrome 기본이 인쇄 안 함이라 영향이 작다).

**고치는 법(1줄)**: print.css:22 의 `:root` 를 `:root, :root:not([data-theme="light"])` 로 바꾸거나,
토큰 블록 전체에 `!important` 를 주거나, 선택자를 `html:root` 급으로 올린다.

**검증 방법**(헤드리스 기본은 light 이라 그냥은 재현 안 됨):
CDP `Emulation.setEmulatedMedia` 로 `prefers-color-scheme: dark` 를 걸고 인쇄한다.
(`--force-dark-mode` 는 Chrome 의 자동 다크 반전이라 `prefers-color-scheme` 과 다르다 — 쓰면 안 된다.)

**기준 O 개정**: "검증 안 됨"이 아니라 **"정적 분석상 결함 있음, 렌더로 재확인 필요"**.
