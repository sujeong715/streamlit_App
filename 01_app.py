import streamlit as st
import requests
import random

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="🍽️ 오늘 뭐 먹지?",
    page_icon="🍓",
    layout="centered"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(180deg,#FFEFF5,#FFF8E7);
}

h1{
    color:#ff4d88;
    text-align:center;
}

h3{
    text-align:center;
}

.menu-box{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0 5px 15px rgba(0,0,0,0.15);
    text-align:center;
}

.info-box{
    background:#FFF4C9;
    padding:20px;
    border-radius:20px;
    font-size:18px;
}

div.stButton > button{
    width:100%;
    height:55px;
    border:none;
    border-radius:20px;
    background:#FF8FAB;
    color:white;
    font-size:20px;
    font-weight:bold;
}

div.stButton > button:hover{
    background:#ff5c8d;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 메뉴 데이터
# -----------------------------
foods = {

    "맑음":[
        {
            "name":"비빔밥",
            "image":"https://images.unsplash.com/photo-1657299156734-8dca2b2f6c6d?w=900",
            "calorie":"580 kcal",
            "nutrition":"탄수화물 72g | 단백질 20g | 지방 18g"
        },
        {
            "name":"냉모밀",
            "image":"https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=900",
            "calorie":"430 kcal",
            "nutrition":"탄수화물 60g | 단백질 16g | 지방 9g"
        }
    ],

    "비":[
        {
            "name":"김치찌개",
            "image":"https://images.unsplash.com/photo-1604908176997-4316b4f6e905?w=900",
            "calorie":"640 kcal",
            "nutrition":"탄수화물 40g | 단백질 35g | 지방 28g"
        },
        {
            "name":"칼국수",
            "image":"https://images.unsplash.com/photo-1555126634-323283e090fa?w=900",
            "calorie":"590 kcal",
            "nutrition":"탄수화물 80g | 단백질 18g | 지방 14g"
        }
    ],

    "눈":[
        {
            "name":"떡국",
            "image":"https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=900",
            "calorie":"520 kcal",
            "nutrition":"탄수화물 68g | 단백질 21g | 지방 12g"
        },
        {
            "name":"전골",
            "image":"https://images.unsplash.com/photo-1512058564366-18510be2db19?w=900",
            "calorie":"610 kcal",
            "nutrition":"탄수화물 32g | 단백질 38g | 지방 30g"
        }
    ],

    "더움":[
        {
            "name":"냉면",
            "image":"https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=900",
            "calorie":"470 kcal",
            "nutrition":"탄수화물 70g | 단백질 17g | 지방 7g"
        },
        {
            "name":"초밥",
            "image":"https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=900",
            "calorie":"510 kcal",
            "nutrition":"탄수화물 55g | 단백질 28g | 지방 12g"
        }
    ],

    "추움":[
        {
            "name":"삼계탕",
            "image":"https://images.unsplash.com/photo-1600891964599-f61ba0e24092?w=900",
            "calorie":"760 kcal",
            "nutrition":"탄수화물 25g | 단백질 45g | 지방 38g"
        },
        {
            "name":"부대찌개",
            "image":"https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?w=900",
            "calorie":"700 kcal",
            "nutrition":"탄수화물 35g | 단백질 42g | 지방 35g"
        }
    ]

}

# -----------------------------
# 서울 날씨 가져오기
# -----------------------------
API_KEY = st.secrets["OPENWEATHER_API_KEY"]

def get_seoul_weather():

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q=Seoul&appid={API_KEY}&units=metric&lang=kr"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None, None

    data = response.json()

    weather = data["weather"][0]["main"]
    temp = data["main"]["temp"]

    if weather == "Rain":
        weather_type = "비"

    elif weather == "Snow":
        weather_type = "눈"

    elif temp >= 28:
        weather_type = "더움"

    elif temp <= 10:
        weather_type = "추움"

    else:
        weather_type = "맑음"

    return weather_type, temp


# -----------------------------
# 화면
# -----------------------------
st.title("🍓 오늘 뭐 먹지?")
st.write("서울의 현재 날씨를 분석하여 메뉴를 추천합니다!")

weather, temp = get_seoul_weather()

if weather is None:
    st.error("날씨 정보를 가져오지 못했습니다.")
    st.stop()

st.success(f"📍 서울 현재 기온 : {temp:.1f}℃")
st.info(f"🌤️ 추천 기준 날씨 : {weather}")

if st.button("🍽️ 메뉴 추천받기"):

    menu = random.choice(foods[weather])

    st.image(menu["image"], use_container_width=True)

    st.markdown(
        f"""
        <div class="menu-box">
            <h2>{menu['name']}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="info-box">

        🔥 <b>칼로리</b><br>
        {menu['calorie']}

        <br><br>

        🥗 <b>영양소</b><br>
        {menu['nutrition']}

        </div>
        """,
        unsafe_allow_html=True
    )

    st.balloons()
