import streamlit as st
import random
from matplotlib import pyplot as plt

st.set_page_config(page_title="AI 수업 설계 및 감정 분석", layout="wide")

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

def generate_rationale(topic, goal, activities):
    rationale = f"이번 수업 주제는 '{topic}'입니다. 주요 학습 목표는 '{goal}'이며, 이는 학생들이 과학 탐구 능력과 환경 문제에 대한 참여 의식을 기르도록 돕기 위함입니다.\n\n"
    rationale += "수업은 전반부, 중반부, 후반부로 나누어 구성하였고, 각 단계별 활동 선정에는 다음과 같은 이유가 있습니다:\n"
    for phase in ["전반부", "중반부", "후반부"]:
        activity = activities[phase]['활동']
        tools = ", ".join(activities[phase]['도구'])
        rationale += f"- [{phase}] '{activity}' 활동은 학생들의 흥미와 참여를 유도하고 학습 효과를 높이기 위해 '{tools}' 도구를 사용합니다.\n"
    rationale += "\n이러한 구성은 학생들의 집중력과 참여도를 높이고, 단계별로 학습 목표를 효과적으로 달성할 수 있도록 설계되었습니다."
    return rationale

def generate_lesson_plan(topic, goal):
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
    plan["설명"] = generate_rationale(topic, goal, plan)
    return plan

positive_keywords = ["좋", "재미있", "이해되", "유익", "도움", "흥미", "재밌"]
negative_keywords = ["어렵", "지루", "이해못", "싫", "부족", "시간없", "혼란", "복잡", "별로", "재미없"]

def simple_sentiment_analysis(text):
    pos_count = sum(text.count(p) for p in positive_keywords)
    neg_count = sum(text.count(n) for n in negative_keywords)
    if pos_count > neg_count:
        return "긍정"
    elif neg_count > pos_count:
        return "부정"
    else:
        return None  # 중립은 None으로 처리

def analyze_feedback(plan, feedbacks):
    phase_activities = {phase: plan[phase]["활동"] for phase in ["전반부", "중반부", "후반부"]}
    phase_feedback = {"전반부": [], "중반부": [], "후반부": []}
    unmatched_feedback = []

    for fb in feedbacks:
        matched_phase = None
        for phase, activity in phase_activities.items():
            if activity in fb:
                matched_phase = phase
                break
        if matched_phase is None:
            unmatched_feedback.append(fb)
        else:
            sentiment = simple_sentiment_analysis(fb)
            if sentiment:
                phase_feedback[matched_phase].append((fb, sentiment))

    return phase_feedback, unmatched_feedback

def plot_feedback(phase_feedback):
    phases = ["전반부", "중반부", "후반부"]
    pos_counts = [sum(1 for _, s in phase_feedback[p] if s == "긍정") for p in phases]
    neg_counts = [sum(1 for _, s in phase_feedback[p] if s == "부정") for p in phases]

    fig, ax = plt.subplots()
    bar_width = 0.35
    index = range(len(phases))

    ax.bar(index, pos_counts, bar_width, label='긍정', color='green')
    ax.bar([i + bar_width for i in index], neg_counts, bar_width, label='부정', color='red')

    ax.set_xlabel('수업 단계')
    ax.set_ylabel('피드백 개수')
    ax.set_title('단계별 긍정/부정 피드백 수')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(phases)
    ax.legend()

    st.pyplot(fig)

def revise_plan(plan, phase_feedback):
    modified = False
    new_plan = plan.copy()
    for phase in ["전반부", "중반부", "후반부"]:
        pos_num = sum(1 for _, s in phase_feedback[phase] if s == "긍정")
        neg_num = sum(1 for _, s in phase_feedback[phase] if s == "부정")
        if neg_num > pos_num:
            current_activity = plan[phase]["활동"]
            options = [m for m, _ in lesson_methods[phase] if m != current_activity]
            if options:
                new_activity = random.choice(options)
                new_tools = [t for m, t in lesson_methods[phase] if m == new_activity][0]
                new_plan[phase] = {"활동": new_activity, "도구": new_tools}
                modified = True
    return new_plan, modified

# --- Streamlit UI ---

st.title("📘 AI 수업 설계 및 단계별 감정 피드백 분석")

goal = st.selectbox("학습 목표를 선택하세요:", lesson_goals)
topic = st.text_input("수업 주제를 입력하세요 (예: 생물과 환경)")

if topic and goal:
    if 'plan' not in st.session_state:
        st.session_state.plan = generate_lesson_plan(topic, goal)

    st.subheader("📋 생성된 수업안")
    st.markdown(f"**주제:** {st.session_state.plan['주제']}")
    st.markdown(f"**목표:** {st.session_state.plan['목표']}")
    for phase in ["전반부", "중반부", "후반부"]:
        tools_str = ", ".join(st.session_state.plan[phase]["도구"])
        st.markdown(f"- **{phase}**: {st.session_state.plan[phase]['활동']}  🧰 도구: {tools_str}")

    st.info(st.session_state.plan["설명"])

    st.header("3️⃣ 수업 피드백 입력")
    st.markdown("각 단계별 활동명을 포함하여 피드백을 작성해주세요.\n(예: 전반부 활동인 '흥미 유발 영상 시청'이 좋았어요.)")

    if 'feedbacks' not in st.session_state:
        st.session_state.feedbacks = []

    new_feedback = st.text_input("피드백 입력", key="feedback_input")
    if st.button("피드백 추가"):
        if new_feedback.strip() != "":
            st.session_state.feedbacks.append(new_feedback.strip())
            st.experimental_rerun()

    if st.session_state.feedbacks:
        st.subheader("현재 입력된 피드백")
        for idx, fb in enumerate(st.session_state.feedbacks):
            st.write(f"{idx + 1}. {fb}")

        if st.button("피드백 분석 및 수업안 수정"):
            phase_feedback, unmatched = analyze_feedback(st.session_state.plan, st.session_state.feedbacks)

            st.subheader("🔍 피드백 분석 결과")
            for phase in ["전반부", "중반부", "후반부"]:
                st.markdown(f"### {phase}")
                pos = [fb for fb, s in phase_feedback[phase] if s == "긍정"]
                neg = [fb for fb, s in phase_feedback[phase] if s == "부정"]
                st.markdown(f"- 긍정 피드백 ({len(pos)}개):")
                for p in pos:
                    st.write(f"  - {p}")
                st.markdown(f"- 부정 피드백 ({len(neg)}개):")
                for n in neg:
                    st.write(f"  - {n}")

            if unmatched:
                st.warning("⚠️ 일부 피드백에서 활동 단계가 인식되지 않았습니다. 아래에서 맞는 단계를 선택해주세요.")
                for i, fb in enumerate(unmatched):
                    phase_select = st.selectbox(f"피드백: {fb}", options=["전반부", "중반부", "후반부"], key=f"unmatched_{i}")
                    phase_feedback[phase_select].append((fb, simple_sentiment_analysis(fb)))

            st.subheader("📊 단계별 긍정/부정 피드백 수 시각화")
            plot_feedback(phase_feedback)

            new_plan, modified = revise_plan(st.session_state.plan, phase_feedback)
            if modified:
                st.success("🔧 부정 피드백이 많은 단계의 활동을 수정하여 새로운 수업안을 제안합니다.")
                st.session_state.plan = new_plan
                st.experimental_rerun()
            else:
                st.info("✅ 모든 단계에서 긍정 피드백이 부정 피드백보다 많아 수업안을 유지합니다.")
else:
    st.info("👈 학습 목표와 수업 주제를 모두 입력해주세요.")
