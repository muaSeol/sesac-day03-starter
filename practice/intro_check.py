"""3일차 노트북 02(day03_02_intro_page.ipynb)의 확인 셀이 호출하는 검사 코드입니다.

배우는 코드가 아니므로 읽거나 고치지 않아도 됩니다. 노트북의 셀은 이 파일의 함수를 한 줄로 호출합니다.
- 점수 칸은 0부터 10 사이의 숫자인지만 봅니다. 점수는 요청할 때마다 조금씩 달라서 맞고 틀림을 가리지 않습니다.
- requirements.md 는 세 구역(내 정보, 3줄 요구사항, 요구사항 체크리스트)이 있고 칸이 채워졌는지 봅니다.
- 검사 중에 문제가 생겨도 영어 오류 화면 대신 한글 안내가 나옵니다.
"""

import re
from pathlib import Path

from error_check import AGAIN, NOT_YET, PASS, _caller_names, _display, _guard, _md, _row, _value

# 노트북은 practice 폴더에서, 터미널은 저장소 맨 위에서 실행하므로 두 곳을 모두 찾습니다.
ROOTS = (Path(".."), Path("."))
INFO_FIELDS = ("이름", "전공", "관심 직무", "고른 이유")
LINE_FIELDS = ("대상 사용자", "해결할 문제", "핵심 기능")
EXAMPLE_NAME = "홍길동"
CHECKBOX = re.compile(r"^\s*[-*]\s*\[[ xX]\]\s*(.+)$")


# ---------------------------------------------------------------- 노트북 셀이 호출하는 함수


def check_scores(upto):
    """점수 칸(score_1 ~ score_upto)이 0부터 10 사이의 숫자인지 확인합니다."""
    names = _caller_names()
    _guard(lambda: _show(_score_rows(names, upto), "점수 적기 셀의 숫자를 고치고 그 셀부터 다시 실행합니다."))


def check_requirements(stage):
    """requirements.md 의 모양을 확인합니다. stage 는 2(요구사항 체크리스트) 또는 3(빠진 항목 보완)입니다."""
    _guard(lambda: _show(_requirement_rows(stage), "고친 뒤 이 셀을 다시 실행합니다."))


def check_deploy():
    """G 묶음: 공개 주소 칸이 https://프로젝트이름.vercel.app 꼴인지 확인합니다(네트워크 요청 없이 글자만 봅니다)."""
    names = _caller_names()
    _guard(lambda: _show(_deploy_rows(names), "적기 셀을 고치고 그 셀부터 다시 실행합니다."))


def check_agents():
    """AGENTS.md 가 저장소 맨 위에 있고 비어 있지 않은지 확인합니다."""
    _guard(lambda: _show(_agents_rows(), "/init 으로 만들거나 파일을 저장한 뒤 이 셀을 다시 실행합니다."))


def check_skill():
    """웹 디자인 스킬이 .agents/skills/web-design/SKILL.md 에 있는지 확인합니다."""
    _guard(lambda: _show(_skill_rows(), "폴더를 옮기고 이 셀을 다시 실행합니다."))


# ---------------------------------------------------------------- 항목별 확인


def _score_rows(names, upto):
    rows = []
    for step in range(1, upto + 1):
        item = "%d단계 점수" % step
        answer = _value(names, "score_%d" % step)
        if answer is None:
            rows.append(_row(item, "적지 않음", NOT_YET, "%d단계의 점수 적기 셀을 먼저 실행합니다." % step))
        elif not re.fullmatch(r"\d{1,2}", answer) or int(answer) > 10:
            rows.append(_row(item, answer[:20] or "비어 있음", AGAIN, "통과한 항목 수를 0부터 10 사이 숫자 하나로 적습니다."))
        else:
            rows.append(_row(item, "%s개" % answer, PASS))
    return rows


def _find(name):
    for root in ROOTS:
        path = root / name
        if path.is_file():
            return path
    return None


def _deploy_rows(names):
    url = _value(names, "public_url")
    if url is None:
        return [_row("공개 주소", "적지 않음", NOT_YET, "G 묶음의 적기 셀을 먼저 실행합니다.")]
    if re.fullmatch(r"https://[a-z0-9-]+\.vercel\.app/?", url):
        return [_row("공개 주소", url, PASS)]
    return [_row("공개 주소", url[:60] or "비어 있음", AGAIN,
                 "https:// 로 시작하고 .vercel.app 으로 끝나는 주소를 적습니다. 배포마다 생기는 긴 주소가 아니라 프로젝트이름.vercel.app 입니다.")]


def _agents_rows():
    path = _find("AGENTS.md")
    if path is None:
        return [_row("AGENTS.md", "찾지 못함", NOT_YET, "Codex 입력 칸에 /init 을 입력해 저장소 맨 위에 AGENTS.md 를 만듭니다.")]
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return [_row("AGENTS.md", "비어 있음", AGAIN, "규칙을 한두 줄 적고 저장합니다.")]
    return [_row("AGENTS.md", "%d줄" % len(lines), PASS)]


def _skill_rows():
    path = _find(".agents/skills/web-design/SKILL.md")
    if path is not None:
        return [_row("스킬 파일", ".agents/skills/web-design/SKILL.md", PASS)]
    return [_row("스킬 파일", "찾지 못함", AGAIN,
                 "저장소 맨 위의 .agents/skills 폴더 바로 안에 web-design 폴더가 있고, 그 안에 SKILL.md 가 있어야 합니다.")]


