import streamlit as st
import pandas as pd
import requests

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# ============================================================
# 1. 페이지 설정
# ============================================================

st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🍿",
    layout="wide"
)


# ============================================================
# 2. CSS 디자인
# ============================================================
# CSS는 한 번에 넣어 HTML 코드가 화면에 그대로 보이는 문제를 줄인다.

st.markdown("""
<style>

/* ==========================================================
   전체 배경
   ========================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            #6a1f47 0%,
            #35152d 28%,
            #1c0e1a 55%,
            #090609 100%
        );
}


/* 전체 콘텐츠 너비 */

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ==========================================================
   상단 CINEMA 제목
   ========================================================== */

.cinema-header {
    text-align: center;
    padding: 15px 10px 20px 10px;
}

.popcorn-logo {
    font-size: 72px;
    line-height: 1;
    margin-bottom: 10px;
}

.main-title {
    font-size: clamp(38px, 6vw, 65px);
    font-weight: 900;
    color: #FFD166;
    letter-spacing: 2px;

    text-shadow:
        0 0 8px rgba(255, 209, 102, 0.7),
        0 0 25px rgba(255, 209, 102, 0.25),
        4px 4px 0 #9D2941;
}

.main-subtitle {
    margin-top: 12px;

    font-size: 18px;
    font-weight: 600;

    color: #F5D8C3;
}


/* ==========================================================
   날짜 표시
   ========================================================== */

.date-ticket {
    width: fit-content;

    margin:
        5px auto
        35px auto;

    padding:
        11px 28px;

    background: #351528;

    color: #FFD166;

    border:
        2px solid #FFD166;

    border-radius: 50px;

    font-size: 16px;
    font-weight: 800;

    box-shadow:
        0 0 18px
        rgba(255, 209, 102, 0.15);
}


/* ==========================================================
   섹션 제목
   ========================================================== */

.section-title {

    margin-top: 35px;
    margin-bottom: 15px;

    font-size: 27px;
    font-weight: 900;

    color: #FFD166;

    text-shadow:
        0 0 10px
        rgba(255, 209, 102, 0.2);
}


/* ==========================================================
   GOLDEN TICKET
   ========================================================== */

.golden-ticket {

    position: relative;

    background:
        linear-gradient(
            135deg,
            #FFF8DF 0%,
            #FFE9AF 50%,
            #FFD98A 100%
        );

    border:
        4px dashed #C23B50;

    border-radius: 28px;

    padding:
        38px 30px;

    margin:
        15px 0
        28px 0;

    box-shadow:
        0 18px 45px
        rgba(0,0,0,0.45);

    text-align: center;

    overflow: hidden;
}


/* 티켓 왼쪽 구멍 */

.golden-ticket::before {

    content: "";

    position: absolute;

    width: 36px;
    height: 36px;

    background: #1c0e1a;

    border-radius: 50%;

    left: -20px;

    top: 50%;

    transform:
        translateY(-50%);
}


/* 티켓 오른쪽 구멍 */

.golden-ticket::after {

    content: "";

    position: absolute;

    width: 36px;
    height: 36px;

    background: #1c0e1a;

    border-radius: 50%;

    right: -20px;

    top: 50%;

    transform:
        translateY(-50%);
}


/* GOLDEN TICKET 작은 글씨 */

.golden-label {

    color: #A92943;

    font-size: 16px;
    font-weight: 900;

    letter-spacing: 4px;

    margin-bottom: 15px;
}


/* ⭐ 영화 제목 - 크게 수정 */

.golden-movie-title {

    color: #35191D;

    font-size:
        clamp(
            42px,
            6vw,
            72px
        );

    line-height: 1.15;

    font-weight: 950;

    margin:
        12px 0
        18px 0;

    word-break: keep-all;
}


/* 티켓 아래 정보 */

.golden-info {

    color: #815157;

    font-size: 16px;
    font-weight: 700;
}


/* ==========================================================
   METRIC 카드
   ========================================================== */

[data-testid="stMetric"] {

    background:
        linear-gradient(
            135deg,
            #FFF8DF,
            #FFE3A1
        );

    border:
        3px dashed #C23B50;

    border-radius: 22px;

    padding:
        22px 20px;

    box-shadow:
        0 10px 25px
        rgba(0,0,0,0.30);

    min-height: 135px;
}


/* metric 제목 */

[data-testid="stMetricLabel"] p {

    color: #A12D43 !important;

    font-size: 15px !important;

    font-weight: 800 !important;
}


/* metric 숫자 */

[data-testid="stMetricValue"] {

    color: #35191D !important;

    font-weight: 900 !important;
}


/* ==========================================================
   팝콘 구분선
   ========================================================== */

.popcorn-divider {

    text-align: center;

    font-size: 30px;

    letter-spacing: 10px;

    margin:
        30px 0
        10px 0;
}


/* ==========================================================
   그래프
   ========================================================== */

[data-testid="stVegaLiteChart"] {

    background:
        rgba(
            255,
            255,
            255,
            0.05
        );

    border:
        1px solid
        rgba(
            255,
            209,
            102,
            0.30
        );

    border-radius: 22px;

    padding: 18px;
}


/* ==========================================================
   표
   ========================================================== */

[data-testid="stDataFrame"] {

    border:
        2px solid
        rgba(
            255,
            209,
            102,
            0.35
        );

    border-radius: 20px;

    overflow: hidden;

    box-shadow:
        0 10px 30px
        rgba(0,0,0,0.25);
}


/* ==========================================================
   Footer
   ========================================================== */

.footer {

    text-align: center;

    color: #C9AAB3;

    font-size: 13px;

    line-height: 2;

    margin-top: 35px;
}


/* ==========================================================
   Streamlit 기본 글자 색
   ========================================================== */

.stMarkdown p {
    color: #F8E8DE;
}


/* ==========================================================
   모바일 화면
   ========================================================== */

@media (max-width: 700px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .golden-ticket {
        padding:
            30px 18px;
    }

    .golden-label {
        font-size: 12px;
        letter-spacing: 2px;
    }

    .golden-info {
        font-size: 13px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. 상단 영화관 간판
# ============================================================

st.markdown(
    """
<div class="cinema-header">
    <div class="popcorn-logo">🍿</div>
    <div class="main-title">YESTERDAY CINEMA</div>
    <div class="main-subtitle">
        🎬 어제 극장가에서는 어떤 영화가 사랑받았을까? 🎬
    </div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# 4. 한국 시간 기준 어제 계산
# ============================================================

# Streamlit Cloud의 서버 시간은 한국 시간이 아닐 수 있다.
# 따라서 반드시 Asia/Seoul 시간대를 지정한다.

kst = ZoneInfo("Asia/Seoul")

today_kst = datetime.now(kst).date()

yesterday = today_kst - timedelta(days=1)


# KOBIS API용 날짜
# 예: 20260914

target_date = yesterday.strftime("%Y%m%d")


# 화면 표시용 날짜
# 예: 2026년 09월 14일

display_date = yesterday.strftime(
    "%Y년 %m월 %d일"
)


# 날짜 티켓

st.markdown(
    f"""
<div class="date-ticket">
    🎟️ {display_date} BOX OFFICE
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# 5. KOBIS 인증키 가져오기
# ============================================================

# 인증키는 코드에 적지 않는다.
# Streamlit Secrets에서 KOBIS_KEY를 불러온다.

try:

    kobis_key = st.secrets["KOBIS_KEY"]

except (KeyError, FileNotFoundError):

    st.error(
        "🎟️ KOBIS 인증키를 불러오지 못했어."
    )

    st.info(
        "Streamlit Cloud의 Settings → Secrets에서 "
        "`KOBIS_KEY`가 정확하게 등록되어 있는지 확인해 줘."
    )

    st.stop()


# ============================================================
# 6. KOBIS API 주소
# ============================================================

api_url = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/"
    "boxoffice/searchDailyBoxOfficeList.json"
)


# API에 전달할 값

params = {

    "key":
        kobis_key,

    "targetDt":
        target_date
}


# ============================================================
# 7. API 요청
# ============================================================

try:

    response = requests.get(

        api_url,

        params=params,

        timeout=10
    )


    # HTTP 오류 확인

    response.raise_for_status()


    # JSON 데이터 읽기

    data = response.json()


except requests.exceptions.RequestException:

    st.error(
        "🍿 KOBIS 서버에 데이터를 요청하는 과정에서 문제가 발생했어."
    )

    st.info(
        "인터넷 연결 상태와 KOBIS API 서버 상태를 확인하고 "
        "잠시 후 다시 시도해 줘."
    )

    st.stop()


except ValueError:

    st.error(
        "🎬 KOBIS 서버의 응답을 정상적으로 읽지 못했어."
    )

    st.info(
        "KOBIS API 주소가 올바른지, "
        "KOBIS 서버가 정상적으로 작동하는지 확인해 줘."
    )

    st.stop()


# ============================================================
# 8. KOBIS faultInfo 확인
# ============================================================

# KOBIS는 인증키가 틀려도
# HTTP 상태코드가 200으로 올 수 있다.
#
# 이 경우 JSON 안에 faultInfo가 들어온다.

if "faultInfo" in data:

    fault = data.get(
        "faultInfo",
        {}
    )


    error_code = fault.get(
        "errorCode",
        "알 수 없음"
    )


    error_message = fault.get(
        "message",
        "알 수 없는 오류"
    )


    st.error(
        "🎟️ KOBIS API에서 오류가 도착했어."
    )


    st.write(
        f"오류 코드: {error_code}"
    )


    st.write(
        f"오류 내용: {error_message}"
    )


    st.info(
        "Streamlit Secrets의 `KOBIS_KEY`가 정확한지 확인하고, "
        "영화진흥위원회에서 발급받은 인증키가 "
        "정상적으로 사용 가능한지도 확인해 줘."
    )


    st.stop()


# ============================================================
# 9. 영화 목록 가져오기
# ============================================================

try:

    movie_list = (
        data["boxOfficeResult"]
        ["dailyBoxOfficeList"]
    )


except (KeyError, TypeError):

    st.error(
        "🎬 KOBIS 응답에서 박스오피스 목록을 찾지 못했어."
    )

    st.info(
        "API 응답 구조가 변경되지 않았는지, "
        "해당 날짜 데이터가 정상적으로 제공되는지 확인해 줘."
    )

    st.stop()


# ============================================================
# 10. 빈 영화 목록 확인
# ============================================================

if not movie_list:

    st.warning(
        f"🍿 {display_date}의 박스오피스 데이터가 비어 있어."
    )

    st.info(
        "해당 날짜의 집계가 아직 완료되지 않았거나 "
        "KOBIS에서 데이터가 제공되지 않은 상태일 수 있어. "
        "잠시 후 다시 확인해 줘."
    )

    st.stop()


# ============================================================
# 11. 필요한 데이터만 정리
# ============================================================

rows = []


for movie in movie_list:

    try:

        rows.append({

            "순위":
                int(movie["rank"]),

            "영화명":
                movie["movieNm"],

            "개봉일":
                movie["openDt"],

            "관객수":
                int(movie["audiCnt"]),

            "누적관객":
                int(movie["audiAcc"]),

            "스크린수":
                int(movie["scrnCnt"])
        })


    except (
        KeyError,
        TypeError,
        ValueError
    ):

        # 일부 영화의 데이터가 이상한 경우
        # 해당 영화만 건너뛴다.

        continue


# DataFrame으로 변환

df = pd.DataFrame(rows)


# ============================================================
# 12. 변환된 데이터 확인
# ============================================================

if df.empty:

    st.error(
        "🍿 박스오피스 데이터를 정상적으로 변환하지 못했어."
    )

    st.info(
        "KOBIS API의 응답 항목이나 "
        "데이터 형식이 변경되지 않았는지 확인해 줘."
    )

    st.stop()


# 순위 순으로 정렬

df = (
    df
    .sort_values("순위")
    .reset_index(drop=True)
)


# ============================================================
# 13. 1위 영화
# ============================================================

top_movie = df.iloc[0]


# ============================================================
# 14. GOLDEN TICKET
# ============================================================

st.markdown(
    '<div class="section-title">🏆 오늘의 GOLDEN TICKET</div>',
    unsafe_allow_html=True
)


# 영화 이름에 혹시 HTML 특수문자가 포함되어 있을 경우를 대비해
# Streamlit 화면에서 이상하게 해석되지 않도록 escape 처리한다.

import html

safe_movie_name = html.escape(
    str(top_movie["영화명"])
)

safe_open_date = html.escape(
    str(top_movie["개봉일"])
)


# GOLDEN TICKET

st.markdown(
    f"""
<div class="golden-ticket">
    <div class="golden-label">
        ★ BOX OFFICE NO.1 ★
    </div>
    <div class="golden-movie-title">
        {safe_movie_name}
    </div>
    <div class="golden-info">
        🎬 BOX OFFICE 1위 &nbsp; • &nbsp;
        📅 개봉일 {safe_open_date}
    </div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# 15. 1위 영화 지표 카드
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        label="🍿 어제 관객수",
        value=f"{top_movie['관객수']:,}명"
    )


with col2:

    st.metric(
        label="👥 누적 관객수",
        value=f"{top_movie['누적관객']:,}명"
    )


with col3:

    st.metric(
        label="🎞️ 스크린수",
        value=f"{top_movie['스크린수']:,}개"
    )


# ============================================================
# 16. 팝콘 구분선
# ============================================================

st.markdown(
    '<div class="popcorn-divider">🍿 ✦ 🍿 ✦ 🍿</div>',
    unsafe_allow_html=True
)


# ============================================================
# 17. 관객수 TOP 5
# ============================================================

st.markdown(
    '<div class="section-title">📊 관객수 TOP 5</div>',
    unsafe_allow_html=True
)


# 순위 상위 5개 영화

top5 = df.nsmallest(
    5,
    "순위"
)


# 그래프용 데이터

chart_data = (
    top5
    .set_index("영화명")
    [["관객수"]]
)


# 막대그래프

st.bar_chart(
    chart_data
)


# ============================================================
# 18. 전체 박스오피스 표
# ============================================================

st.markdown(
    '<div class="section-title">🎬 어제의 박스오피스 순위</div>',
    unsafe_allow_html=True
)


st.dataframe(

    df,

    use_container_width=True,

    hide_index=True,

    column_config={

        "순위":
            st.column_config.NumberColumn(
                "🎟️ 순위",
                format="%d위"
            ),

        "영화명":
            st.column_config.TextColumn(
                "🎬 영화명"
            ),

        "개봉일":
            st.column_config.TextColumn(
                "📅 개봉일"
            ),

        "관객수":
            st.column_config.NumberColumn(
                "🍿 관객수",
                format="%,d명"
            ),

        "누적관객":
            st.column_config.NumberColumn(
                "👥 누적관객",
                format="%,d명"
            ),

        "스크린수":
            st.column_config.NumberColumn(
                "🎞️ 스크린수",
                format="%,d개"
            )
    }
)


# ============================================================
# 19. 마지막 팝콘 장식
# ============================================================

st.markdown(
    '<div class="popcorn-divider">🎞️ 🍿 🎬 🍿 🎞️</div>',
    unsafe_allow_html=True
)


# ============================================================
# 20. 하단 출처
# ============================================================

st.markdown(
    f"""
<div class="footer">
    🎟️ 조회 기준 : {display_date}<br>
    🎬 데이터 출처 : 영화진흥위원회 KOBIS<br>
    🍿 Have a nice movie day!
</div>
""",
    unsafe_allow_html=True
)
