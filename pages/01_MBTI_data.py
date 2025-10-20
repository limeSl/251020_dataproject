import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# 데이터 불러오기
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
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
# ==============================
colors = ["#FF0000"] + px.colors.sequential.Reds[len(country_df) - 1][::-1]

# ==============================
# Plotly 그래프 생성
# ==============================
fig = px.bar(
    country_df,
    x="MBTI 유형",
    y="비율",
    text=country_df["비율"].apply(lambda x: f"{x:.2%}"),
)

fig.update_traces(
    marker_color=colors,
    textposition="outside"
)

fig.update_layout(
    title=f"{selected_country}의 MBTI 유형 분포",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (0~1)",
    yaxis_tickformat=".0%",
    template="plotly_white",
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)

# ==============================
# 데이터 미리보기
# ==============================
with st.expander("📋 원본 데이터 보기"):
    st.dataframe(df)
