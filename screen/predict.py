def show_page_6():
  import streamlit as st
  import pandas as pd
  import numpy as np
  import matplotlib.pyplot as plt
  import matplotlib.font_manager as fm
  import platform
  import sqlite3



  #폰트 설정
  font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
  fontprop = fm.FontProperties(fname=font_path, size=10)
  plt.rcParams['font.family'] = 'NanumGothic'
  plt.rcParams['axes.unicode_minus'] = False


  #sqlite 메모리 DB 생성
  conn = sqlite3.connect(':memory:')

  #sql 파일 읽기
  with open('/content/SQL/ev.sql', 'r', encoding='utf-8') as f:
      sql_script = f.read()

  #sql 스크립트 실행 (테이블 생성 + 데이터 삽입)
  conn.executescript(sql_script)

  # 쿼리 실행 후 데이터프레임으로 변환
  df = pd.read_sql_query("""
      SELECT 
          year || '-' || printf('%02d', month) AS 연도월,
          region,
          charger_count
      FROM charger_summary
      ORDER BY year, month
    """, conn)
  
    
  # ✅ 2. 피벗 테이블로 변환 (행: 연도월, 열: 지역)
  df_pivot = df.pivot(index='연도월', columns='region', values='charger_count').reset_index()
  df_pivot['연도월'] = pd.to_datetime(df_pivot['연도월'])
  df_pivot['월수'] = np.arange(len(df_pivot))

  # ✅ 3. 예측 수행 (선형 회귀 기반)
  future_months = 14
  region_list = df['region'].unique().tolist()
  predict_df = pd.DataFrame()

  for region in region_list:
      coef = np.polyfit(df_pivot['월수'], df_pivot[region], 1)
      poly_fn = np.poly1d(coef)
      future_x = np.arange(len(df_pivot), len(df_pivot) + future_months)
      predict_df[region] = poly_fn(future_x)

  # ✅ 4. 연도월 생성 및 병합
  start_date = df_pivot['연도월'].iloc[-1] + pd.DateOffset(months=1)
  predict_df['연도월'] = pd.date_range(start=start_date, periods=future_months, freq='MS')
  full_df = pd.concat([df_pivot.drop(columns=['월수']), predict_df], ignore_index=True)
  full_df['연도월'] = pd.to_datetime(full_df['연도월'])

  # ✅ 5. Streamlit UI
  st.title("📊 지역별 전기차 1대당 충전소 비율 예측")
  region_selected = st.selectbox("지역을 선택하세요", region_list)

  # ✅ 6. 시각화
  fig, ax = plt.subplots(figsize=(12, 5))
  ax.plot(full_df['연도월'], full_df[region_selected], marker='o', label=region_selected)
  ax.axvline(pd.to_datetime('2025-05'), color='gray', linestyle='--', label='예측 시작')
  ax.set_title(f"{region_selected} 지역 전기차 1대당 충전소 비율 예측 (2023.06 ~ 2026.06)")
  ax.set_xlabel("연도-월")
  ax.set_ylabel("1대당 충전소 수")
  ax.grid(True, linestyle='--', alpha=0.6)
  ax.legend()
  st.pyplot(fig)