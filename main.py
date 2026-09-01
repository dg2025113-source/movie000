import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# 기본 설정
# ==================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)


# ==================================================
# 제목
# ==================================================

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.markdown(
    "1년치 일별 박스오피스 데이터를 이용해 "
    "영화의 시간에 따른 관객 변화를 살펴봅니다."
)


# ==================================================
# 데이터 불러오기
# ==================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


def load_data():

    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜형으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형 데이터 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


try:
    df = load_data()

except Exception as e:

    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(e)
    st.stop()


# ==================================================
# 데이터 정보
# ==================================================

with st.expander("📊 데이터 정보 보기"):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "전체 기록 수",
            f"{len(df):,}개"
        )

    with col2:
        st.metric(
            "영화 수",
            f"{df['영화명'].nunique():,}편"
        )

    with col3:
        st.metric(
            "데이터 기간",
            f"{df['날짜'].min().strftime('%Y-%m-%d')} ~ "
            f"{df['날짜'].max().strftime('%Y-%m-%d')}"
        )


# ==================================================
# 그래프 1
# 영화별 일관객 변화
# ==================================================

st.divider()

st.header("1. 영화별 일관객 변화")

st.markdown(
    "영화를 하나 선택하면 해당 영화의 날짜별 "
    "일관객 변화를 확인할 수 있습니다."
)


movie_list = sorted(
    df["영화명"].dropna().unique()
)

selected_movie = st.selectbox(
    "🎞️ 영화를 선택하세요",
    movie_list
)


movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)


fig1.update_traces(
    hovertemplate=(
        "<b>날짜</b>: %{x|%Y-%m-%d}<br>"
        "<b>일관객</b>: %{y:,}명"
        "<extra></extra>"
    )
)


fig1.update_layout(
    height=500,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)


st.plotly_chart(
    fig1,
    use_container_width=True
)


st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    f"「{selected_movie}」의 일관객이 시간의 흐름에 따라 "
    "어떻게 증가하거나 감소했는지 확인할 수 있습니다."
)


# ==================================================
# 그래프 2
# 일관객 합계 TOP 5 영화 비교
# ==================================================

st.divider()

st.header("2. 일관객 합계 TOP 5 영화")

st.markdown(
    "전체 기간 동안 일관객의 합계가 가장 큰 5편의 "
    "날짜별 일관객 변화를 비교합니다."
)


top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values(
        "일관객",
        ascending=False
    )
    .head(5)
)


top5_df = df[
    df["영화명"].isin(
        top5_movies["영화명"]
    )
].copy()

top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)


fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    title="일관객 합계 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)


fig2.update_traces(
    hovertemplate=(
        "<b>%{fullData.name}</b><br>"
        "<b>날짜</b>: %{x|%Y-%m-%d}<br>"
        "<b>일관객</b>: %{y:,}명"
        "<extra></extra>"
    )
)


fig2.update_layout(
    height=550,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화",
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    "전체 기간의 일관객 합계가 큰 상위 5편의 영화가 "
    "시간에 따라 어떤 관객 추이를 보였는지 비교할 수 있습니다."
)


with st.expander("📊 TOP 5 영화의 기간 내 일관객 합계 보기"):

    top5_display = top5_movies.copy()

    top5_display["일관객"] = (
        top5_display["일관객"]
        .map(lambda x: f"{x:,}명")
    )

    top5_display.columns = [
        "영화명",
        "기간 내 일관객 합계"
    ]

    st.dataframe(
        top5_display,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# 그래프 3
# 날짜별 10위권 일관객 합계
# ==================================================

st.divider()

st.header("3. 날짜별 10위권 일관객 합계")

st.markdown(
    "각 날짜의 박스오피스 10위권 영화들의 일관객을 모두 합산하여 "
    "전체적인 영화 관객 규모의 변화를 확인합니다."
)


daily_audience = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)


top3_days = (
    daily_audience
    .sort_values(
        "일관객",
        ascending=False
    )
    .head(3)
    .sort_values("날짜")
)


fig3 = px.area(
    daily_audience,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)


for _, row in top3_days.iterrows():

    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=(
            f"<b>{row['날짜'].strftime('%Y-%m-%d')}</b><br>"
            f"{row['일관객']:,}명"
        ),
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-60,
        font=dict(
            size=12
        ),
        bgcolor="white",
        bordercolor="gray",
        borderwidth=1,
        borderpad=4
    )


fig3.update_traces(
    hovertemplate=(
        "<b>날짜</b>: %{x|%Y-%m-%d}<br>"
        "<b>10위권 일관객 합계</b>: %{y:,}명"
        "<extra></extra>"
    )
)


fig3.update_layout(
    height=550,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)",
    margin=dict(
        l=20,
        r=20,
        t=80,
        b=20
    )
)


st.plotly_chart(
    fig3,
    use_container_width=True
)


st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    "날짜별 박스오피스 10위권의 일관객 합계를 통해 "
    "전체적인 영화 관객 규모가 시기에 따라 어떻게 변했는지 확인할 수 있습니다."
)


with st.expander("🏆 일관객 합계가 가장 컸던 날 TOP 3"):

    top3_display = top3_days.copy()

    top3_display["날짜"] = (
        top3_display["날짜"]
        .dt.strftime("%Y-%m-%d")
    )

    top3_display["일관객"] = (
        top3_display["일관객"]
        .map(lambda x: f"{x:,}명")
    )

    top3_display.columns = [
        "날짜",
        "10위권 일관객 합계"
    ]

    st.dataframe(
        top3_display,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# 그래프 4
# 영화별 일관객 합계 TOP 10
# ==================================================

st.divider()

st.header("4. 영화별 일관객 합계 TOP 10")

st.markdown(
    "전체 기간 동안 영화별 일관객을 모두 더해 "
    "관객 수가 가장 많은 10편을 비교합니다."
)


# 영화별 일관객 합계와 10위권에 든 날 수 계산
movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        일수=("날짜", "nunique")
    )
    .reset_index()
)


