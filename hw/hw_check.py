"""3일차 현장조교 실습(과제) 노트북 day03_hw_todo_app.ipynb 의 확인 셀이 호출하는 검사 코드입니다.

배우는 코드가 아니므로 읽거나 고치지 않아도 됩니다. 노트북의 셀은 이 파일의 함수를 한 줄로 호출합니다.
- 파일이 제자리에 있는지, 적기 칸이 채워졌는지, README 칸이 채워졌는지만 봅니다. 앱이 잘 만들어졌는지는 내가 직접 눌러 보고 판단합니다.
- 검사 중에 문제가 생겨도 영어 오류 화면 대신 한글 안내가 나옵니다.
"""

import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "practice"))
from error_check import AGAIN, NOT_YET, PASS, _caller_names, _display, _guard, _md, _row, _value  # noqa: E402

# 노트북은 hw 폴더에서, 터미널은 저장소 맨 위에서 실행하므로 두 곳을 모두 찾습니다.
ROOTS = (Path(".."), Path("."))
ALLOWED = {"streamlit", "sqlite3", "datetime", "calendar"}
SECTIONS = ("주요 기능", "시스템 구조", "핵심 코드 원리")


# ---------------------------------------------------------------- 노트북 셀이 호출하는 함수


def check_ready():
    """A 묶음: todo 폴더의 과제 파일 세 개가 있는지 확인합니다."""
    _guard(lambda: _show([_exists("todo/requirements.md", "요구사항"), _exists("todo/check-inputs.md", "확인용 입력"),
                          _exists("todo/design.webp", "최종 화면 시안")], "저장소 맨 위의 todo 폴더를 확인합니다."))


def check_app():
    """B 묶음: todo/app.py 가 있고 허용한 패키지만 쓰는지 확인합니다."""
    _guard(lambda: _show(_app_rows(), "Codex 에 다시 요청해 고친 뒤 이 셀을 다시 실행합니다."))


def check_inputs():
    """C 묶음: 확인용 입력 3개의 결과 칸을 확인합니다."""
    names = _caller_names()
    _guard(lambda: _show(_input_rows(names), "적기 셀을 고치고 그 셀부터 다시 실행합니다."))


def check_grade():
    """D 묶음: 자가 채점 칸과 todos.db 를 확인합니다."""
    names = _caller_names()
    _guard(lambda: _show(_grade_rows(names), "적기 셀을 고치고 그 셀부터 다시 실행합니다."))


def check_submit():
    """E 묶음: README 칸과 제출 전 확인, .gitignore 를 확인합니다."""
    _guard(lambda: _show(_submit_rows(), "README 를 고치고 저장한 뒤 이 셀을 다시 실행합니다."))


# ---------------------------------------------------------------- 항목별 확인


def _find(name):
    for root in ROOTS:
        path = root / name
        if path.is_file():
            return path
    return None


def _exists(name, label):
    if _find(name) is not None:
        return _row(label, name, PASS)
    return _row(label, "찾지 못함", AGAIN, "저장소 맨 위의 %s 위치에 있어야 합니다." % name)


def _app_rows():
    path = _find("todo/app.py")
    if path is None:
        return [_row("todo/app.py", "찾지 못함", NOT_YET, "B 묶음의 요청으로 Codex 가 앱을 먼저 만들게 합니다.")]
    source = path.read_text(encoding="utf-8")
    rows = [_row("todo/app.py", "%d줄" % len(source.splitlines()), PASS if source.strip() else AGAIN)]
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return rows + [_row("파이썬 문법", "오류", AGAIN, "Codex 에 오류 메시지 전체를 붙여 다시 요청합니다.")]
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])
    outside = sorted(name for name in modules if name not in ALLOWED and name not in sys.stdlib_module_names)
    if outside:
        rows.append(_row("쓴 패키지", ", ".join(outside), AGAIN, "설치하지 말고, 그 패키지 없이 만들어 달라고 Codex 에 다시 요청합니다."))
    else:
        rows.append(_row("쓴 패키지", "허용한 것만", PASS))
    rows.append(_row("SQLite", "사용함" if "sqlite3" in modules else "쓰지 않음", PASS if "sqlite3" in modules else AGAIN,
                     "" if "sqlite3" in modules else "할 일을 SQLite 파일(todos.db)에 저장하게 다시 요청합니다."))
    return rows


