
import streamlit as st
import pandas as pd
import os

def show_faq_page():
  st.header("❓ 브랜드별 자주 묻는 질문 (FAQ)")

  # ✅ 브랜드 선택
  faq_dir = "csv"
  brands = ['hyundai','kia','genesis','benz']
  selected_brand = st.selectbox("브랜드 선택", brands, index=0)

  # ✅ 해당 브랜드의 FAQ 불러오기
  file_path = os.path.join(faq_dir, f"{selected_brand}_faq_final.csv")


  try:
      df = pd.read_csv(file_path)

      st.markdown(f"### 💡 {selected_brand.upper()} 관련 FAQ")

      for _, row in df.iterrows():
          with st.expander(f"❓ {row['질문']}"):
              st.markdown(f"**분류:** {row['분류']}")
              st.markdown(f"{row['답변']}")

  except Exception as e:
      st.error(f"FAQ를 불러오는 중 오류 발생: {e}")

