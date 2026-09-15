import streamlit as st
import pandas as pd
import requests

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# ---------------------------------------------------------
# 1. 페이지 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 어제의 박스오피스")
st.caption("영화진흥위원회 KOBIS 일별 박스오피스 데이터")


# ---------------------------------------------------------
# 2. 한국 시간(KST)을 기준으로 '어제' 날짜 계산
# ---------------------------------------------------------
# Streamlit Cloud 서버의 시간이 한국 시간이 아닐 수 있기 때문에
# 반드시 Asia/Seoul 시간대를 직접 지정한다.
kst = ZoneInfo("Asia/Seoul")
today_kst = datetime.now(kst).date()
yesterday = today_kst - timedelta(days=1)

# KOBIS API는 날짜를 yyyymmdd 형식으로 요구한다.
target_date = yesterday.strftime("%Y%m%d")

# 화면에 보여 줄 날짜는 읽기 편하게 따로 만든다.
display_date = yesterday.strftime("%Y년 %m월 %d일")

st.subheader(f"📅 {display_date} 박스오피스")


# ---------------------------------------------------------
# 3. Streamlit 비밀 금고에서 KOBIS 인증키 불러오기
# ---------------------------------------------------------
# 인증키를 코드에 직접 적지 않고
# Streamlit Cloud의 Secrets에 저장한 값을 사용한다.
try:
    kobis_key = st.secrets["KOBIS_KEY"]
except (KeyError, FileNotFoundError):
    st.error("KOBIS 인증키를 불러오지 못했어.")
    st.info(
        "Streamlit Cloud의 **Settings → Secrets**에서 "
        "`KOBIS_KEY`가 올바르게 등록되어 있는지 확인해 줘."
    )
    st.stop()


# ---------------------------------------------------------
# 4. KOBIS 일별 박스오피스 API 요청
# ---------------------------------------------------------
api_url = (
    "https://www.kobis.or.kr/kobisopenapi/webservice/rest/"
    "boxoffice/searchDailyBoxOfficeList.json"
)

params = {
    "key": kobis_key,
    "targetDt": target_date
}

try:
    response = requests.get(
        api_url,
        params=params,
        timeout=10
    )

    # 404, 500 등 HTTP 요청 자체에 문제가 있으면 오류 발생
    response.raise_for_status()

    # 받은 JSON 데이터를 파이썬 딕셔너리로 변환
    data = response.json()

except requests.exceptions.RequestException:
    st.error("KOBIS 서버에 데이터를 요청하는 과정에서 문제가 발생했어.")
    st.info(
        "인터넷 연결 상태와 KOBIS API 서버 상태를 확인한 뒤 "
        "잠시 후 다시 시도해 줘."
    )
    st.stop()

except ValueError:
    st.error("KOBIS 서버의 응답을 정상적으로 읽지 못했어.")
    st.info(
        "API 주소가 올바른지 확인하고, "
        "KOBIS 서버가 정상적으로 응답하고 있는지 확인해 줘."
    )
    st.stop()


# ---------------------------------------------------------
# 5. KOBIS가 faultInfo를 보냈는지 확인
# ---------------------------------------------------------
# KOBIS는 인증키가 잘못된 경우에도 HTTP 상태코드가 200일 수 있다.
# 따라서 상태코드만 확인하면 안 되고 faultInfo도 검사해야 한다.
if "faultInfo" in data:
    fault = data.get("faultInfo", {})

    error_code = fault.get("errorCode", "알 수 없음")
    error_message = fault.get("message", "알 수 없는 오류")

    st.error("KOBIS API에서 오류를 반환했어.")

    st.write(f"**오류 코드:** {error_code}")
    st.write(f"**오류 내용:** {error_message}")

    st.info(
        "Streamlit Secrets의 `KOBIS_KEY`가 정확한지, "
        "영화진흥위원회에서 발급받은 인증키가 정상적으로 사용 가능한지 "
        "확인해 줘."
    )
    st.stop()