def _requirement_rows(stage):
    path = _find("requirements.md")
    if path is None:
        return [_row("requirements.md", "찾지 못함", NOT_YET, "저장소 맨 위(README.md 옆)에 requirements.md 를 만들어 저장합니다.")]
    text = path.read_text(encoding="utf-8")
    sections = _sections(text)
    rows = [_row("requirements.md", "찾음", PASS)]

    info = sections.get("내 정보")
    if info is None:
        rows.append(_row("내 정보", "구역 없음", AGAIN, "제목 줄 '## 내 정보' 아래에 이름, 전공, 관심 직무, 고른 이유를 적습니다."))
    else:
        values = {field: _field(info, field) for field in INFO_FIELDS}
        empty = [field for field in INFO_FIELDS if len(values[field]) < 2]
        if empty:
            rows.append(_row("내 정보", "빈 칸: " + ", ".join(empty), AGAIN, "빈 칸에 내 값을 적습니다."))
        elif EXAMPLE_NAME in values["이름"]:
            rows.append(_row("내 정보", values["이름"], AGAIN, "내 이름, 전공, 관심 직무, 고른 이유로 바꿉니다."))
        else:
            rows.append(_row("내 정보", "네 칸 채움", PASS))

    lines = sections.get("3줄 요구사항")
    if lines is None:
        rows.append(_row("3줄 요구사항", "구역 없음", AGAIN, "제목 줄 '## 3줄 요구사항' 아래에 대상 사용자, 해결할 문제, 핵심 기능을 한 줄씩 적습니다."))
    else:
        empty = [field for field in LINE_FIELDS if len(_field(lines, field)) < 4]
        if empty:
            rows.append(_row("3줄 요구사항", "빈 칸: " + ", ".join(empty), AGAIN, "누가 읽어도 같은 페이지를 떠올릴 수 있게 한 줄씩 적습니다."))
        else:
            rows.append(_row("3줄 요구사항", "세 줄 채움", PASS))

    checklist = sections.get("요구사항 체크리스트")
    items = [] if checklist is None else [m.group(1) for m in map(CHECKBOX.match, checklist) if m]
    if checklist is None:
        rows.append(_row("요구사항 체크리스트", "구역 없음", AGAIN, "제목 줄 '## 요구사항 체크리스트' 아래에 '- [ ] 항목' 줄을 적습니다."))
    elif len(items) < 3:
        rows.append(_row("요구사항 체크리스트", "%d개" % len(items), AGAIN, "'- [ ] ' 로 시작하는 항목을 세 개 이상 적습니다."))
    else:
        rows.append(_row("요구사항 체크리스트", "%d개" % len(items), PASS))

    if stage >= 3:
        rows.extend(_experience_rows(info or [], items))
    return rows


def _experience_rows(info, items):
    rows = []
    experiences = [line for line in info if re.match(r"^\s*[-*]\s*경험\s*\d*\s*:\s*\S", line)]
    if not experiences:
        rows.append(_row("경험", "없음", AGAIN, "내 정보에 '- 경험 1: ...' 줄을 한두 개 적습니다. 각 경험에서 무엇을 했고 무엇을 배웠는지 씁니다."))
    elif any(len(line) < 20 for line in experiences):
        rows.append(_row("경험", "%d개" % len(experiences), AGAIN, "경험마다 무엇을 했고 무엇을 배웠는지까지 적습니다."))
    else:
        rows.append(_row("경험", "%d개" % len(experiences), PASS))

    asks = [item for item in items if "경험" in item and "지어내" not in item]
    if not asks:
        rows.append(_row("체크리스트의 경험 항목", "없음", AGAIN, "'- [ ] 경험마다 무엇을 했고 무엇을 배웠는지 보인다' 같은 줄을 더합니다."))
    elif any("경험" in item for item in items if "지어내" in item):
        rows.append(_row("체크리스트의 경험 항목", "있음", AGAIN, "'지어내지 않는다' 줄의 괄호(경험 등)를 지웁니다."))
    else:
        rows.append(_row("체크리스트의 경험 항목", "있음", PASS))
    return rows


# ---------------------------------------------------------------- 보여 주기와 작은 도움 함수


def _sections(text):
    """'## 제목' 줄을 기준으로 requirements.md 를 구역별 줄 목록으로 나눕니다."""
    sections, current = {}, None
    for line in text.splitlines():
        heading = re.match(r"^#{2,}\s*(.+?)\s*$", line)
        if heading:
            current = heading.group(1)
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return sections


def _field(lines, name):
    """'- 이름: 값' 줄에서 값을 읽습니다. 없으면 빈 글자를 돌려줍니다."""
    for line in lines:
        found = re.match(r"^\s*[-*]\s*%s\s*:\s*(.*)$" % re.escape(name), line)
        if found:
            return found.group(1).strip()
    return ""


def _show(rows, again_hint):
    statuses = [row["status"] for row in rows]
    if AGAIN in statuses:
        closing = "다시가 나온 줄은 할 일을 따라 고칩니다. " + again_hint
    elif NOT_YET in statuses:
        closing = "아직이 나온 줄은 먼저 할 일을 마친 뒤 이 셀을 다시 실행합니다."
    else:
        closing = "모두 통과입니다."
    table = ["| 항목 | 확인한 값 | 결과 | 할 일 |", "|---|---|---|---|"]
    plain = []
    for row in rows:
        status = row["status"] if row["status"] == PASS else "**%s**" % row["status"]
        table.append("| %s | %s | %s | %s |" % (_md(row["item"]), _md(row["value"]), status, _md(row["todo"])))
        plain.append(("%s: %s [%s] %s" % (row["item"], row["value"], row["status"], row["todo"])).rstrip())
    _display("\n".join(table + ["", closing]), "\n".join(plain + [closing]))
