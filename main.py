# ==================================================
# 그래프 2. 일관객 합계 TOP 5 영화 비교
# ==================================================
st.divider()
st.header("2. 일관객 합계 TOP 5 영화")
st.markdown(
    "전체 기간 동안 일관객의 합계가 가장 큰 5편의 날짜별 관객 변화를 비교합니다."
)


# 영화별 일관객 합계 계산
top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)
)


# TOP 5 영화만 추출
top5_df = df[df["영화명"].isin(top5_movies["영화명"])].copy()
top5_df = top5_df.sort_values(["날짜", "영화명"])


# Plotly 선 그래프
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=False,
    title="일관객 합계 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,",
        "영화명": True
    }
)


# 마우스를 올렸을 때 표시되는 정보
fig2.update_traces(
    hovertemplate=(
        "<b>%{fullData.name}</b><br>"
        "<b>날짜</b>: %{x|%Y-%m-%d}<br>"
        "<b>일관객</b>: %{y:,}명"
        "<extra></extra>"
    )
)


# 범례 클릭으로 영화 켜기/끄기
fig2.update_layout(
    height=550,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화",
    margin=dict(l=20, r=20, t=60, b=20)
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# 그래프로 알 수 있는 것
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "전체 기간의 일관객 합계가 큰 상위 5편의 영화가 시간에 따라 "
    "어떻게 다른 관객 추이를 보였는지 비교할 수 있습니다."
)


# TOP 5 영화의 누적 일관객 합계
with st.expander("📊 TOP 5 영화의 기간 내 일관객 합계 보기"):
    top5_display = top5_movies.copy()
    top5_display["일관객"] = top5_display["일관객"].map(lambda x: f"{x:,}명")
    top5_display.columns = ["영화명", "기간 내 일관객 합계"]

    st.dataframe(
        top5_display,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# 그래프 3. 추가 예정
# ==================================================
st.divider()
st.header("3. 추가 그래프")
st.caption("새로운 분석 그래프를 이곳에 추가할 예정입니다.")
