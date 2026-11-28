# 오류 메시지 읽기 연습용 앱입니다(덱 "한 줄 요청으로 만들기"). 오류 하나를 일부러 심어 두었습니다.
# 자기소개 페이지와는 상관없는 연습용 파일이라, 페이지를 만들 때 참고하지 않습니다.
# 실행: 저장소 폴더의 터미널에서 uv run streamlit run practice/broken_app.py
# 터미널과 브라우저에 나온 오류 메시지를 읽고, 고치는 것은 Codex 에 다시 요청해서 합니다.
import streamlit as st

profile = {
    "이름": "홍길동",
    "전공": "국어국문학",
    "관심 직무": "UX 리서처",
}

st.title("연습용 소개 카드")
st.write("이름:", profile["이름"])
st.write("전공:", profile["전공"])
st.write("관심 직무:", profile["관심직무"])
