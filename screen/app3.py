def show_page_3():
  import streamlit as st
  import pandas as pd
  import folium
  import json
  from streamlit_folium import st_folium

  # ✅ 제목
  st.title("📍 지역별 전기차 등록 현황 시각화")

  # ✅ 1. 데이터 불러오기
  geojson_path = '/content/skorea_provinces_geo.json'
  csv_path = '/content/csv/registration_status.csv'

  with open(geojson_path, encoding='utf-8') as f:
      geo_data = json.load(f)

  df = pd.read_csv(csv_path, encoding='utf-8')

  # ✅ 2. 필요한 컬럼 추출 및 변환
  region_columns = df.columns[1:-1]  # '서울' ~ '제주'

  map_df = pd.DataFrame({
      '지역명': region_columns,
      '값': df.iloc[0, 1:-1].values
  })

  # ✅ 3. 지역명 매핑
  name_mapping = {
      '서울': '서울특별시',
      '부산': '부산광역시',
      '대구': '대구광역시',
      '인천': '인천광역시',
      '광주': '광주광역시',
      '대전': '대전광역시',
      '울산': '울산광역시',
      '세종': '세종특별자치시',
      '경기': '경기도',
      '강원': '강원도',
      '충북': '충청북도',
      '충남': '충청남도',
      '전북': '전라북도',
      '전남': '전라남도',
      '경북': '경상북도',
      '경남': '경상남도',
      '제주': '제주특별자치도'
  }

  map_df['지역명'] = map_df['지역명'].map(name_mapping)
  map_df['값'] = pd.to_numeric(map_df['값'], errors='coerce')
  map_df = map_df.dropna(subset=['값'])

  # ✅ 4. GeoJSON에 value 주입
  value_dict = map_df.set_index('지역명')['값'].to_dict()

  for feature in geo_data['features']:
      name = feature['properties']['name']
      feature['properties']['value'] = value_dict.get(name, 0)

  # ✅ 5. Folium 지도 생성
  m = folium.Map(location=[36.5, 127.5], zoom_start=7)

  folium.Choropleth(
      geo_data=geo_data,
      data=map_df,
      columns=['지역명', '값'],
      key_on='feature.properties.name',
      fill_color='YlOrRd',
      fill_opacity=0.7,
      line_opacity=0.2,
      legend_name='지역별 등록 수'
  ).add_to(m)

  folium.GeoJson(
      geo_data,
      style_function=lambda feature: {
          'fillColor': 'transparent',
          'color': 'transparent',
          'weight': 0,
      },
      tooltip=folium.GeoJsonTooltip(
          fields=['name', 'value'],
          aliases=['지역', '등록 수'],
          localize=True,
          style="""
              font-size: 14px;
              font-weight: bold;
              background-color: white;
              border: 1px solid black;
              border-radius: 3px;
              box-shadow: 3px;
          """
      )
  ).add_to(m)

  # ✅ 6. Streamlit에서 지도 렌더링
  st_folium(m, width=800, height=600)
