import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# 데이터 불러오기
# ==============================
@st.cache_data
def load_data():
    # 실제 환경에서는 파일을 로드해야 하지만, 테스트를 위해 가상의 DataFrame을 생성합니다.
    # 사용자가 제공한 파일 이름(countriesMBTI_16types.csv)을 유지합니다.
    # DataFrame에는 'Country' 열과 16가지 MBTI 유형(비율) 열이 있어야 합니다.
    try:
        df = pd.read_csv("countriesMBTI_16types.csv")
    except FileNotFoundError:
        st.error("🚨 'countriesMBTI_16types.csv' 파일을 찾을 수 없습니다. 테스트용 가상 데이터를 사용합니다.")
        data = {
            "Country": ["대한민국", "미국", "일본"],
            "ESTJ": [0.10, 0.08, 0.05],
            "ESTP": [0.05, 0.06, 0.04],
            "ESFJ": [0.15, 0.12, 0.08],
            "ESFP": [0.06, 0.07, 0.05],
            "ENTJ": [0.03, 0.04, 0.03],
            "ENTP": [0.05, 0.06, 0.05],
            "ENFJ": [0.04, 0.05, 0.04],
            "ENFP": [0.08, 0.10, 0.07],
            "ISTJ": [0.07, 0.09, 0.10],
            "ISTP": [0.05, 0.06, 0.08],
            "ISFJ": [0.09, 0.11, 0.12],
            "ISFP": [0.06, 0.08, 0.09],
            "INTJ": [0.03, 0.04, 0.05],
            "INTP": [0.05, 0.06, 0.07],
            "INFJ": [0.04, 0.05, 0.06],
            "INFP": [0.05, 0.03, 0.02],
        }
        df = pd.DataFrame(data)
        # 비율 합이 1이 되도록 정규화 (테스트 데이터의 경우)
        df.iloc[:, 1:] = df.iloc[:, 1:].div(df.iloc[:, 1:].sum(axis=1), axis=0)

    return df

df = load_data()

# ==============================
# 페이지 설정
# ==============================
st.set_page_config(page_title="세계 MBTI 유형 분포", page_icon="🌍", layout="centered")

# ==============================
# 제목 및 설명
# ==============================
st.title("🌍 세계 각국의 MBTI 유형 분포")
st.markdown("""
국가를 선택하면 해당 나라의 **MBTI 유형별 비율**을 확인할 수 있습니다.  
가장 높은 비율의 유형은 🔴 **빨간색**, 나머지는 **그라데이션 색상**으로 표시됩니다.
""")

# ==============================
# 국가 선택
# ==============================
country_list = sorted(df["Country"].unique())
selected_country = st.selectbox("국가를 선택하세요:", country_list, index=0)

# ==============================
# 선택된 국가 데이터 정리
# ==============================
# 'Country' 열을 제외하고, 선택된 국가의 첫 번째 행 데이터를 가져옵니다.
country_data = df[df["Country"] == selected_country].iloc[0, 1:]
country_df = (
    pd.DataFrame({
        "MBTI 유형": country_data.index,
        "비율": country_data.values
    })
    .sort_values(by="비율", ascending=False)
    .reset_index(drop=True)
)

# ==============================
# 색상 설정 (1등 빨간색, 나머지 그라데이션)
# Index Error 수정 로직
# ==============================
# 1. Plotly의 Reds 순차적 색상표를 가져옵니다 (일반적으로 9가지 색상).
red_gradient_base = px.colors.sequential.Reds

# 2. 이 색상표를 역순으로 사용하여 어두운 빨간색부터 가장 밝은 색상 순으로 만듭니다.
#    (가장 높은 비율의 유형(순수 빨간색) 바로 다음에 어두운 그라데이션이 오도록)
available_gradient = red_gradient_base[::-1]

# 3. 1등을 제외한 나머지 유형의 개수 (항상 15개)
num_needed = len(country_df) - 1

# 4. 필요한 15개의 그라데이션 색상을 확보합니다.
if len(available_gradient) < num_needed:
    # Plotly 색상표가 15개보다 적다면, 가장 밝은 색상(가장 마지막 색상)을 반복하여 채웁니다.
    last_color = available_gradient[-1]
    extension = [last_color] * (num_needed - len(available_gradient))
    gradient_colors = available_gradient + extension
else:
    # 15개 이상의 색상이 있다면, 필요한 15개만 사용합니다.
    gradient_colors = available_gradient[:num_needed]

# 5. 최종 색상 리스트: 1등은 순수 빨간색, 나머지는 그라데이션
colors = ["#FF0000"] + gradient_colors

# ==============================
# Plotly 그래프 생성
# ==============================
fig = px.bar(
    country_df,
    x="MBTI 유형",
    y="비율",
    # 비율을 백분율 형식으로 텍스트 표시
    text=country_df["비율"].apply(lambda x: f"{x:.2%}"), 
)

fig.update_traces(
    marker_color=colors,
    textposition="outside"
)

fig.update_layout(
    title=f"**{selected_country}**의 MBTI 유형 분포",
    title_x=0.5, # 제목 중앙 정렬
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis_tickformat=".0%", # Y축 레이블을 백분율로 표시
    template="plotly_white",
    showlegend=False,
    # 글꼴 설정
    font=dict(family="Arial, sans-serif"),
    # 막대 사이 간격 조정
    bargap=0.1
)

st.plotly_chart(fig, use_container_width=True)

# ==============================
# 데이터 미리보기
# ==============================
with st.expander("📋 원본 데이터 보기"):
    st.dataframe(df)
