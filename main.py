st.markdown("""
<style>

/* 전체 영화관 배경 */
.stApp {
    background:
        radial-gradient(
            circle at top,
            #4b1635 0%,
            #211020 35%,
            #0e0910 75%
        );
    color: #fff7e8;
}

/* 화면 가운데 영역 */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

/* 메인 제목 */
.cinema-title {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    color: #ffd166;
    text-shadow:
        0 0 10px rgba(255, 209, 102, 0.5),
        3px 3px 0 #9b2335;
    margin-bottom: 5px;
}

/* 부제 */
.cinema-subtitle {
    text-align: center;
    color: #f8d7b0;
    font-size: 17px;
    margin-bottom: 30px;
}

/* 영화 티켓 */
.movie-ticket {
    position: relative;
    background: #fff2cf;
    color: #3b2020;
    border-radius: 22px;
    padding: 28px 35px;
    margin: 20px 0 30px 0;

    border: 4px dashed #c84747;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.35);
}

/* 티켓 제목 */
.ticket-label {
    text-align: center;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #b93645;
}

/* 1위 영화명 */
.ticket-movie {
    text-align: center;
    font-size: 35px;
    font-weight: 900;
    margin-top: 8px;
    margin-bottom: 10px;
}

/* 팝콘 */
.popcorn {
    text-align: center;
    font-size: 55px;
    margin: 5px;
}

/* 섹션 제목 */
.section-title {
    font-size: 25px;
    font-weight: 900;
    color: #ffd166;
    margin-top: 35px;
    margin-bottom: 15px;
}

/* Streamlit metric */
[data-testid="stMetric"] {
    background: #fff2cf;
    color: #3b2020;
    padding: 18px;
    border-radius: 18px;
    border: 3px dashed #c84747;
    box-shadow: 0 7px 15px rgba(0,0,0,0.25);
}

/* metric 글자 */
[data-testid="stMetricLabel"] {
    color: #8f3340;
    font-weight: 800;
}

[data-testid="stMetricValue"] {
    color: #3b2020;
    font-weight: 900;
}

/* 데이터 표 둥글게 */
[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

/* 하단 글씨 */
.cinema-footer {
    text-align: center;
    color: #c7a9a9;
    margin-top: 30px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)