# ---------------------------------------------------------
# 6. 영화 목록 가져오기
# ---------------------------------------------------------
try:
    movie_list = data["boxOfficeResult"]["dailyBoxOfficeList"]
except (KeyError, TypeError):
    st.error("KOBIS 응답에서 박스오피스 목록을 찾지 못했어.")
    st.info(
        "API 응답 구조가 변경되지 않았는지, "
        "조회 날짜에 데이터가 정상적으로 제공되고 있는지 확인해 줘."
    )
    st.stop()


# 목록 자체가 비어 있는 경우도 따로 처리한다.
if not movie_list:
    st.warning(f"{display_date}의 박스오피스 데이터가 비어 있어.")
    st.info(
        "해당 날짜의 집계가 아직 완료되지 않았거나 "
        "KOBIS에서 데이터가 제공되지 않은 상태일 수 있어. "
        "잠시 후 다시 확인해 줘."
    )
    st.stop()


# ---------------------------------------------------------
# 7. 필요한 데이터만 정리
# ---------------------------------------------------------
rows = []

for movie in movie_list:
    try:
        rows.append(
            {
                "순위": int(movie["rank"]),
                "영화명": movie["movieNm"],
                "개봉일": movie["openDt"],
                "관객수": int(movie["audiCnt"]),
                "누적관객": int(movie["audiAcc"]),
                "스크린수": int(movie["scrnCnt"]),
            }
        )
    except (KeyError, TypeError, ValueError):
        # 특정 영화 데이터가 비정상적이면 그 행은 건너뛴다.
        continue


df = pd.DataFrame(rows)


# 변환 후 데이터가 하나도 남지 않은 경우
if df.empty:
    st.error("박스오피스 데이터를 정상적으로 변환하지 못했어.")
    st.info(
        "KOBIS API의 응답 항목이나 데이터 형식이 변경되지 않았는지 "
        "확인해 줘."
    )
    st.stop()


# 순위 순서대로 정렬
df = df.sort_values("순위").reset_index(drop=True)


# ---------------------------------------------------------
# 8. 1위 영화의 주요 정보 표시
# ---------------------------------------------------------
top_movie = df.iloc[0]

st.markdown("### 🏆 박스오피스 1위")
st.markdown(f"## {top_movie['영화명']}")

# 지표 카드 3개를 가로로 배치
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="어제 관객수",
        value=f"{top_movie['관객수']:,}명"
    )

with col2:
    st.metric(
        label="누적 관객수",
        value=f"{top_movie['누적관객']:,}명"
    )

with col3:
    st.metric(
        label="스크린수",
        value=f"{top_movie['스크린수']:,}개"
    )


# ---------------------------------------------------------
# 9. 관객수 상위 5편 막대그래프
# ---------------------------------------------------------
st.markdown("### 📊 관객수 TOP 5")

top5 = df.nsmallest(5, "순위")

# 영화명을 인덱스로 지정하면 그래프의 항목 이름으로 영화명이 표시된다.
chart_data = top5.set_index("영화명")[["관객수"]]

st.bar_chart(chart_data)


# ---------------------------------------------------------
# 10. 전체 박스오피스 표
# ---------------------------------------------------------
st.markdown("### 🍿 일별 박스오피스 순위")

# 표에서 숫자를 보기 좋게 천 단위 쉼표로 표시한다.
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "순위": st.column_config.NumberColumn(
            "순위",
            format="%d위"
        ),
        "영화명": st.column_config.TextColumn(
            "영화명"
        ),
        "개봉일": st.column_config.TextColumn(
            "개봉일"
        ),
        "관객수": st.column_config.NumberColumn(
            "관객수",
            format="%,d명"
        ),
        "누적관객": st.column_config.NumberColumn(
            "누적관객",
            format="%,d명"
        ),
        "스크린수": st.column_config.NumberColumn(
            "스크린수",
            format="%,d개"
        ),
    }
)


# ---------------------------------------------------------
# 11. 하단 출처 표시
# ---------------------------------------------------------
st.divider()

st.caption(
    f"조회 기준: {display_date} · "
    "데이터 출처: 영화진흥위원회 KOBIS"
)
