youtube-comment-analyzer/

│ app.py
│ requirements.txt
│ README.md
│
├── font/
│      NanumGothic.ttf
│
└── .streamlit/
       secrets.toml
streamlit
google-api-python-client
pandas
numpy
plotly
wordcloud
matplotlib
Pillow
konlpy
API_KEY = st.secrets["YOUTUBE_API_KEY"]
import streamlit as st
import pandas as pd
import plotly.express as px

from googleapiclient.discovery import build

st.set_page_config(
    page_title="유튜브 댓글 분석기",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 유튜브 댓글 분석기")

st.write(
    "유튜브 영상의 댓글을 분석하여 "
    "시간대별 추이, 반응도, 워드클라우드를 제공합니다."
)

# -----------------------------
# API Key
# -----------------------------
API_KEY = st.secrets["YOUTUBE_API_KEY"]

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

# -----------------------------
# 입력
# -----------------------------
url = st.text_input(
    "유튜브 영상 URL"
)

comment_count = st.slider(
    "가져올 댓글 개수",
    min_value=100,
    max_value=1000,
    step=100,
    value=300
)

analyze = st.button("댓글 분석 시작", use_container_width=True)

# -----------------------------
# 영상 표시
# -----------------------------
if url:

    st.video(url)

# -----------------------------
# 버튼 클릭
# -----------------------------
if analyze:

    if url == "":
        st.warning("유튜브 URL을 입력하세요.")
        st.stop()

    st.info("다음 단계에서 댓글을 수집합니다.")
import re
from urllib.parse import urlparse, parse_qs
def get_video_id(url):
    """
    일반 유튜브 URL, Shorts, youtu.be 링크 모두 지원
    """

    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]

    if "shorts/" in url:
        return url.split("shorts/")[1].split("?")[0]

    query = urlparse(url)

    if query.hostname in [
        "www.youtube.com",
        "youtube.com",
        "m.youtube.com"
    ]:
        return parse_qs(query.query).get("v", [None])[0]

    return None
    @st.cache_data(show_spinner=False)
def get_comments(video_id, max_comments):

    comments = []

    next_page = None

    while len(comments) < max_comments:

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page,
            textFormat="plainText",
            order="time"
        )

        response = request.execute()

        for item in response["items"]:

            comment = item["snippet"]["topLevelComment"]["snippet"]

            comments.append({
                "작성시간": comment["publishedAt"],
                "작성자": comment["authorDisplayName"],
                "댓글": comment["textDisplay"],
                "좋아요": comment["likeCount"]
            })

            if len(comments) >= max_comments:
                break

        next_page = response.get("nextPageToken")

        if next_page is None:
            break

    return pd.DataFrame(comments)
    video_id = get_video_id(url)

if video_id is None:
    st.error("올바른 유튜브 URL이 아닙니다.")
    st.stop()

with st.spinner("댓글을 수집하는 중..."):

    df = get_comments(video_id, comment_count)

if len(df) == 0:
    st.warning("댓글이 없습니다.")
    st.stop()

st.success(f"{len(df)}개의 댓글을 수집했습니다.")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)
from datetime import timedelta
# UTC → 한국시간(KST)

df["작성시간"] = pd.to_datetime(df["작성시간"], utc=True)

df["작성시간"] = df["작성시간"] + timedelta(hours=9)

df["날짜"] = df["작성시간"].dt.date

df["시간"] = df["작성시간"].dt.hour

df["요일"] = df["작성시간"].dt.day_name()
hour_df = (
    df.groupby("시간")
      .size()
      .reset_index(name="댓글수")
)

hour_df = hour_df.sort_values("시간")
date_df = (
    df.groupby("날짜")
      .size()
      .reset_index(name="댓글수")
)
st.subheader("🕒 시간대별 댓글 작성 추이")

fig = px.bar(
    hour_df,
    x="시간",
    y="댓글수",
    text="댓글수"
)

fig.update_layout(
    xaxis_title="시간",
    yaxis_title="댓글 개수",
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader("📅 날짜별 댓글 작성 추이")

fig2 = px.line(
    date_df,
    x="날짜",
    y="댓글수",
    markers=True
)

fig2.update_layout(height=450)

st.plotly_chart(
    fig2,
    use_container_width=True
)
col1, col2, col3 = st.columns(3)

col1.metric(
    "총 댓글",
    len(df)
)

col2.metric(
    "평균 좋아요",
    round(df["좋아요"].mean(), 1)
)

peak = hour_df.loc[
    hour_df["댓글수"].idxmax(),
    "시간"
]

col3.metric(
    "댓글 최다 시간",
    f"{peak}시"
)
# 댓글 길이

df["댓글길이"] = df["댓글"].astype(str).str.len()
st.subheader("👍 댓글 반응도")

c1, c2, c3 = st.columns(3)

c1.metric(
    "평균 좋아요",
    round(df["좋아요"].mean(), 2)
)

c2.metric(
    "최대 좋아요",
    int(df["좋아요"].max())
)

c3.metric(
    "좋아요 총합",
    int(df["좋아요"].sum())
)
top_comments = (
    df.sort_values("좋아요", ascending=False)
      .head(20)
)

st.subheader("🏆 좋아요 TOP 20 댓글")

st.dataframe(
    top_comments[
        ["좋아요", "작성자", "댓글"]
    ],
    use_container_width=True
)
fig = px.histogram(
    df,
    x="좋아요",
    nbins=30,
    title="좋아요 분포"
)

fig.update_layout(
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)
fig = px.scatter(
    df,
    x="댓글길이",
    y="좋아요",
    hover_data=["작성자"]
)

fig.update_layout(
    title="댓글 길이와 좋아요의 관계",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)
best = df.sort_values(
    "좋아요",
    ascending=False
).iloc[0]

st.subheader("🌟 가장 반응이 좋은 댓글")

st.success(
    f"""
👤 작성자 : {best['작성자']}

👍 좋아요 : {best['좋아요']}

💬 댓글

{best['댓글']}
"""
)
author = (
    df.groupby("작성자")
      .size()
      .reset_index(name="댓글수")
      .sort_values("댓글수", ascending=False)
      .head(10)
)

fig = px.bar(
    author,
    x="작성자",
    y="댓글수",
    text="댓글수",
    title="댓글을 많이 작성한 사용자"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
