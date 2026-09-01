import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# 제목
# --------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown(
    """
    **1년치 일별 박스오피스 데이터를 이용해 영화의 시간에 따른 관객 변화를 살펴봅니다.**
    """
)


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 실제 날짜형으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형 열 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# 데이터 기본 정보
# --------------------------------------------------
with st.expander("📊 데이터 정보 보기"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("전체 기록 수", f"{len(df):,}개")

    with col2:
        st.metric("영화 수", f"{df['영화명'].nunique():,}편")

    with col3:
        st.metric(
            "데이터 기간",
            f"{df['날짜'].min().strftime('%Y-%m-%d')} ~ "
            f"{df['날짜'].max().strftime('%Y-%m-%d')}"
        )


# ==================================================
# 그래프 1. 영화별 일관객 변화
# ==================================================
st.divider()
st.header("1. 영화별 일관객 변화")
st.markdown(
    "영화를 하나 선택하면 해당 영화의 날짜별 일관객 변화를 확인할 수 있습니다."
)


# 영화 목록 정렬
movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "🎞️ 영화를 선택하세요",
    movie_list
)


# 선택한 영화 데이터
movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")


# 그래프
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,",
        "순위": True,
        "스크린수": ":,",
        "상영횟수": ":,"
    }
)

fig.update_traces(
    hovertemplate=(
        "<b>날짜</b>: %{x|%Y-%m-%d}<br>"
        "<b>일관객</b>: %{y:,}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    height=500,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# 그래프로 알 수 있는 것
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    f"「{selected_movie}」의 일관객이 시간의 흐름에 따라 어떻게 증가하거나 감소했는지 확인할 수 있습니다."
)


# ==================================================
# 앞으로 추가할 그래프 영역
# ==================================================
st.divider()
st.header("2. 추가 그래프")
st.caption("앞으로 새로운 영화 데이터 그래프를 이곳에 추가할 예정입니다.")

st.markdown(
    """
    > 📌 **다음 그래프를 추가할 수 있는 공간입니다.**
    >
    > 예: 누적관객 변화 / 스크린 수 변화 / 상영횟수 변화 / 순위 변화 등
    """
)


st.divider()
st.header("3. 추가 그래프")
st.caption("새로운 분석 그래프를 추가할 수 있는 공간입니다.")


# --------------------------------------------------
# 하단
# --------------------------------------------------
st.divider()

st.caption(
    "데이터 출처: 영화관입장권통합전산망(KOBIS) 일별 박스오피스 데이터"
)
