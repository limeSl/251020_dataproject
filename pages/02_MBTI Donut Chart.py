import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==============================
# 데이터 불러오기 및 캐싱
# ==============================
@st.cache_data
def load_data():
    """CSV 파일을 불러오거나, 파일이 없을 경우 테스트용 더미 데이터를 생성합니다."""
    try:
        df = pd.read_csv("countriesMBTI_16types.csv")
        # 데이터 유효성 검사 (MBTI 16개 유형 컬럼이 있는지 확인)
        mbti_types = ['ESTJ', 'ESTP', 'ESFJ', 'ESFP', 'ENTJ', 'ENTP', 'ENFJ', 'ENFP', 
                      'ISTJ', 'ISTP', 'ISFJ', 'ISFP', 'INTJ', 'INTP', 'INFJ', 'INFP']
        
        # 실제 데이터의 컬럼과 MBTI 유형 리스트를 비교하여 누락된 컬럼 처리
        if not all(col in df.columns for col in mbti_types):
             raise ValueError("CSV 파일에 16가지 MBTI 유형 중 일부가 누락되었습니다.")
        
        return df

    except (FileNotFoundError, ValueError) as e:
        st.warning(f"🚨 {e}. 테스트용 가상 데이터를 사용합니다.")
        
        # 파일이 없거나 컬럼이 부족할 경우 사용할 가상 데이터
        data = {
            "Country": ["대한민국", "미국", "일본", "독일", "브라질"],
            "ESTJ": [0.10, 0.08, 0.05, 0.09, 0.07], "ESTP": [0.05, 0.06, 0.04, 0.05, 0.06],
            "ESFJ": [0.15, 0.12, 0.08, 0.11, 0.13], "ESFP": [0.06, 0.07, 0.05, 0.06, 0.08],
            "ENTJ": [0.03, 0.04, 0.03, 0.05, 0.03], "ENTP": [0.05, 0.06, 0.05, 0.07, 0.06],
            "ENFJ": [0.04, 0.05, 0.04, 0.06, 0.05], "ENFP": [0.08, 0.10, 0.07, 0.09, 0.11],
            "ISTJ": [0.07, 0.09, 0.10, 0.08, 0.06], "ISTP": [0.05, 0.06, 0.08, 0.04, 0.05],
            "ISFJ": [0.09, 0.11, 0.12, 0.10, 0.09], "ISFP": [0.06, 0.08, 0.09, 0.07, 0.06],
            "INTJ": [0.03, 0.04, 0.05, 0.03, 0.04], "INTP": [0.05, 0.06, 0.07, 0.05, 0.06],
            "INFJ": [0.04, 0.05, 0.06, 0.04, 0.05], "INFP": [0.05, 0.03, 0.02, 0.01, 0.02],
        }
        temp_df = pd.DataFrame(data)
        # 비율 합이 1이 되도록 정규화
        temp_df.iloc[:, 1:] = temp_df.iloc[:, 1:].div(temp_df.iloc[:, 1:].sum(axis=1), axis=0)
        return temp_df

df = load_data()

# ==============================
# MBTI 축별 비율 계산 함수
# ==============================
def calculate_dichotomy_ratios(df, selected_country):
    """선택된 국가의 16가지 유형 비율을 4가지 축의 비율로 계산합니다."""
    
    country_data = df[df["Country"] == selected_country].iloc[0, 1:]
    
    # 1. 외향(E) vs 내향(I)
    E_types = [col for col in country_data.index if col.startswith(('E'))]
    I_types = [col for col in country_data.index if col.startswith(('I'))]
    E_ratio = country_data[E_types].sum()
    I_ratio = country_data[I_types].sum()
    
    # 2. 감각(S) vs 직관(N)
    S_types = [col for col in country_data.index if col[1] == 'S']
    N_types = [col for col in country_data.index if col[1] == 'N']
    S_ratio = country_data[S_types].sum()
    N_ratio = country_data[N_types].sum()
    
    # 3. 사고(T) vs 감정(F)
    T_types = [col for col in country_data.index if col[2] == 'T']
    F_types = [col for col in country_data.index if col[2] == 'F']
    T_ratio = country_data[T_types].sum()
    F_ratio = country_data[F_types].sum()

    # 4. 판단(J) vs 인식(P)
    J_types = [col for col in country_data.index if col.endswith(('J'))]
    P_types = [col for col in country_data.index if col.endswith(('P'))]
    J_ratio = country_data[J_types].sum()
    P_ratio = country_data[P_types].sum()

    results = {
        'E/I': {'E': E_ratio, 'I': I_ratio},
        'S/N': {'S': S_ratio, 'N': N_ratio},
        'T/F': {'T': T_ratio, 'F': F_ratio},
        'J/P': {'J': J_ratio, 'P': P_ratio},
    }
    
    return results

