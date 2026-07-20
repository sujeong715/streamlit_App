youtube-comment-analyzer/
│
├── app.py
├── youtube.py
├── analysis.py
├── wordcloud_util.py
├── requirements.txt
│
├── assets/
│   └── NanumGothic.ttf
│
└── .streamlit/
    └── secrets.toml

  import streamlit as st
import pandas as pd
import plotly.express as px
from youtube import get_video_id, get_video_info, get_comments
from analysis import analyze_sentiment, prepare_timeline
from wordcloud_util import generate_wordcloud

st.set_page_config(
    page_title="유튜브 댓글 분석기",
    page_icon="📊",
    layout="wide"
)

st.title("📊 유튜브 댓글 분석기")
st.markdown("유튜브 링크를 입력하면 댓글을 분석합니다.")

# secrets에서 API 키 읽기
API_KEY = st.secrets["YOUTUBE_API_KEY"]

url = st.text_input(
    "유튜브 링크",
    placeholder="https://www.youtube.com/watch?v=..."
)

comment_count = st.slider(
    "수집할 댓글 개수",
    min_value=100,
    max_value=5000,
    value=500,
    step=100
)

if st.button("분석 시작"):

    if not url:
        st.error("유튜브 링크를 입력하세요.")
        st.stop()

    try:
        video_id = get_video_id(url)

        st.subheader("🎬 영상")
        st.video(url)

        with st.spinner("영상 정보 가져오는 중..."):
            video_info = get_video_info(video_id, API_KEY)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("조회수", f"{video_info['viewCount']:,}")

        with col2:
            st.metric("좋아요", f"{video_info['likeCount']:,}")

        with col3:
            st.metric("댓글 수", f"{video_info['commentCount']:,}")

        progress = st.progress(0)

        with st.spinner("댓글 수집 중..."):
            comments_df = get_comments(
                video_id,
                API_KEY,
                comment_count,
                progress
            )

        st.success(f"{len(comments_df)}개 댓글 수집 완료")

        st.subheader("📄 댓글 데이터")

        st.dataframe(
            comments_df[
                ["author", "publishedAt", "likeCount", "text"]
            ].head(100)
        )

        csv = comments_df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "CSV 다운로드",
            csv,
            file_name="youtube_comments.csv",
            mime="text/csv"
        )

        st.divider()

        st.subheader("📈 시간대별 댓글 작성 추이")

        timeline_df = prepare_timeline(comments_df)

        fig = px.line(
            timeline_df,
            x="date",
            y="count",
            markers=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        st.subheader("😊 댓글 감성 분석")

        sentiment_df, sentiment_count = analyze_sentiment(
            comments_df
        )

        fig2 = px.pie(
            values=sentiment_count.values(),
            names=sentiment_count.keys(),
            hole=0.4
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.dataframe(
            sentiment_df[
                ["text", "sentiment"]
            ].head(100)
        )

        st.divider()

        st.subheader("☁️ 한글 워드클라우드")

        wc_img = generate_wordcloud(
            comments_df["text"].tolist()
        )

        st.image(
            wc_img,
            use_container_width=True
        )

    except Exception as e:
        st.error(f"오류 발생: {e}")

  import re
import pandas as pd
import streamlit as st

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


@st.cache_resource
def youtube_client(api_key):
    return build(
        "youtube",
        "v3",
        developerKey=api_key
    )


def get_video_id(url):

    patterns = [
        r"v=([^&]+)",
        r"youtu\.be/([^?]+)",
        r"shorts/([^?]+)"
    ]

    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)

    raise Exception("유튜브 URL을 확인하세요.")


def get_video_info(video_id, api_key):

    youtube = youtube_client(api_key)

    request = youtube.videos().list(
        part="statistics,snippet",
        id=video_id
    )

    response = request.execute()

    if len(response["items"]) == 0:
        raise Exception("영상을 찾을 수 없습니다.")

    item = response["items"][0]

    stat = item["statistics"]

    return {
        "title": item["snippet"]["title"],
        "viewCount": int(stat.get("viewCount", 0)),
        "likeCount": int(stat.get("likeCount", 0)),
        "commentCount": int(stat.get("commentCount", 0))
    }


def get_comments(video_id,
                 api_key,
                 max_comments,
                 progress):

    youtube = youtube_client(api_key)

    comments = []

    next_page = None

    while len(comments) < max_comments:

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page,
            textFormat="plainText",
            order="relevance"
        )

        try:
            response = request.execute()

        except HttpError:
            raise Exception("댓글이 비활성화된 영상입니다.")

        items = response.get("items", [])

        if len(items) == 0:
            break

        for item in items:

            c = item["snippet"]["topLevelComment"]["snippet"]

            comments.append({

                "author": c["authorDisplayName"],

                "text": c["textDisplay"],

                "publishedAt": c["publishedAt"],

                "likeCount": c["likeCount"]

            })

            if len(comments) >= max_comments:
                break

        progress.progress(
            min(len(comments) / max_comments, 1.0)
        )

        next_page = response.get("nextPageToken")

        if next_page is None:
            break

    df = pd.DataFrame(comments)

    df["publishedAt"] = pd.to_datetime(df["publishedAt"])

    return df

google-api-python-client
pandas
streamlit
plotly
