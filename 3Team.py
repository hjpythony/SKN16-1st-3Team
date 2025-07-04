# 3Team.py
import streamlit as st
from urllib.parse import parse_qs
from screen.ev import show_page_1
from screen.app2 import show_page_2
from screen.app3 import show_page_3
from screen.app4 import show_page_4
from screen.linegraph2 import show_page_5
from screen.faq import show_faq_page

st.set_page_config(page_title="전기차 인프라 대시보드", layout="wide")

# ✅ 세션 초기화
if "mode" not in st.session_state:
    st.session_state["mode"] = "analysis"
if "analysis_menu" not in st.session_state:
    st.session_state["analysis_menu"] = None

# ✅ 쿼리 스트링 읽어오기 (Streamlit workaround)
query_params = st.query_params
if "analysis_menu" in query_params:
    st.session_state["analysis_menu"] = query_params["analysis_menu"]

# ✅ CSS 스타일 정의
st.markdown("""
<style>
.sidebar-button {
    display: block;
    width: 100%;
    padding: 12px 15px;
    margin: 6px 0;
    font-size: 13px;
    font-weight: 500;
    color: #333;
    background-color: #f0f2f6;
    border: 2px solid #ccc;
    border-radius: 8px;
    text-align: center;
    white-space: normal;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
}
.sidebar-button:hover {
    background-color: #4a90e2;
    color: white;
}
.sidebar-button.selected {
    background-color: #0057b8;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ✅ 사이드바 버튼 UI
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("분석 화면📊"):
            st.session_state["mode"] = "analysis"
    with col2:
        if st.button("브랜드 FAQ❓"):
            st.session_state["mode"] = "faq"

    # 분석 화면 버튼 세트
    if st.session_state["mode"] == "analysis":
        st.markdown("---")
        st.markdown("### 분석 화면 선택")

        # (라벨, 키) 리스트
        buttons = [
            ("지역별 전기차 & 충전소 비율", "비율"),
            ("전기차 등록 대수 vs 충전기 개수", "비교"),
            ("지역별 히트맵", "히트맵"),
            ("차량당 충전기 수 변화", "변화"),
            ("등록 수 vs 충전기 수 추세 그래프", "추세"),
        ]

        for label, key in buttons:
            selected_class = "selected" if st.session_state["analysis_menu"] == key else ""
            btn_html = f'''
              <a href="?analysis_menu={key}" target="_self">
                  <button class="sidebar-button {selected_class}">{label}</button>
              </a>
            '''
            st.markdown(btn_html, unsafe_allow_html=True)

# ✅ 화면 표시
if st.session_state["mode"] == "faq":
    show_faq_page()

elif st.session_state["mode"] == "analysis":
    selected = st.session_state["analysis_menu"]

    if selected == "비율":
        show_page_1()
    elif selected == "비교":
        show_page_2()
    elif selected == "히트맵":
        show_page_3()
    elif selected == "변화":
        show_page_4()
    elif selected == "추세":
        show_page_5()
    else:
        st.info("왼쪽에서 분석 화면을 선택해주세요.")

