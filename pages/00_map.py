# You can use korean ttile

import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광지도", layout="wide")

st.title("🌏 외국인들이 좋아하는 서울의 주요 관광지 Top 10")
st.markdown("서울을 찾는 외국인 관광객들이 자주 찾는 명소 10곳을 지도에 표시했습니다!")

# 관광지 데이터
places = [
    {"name": "경복궁", "lat": 37.579617, "lon": 126.977041, "desc": "조선의 대표 궁궐 🇰🇷"},
    {"name": "명동거리", "lat": 37.563757, "lon": 126.982684, "desc": "쇼핑과 길거리 음식의 천국 🛍️"},
    {"name": "남산타워 (N서울타워)", "lat": 37.551169, "lon": 126.988227, "desc": "서울의 랜드마크 전망대 🗼"},
    {"name": "북촌한옥마을", "lat": 37.582604, "lon": 126.983998, "desc": "전통과 현대가 공존하는 한옥마을 🏡"},
    {"name": "홍대거리", "lat": 37.556327, "lon": 126.922651, "desc": "젊음과 예술의 거리 🎶"},
    {"name": "동대문디자인플라자(DDP)", "lat": 37.566478, "lon": 127.009105, "desc": "미래적인 디자인의 명소 💡"},
    {"name": "잠실 롯데월드타워", "lat": 37.513068, "lon": 127.102494, "desc": "서울의 초고층 타워 🏙️"},
    {"name": "이태원", "lat": 37.534855, "lon": 126.994322, "desc": "다문화와 음식의 중심 🍽️"},
    {"name": "청계천", "lat": 37.569012, "lon": 126.978388, "desc": "도심 속 휴식 공간 🌿"},
    {"name": "한강공원 (여의도)", "lat": 37.528601, "lon": 126.934174, "desc": "서울의 여유를 느낄 수 있는 강변 🏞️"},
]

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 표시
for place in places:
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=f"<b>{place['name']}</b><br>{place['desc']}",
        tooltip=place["name"],
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)

# 지도 표시
st_folium(m, width=900, height=600)