# 일관객 합계 기준 TOP 10
top10_movies = (
    movie_summary
    .sort_values(
        "일관객합계",
        ascending=False
    )
    .head(10)
    .copy()
)


# 관객이 많은 영화가 위에 오도록 역순 정렬
top10_movies = top10_movies.sort_values(
    "일관객합계",
    ascending=True
)


# 가로 막대그래프
fig4 = px.bar(
    top10_movies,
    x="일관객합계",
    y="영화명",
    orientation="h",
    text="일관객합계",
    title="영화별 기간 내 일관객 합계 TOP 10",
    labels={
        "영화명": "영화",
        "일관객합계": "기간 내 일관객 합계"
    },
    custom_data=["일수"]
)


fig4.update_traces(
    texttemplate="%{x:,}명",
    textposition="outside",
    cliponaxis=False,

    hovertemplate=(
        "<b>%{y}</b><br>"
        "<b>일관객 합계</b>: %{x:,}명<br>"
        "<b>10위권에 든 날</b>: %{customdata[0]}일"
        "<extra></extra>"
    )
)


fig4.update_layout(
    height=600,
    xaxis_title="기간 내 일관객 합계(명)",
    yaxis_title="영화",
    margin=dict(
        l=20,
        r=100,
        t=60,
        b=20
    )
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    "전체 기간 동안 누적 일관객이 가장 많았던 영화와 "
    "각 영화가 박스오피스 10위권에 머문 기간을 함께 비교할 수 있습니다."
)


with st.expander("📊 TOP 10 영화 상세 정보 보기"):

    top10_table = (
        top10_movies
        .sort_values(
            "일관객합계",
            ascending=False
        )
        .copy()
    )

    top10_table["일관객합계"] = (
        top10_table["일관객합계"]
        .map(lambda x: f"{x:,}명")
    )

    top10_table["일수"] = (
        top10_table["일수"]
        .map(lambda x: f"{x}일")
    )

    top10_table.columns = [
        "영화명",
        "기간 내 일관객 합계",
        "10위권에 든 날"
    ]

    st.dataframe(
        top10_table,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# 그래프 5
# 월 × 요일별 일관객 평균 히트맵
# ==================================================

st.divider()

st.header("5. 월 × 요일별 일관객 평균")

st.markdown(
    "각 날짜에서 월과 요일을 추출하여, "
    "월별·요일별 하루 평균 일관객을 히트맵으로 나타냅니다."
)


# --------------------------------------------------
# 월과 요일 추출
# --------------------------------------------------

heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month


weekday_map = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일"
}


heatmap_df["요일"] = (
    heatmap_df["날짜"]
    .dt.weekday
    .map(weekday_map)
)


# --------------------------------------------------
# 먼저 날짜별 10위권 일관객 합계 계산
# --------------------------------------------------

daily_heatmap = (
    heatmap_df
    .groupby(
        ["날짜", "월", "요일"],
        as_index=False
    )["일관객"]
    .sum()
)


# --------------------------------------------------
# 월 × 요일별 하루 평균 계산
# --------------------------------------------------

heatmap_data = (
    daily_heatmap
    .groupby(
        ["월", "요일"],
        as_index=False
    )["일관객"]
    .mean()
)


# --------------------------------------------------
# 요일 순서 지정
# --------------------------------------------------

weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]


heatmap_data["요일"] = pd.Categorical(
    heatmap_data["요일"],
    categories=weekday_order,
    ordered=True
)


heatmap_data = heatmap_data.sort_values(
    ["월", "요일"]
)


# --------------------------------------------------
# 히트맵
# --------------------------------------------------

fig5 = px.density_heatmap(
    heatmap_data,
    x="요일",
    y="월",
    z="일관객",
    category_orders={
        "요일": weekday_order,
        "월": list(range(1, 13))
    },
    color_continuous_scale="Blues",
    text_auto=".3s",
    title="월 × 요일별 10위권 일관객 평균",
    labels={
        "요일": "요일",
        "월": "월",
        "일관객": "일평균 일관객"
    }
)


fig5.update_layout(
    height=600,
    xaxis_title="요일",
    yaxis_title="월",
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    ),
    coloraxis_colorbar_title="일평균 일관객"
)


fig5.update_yaxes(
    tickmode="linear",
    dtick=1,
    autorange="reversed"
)


fig5.update_traces(
    hovertemplate=(
        "<b>%{y}월 %{x}</b><br>"
        "<b>일평균 일관객</b>: %{z:,.0f}명"
        "<extra></extra>"
    )
)


st.plotly_chart(
    fig5,
    use_container_width=True
)


# --------------------------------------------------
# 그래프로 알 수 있는 것
# --------------------------------------------------

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    "월과 요일에 따른 하루 평균 관객 규모를 비교하여 "
    "특정 시기와 요일에 영화 관객이 많이 몰리는 경향을 확인할 수 있습니다."
)


# ==================================================
# 그래프 6
# 추가 예정
# ==================================================

st.divider()

st.header("6. 추가 그래프")

st.caption(
    "앞으로 새로운 영화 데이터 그래프를 이곳에 추가할 예정입니다."
)

st.markdown(
    """
    📌 **다음 그래프를 추가할 공간입니다.**

    예: 누적관객 변화 / 스크린 수 변화 / 상영횟수 변화 / 순위 변화
    """
)


# ==================================================
# 마무리
# ==================================================

st.divider()

st.caption(
    "데이터 출처: 영화관입장권통합전산망(KOBIS) "
    "일별 박스오피스 데이터"
)
