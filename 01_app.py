import streamlit as st
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
# CSS (귀여운 디자인)
# -----------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(180deg,#FFEFF5,#FFF8E7);
}

h1{
    text-align:center;
    color:#ff5c8d;
}

.menu-box{
    background:white;
    padding:20px;
    border-radius:25px;
    box-shadow:0px 6px 15px rgba(0,0,0,0.15);
    text-align:center;
}

.info-box{
    background:#FFF3CD;
    padding:15px;
    border-radius:15px;
    font-size:18px;
}

div.stButton>button{
    background:#FF8FAB;
    color:white;
    border-radius:20px;
    height:55px;
    width:100%;
    font-size:20px;
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
# 제목
# -----------------------------

st.title("🍓 오늘 뭐 먹지?")

st.write("🌈 날씨에 맞는 메뉴를 추천해드려요!")

weather = st.selectbox(
    "오늘의 날씨를 선택하세요",
    ["맑음","비","눈","더움","추움"]
)

if st.button("🍽️ 메뉴 추천받기"):

    menu = random.choice(foods[weather])

    st.image(menu["image"], use_container_width=True)

    st.markdown(
        f"""
        <div class="menu-box">

        <h2>💖 {menu["name"]}</h2>

        </div>

        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="info-box">

        🔥 <b>칼로리</b><br>
        {menu["calorie"]}

        <br><br>

        🥗 <b>영양소</b><br>
        {menu["nutrition"]}

        </div>
        """,
        unsafe_allow_html=True
    )

    st.balloons()
