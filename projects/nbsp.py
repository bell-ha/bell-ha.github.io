#!/usr/bin/env python3
"""한글 문장의 줄바꿈을 쉼표·마침표 뒤로만 모은다.

build.py 를 폐기하면서 거기서 떼어낸 규칙이다(원래 이름 clause_wrap).
한국어는 어절마다 띄어 쓰므로 브라우저는 아무 띄어쓰기에서나 줄을 바꾼다.
그대로 두면 '손잡이 직접 설계·3D 출력' 이 '설계'와 '3D' 사이에서 끊긴다.
절 안의 띄어쓰기를 줄바꿈 없는 공백(NBSP)으로 바꿔 끊길 자리를 문장부호 뒤로 모은다.

쓰기
    python3 nbsp.py "ROS2·Nav2 자율주행과 엘리베이터 탑승으로 1층에서 5층까지 완주."
    echo "문장" | python3 nbsp.py
결과를 그대로 HTML 에 붙여 넣는다. 눈에는 보통 공백과 똑같이 보인다.
"""
import sys

NBSP = " "
# 절이 끝났다고 보는 글자. 이 뒤의 띄어쓰기에서만 줄을 바꾼다.
CLAUSE_END = tuple(",.·…!?;:)—’”")
WJ = "⁠"  # WORD JOINER — 이 앞뒤로는 절대 안 끊긴다


def visual_len(t: str) -> float:
    """한글 한 글자를 1로 보고 잰 대략적인 길이."""
    return sum(1.0 if ord(c) > 0x2E80 else 0.55 for c in t)


def clause_wrap(text: str, limit: float = 20.0) -> str:
    """절 하나가 limit(한글 20자) 보다 길면 손대지 않는다.

    긴 절에 줄바꿈을 막으면 이번엔 단어 한가운데가 잘리기 때문이다.
    폰(390px)에서 본문 한 줄이 21자라 20 을 상한으로 잡았다.
    """
    if " " not in text:
        return text
    words = text.split(" ")
    out, clause, clauses = [], [], []
    for i, w in enumerate(words):
        clause.append(w)
        if w.endswith(CLAUSE_END) or i == len(words) - 1:
            clauses.append(" ".join(clause))
            out.append(NBSP.join(clause))
            clause = []
    if len(clauses) < 2:
        return text                      # 끊을 자리가 없으면 원문 그대로
    if max(visual_len(c) for c in clauses) > limit:
        return text                      # 절이 길면 강제하지 않는다
    return " ".join(out)


def join_marks(text: str) -> str:
    """가운데점과 붙임표에서 끊기는 것을 막는다. 나열이라 끊겨도 되는 자리면 쓰지 않는다."""
    import re
    t = text.replace("·", WJ + "·" + WJ)
    return re.sub(r"(?<=[가-힣A-Za-z0-9])-(?=[가-힣A-Za-z0-9])", WJ + "-" + WJ, t)


if __name__ == "__main__":
    src = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read().rstrip("\n")
    for line in src.split("\n"):
        print(join_marks(clause_wrap(line)))
