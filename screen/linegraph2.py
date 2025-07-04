
def show_page_5():
    

  import streamlit as st
  import pandas as pd
  import matplotlib.pyplot as plt
  import sqlite3
  import matplotlib.font_manager as fm

  font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
  fontprop = fm.FontProperties(fname=font_path, size=10)
  plt.rcParams['font.family'] = 'NanumGothic'
  plt.rcParams['axes.unicode_minus'] = False

  # 기본 설정
  st.set_page_config(page_title="EV vs Charger Trend", layout="wide")

  st.title("📈 전기차 등록 수 vs 충전기 수 추세 그래프")

  # SQLite 메모리 DB 생성
  conn = sqlite3.connect(':memory:')

  # sql.sql 파일 실행
  with open('/content/SQL/ev.sql', 'r', encoding='utf-8') as f:
      sql_script = f.read()
  conn.executescript(sql_script)

  # ev 테이블 집계
  ev_df = pd.read_sql_query('''
      SELECT year, month, SUM(ev_count) as total_ev
      FROM ev
      GROUP BY year, month
  ''', conn)

  # charger 테이블 집계
  charger_df = pd.read_sql_query('''
      SELECT year, month, SUM(charger_count) as total_charger
      FROM charger
      GROUP BY year, month
  ''', conn)

  # date 컬럼 생성
  ev_df['date'] = pd.to_datetime(ev_df['year'].astype(str) + '-' + ev_df['month'].astype(str).str.zfill(2))
  charger_df['date'] = pd.to_datetime(charger_df['year'].astype(str) + '-' + charger_df['month'].astype(str).str.zfill(2))

  # 병합 및 정렬
  merged_df = pd.merge(ev_df[['date', 'total_ev']], charger_df[['date', 'total_charger']], on='date')
  merged_df = merged_df.sort_values('date')

  # Streamlit 그래프 출력
  fig, ax = plt.subplots(figsize=(8, 4))
  ax.plot(merged_df['date'], merged_df['total_ev'], label='EV 등록 수', marker='o')
  ax.plot(merged_df['date'], merged_df['total_charger'], label='충전기 수', marker='s')
  # ax.set_title('전기차 등록 수 및 충전기 수 추세', fontsize=16)
  ax.set_xlabel('날짜', fontsize=12)
  ax.set_ylabel('수량', fontsize=12)
  ax.grid(True)
  ax.legend()
  plt.xticks(rotation=45)

  st.pyplot(fig)
