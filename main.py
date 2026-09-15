# ============================================================
# 17. 관객수 TOP 5
# ============================================================

st.markdown(
    '<div class="section-title">🍿 관객수 TOP 5</div>',
    unsafe_allow_html=True
)

# 상위 5개 영화
top5 = df.nsmallest(5, "순위").copy()

# 가장 관객수가 많은 영화의 관객수를 기준으로
# 막대 길이를 100%로 계산한다.
max_audience = top5["관객수"].max()


# TOP 5 전체를 감싸는 영화관 매점 보드
st.markdown(
    """
<div style="
    background: rgba(20, 9, 18, 0.75);
    border: 2px solid rgba(255, 209, 102, 0.55);
    border-radius: 25px;
    padding: 25px 28px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.35);
">
    <div style="
        text-align:center;
        color:#FFD166;
        font-size:14px;
        font-weight:900;
        letter-spacing:4px;
        margin-bottom:6px;
    ">
        🍿 NOW SHOWING 🍿
    </div>

    <div style="
        text-align:center;
        color:#FFF1DB;
        font-size:24px;
        font-weight:900;
        margin-bottom:25px;
    ">
        AUDIENCE TOP 5
    </div>
""",
    unsafe_allow_html=True
)


# 영화 5개를 하나씩 예쁜 막대 형태로 표시
for _, movie in top5.iterrows():

    movie_name = html.escape(str(movie["영화명"]))
    audience = int(movie["관객수"])
    rank = int(movie["순위"])

    # 가장 관객수가 많은 영화를 100%로 하여
    # 상대적인 막대 길이를 계산
    bar_width = (audience / max_audience) * 100

    # 순위별 아이콘
    if rank == 1:
        rank_icon = "🥇"
    elif rank == 2:
        rank_icon = "🥈"
    elif rank == 3:
        rank_icon = "🥉"
    else:
        rank_icon = "🎟️"

    st.markdown(
        f"""
<div style="
    margin-bottom:20px;
">

    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        gap:15px;
        margin-bottom:8px;
    ">

        <div style="
            color:#FFF5E6;
            font-weight:800;
            font-size:16px;
        ">
            {rank_icon} {rank}위 &nbsp; {movie_name}
        </div>

        <div style="
            color:#FFD166;
            font-weight:900;
            font-size:15px;
            white-space:nowrap;
        ">
            🍿 {audience:,}명
        </div>

    </div>


    <div style="
        width:100%;
        height:18px;
        background:#3A2434;
        border-radius:50px;
        overflow:hidden;
        border:1px solid rgba(255,255,255,0.08);
    ">

        <div style="
            width:{bar_width}%;
            height:100%;
            background:linear-gradient(
                90deg,
                #FF6B81,
                #FFD166
            );
            border-radius:50px;
        ">
        </div>

    </div>

</div>
""",
        unsafe_allow_html=True
    )


# TOP5 보드 닫기
st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:8px;
        color:#C9AAB3;
        font-size:13px;
    ">
        🎬 어제 하루 동안 극장을 찾은 관객 기준
    </div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# 18. 팝콘 구분선
# ============================================================

st.markdown(
    '<div class="popcorn-divider">🍿 ✦ 🎬 ✦ 🍿</div>',
    unsafe_allow_html=True
)


# ============================================================
# 19. 전체 박스오피스 순위
# ============================================================

st.markdown(
    '<div class="section-title">🎟️ 어제의 BOX OFFICE</div>',
    unsafe_allow_html=True
)


