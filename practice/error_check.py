"""3일차 오류 메시지 읽기 노트북(day03_01_error_reading.ipynb)의 확인 셀이 부르는 검사 코드입니다.

배우는 코드가 아니므로 읽거나 고치지 않아도 됩니다. 노트북의 셀은 이 파일의 함수를 한 줄로 부릅니다.
- 오류 예시는 일부러 만든 것이라 오류 이름과 줄 번호의 정답이 정해져 있습니다. 뜻은 내 말로 적으므로 비어 있는지만 봅니다.
- 검사 중에 문제가 생겨도 영어 오류 화면 대신 한글 안내가 나옵니다.
"""

import inspect
import re

PASS = "통과"
AGAIN = "다시"
NOT_YET = "아직"

# 묶음마다: (적기 셀의 변수 앞이름, 묶음 이름, 오류 이름, 줄 번호)
EXAMPLES = {
    "b1": ("B1 이름 오타", "NameError", 4),
    "b2": ("B2 없는 딕셔너리 키", "KeyError", 4),
    "d1": ("더 해 보기 1 설치되지 않은 패키지", "ModuleNotFoundError", 2),
    "d2": ("더 해 보기 2 없는 파일", "FileNotFoundError", 2),
}
ERROR_NAMES = ("ZeroDivisionError", "NameError", "KeyError", "ModuleNotFoundError", "FileNotFoundError")


# ---------------------------------------------------------------- 노트북 셀이 부르는 함수


def check_b1():
    """B1 묶음의 적기 칸 세 개를 확인합니다."""
    names = _caller_names()
    _guard(lambda: _show(_example_rows("b1", names)))


def check_b2():
    """B2 묶음의 적기 칸 세 개를 확인합니다."""
    names = _caller_names()
    _guard(lambda: _show(_example_rows("b2", names)))


def check_d1():
    """더 해 보기 1 묶음의 적기 칸 세 개를 확인합니다."""
    names = _caller_names()
    _guard(lambda: _show(_example_rows("d1", names)))


def check_d2():
    """더 해 보기 2 묶음의 적기 칸 세 개를 확인합니다."""
    names = _caller_names()
    _guard(lambda: _show(_example_rows("d2", names)))


def check_request():
    """C 묶음: 재요청 문장 틀의 세 칸을 확인하고, 다 채웠으면 요청문을 한 덩어리로 보여 줍니다."""
    names = _caller_names()
    _guard(lambda: _check_request(names))


# ---------------------------------------------------------------- 항목별 확인


def _example_rows(key, names):
    group, error_name, line = EXAMPLES[key]
    write_cell = "%s 묶음의 적기 셀을 먼저 실행합니다." % group
    rows = []

    answer = _value(names, key + "_error_name")
    if answer is None:
        rows.append(_row("오류 이름", "적지 않음", NOT_YET, write_cell))
    elif answer == "":
        rows.append(_row("오류 이름", "비어 있음", AGAIN, "오류 메시지 맨 아래 줄에서 콜론(:) 앞의 영어 낱말을 적습니다."))
    elif re.search(r"\b%s\b" % error_name, answer, re.IGNORECASE):
        rows.append(_row("오류 이름", error_name, PASS))
    elif _other_error_name(answer):
        rows.append(_row("오류 이름", answer[:40], AGAIN,
                         "다른 묶음의 오류 이름입니다. 바로 위 오류 셀의 맨 아래 줄을 다시 봅니다."))
    else:
        rows.append(_row("오류 이름", answer[:40], AGAIN,
                         "맨 아래 줄에서 콜론(:) 앞의 영어 낱말을 글자 그대로 적습니다. 예: ZeroDivisionError"))

    answer = _value(names, key + "_line")
    if answer is None:
        rows.append(_row("줄 번호", "적지 않음", NOT_YET, write_cell))
    elif answer == "":
        rows.append(_row("줄 번호", "비어 있음", AGAIN, "Cell In[ ] 뒤의 line 다음 숫자를 적습니다."))
    else:
        numbers = re.findall(r"\d+", answer)
        if str(line) in numbers[-1:] or numbers == [str(line)]:
            rows.append(_row("줄 번호", str(line), PASS))
        elif not numbers:
            rows.append(_row("줄 번호", answer[:40], AGAIN, "숫자로 적습니다. Cell In[ ] 뒤의 line 다음 숫자입니다."))
        else:
            rows.append(_row("줄 번호", answer[:40], AGAIN,
                             "In[ ] 안의 숫자는 셀을 실행한 순서입니다. 그 뒤 line 다음 숫자(셀 안에서 몇째 줄인지)를 적습니다."))

    answer = _value(names, key + "_meaning")
    if answer is None:
        rows.append(_row("뜻", "적지 않음", NOT_YET, write_cell))
    elif len(answer) < 2:
        rows.append(_row("뜻", "비어 있음", AGAIN, "이 오류가 무슨 뜻인지 내 말로 한 줄 적습니다."))
    elif answer.strip(" :").lower() == error_name.lower():
        rows.append(_row("뜻", answer[:40], AGAIN, "오류 이름을 그대로 쓰지 않고, 무엇이 잘못됐는지 내 말로 적습니다."))
    else:
        rows.append(_row("뜻", answer[:40], PASS))
    return rows