# ==============================
# 시각화 함수 (도넛 차트)
# ==============================
def plot_dichotomy_chart(dichotomy_ratios, country_name):
    """4가지 축의 비율을 도넛 차트로 시각화합니다."""
    
    titles = [
        "에너지 축 (E vs I)",
        "인식 축 (S vs N)",
        "판단 축 (T vs F)",
        "생활 양식 축 (J vs P)"
    ]
    
    # Plotly Subplots 생성 (2x2 그리드)
    fig = make_subplots(
        rows=2, 
        cols=2, 
        specs=[[{'type':'domain'}, {'type':'domain'}], 
               [{'type':'domain'}, {'type':'domain'}]], 
        subplot_titles=titles
    )

    # 각 축별 색상 팔레트 정의 (가독성 및 대비 고려)
    color_map = {
        'E': '#F07167', 'I': '#00B2CA',  # E: 밝은 주황/빨강, I: 청록색
        'S': '#6930C3', 'N': '#FFC300',  # S: 보라색, N: 밝은 노랑
        'T': '#0096C7', 'F': '#FF884B',  # T: 파란색, F: 살구색
        'J': '#1A759F', 'P': '#A9E5BB'   # J: 진한 청색, P: 연한 녹색
    }
    
    # Subplot에 도넛 차트 추가
    dichotomy_keys = list(dichotomy_ratios.keys())
    
    for i, (key, ratios) in enumerate(dichotomy_ratios.items()):
        row = i // 2 + 1
        col = i % 2 + 1
        
        labels = list(ratios.keys())
        values = list(ratios.values())
        colors = [color_map[label] for label in labels]

        fig.add_trace(go.Pie(
            labels=labels, 
            values=values, 
            name=key,
            hole=.3, # 도넛 차트 설정
            marker=dict(colors=colors),
            hovertemplate = "<b>%{label}</b>: %{value:.1%}<extra></extra>", # 호버 텍스트 포맷
            textinfo='label+percent', # 차트 내부에 라벨과 비율 표시
            textposition='inside'
        ), row=row, col=col)

    # 레이아웃 업데이트
    fig.update_layout(
        title_text=f"**{country_name}**의 MBTI 4가지 축 선호도 분석",
        title_x=0.5,
        height=700,
        font=dict(family="Arial, sans-serif", size=14),
        margin=dict(t=80, b=20, l=20, r=20)
    )
    
    # Subplot 제목 스타일 조정
    fig.update_annotations(font_size=16)

    return fig

# ==============================
# Streamlit 페이지 구성
# ==============================
st.set_page_config(page_title="MBTI 4분할 분석", page_icon="📊", layout="wide")

st.title("📊 MBTI 4분할 축 선호도 비교 분석")
st.markdown("""
이 페이지에서는 **선택한 국가의 MBTI 16가지 유형 비율**을 바탕으로,  
**4가지 MBTI 축(E/I, S/N, T/F, J/P)** 각각의 선호도 비율을 분석합니다.
""")

# ==============================
# 사이드바: 국가 선택
# ==============================
with st.sidebar:
    st.header("설정")
    country_list = sorted(df["Country"].unique())
    selected_country = st.selectbox(
        "분석할 국가를 선택하세요:", 
        country_list, 
        index=country_list.index("대한민국") if "대한민국" in country_list else 0
    )

# ==============================
# 메인 컨텐츠: 분석 결과 표시
# ==============================
if selected_country:
    st.header(f"⭐ {selected_country} - MBTI 축 선호도 비율")
    
    # 1. 비율 계산
    dichotomy_ratios = calculate_dichotomy_ratios(df, selected_country)
    
    # 2. 시각화
    fig = plot_dichotomy_chart(dichotomy_ratios, selected_country)
    st.plotly_chart(fig, use_container_width=True)
    
    # 3. 분석 결과 요약 텍스트
    st.subheader("💡 분석 요약")
    
    analysis_markdown = []
    
    # E/I 분석
    E_ratio = dichotomy_ratios['E/I']['E']
    I_ratio = dichotomy_ratios['E/I']['I']
    dominant_EI = '외향(E)' if E_ratio > I_ratio else '내향(I)'
    analysis_markdown.append(f"- **에너지 축 (E/I):** 이 국가는 **{dominant_EI}** 성향이 약 {abs(E_ratio - I_ratio) * 100:.1f}%p 더 높게 나타났습니다. 이는 국민들이 에너지를 어디에서 얻는지를 보여줍니다.")

    # S/N 분석
    S_ratio = dichotomy_ratios['S/N']['S']
    N_ratio = dichotomy_ratios['S/N']['N']
    dominant_SN = '감각(S)' if S_ratio > N_ratio else '직관(N)'
    analysis_markdown.append(f"- **인식 축 (S/N):** **{dominant_SN}** 성향이 약 {abs(S_ratio - N_ratio) * 100:.1f}%p 더 지배적입니다. 이는 정보를 인식하는 방식(사실 vs 가능성)의 차이를 나타냅니다.")

    # T/F 분석
    T_ratio = dichotomy_ratios['T/F']['T']
    F_ratio = dichotomy_ratios['T/F']['F']
    dominant_TF = '사고(T)' if T_ratio > F_ratio else '감정(F)'
    analysis_markdown.append(f"- **판단 축 (T/F):** **{dominant_TF}** 성향이 약 {abs(T_ratio - F_ratio) * 100:.1f}%p 더 강합니다. 이는 결정을 내릴 때 논리/객관성(T)을 중시하는지, 가치/관계(F)를 중시하는지를 보여줍니다.")

    # J/P 분석
    J_ratio = dichotomy_ratios['J/P']['J']
    P_ratio = dichotomy_ratios['J/P']['P']
    dominant_JP = '판단(J)' if J_ratio > P_ratio else '인식(P)'
    analysis_markdown.append(f"- **생활 양식 축 (J/P):** **{dominant_JP}** 성향이 약 {abs(J_ratio - P_ratio) * 100:.1f}%p 더 높습니다. 이는 삶의 패턴이 계획적이고 체계적(J)인지, 유연하고 개방적(P)인지를 반영합니다.")

    st.markdown("\n".join(analysis_markdown))

    # 데이터프레임 미리보기
    with st.expander("📋 계산된 비율 데이터 보기"):
        st.dataframe(pd.DataFrame(dichotomy_ratios).T.style.format("{:.2%}"))