# 영화관 전광판 제목
st.markdown(
    f"""
<div style="
    text-align:center;
    margin-bottom:22px;
">

    <div style="
        color:#FFD166;
        font-size:13px;
        font-weight:900;
        letter-spacing:4px;
    ">
        ★ NOW SHOWING ★
    </div>

    <div style="
        color:#FFF3DF;
        font-size:23px;
        font-weight:900;
        margin-top:5px;
    ">
        {display_date} RANKING
    </div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# 각 영화를 하나의 영화 티켓으로 표시
# ============================================================

for _, movie in df.iterrows():

    rank = int(movie["순위"])

    movie_name = html.escape(
        str(movie["영화명"])
    )

    open_date = html.escape(
        str(movie["개봉일"])
    )

    audience = int(
        movie["관객수"]
    )

    total_audience = int(
        movie["누적관객"]
    )

    screens = int(
        movie["스크린수"]
    )


    # --------------------------------------------------------
    # 1~3위는 특별한 아이콘
    # --------------------------------------------------------

    if rank == 1:

        rank_icon = "🥇"

        ticket_background = (
            "linear-gradient(135deg,#FFF4C7,#FFD978)"
        )

    elif rank == 2:

        rank_icon = "🥈"

        ticket_background = (
            "linear-gradient(135deg,#F8F8F8,#DCDCDC)"
        )

    elif rank == 3:

        rank_icon = "🥉"

        ticket_background = (
            "linear-gradient(135deg,#F8D5B5,#DDA06C)"
        )

    else:

        rank_icon = "🎟️"

        ticket_background = (
            "linear-gradient(135deg,#FFF7E5,#FFE7B3)"
        )


    # --------------------------------------------------------
    # 티켓 출력
    # --------------------------------------------------------

    st.markdown(
        f"""
<div style="
    position:relative;

    background:{ticket_background};

    border-radius:22px;

    margin-bottom:16px;

    padding:22px 28px;

    color:#35191D;

    border:3px dashed #C23B50;

    box-shadow:
        0 8px 22px
        rgba(0,0,0,0.28);
">


    <!-- 위쪽 : 순위 + 영화 제목 -->

    <div style="
        display:flex;
        align-items:center;
        gap:18px;
        margin-bottom:17px;
    ">


        <!-- 순위 -->

        <div style="
            min-width:70px;

            text-align:center;

            font-size:31px;

            font-weight:900;

            color:#A72D43;
        ">

            {rank_icon}

            <div style="
                font-size:14px;
                margin-top:2px;
            ">
                {rank}위
            </div>

        </div>


        <!-- 영화 제목 -->

        <div style="
            flex:1;
        ">

            <div style="
                color:#A72D43;

                font-size:11px;

                font-weight:900;

                letter-spacing:2px;

                margin-bottom:3px;
            ">
                ADMIT ONE
            </div>


            <div style="
                color:#35191D;

                font-size:clamp(
                    20px,
                    3vw,
                    28px
                );

                font-weight:950;

                line-height:1.2;

                word-break:keep-all;
            ">

                {movie_name}

            </div>


            <div style="
                color:#815157;

                font-size:12px;

                font-weight:700;

                margin-top:6px;
            ">

                📅 개봉일 {open_date}

            </div>

        </div>

    </div>


    <!-- 점선 -->

    <div style="
        border-top:
            2px dotted
            rgba(156,56,70,0.35);

        margin-bottom:15px;
    ">
    </div>


    <!-- 아래쪽 영화 정보 -->

    <div style="
        display:grid;

        grid-template-columns:
            repeat(
                3,
                1fr
            );

        gap:10px;

        text-align:center;
    ">


        <!-- 관객수 -->

        <div>

            <div style="
                color:#9B4050;
                font-size:11px;
                font-weight:800;
            ">
                TODAY
            </div>

            <div style="
                font-size:16px;
                font-weight:900;
                margin-top:2px;
            ">
                🍿 {audience:,}명
            </div>

        </div>


        <!-- 누적관객 -->

        <div>

            <div style="
                color:#9B4050;
                font-size:11px;
                font-weight:800;
            ">
                TOTAL
            </div>

            <div style="
                font-size:16px;
                font-weight:900;
                margin-top:2px;
            ">
                👥 {total_audience:,}명
            </div>

        </div>


        <!-- 스크린 -->

        <div>

            <div style="
                color:#9B4050;
                font-size:11px;
                font-weight:800;
            ">
                SCREEN
            </div>

            <div style="
                font-size:16px;
                font-weight:900;
                margin-top:2px;
            ">
                🎞️ {screens:,}개
            </div>

        </div>

    </div>

</div>
""",
        unsafe_allow_html=True
    )


# ============================================================
# 20. 마지막 장식
# ============================================================

st.markdown(
    '<div class="popcorn-divider">🎞️ 🍿 🎬 🍿 🎞️</div>',
    unsafe_allow_html=True
)


# ============================================================
# 21. 하단 출처
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