def _input_rows(names):
    rows = []
    for number in (1, 2, 3):
        item = "입력 %d" % number
        result = _value(names, "input%d_result" % number)
        diff = _value(names, "input%d_diff" % number)
        if result is None:
            rows.append(_row(item, "적지 않음", NOT_YET, "C 묶음의 적기 셀을 먼저 실행합니다."))
        elif result not in ("같음", "다름"):
            rows.append(_row(item, result[:20] or "비어 있음", AGAIN, "기대 결과와 같으면 같음을 적습니다. 다르면 다름을 적습니다."))
        elif result == "다름" and len(diff or "") < 2:
            rows.append(_row(item, "다름", AGAIN, "무엇이 달랐는지 한 줄 적습니다."))
        else:
            rows.append(_row(item, result, PASS))
    return rows


def _grade_rows(names):
    rows = []
    yes = _value(names, "required_yes")
    failed = _value(names, "failed_items")
    bonus = _value(names, "bonus_13")
    if yes is None:
        rows.append(_row("필수 통과 수", "적지 않음", NOT_YET, "D 묶음의 적기 셀을 먼저 실행합니다."))
    elif not re.fullmatch(r"\d{1,2}", yes) or int(yes) > 12:
        rows.append(_row("필수 통과 수", yes[:20] or "비어 있음", AGAIN, "필수 12개 중 통과한 개수를 0부터 12 사이의 숫자로 적습니다."))
    else:
        rows.append(_row("필수 통과 수", "%s개" % yes, PASS))
        if int(yes) < 12 and not re.search(r"\d", failed or ""):
            rows.append(_row("통과하지 못한 항목", failed or "비어 있음", AGAIN, "통과하지 못한 항목 번호를 적습니다. 예: 5, 7"))
        elif failed is not None:
            rows.append(_row("통과하지 못한 항목", failed or "없음", PASS))
    if bonus is not None:
        ok = bonus in ("했음", "안 함")
        rows.append(_row("더 하기 13번", bonus[:20] or "비어 있음", PASS if ok else AGAIN, "" if ok else "했음 또는 안 함 중 하나를 적습니다."))
    db = _find("todo/todos.db")
    rows.append(_row("todos.db", "있음" if db else "없음", PASS if db else AGAIN,
                     "" if db else "앱을 한 번 실행해 할 일을 추가하면 todo 폴더에 생깁니다."))
    return rows


def _submit_rows():
    rows = []
    ignore = _find(".gitignore")
    ignored = ignore is not None and re.search(r"^\*\.db\s*$", ignore.read_text(encoding="utf-8"), re.MULTILINE)
    rows.append(_row(".gitignore 의 *.db 줄", "있음" if ignored else "없음", PASS if ignored else AGAIN,
                     "" if ignored else ".gitignore 에 *.db 한 줄을 넣어 todos.db 가 올라가지 않게 합니다."))
    readme = _find("README.md")
    if readme is None:
        return rows + [_row("README.md", "찾지 못함", NOT_YET, "저장소 맨 위의 README.md 를 확인합니다.")]
    text = readme.read_text(encoding="utf-8")
    for name in SECTIONS:
        body = _section(text, name)
        lines = [line for line in body if line.strip() and not line.strip().startswith("(")]
        if len("".join(lines)) < 20:
            rows.append(_row("README: " + name, "비어 있음", AGAIN, "내 말로 두세 줄 적습니다. 괄호 안의 안내 글을 지웁니다."))
        else:
            rows.append(_row("README: " + name, "적음", PASS))
    marks = [line for line in _section(text, "제출 전 확인", level="##") if re.match(r"^\s*- \[[ xX]\]", line)]
    marks = marks[:7]
    done = sum(1 for line in marks if re.match(r"^\s*- \[[xX]\]", line))
    rows.append(_row("제출 전 확인", "%d / 7 표시" % done, PASS if done == 7 else AGAIN,
                     "" if done == 7 else "마친 항목의 [ ] 를 [x] 로 바꿉니다."))
    return rows


# ---------------------------------------------------------------- 보여 주기와 작은 도움 함수


def _section(text, name, level="###"):
    """README 에서 제목이 name 인 구역의 줄 목록을 돌려줍니다."""
    lines, inside = [], False
    for line in text.splitlines():
        heading = re.match(r"^(#+)\s*(.+?)\s*$", line)
        if heading:
            if inside:
                break
            inside = heading.group(2) == name and heading.group(1) == level
        elif inside:
            lines.append(line)
    return lines


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
