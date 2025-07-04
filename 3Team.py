import streamlit as st
from screen.ev import show_page_1
from screen.app2 import show_page_2
from screen.app3 import show_page_3
from screen.app4 import show_page_4
from screen.linegraph2 import show_page_5
from screen.faq import show_faq_page

st.set_page_config(page_title="전기차 인프라 대시보드", layout="wide")

# 🎯 첫 번째 사이드바 섹션: 분석 화면 선택
# st.sidebar.markdown("## 📂 분석 화면 선택")
# menu = st.sidebar.radio("", [
#     "1. 지역별 전기차 & 충전소 비율",
#     "2. 지역별 전기차 등록 대수 및 충전기 개수 비교",
#     "3. 지역별 히트맵",
#     "4. 차량당 충전기 수 변화",
#     "5. 전기차 등록 수 vs 충전기 수 추세 그래프"
# ])

# # 🎯 두 번째 사이드바 섹션: FAQ
# st.sidebar.markdown("## ❓ FAQ")
# faq_menu = st.sidebar.radio("", [
#     "자주 묻는 질문 보기"
# ])

# FAQ 체크 여부
# show_faq = st.sidebar.checkbox("❓ 브랜드 FAQ 보기")

# ✅ 상태 저장용 세션 변수 초기화
if "mode" not in st.session_state:
    st.session_state["mode"] = "analysis"  # or "faq"

# ✅ 버튼 UI
with st.sidebar:
    #st.markdown("## 🔘 화면 선택")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 분석 화면"):
            st.session_state["mode"] = "analysis"
    with col2:
        if st.button("❓ 브랜드 FAQ"):
            st.session_state["mode"] = "faq"

# ✅ 화면 표시 조건 분기
if st.session_state["mode"] == "faq":
    show_faq_page()

elif st.session_state["mode"] == "analysis":
    menu = st.sidebar.radio("📂 분석 화면 선택", [
        "1. 지역별 전기차 & 충전소 비율",
        "2. 전기차 등록 대수 vs 충전기 개수",
        "3. 지역별 히트맵",
        "4. 차량당 충전기 수 변화",
        "5. 등록 수 vs 충전기 수 추세 그래프"
    ])



# ✅ 메인 컨텐츠 라우팅
if menu.startswith("1"):
    show_page_1()
elif menu.startswith("2"):
    show_page_2()
elif menu.startswith("3"):
    show_page_3()
elif menu.startswith("4"):
    show_page_4()
elif menu.startswith("5"):
    show_page_5()