def _check_request(names):
    rows = []
    goal = _value(names, "request_goal")
    error = _value(names, "request_error", keep_lines=True)
    expected = _value(names, "request_expected")
    write_cell = "C 묶음의 적기 셀을 먼저 실행합니다."

    if goal is None:
        rows.append(_row("하려던 일", "적지 않음", NOT_YET, write_cell))
    elif len(goal) < 2:
        rows.append(_row("하려던 일", "비어 있음", AGAIN, "무엇을 하려다 오류가 났는지 한 줄 적습니다."))
    else:
        rows.append(_row("하려던 일", goal[:40], PASS))

    if error is None:
        rows.append(_row("오류 메시지 전체", "적지 않음", NOT_YET, write_cell))
    else:
        lines = [line for line in error.splitlines() if line.strip()]
        if not lines:
            rows.append(_row("오류 메시지 전체", "비어 있음", AGAIN, "B 묶음 오류 셀의 출력을 끌어서 선택해 복사한 뒤 붙여 넣습니다."))
        elif not re.search(r"[A-Za-z]*(Error|Exception)", error):
            rows.append(_row("오류 메시지 전체", lines[-1][:40], AGAIN,
                             "오류 이름이 있는 맨 아래 줄까지 들어가게 붙여 넣습니다."))
        elif len(lines) < 2:
            rows.append(_row("오류 메시지 전체", "한 줄만 있음", AGAIN,
                             "맨 아래 줄만이 아니라 줄 번호가 나온 부분부터 맨 아래 줄까지 모두 붙여 넣습니다."))
        else:
            rows.append(_row("오류 메시지 전체", "%d줄" % len(lines), PASS))

    if expected is None:
        rows.append(_row("기대한 결과", "적지 않음", NOT_YET, write_cell))
    elif len(expected) < 2:
        rows.append(_row("기대한 결과", "비어 있음", AGAIN, "고쳐진 뒤 화면에 무엇이 나오면 되는지 한 줄 적습니다."))
    else:
        rows.append(_row("기대한 결과", expected[:40], PASS))

    _show(rows)
    if all(row["status"] == PASS for row in rows):
        print("")
        print("Codex에 보낼 요청문(세 칸을 한 덩어리로 모은 것):")
        print("----")
        print("하려던 일: " + goal)
        print("오류 메시지 전체:")
        print("\n".join(line.rstrip() for line in error.strip("\n").splitlines()))
        print("기대한 결과: " + expected)
        print("----")


# ---------------------------------------------------------------- 보여 주기


def _row(item, value, status, todo=""):
    return {"item": item, "value": value, "status": status, "todo": todo}


def _closing(rows):
    statuses = [row["status"] for row in rows]
    if NOT_YET in statuses:
        return "아직 실행하지 않은 적기 셀이 있습니다. 그 셀을 먼저 실행한 뒤 이 셀을 다시 실행합니다."
    if AGAIN in statuses:
        return "다시가 나온 줄은 '할 일'을 따라 적기 칸을 고치고, 그 적기 셀부터 다시 실행합니다."
    return "모두 통과입니다."


def _show(rows):
    """결과를 표로 보여 줍니다. 노트북에서는 표 모양으로, 터미널에서는 줄 글로 나옵니다."""
    table = ["| 항목 | 적은 값 | 결과 | 할 일 |", "|---|---|---|---|"]
    lines = []
    for row in rows:
        status = row["status"] if row["status"] == PASS else "**%s**" % row["status"]
        table.append("| %s | %s | %s | %s |" % (_md(row["item"]), _md(row["value"]), status, _md(row["todo"])))
        lines.append(("%s: %s [%s] %s" % (row["item"], row["value"], row["status"], row["todo"])).rstrip())
    closing = _closing(rows)
    _display("\n".join(table + ["", closing]), "\n".join(lines + [closing]))


def _display(markdown_text, plain_text):
    try:
        from IPython import get_ipython
        from IPython.display import display
        shell = get_ipython()
    except ImportError:
        shell = None
    if shell is None:
        print(plain_text)
    else:
        display({"text/markdown": markdown_text, "text/plain": plain_text}, raw=True)


def _guard(job):
    """확인 중에 생긴 문제를 영어 오류 화면 대신 한글 안내로 보여 줍니다."""
    try:
        job()
    except Exception as error:
        print("확인하는 중에 예상하지 못한 문제가 생겼습니다. 이 화면을 현장조교에게 보여 줍니다.")
        print("(문제 종류: %s)" % type(error).__name__)


# ---------------------------------------------------------------- 작은 도움 함수


def _value(names, key, keep_lines=False):
    """적기 칸의 값을 읽습니다. 셀을 실행하지 않았으면 None 을 돌려줍니다."""
    if key not in names:
        return None
    text = str(names[key])
    if keep_lines:
        return text.strip()
    return " ".join(text.split())


def _other_error_name(answer):
    return any(re.search(r"\b%s\b" % name, answer, re.IGNORECASE) for name in ERROR_NAMES)


def _md(text):
    """표 칸 안의 글자가 표 모양을 깨지 않게 기호 앞에 역슬래시를 붙입니다."""
    return re.sub(r"([\\`*_\[\]<>|#])", r"\\\1", str(text))


def _caller_names():
    """이 함수를 부른 노트북 셀의 변수들(적기 셀에 적은 값)을 읽습니다."""
    try:
        return dict(inspect.currentframe().f_back.f_back.f_globals)
    except Exception:
        return {}
