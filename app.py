import streamlit as st
import random
import copy
from transformers import pipeline

# ✅ 감정 분석 모델 캐시 로딩 (한 번만)
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

sentiment_model = load_sentiment_model()

# ✅ 키워드 기반 간단 감정 분석용 사전 (선택적)
positive_keywords = ["좋", "재미있", "이해되", "유익", "도움", "흥미","재밌"]
negative_keywords = ["어렵", "지루", "이해못", "싫", "부족", "시간없", "혼란", "복잡","별로","재미없"]

# ✅ 수업 목표와 수업 방법
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
        ("먹이사슬 모형 만들기", ["종이, 가위, 풀", "생물 카드를 출력"]),
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

# ✅ 수업안 생성
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

# ✅ 키워드 기반 간단 감정 분석 함수 (선택적, 참고용)
def keyword_sentiment(feedback):
    pos = [k for k in positive_keywords if k in feedback]
    neg = [k for k in negative_keywords if k in feedback]
    if pos and not neg:
        return "긍정"
    elif neg and not pos:
        return "부정"
    elif pos and neg:
        return "혼합"
    else:
        return "중립"

# ✅ 피드백 분석 및 단계 매칭 (활동명 포함 여부 기반)
def analyze_feedback(plan, feedback_list):
    activity_map = {phase: plan[phase]["활동"] for phase in ["전반부", "중반부", "후반부"]}
    results = []
    phase_feedback = {"전반부": [], "중반부": [], "후반부": []}

    for fb in feedback_list:
        # AI 감정 분석
        ai_result = sentiment_model(fb)[0]
        # 키워드 감정 (선택)
        kw_sent = keyword_sentiment(fb)

        matched_phase = None
        for phase, activity in activity_map.items():
            if activity.replace(" ", "") in fb.replace(" ", ""):
                matched_phase = phase
                break
        if matched_phase is None:
            matched_phase = "미확인"

        results.append({
            "피드백": fb,
            "AI감정": ai_result,
            "키워드감정": kw_sent,
            "단계": matched_phase
        })

        if matched_phase in phase_feedback:
            phase_feedback[matched_phase].append(ai_result["label"])

    return results, phase_feedback

# ✅ 피드백 반영 수업안 수정 (부정 비율 높으면 활동 변경)
def update_lesson_plan(plan, phase_feedback):
    new_plan = copy.deepcopy(plan)
    modified = False

    for phase in ["전반부", "중반부", "후반부"]:
        sentiments = phase_feedback.get(phase, [])
        neg_count = sum(1 for s in sentiments if s in ["1 star", "2 stars"])
        pos_count = sum(1 for s in sentiments if s in ["4 stars", "5 stars"])

        if neg_count > pos_count:
            current = plan[phase]["활동"]
            options = [m for m, _ in lesson_methods[phase] if m != current]
            new_method = random.choice(options)
            new_tools = [t for m, t in lesson_methods[phase] if m == new_method][0]
            new_plan[phase] = {"활동": new_method, "도구": new_tools}
            modified = True

    return new_plan, modified

# ===========================
# Streamlit 웹앱 시작
# ===========================

st.title("📚 AI 수업 설계 및 감정 분석 웹앱 (konlpy 없이)")

topic = st.text_input("수업 주제를 입력하세요")

if topic:
    plan = generate_lesson_plan(topic)

    st.subheader("▶️ 생성된 수업안")
    st.write(f"**주제:** {plan['주제']}")
    st.write(f"**목표:** {plan['목표']}")
    for phase in ["전반부", "중반부", "후반부"]:
        act = plan[phase]["활동"]
        tools = ", ".join(plan[phase]["도구"])
        st.write(f"- **{phase}** 활동: {act}  \n  🧰 도구: {tools}")

    st.markdown("---")
    st.subheader("💬 학생 피드백 입력 (줄바꿈 구분)")

    feedback_input = st.text_area("피드백을 여러 줄로 입력하세요", height=150)

    if st.button("분석 및 수업안 개선"):
        feedback_list = [f.strip() for f in feedback_input.split("\n") if f.strip()]
        if not feedback_list:
            st.warning("피드백을 입력해주세요.")
        else:
            results, phase_feedback = analyze_feedback(plan, feedback_list)

            st.subheader("🔍 피드백 분석 결과")
            for r in results:
                st.write(f"\"{r['피드백']}\"")
                st.write(f"- AI 감정 분석: {r['AI감정']['label']} ({r['AI감정']['score']:.2f})")
                st.write(f"- 키워드 감정 분석: {r['키워드감정']}")
                st.write(f"- 매칭된 수업 단계: {r['단계']}")
                st.markdown("---")

            new_plan, modified = update_lesson_plan(plan, phase_feedback)

            if modified:
                st.success("⚠️ 일부 수업 단계가 피드백을 반영하여 변경되었습니다.")
            else:
                st.info("👍 모든 단계에서 긍정적 피드백이 우세합니다.")

            st.subheader("▶️ 최종 수업안")
            st.write(f"**주제:** {new_plan['주제']}")
            st.write(f"**목표:** {new_plan['목표']}")
            for phase in ["전반부", "중반부", "후반부"]:
                act = new_plan[phase]["활동"]
                tools = ", ".join(new_plan[phase]["도구"])
                st.write(f"- **{phase}** 활동: {act}  \n  🧰 도구: {tools}")
