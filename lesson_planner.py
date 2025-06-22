import streamlit as st
import random
from transformers import pipeline

# ✅ 감정 분석 모델 로딩 (가벼운 모델로 변경 + 캐시 안정화)
@st.cache(allow_output_mutation=True)
def load_sentiment_model():
    return pipeline("sentiment-analysis", 
                    model="distilbert-base-multilingual-cased", 
                    device=-1)  # CPU 명시

sentiment_model = load_sentiment_model()

# ✅ 긍정/부정 키워드 리스트
positive_keywords = ["좋", "재미있", "이해되", "유익", "도움", "흥미", "재밌"]
negative_keywords = ["어렵", "지루", "이해못", "싫", "부족", "시간없", "혼란", "복잡", "별로", "재미없"]

# ✅ 수업 목표
lesson_goals = [
    "자연 현상과 일상생활에 대한 흥미와 호기심을 바탕으로 문제를 인식하고 해결하는 태도 함양",
    "과학 탐구 방법을 이해하고 문제를 과학적으로 탐구하는 능력 기르기",
    "생태계의 개념을 이해하고 환경 문제 해결 의지 함양",
    "과학과 기술 및 사회의 상호 관계를 이해하고 참여적 시민의식 기르기"
]

# ✅ 수업 활동 사전
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
    explanation = f"이 수업은 '{topic}' 주제를 중심으로 구성되며, 주요 목표는 '{goal}'입니다.\n"
    explanation += "도입→전개→정리 흐름에 따라 학생의 흥미 유도, 탐구 활동, 개념 정리로 구성됩니다.\n"

    for phase in ["전반부", "중반부", "후반부"]:
        method, tools = random.choice(lesson_methods[phase])
        plan[phase] = {"활동": method, "도구": tools}
        explanation += f"- [{phase}] 단계: '{method}' 활동은 학생 참여를 이끌고 개념 형성에 기여합니다.\n"

    plan["설명"] = explanation
    return plan

# ✅ 피드백 분석 함수
def analyze_feedback(feedback, activity_map):
    pos = [k for k in positive_keywords if k in feedback]
    neg = [k for k in negative_keywords if k in feedback]

    if pos and not neg:
        sentiment_label = "긍정"
    elif neg and not pos:
        sentiment_label = "부정"
    elif pos and neg:
        sentiment_label = "혼합"
    else:
        sentiment_label = "중립"

    matched_phase = None
    for phase, activity in activity_map.items():
        if activity.replace(" ", "") in feedback.replace(" ", ""):
            matched_phase = phase
            break

    return {
        "피드백": feedback,
        "감정": sentiment_label,
        "긍정어": pos,
        "부정어": neg,
        "단계": matched_phase or "(자동 인식 실패)"
    }

# ✅ Streamlit 웹 UI
st.set_page_config(page_title="AI 수업 설계 및 피드백 분석기", layout="wide")
st.title("📘 AI 수업 설계 및 감정 기반 개선 도우미")
st.markdown("---")

st.header("1️⃣ 수업 주제 선택")
subject_input = st.text_input("수업 주제를 입력하세요 (예: 생물과 환경)")

if subject_input:
    plan = generate_lesson_plan(subject_input)
    st.subheader("📋 생성된 수업안")
    st.markdown(f"**주제:** {plan['주제']}  \n**목표:** {plan['목표']}")

    for phase in ["전반부", "중반부", "후반부"]:
        act = plan[phase]["활동"]
        tools = ", ".join(plan[phase]["도구"])
        st.markdown(f"- **{phase}**: {act}  \n  🧰 도구: {tools}")

    st.info(plan["설명"])

    st.markdown("---")
    st.header("2️⃣ 피드백 입력 및 분석")
    feedback_input = st.text_area("학생 피드백을 입력하세요 (여러 줄 가능)", height=200)

    if st.button("🧠 감정 분석 및 개선 제안"):
        if not feedback_input.strip():
            st.warning("피드백 내용을 입력해주세요.")
        else:
            activity_map = {phase: plan[phase]["활동"] for phase in ["전반부", "중반부", "후반부"]}
            feedbacks = feedback_input.strip().split("\n")
            st.subheader("📊 피드백 분석 결과")

            for fb in feedbacks:
                analysis = analyze_feedback(fb, activity_map)
                ai_result = sentiment_model(fb)[0]  # 감정분석 모델 호출

                st.markdown(f"**📝 피드백:** {fb}")
                st.markdown(f"- 감정 분류(키워드 기반): {analysis['감정']}  \n"
                            f"- 긍정어: {analysis['긍정어']} / 부정어: {analysis['부정어']}  \n"
                            f"- AI 감정 분석: {ai_result['label']} ({ai_result['score']:.2f})  \n"
                            f"- 매칭된 단계: {analysis['단계']}")
                st.markdown("---")

            st.success("✅ 분석이 완료되었습니다. 수업안 개선에 참고하세요!")

else:
    st.info("👈 왼쪽 입력창에 수업 주제를 먼저 입력해주세요.")
