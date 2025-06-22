import streamlit as st
import random
from matplotlib import pyplot as plt

st.set_page_config(page_title="AI 수업 설계 및 감정 분석", layout="wide")

if "plan" not in st.session_state:
    st.session_state.plan = None

# ... (lesson_goals, lesson_methods, generate_rationale, generate_lesson_plan 등 기존 함수 유지) ...

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
        return "중립"

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
            if sentiment != "중립":
                phase_feedback[matched_phase].append((fb, sentiment))

    return phase_feedback, unmatched_feedback

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
    ax.set_xticks([i + bar_width/2 for i in index])
    ax.set_xticklabels(phases)
    ax.legend()

    st.pyplot(fig)


# UI 시작
st.title("📘 AI 수업 설계 및 단계별 감정 피드백 분석")

st.header("1️⃣ 학습 목표 입력")
goal = st.selectbox("학습 목표를 선택하세요:", lesson_goals)

st.header("2️⃣ 수업 주제 입력")
topic = st.text_input("수업 주제를 입력하세요 (예: 생물과 환경)")

if topic and goal:
    if st.session_state.plan is None:
        st.session_state.plan = generate_lesson_plan(topic, goal)

    plan = st.session_state.plan

    st.subheader("📋 생성된 수업안")
    st.markdown(f"**주제:** {plan['주제']}")
    st.markdown(f"**목표:** {plan['목표']}")
    for phase in ["전반부", "중반부", "후반부"]:
        tools_str = ", ".join(plan[phase]["도구"])
        st.markdown(f"- **{phase}**: {plan[phase]['활동']}  🧰 도구: {tools_str}")

    st.info(plan["설명"])

    st.header("3️⃣ 수업 피드백 입력")
    st.markdown("피드백을 한 줄에 하나씩 작성하세요. 여러 줄 입력란에 줄바꿈으로 구분합니다.")

    feedback_text = st.text_area("피드백 입력 (줄바꿈으로 구분)", height=200)

    if st.button("피드백 분석 및 수업안 수정"):
        feedbacks = [line.strip() for line in feedback_text.split("\n") if line.strip()]
        if not feedbacks:
            st.warning("하나 이상의 피드백을 입력해주세요.")
        else:
            phase_feedback, unmatched = analyze_feedback(plan, feedbacks)

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
                unmatched_phase_map = {}
                for i, fb in enumerate(unmatched):
                    phase_select = st.selectbox(f"피드백: {fb}", options=["전반부", "중반부", "후반부"], key=f"unmatched_{i}")
                    unmatched_phase_map[fb] = phase_select
                    phase_feedback[phase_select].append((fb, simple_sentiment_analysis(fb)))

            st.subheader("📊 단계별 긍정/부정 피드백 수 시각화")
            plot_feedback(phase_feedback)

            new_plan, modified = revise_plan(plan, phase_feedback)

            if modified:
                st.success("🔧 부정 피드백이 많은 단계의 활동을 수정하여 새로운 수업안을 제안합니다.")
                st.markdown("### ✏️ 수정된 수업안")
                for phase in ["전반부", "중반부", "후반부"]:
                    tools_str = ", ".join(new_plan[phase]["도구"])
                    st.markdown(f"- **{phase}**: {new_plan[phase]['활동']}  🧰 도구: {tools_str}")

                st.session_state.plan = new_plan
            else:
                st.info("✅ 모든 단계에서 긍정 피드백이 부정 피드백보다 많아 수업안을 유지합니다.")

else:
    st.info("👈 학습 목표와 수업 주제를 모두 입력해주세요.")
