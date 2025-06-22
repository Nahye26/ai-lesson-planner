import streamlit as st
import random
import matplotlib.pyplot as plt

# -------------------
# ✅ 수업 목표
lesson_goals = [
    "자연 현상과 일상생활에 대한 흥미와 호기심을 바탕으로 문제를 인식하고 해결하는 태도 함양",
    "과학 탐구 방법을 이해하고 문제를 과학적으로 탐구하는 능력 기르기",
    "생태계의 개념을 이해하고 환경 문제 해결 의지 함양",
    "과학과 기술 및 사회의 상호 관계를 이해하고 참여적 시민의식 기르기"
]

# ✅ 수업 방법 + 도구
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

positive_keywords = ["좋", "재미있", "이해되", "유익", "도움", "흥미", "재밌"]
negative_keywords = ["어렵", "지루", "이해못", "싫", "부족", "시간없", "혼란", "복잡", "별로", "재미없"]

# -------------------
def generate_rationale(goal, plan):
    rationale = f"입력한 학습 목표는 '{goal}'입니다. 이 목표는 학생들이 과학적 태도와 문제 해결력을 기를 수 있도록 설계되었습니다.\n"
    rationale += "수업은 전반부, 중반부, 후반부로 나누어 구성되었으며, 각 활동은 다음과 같은 이유로 선택되었습니다:\n"
    for phase in ["전반부", "중반부", "후반부"]:
        activity = plan[phase]['활동']
        tools = ", ".join(plan[phase]['도구'])
        rationale += f"- [{phase}] '{activity}' 활동은 '{tools}' 등의 도구를 활용해 학습 목표 달성을 돕습니다.\n"
    return rationale

# -------------------
def generate_lesson_plan(goal):
    plan = {"목표": goal}
    for phase in ["전반부", "중반부", "후반부"]:
        method, tools = random.choice(lesson_methods[phase])
        plan[phase] = {"활동": method, "도구": tools}
    plan["설명"] = generate_rationale(goal, plan)
    return plan

# -------------------
def analyze_feedback(feedbacks, plan):
    phase_keywords = {phase: plan[phase]['활동'] + " " + " ".join(plan[phase]['도구']) for phase in ["전반부", "중반부", "후반부"]}
    phase_counts = {p: {"긍정": 0, "부정": 0} for p in phase_keywords}
    unmatched = []

    for f in feedbacks:
        matched = False
        for phase, keywords in phase_keywords.items():
            if any(k in f for k in keywords.split()):
                phase_counts[phase]["긍정"] += any(pk in f for pk in positive_keywords)
                phase_counts[phase]["부정"] += any(nk in f for nk in negative_keywords)
                matched = True
                break
        if not matched:
            unmatched.append(f)

    return phase_counts, unmatched

# -------------------
def visualize_sentiment(phase_counts):
    phases = list(phase_counts.keys())
    positives = [phase_counts[p]["긍정"] for p in phases]
    negatives = [phase_counts[p]["부정"] for p in phases]

    fig, ax = plt.subplots()
    bar_width = 0.35
    index = range(len(phases))

    ax.bar(index, positives, bar_width, label='긍정', color='skyblue')
    ax.bar([i + bar_width for i in index], negatives, bar_width, label='부정', color='salmon')

    ax.set_xlabel('수업 단계')
    ax.set_ylabel('피드백 수')
    ax.set_title('단계별 긍정/부정 피드백 수')
    ax.set_xticks([i + bar_width/2 for i in index])
    ax.set_xticklabels(phases)
    ax.legend()

    st.pyplot(fig)

# -------------------
st.set_page_config(page_title="AI 수업 설계 및 감정 분석", layout="centered")
st.title("📘 AI 수업 설계 및 감정 분석")

st.header("1️⃣ 학습 목표 입력")
goal = st.text_input("학습 목표를 입력하세요:")

if goal:
    st.header("2️⃣ 수업안 생성")
    plan = generate_lesson_plan(goal)
    st.markdown(f"**🎯 목표:** {goal}")
    for phase in ["전반부", "중반부", "후반부"]:
        st.markdown(f"- **{phase}**: {plan[phase]['활동']} 🧰 {', '.join(plan[phase]['도구'])}")
    st.info(plan["설명"])

    st.header("3️⃣ 피드백 입력")
    if "feedbacks" not in st.session_state:
        st.session_state.feedbacks = [""]
    for i in range(len(st.session_state.feedbacks)):
        st.session_state.feedbacks[i] = st.text_input(f"피드백 #{i+1}", st.session_state.feedbacks[i], key=f"fb_{i}")
    if st.button("➕ 피드백 입력창 추가"):
        st.session_state.feedbacks.append("")

    if st.button("📊 피드백 분석"):
        feedbacks = [f for f in st.session_state.feedbacks if f.strip() != ""]
        phase_counts, unmatched = analyze_feedback(feedbacks, plan)

        st.subheader("📈 피드백 분석 결과")
        for phase, counts in phase_counts.items():
            st.write(f"- **{phase}**: ➕ 긍정 {counts['긍정']} / ➖ 부정 {counts['부정']}")

        if unmatched:
            st.warning(f"📌 매칭되지 않은 피드백이 {len(unmatched)}개 있습니다.\n")
            for f in unmatched:
                st.text(f"- {f}")

        visualize_sentiment(phase_counts)
else:
    st.info("👈 위에 학습 목표를 입력해주세요.")
