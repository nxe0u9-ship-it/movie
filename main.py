import streamlit as st
import pandas as pd
import requests

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# =========================================================
# 1. 페이지 기본 설정
# =========================================================
st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🍿",
    layout="wide"
)


# =========================================================
# 2. 영화관 + 티켓 테마 디자인
# =========================================================
# Streamlit의 기본 화면에 CSS를 적용해서
# 영화관처럼 어둡고 따뜻한 분위기로 꾸며 준다.
st.markdown(
    """
    <style>

    /* -----------------------------------------------------
       전체 배경 : 어두운 영화관 느낌
    ----------------------------------------------------- */
    .stApp {
        background:
            radial-gradient(
                circle at top,
                #5b193c 0%,
                #2b1024 30%,
                #160b15 60%,
                #090609 100%
            );
        color: #fff7e8;
    }

    /* 화면의 최대 너비 */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* -----------------------------------------------------
       맨 위 영화관 간판
    ----------------------------------------------------- */
    .cinema-sign {
        text-align: center;
        margin-top: 5px;
        margin-bottom: 10px;
    }

    .popcorn-big {
        font-size: 65px;
        line-height: 1;
        margin-bottom: 5px;
    }

    .cinema-title {
        font-size: 50px;
        font-weight: 900;
        color: #FFD166;

        text-shadow:
            0 0 8px rgba(255,209,102,0.6),
            0 0 20px rgba(255,209,102,0.25),
            4px 4px 0 #9D2941;

        letter-spacing: 2px;
    }

    .cinema-subtitle {
        color: #F4D6C1;
        font-size: 17px;
        margin-top: 8px;
    }


    /* -----------------------------------------------------
       날짜 표시
    ----------------------------------------------------- */
    .date-board {
        width: fit-content;
        margin: 25px auto 30px auto;

        padding: 10px 25px;

        background: #311628;
        border: 2px solid #FFD166;
        border-radius: 50px;

        color: #FFD166;

        font-size: 16px;
        font-weight: 700;

        box-shadow:
            0 0 15px rgba(255,209,102,0.15);
    }


    /* -----------------------------------------------------
       1위 영화의 큰 티켓
    ----------------------------------------------------- */
    .movie-ticket {
        position: relative;

        background:
            linear-gradient(
                135deg,
                #FFF4D6,
                #FFE7AE
            );

        color: #3C2023;

        border-radius: 24px;

        padding: 30px 35px;

        margin-top: 15px;
        margin-bottom: 25px;

        border: 4px dashed #C94654;

        box-shadow:
            0 15px 35px rgba(0,0,0,0.40);
    }

    .ticket-label {
        text-align: center;

        color: #B32F45;

        font-size: 14px;
        font-weight: 900;

        letter-spacing: 3px;

        margin-bottom: 10px;
    }

    .ticket-movie {
        text-align: center;

        font-size: 37px;
        font-weight: 900;

        color: #3C2023;

        margin-bottom: 8px;
    }

    .ticket-info {
        text-align: center;

        color: #85565B;

        font-size: 14px;

        font-weight: 600;
    }


    /* -----------------------------------------------------
       섹션 제목
    ----------------------------------------------------- */
    .section-title {
        font-size: 26px;
        font-weight: 900;

        color: #FFD166;

        margin-top: 38px;
        margin-bottom: 17px;

        text-shadow:
            0 0 8px rgba(255,209,102,0.2);
    }


    /* -----------------------------------------------------
       Streamlit 지표(metric)를 작은 영화 티켓처럼 꾸미기
    ----------------------------------------------------- */
    [data-testid="stMetric"] {

        background:
            linear-gradient(
                135deg,
                #FFF4D6,
                #FFE5A5
            );

        padding: 22px;

        border-radius: 20px;

        border: 3px dashed #C94654;

        box-shadow:
            0 8px 20px rgba(0,0,0,0.30);
    }


    [data-testid="stMetricLabel"] {
        color: #A03547 !important;
        font-weight: 800;
    }

    [data-testid="stMetricValue"] {
        color: #3C2023 !important;
        font-weight: 900;
    }


    /* -----------------------------------------------------
       그래프 영역
    ----------------------------------------------------- */
    [data-testid="stVegaLiteChart"] {

        background:
            rgba(255,255,255,0.04);

        border-radius: 20px;

        padding: 15px;

        border:
            1px solid rgba(255,209,102,0.25);
    }


    /* -----------------------------------------------------
       데이터 표
    ----------------------------------------------------- */
    [data-testid="stDataFrame"] {

        border-radius: 18px;

        overflow: hidden;

        border:
            2px solid rgba(255,209,102,0.35);

        box-shadow:
            0 8px 25px rgba(0,0,0,0.25);
    }


    /* -----------------------------------------------------
       팝콘 장식
    ----------------------------------------------------- */
    .popcorn-divider {

        text-align: center;

        font-size: 27px;

        letter-spacing: 10px;

        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* -----------------------------------------------------
       하단
    ----------------------------------------------------- */
    .cinema-footer {

        text-align: center;

        color: #C9A9B2;

        margin-top: 35px;

        font-size: 13px;
    }


    /* Streamlit 기본 구분선 색 */
    hr {
        border-color:
            rgba(255,209,102,0.25);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 3. 상단 영화관 간판
# =========================================================
st.markdown(
    """
    <div class="cinema-sign">

        <div class="popcorn-big">
            🍿
        </div>

        <div class="cinema-title">
            YESTERDAY CINEMA
        </div>

        <div class="cinema-subtitle">
            🎬 어제 극장가에서는 어떤 영화가 사랑받았을까? 🎬
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 4. 한국 시간 기준으로 '어제' 계산
# =========================================================

# Streamlit Cloud 서버는 한국에 있지 않을 수 있다.
# 따라서 서버 시간을 그대로 사용하면 날짜가 틀릴 수 있다.
# Asia/Seoul 시간대를 직접 지정해 준다.
kst = ZoneInfo("Asia/Seoul")

today_kst = datetime.now(kst).date()

# 오늘에서 하루를 빼면 어제 날짜가 된다.
yesterday = today_kst - timedelta(days=1)


# KOBIS API에서 사용하는 형식
# 예: 20260914
target_date = yesterday.strftime("%Y%m%d")


# 사람이 보기 편한 형식
# 예: 2026년 09월 14일
display_date = yesterday.strftime("%Y년 %m월 %d일")


# 날짜를 영화관 전광판처럼 표시
st.markdown(
    f"""
    <div class="date-board">
        🎟️ {display_date} BOX OFFICE
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 5. Streamlit Secrets에서 KOBIS 인증키 가져오기
# =========================================================

# 인증키는 절대 코드에 직접 작성하지 않는다.
# Streamlit Cloud의 Secrets에 저장된 KOBIS_KEY를 가져온다.

try:

    kobis_key = st.secrets["KOBIS_KEY"]

except (KeyError, FileNotFoundError):

    st.error("🎟️ KOBIS 인증키를 불러오지 못했어.")

    st.info(
        "Streamlit Cloud의 **Settings → Secrets**에서 "
        "`KOBIS_KEY`가 정확하게 등록되어 있는지 확인해 줘."
    )

    st.stop()


# =========================================================
# 6. KOBIS 일별 박스오피스 API 요청
# =========================================================

api_url = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/"
    "boxoffice/searchDailyBoxOfficeList.json"
)


# API에 보낼 값
params = {

    # Secrets에서 가져온 인증키
    "key": kobis_key,

    # 한국 시간 기준 어제
    "targetDt": target_date
}


try:

    # KOBIS 서버에 데이터 요청
    response = requests.get(
        api_url,
        params=params,
        timeout=10
    )

    # 404, 500 등의 HTTP 오류가 있는지 확인
    response.raise_for_status()

    # JSON → 파이썬 딕셔너리
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
        "🎬 KOBIS 서버에서 받은 데이터를 정상적으로 읽지 못했어."
    )

    st.info(
        "KOBIS API 주소가 올바른지, "
        "서버가 정상적으로 응답하고 있는지 확인해 줘."
    )

    st.stop()


# =========================================================
# 7. faultInfo 확인
# =========================================================

# 중요!
#
# KOBIS는 인증키가 틀렸더라도
# HTTP 상태코드를 200으로 보내는 경우가 있다.
#
# 대신 JSON 안에 faultInfo가 들어온다.
#
# 따라서 response.status_code만 검사해서는 안 된다.

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
        f"**오류 코드:** {error_code}"
    )

    st.write(
        f"**오류 내용:** {error_message}"
    )

    st.info(
        "Streamlit Secrets의 `KOBIS_KEY`가 정확한지 확인하고, "
        "영화진흥위원회에서 발급받은 인증키가 "
        "현재 정상적으로 사용 가능한지도 확인해 줘."
    )

    st.stop()


# =========================================================
# 8. 영화 목록 가져오기
# =========================================================

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
        "해당 날짜의 데이터가 정상적으로 제공되고 있는지 확인해 줘."
    )

    st.stop()


# 목록 자체가 비어 있을 수도 있다.
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


# =========================================================
# 9. 필요한 데이터 정리
# =========================================================

rows = []


for movie in movie_list:

    try:

        rows.append(
            {
                # KOBIS 숫자 값은 문자열로 오기 때문에
                # int()로 숫자로 변환한다.

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
                    int(movie["scrnCnt"]),
            }
        )


    except (
        KeyError,
        TypeError,
        ValueError
    ):

        # 특정 영화의 데이터가 이상하면
        # 전체 앱을 멈추지 않고 해당 영화만 건너뛴다.
        continue


# 리스트 → pandas DataFrame
df = pd.DataFrame(rows)


# 변환했는데 아무 데이터도 남지 않은 경우
if df.empty:

    st.error(
        "🍿 박스오피스 데이터를 정상적으로 변환하지 못했어."
    )

    st.info(
        "KOBIS API의 응답 항목이나 "
        "데이터 형식이 변경되지 않았는지 확인해 줘."
    )

    st.stop()


# 순위 순서대로 정렬
df = (
    df
    .sort_values("순위")
    .reset_index(drop=True)
)


# =========================================================
# 10. 1위 영화 가져오기
# =========================================================

top_movie = df.iloc[0]


# =========================================================
# 11. 1위 영화 GOLDEN TICKET
# =========================================================

st.markdown(
    """
    <div class="section-title">
        🏆 오늘의 GOLDEN TICKET
    </div>
    """,
    unsafe_allow_html=True
)


# 1위 영화 정보를 커다란 영화 티켓처럼 표시
st.markdown(
    f"""
    <div class="movie-ticket">

        <div class="ticket-label">
            ★ BOX OFFICE NO.1 ★
        </div>

        <div class="ticket-movie">
            🎟️ {top_movie['영화명']}
        </div>

        <div class="ticket-info">
            {display_date}
            &nbsp;&nbsp;•&nbsp;&nbsp;
            개봉일 {top_movie['개봉일']}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 12. 1위 영화 지표 카드 3개
# =========================================================

# 세 개의 열을 만든다.
col1, col2, col3 = st.columns(3)


# 첫 번째 티켓
with col1:

    st.metric(
        label="🍿 어제 관객수",
        value=f"{top_movie['관객수']:,}명"
    )


# 두 번째 티켓
with col2:

    st.metric(
        label="🎬 누적 관객수",
        value=f"{top_movie['누적관객']:,}명"
    )


# 세 번째 티켓
with col3:

    st.metric(
        label="🎞️ 스크린수",
        value=f"{top_movie['스크린수']:,}개"
    )


# 팝콘 장식
st.markdown(
    """
    <div class="popcorn-divider">
        🍿 ✦ 🍿 ✦ 🍿
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 13. 관객수 TOP 5
# =========================================================

st.markdown(
    """
    <div class="section-title">
        📊 🍿 관객수 TOP 5
    </div>
    """,
    unsafe_allow_html=True
)


# 순위가 가장 높은 영화 5편
top5 = df.nsmallest(
    5,
    "순위"
)


# 영화명을 그래프의 이름으로 사용한다.
chart_data = (
    top5
    .set_index("영화명")
    [["관객수"]]
)


# Streamlit 기본 막대그래프
st.bar_chart(
    chart_data
)


# =========================================================
# 14. 전체 박스오피스 순위
# =========================================================

st.markdown(
    """
    <div class="section-title">
        🎬 오늘의 영화관 상영표
    </div>
    """,
    unsafe_allow_html=True
)


# 데이터 표 표시
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
            ),
    }
)


# =========================================================
# 15. 마지막 장식
# =========================================================

st.markdown(
    """
    <div class="popcorn-divider">
        🎞️ 🍿 🎬 🍿 🎞️
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 16. 출처
# =========================================================

st.markdown(
    f"""
    <div class="cinema-footer">

        🎟️ 조회 기준 : {display_date}<br><br>

        🎬 데이터 출처 : 영화진흥위원회 KOBIS<br><br>

        🍿 Have a nice movie day!

    </div>
    """,
    unsafe_allow_html=True
)
