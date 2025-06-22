import streamlit as st
import random
from transformers import pipeline

# ✅ Hugging Face 감정분석 모델 로드 (가벼운 모델)
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

sentiment_model = load_sentiment_model()

# ✅ 키워드 기반 감정 분석용 단어 사전
positive_keywords = ["좋", "재미있", "이해되", "유익", "도움", "흥미", "재밌"]
negative_keywords = ["어렵", "지루", "이해못", "싫", "부족", "시간없", "혼란", "복잡", "별로", "재미없"]

# ✅ 수업 목표 및 방법 사전
lesson_goals = [
    "자연 현상과 일상생활에 대한 흥미와 호기심을 바탕으로 문제를 인식하고 해결하는 태도 함양",
    "과학 탐구 방법을 이해하고 문제를 과학적으로 탐구하는 능력 기르기",
    "생태계의 개념을 이해하고 환경 문제 해결 의지 함양",
    "과학과 기술 및 사회의 상호 관계를 이해하고 참여적 시민의식 기르기"
]

lesson_methods = {
    "전반부": [
        ("흥미 유발 영상 시청", ["프로젝터", "영상 자료"]),
        ("생태계 관련 시각 자료 제공", ["사진 자료", "빔스크린"]),
        ("간단한 퀴즈로 아이스브레이킹", ["퀴즈지", "화이트보드"]),
        ("환경 문제 사례 이야기", ["신문 스크랩", "교사용 자료"])
    ],
    "중반부": [
        ("생태계 오염 실험 활동", ["페트병", "토양 샘플", "비커"]),
        ("먹이사슬 모형 만들기", ["종이, 가위, 풀", "생물 카드"]),
        ("조사 활동 및 발표", ["탐구 노트", "마이크", "포스트잇"]),
        ("환경 보호 아이디어 브레인스토밍", ["칠판", "마인드맵 도구"])
    ],
    "후반부": [
        ("과학 글쓰기", ["학습지", "노트"]),
        ("환경 캠페인 역할극", ["역할 명찰", "소품"]),
        ("토론 활동", ["토론 주제 카드", "타이머"]),
        ("퀴즈 또는 게임", ["문제 카드", "스피드 퀴즈 도구"])
    ]
}

# ✅ 수업안 생성 함수
def generate_lesson_plan(topic):
    goal = random.choice(lesson_goals)
    plan = {
        "주제": topic,
        "목표": goal
    }
    for phase in ["전반부", "중반부", "후반부"]:
        method, tools = random.choice(lesson_methods[phase])
        plan[phase] = {
            "활동": method,
            "도구": tools
        }
    return plan

# ✅ 키워드 기반 감정 분석 함수
def analyze_sentiment_by_keywords(text):
    pos = [kw for kw in positive_keywords if kw in text]
    neg = [kw for kw in negative_keywords if kw in text]
    if pos and not neg:
        return "긍정", pos, neg
    elif neg and not pos:
        return "부정", pos, neg
    elif pos and neg:
        return "혼합", pos, neg
    else:
        return "중립", pos, neg

# ✅ 피드백을 수업 단계별로 매칭하기 위한 간단 매핑 (활동명 포함 텍스트에 따라)
def match_phase(feedback, plan):
    for phase in ["전반부", "중반부", "후반부"]:
        activity = plan[phase]["활동"].replace(" ", "")
        if activity in feedback.replace(" ", ""):
            return phase
    return "(자동 인식 실패)"

# ========== Streamlit UI 시작 ==========

st.set_page_config(page_title="AI 수업 설계 및 피드백 분석기", layout="wide")
st.title("📘 AI 수업 설계 및 감정 기반 피드백 분석기")

st.header("1️⃣ 수업 주제 입력")
topic = st.text_input("수업 주제를 입력하세요 (예: 생물과 환경)")

if topic:
    plan = generate_lesson_plan(topic)

    st.subheader("📋 생성된 수업안")
    st.markdown(f"**주제:** {plan['주제']}")
    st.markdown(f"**목표:** {plan['목표']}")

    for phase in ["전반부", "중반부", "후반부"]:
        activity = plan[phase]["활동"]
        tools = ", ".join(plan[phase]["도구"])
        st.markdown(f"- **{phase}**: {activity}  \n  🧰 도구: {tools}")

    st.markdown("---")
    st.header("2️⃣ 학생 피드백 입력 및 감정 분석")

    feedback_input = st.text_area("학생 피드백을 한 줄씩 입력하세요", height=200)
    if st.button("감정 분석 실행"):
        if not feedback_input.strip():
            st.warning("피드백을 입력해주세요.")
        else:
            feedbacks = [f.strip() for f in feedback_input.strip().split("\n") if f.strip()]
            st.subheader("📊 피드백 분석 결과")
            for fb in feedbacks:
                # 키워드 분석
                label_kw, pos_kw, neg_kw = analyze_sentiment_by_keywords(fb)
                # HF 모델 분석
                hf_result = sentiment_model(fb)[0]
                # 단계 매칭
                phase = match_phase(fb, plan)

                st.markdown(f"**피드백:** {fb}")
                st.markdown(f"- 키워드 기반 감정: {label_kw}")
                st.markdown(f"- 긍정 단어: {pos_kw}")
                st.markdown(f"- 부정 단어: {neg_kw}")
                st.markdown(f"- HuggingFace 감정 분석: {hf_result['label']} (신뢰도: {hf_result['score']:.2f})")
                st.markdown(f"- 매칭된 수업 단계: {phase}")
                st.markdown("---")

else:
    st.info("왼쪽에서 수업 주제를 입력해주세요.")
