import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(page_title="AI 정보 선생님", page_icon="🤖")
st.title("🤖 AI 정보 선생님")

# 비밀 금고(secrets)에서 API 키를 꺼내 접속 준비
client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# -----------------------------
# 말투별 기본 성격
# -----------------------------
PERSONALITIES = {
    "친절한 선생님": (
        "너는 중고등학생에게 설명하는 친절한 정보 선생님이야. "
        "어려운 말은 쉬운 말로 바꿔 주고, 학생이 이해하기 쉽도록 차근차근 설명해. "
        "반드시 순수 한국어로만 답해."
    ),
    "시크한 전문가": (
        "너는 정확하고 간결하게 설명하는 시크한 정보 전문가야. "
        "불필요하게 말을 길게 하지 말고 핵심 내용을 명확하게 설명해. "
        "어려운 내용도 중고등학생이 이해할 수 있도록 설명하고, "
        "반드시 순수 한국어로만 답해."
    ),
    "되물어보는 조교": (
        "너는 학생이 스스로 답을 찾도록 도와주는 정보 조교야. "
        "학생이 문제나 질문을 하면 정답을 바로 알려 주지 마. "
        "먼저 답을 생각하는 데 도움이 되는 힌트를 하나만 주고, "
        "학생이 어떻게 생각하는지 질문해. "
        "학생이 스스로 답을 말하면 그 답이 맞는지 확인해 주고, "
        "필요한 경우에만 추가 설명을 해. "
        "반드시 순수 한국어로만 답해."
    ),
}

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "tone" not in st.session_state:
    st.session_state.tone = "친절한 선생님"

if "personality_text" not in st.session_state:
    st.session_state.personality_text = PERSONALITIES["친절한 선생님"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("⚙️ AI 선생님 설정")

    selected_tone = st.selectbox(
        "말투 고르기",
        ["친절한 선생님", "시크한 전문가", "되물어보는 조교"],
        index=[
            "친절한 선생님",
            "시크한 전문가",
            "되물어보는 조교",
        ].index(st.session_state.tone),
    )

    # 말투가 변경되면 해당 말투의 기본 성격 문장으로 즉시 변경
    if selected_tone != st.session_state.tone:
        st.session_state.tone = selected_tone
        st.session_state.personality_text = PERSONALITIES[selected_tone]
        st.rerun()

    st.subheader("✏️ 성격 직접 고치기")

    personality_text = st.text_area(
        "AI의 성격 문장",
        value=st.session_state.personality_text,
        height=180,
        help="이 내용을 수정하면 다음 답변부터 바로 적용됩니다.",
    )

    st.session_state.personality_text = personality_text

    st.divider()

    if st.button("🗑️ 대화 지우기", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# 지금까지의 대화 표시
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# 채팅 입력창
# -----------------------------
user_input = st.chat_input("궁금한 것을 물어보세요!")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # 현재 선택된 성격을 매 요청마다 새로 넣음
    # 따라서 대화 도중 말투를 바꿔도 다음 답변부터 바로 적용됨
    messages_for_ai = [
        {
            "role": "system",
            "content": st.session_state.personality_text,
        }
    ] + st.session_state.messages

    # AI 답변
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="gemini-3.5-flash-lite",
                messages=messages_for_ai,
                stream=True,
            )

            answer = st.write_stream(
                chunk.choices[0].delta.content or ""
                for chunk in stream
                if chunk.choices
            )

            # AI 답변 저장
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception:
            st.error(
                "응답을 받지 못했습니다. 잠시 후 다시 보내 주세요."
            )
