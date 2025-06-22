import streamlit as st
import random
from matplotlib import pyplot as plt

# 가장 위에 배치 (중요!)
st.set_page_config(page_title="AI 수업 설계 및 감정 분석", layout="wide")

# 1. 수업 목표 리스트
lesson_goals = [
    "자연 현상과 일상생활에 대한 흥미와 호기심을 바탕으로 문제를 인식하고 해결하는 태도 함양",
    "과학 탐구 방법을 이해하고 문제를 과학적으로 탐구하는 능력 기르기",
    "생태계의 개념을 이해하고 환경 문제 해결 의지 함양",
    "과학과 기술 및 사회의 상호 관계를 이해하고 참여적 시민의식 기르기"
]

# 2. 수업 방법과 도구
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

# 수업 설명 생성

def generate_rationale(topic, goal, activities):
    rationale = f"이번 수업 주제는 '{topic}'입니다. 주요 학습 목표는 '{goal}'이며, 이는 학생들이 과학 탐구 능력과 환경 문제에 대한 참여 의식을 기르도록 돕기 위함입니다.\n\n"
    rationale += "수업은 전반부, 중반부, 후반부로 나누어 구성하였고, 각 단계별 활동 선정에는 다음과 같은 이유가 있습니다:\n"
    for phase in ["전반부", "중반부", "후반부"]:
        activity = activities[phase]['활동']
        tools = ", ".join(activities[phase]['도구'])
        rationale += f"- [{phase}] '{activity}' 활동은 학생들의 흥미와 참여를 유도하고 학습 효과를 높이기 위해 '{tools}' 도구를 사용합니다.\n"
    rationale += "\n이러한 구성은 학생들의 집중력과 참여도를 높이고, 단계별로 학습 목표를 효과적으로 달성할 수 있도록 설계되었습니다."
    return rationale

# 수업 계획 생성 함수
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

# 감정 분석 키워드
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

# 피드백 분석

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

# 피드백 기반 수업 수정
def revise_plan(plan, phase_feedback):
    modified = False
    new_plan = plan.copy()
    for phase in ["전반부", "중반부", "후반부"]:
        pos = sum(1 for _, s in phase_feedback[phase] if s == "긍정")
        neg = sum(1 for _, s in phase_feedback[phase] if s == "부정")
        if neg > pos:
            current = plan[phase]["활동"]
            options = [m for m, _ in lesson_methods[phase] if m != current]
            if options:
                new_method = random.choice(options)
                new_tools = [t for m, t in lesson_methods[phase] if m == new_method][0]
                new_plan[phase] = {"활동": new_method, "도구": new_tools}
                modified = True
    return new_plan, modified

# 시각화 함수
def plot_feedback(phase_feedback):
    phases = ["전반부", "중반부", "후반부"]
    pos = [sum(1 for _, s in phase_feedback[p] if s == "긍정") for p in phases]
    neg = [sum(1 for _, s in phase_feedback[p] if s == "부정") for p in phases]
    fig, ax = plt.subplots()
    width = 0.35
    idx = range(len(phases))
    ax.bar(idx, pos, width, label="긍정", color="green")
    ax.bar([i + width for i in idx], neg, width, label="부정", color="red")
    ax.set_xticks([i + width / 2 for i in idx])
    ax.set_xticklabels(phases)
    ax.set_ylabel("피드백 수")
    ax.set_title("단계별 피드백 분석")
    ax.legend()
    st.pyplot(fig)

# Streamlit 인터페이스 시작
st.title("📘 AI 수업 설계 및 감정 분석 도구")
st.header("1️⃣ 학습 목표와 주제 설정")
goal = st.selectbox("학습 목표를 선택하세요:", lesson_goals)
topic = st.text_input("수업 주제를 입력하세요")

if goal and topic:
    plan = generate_lesson_plan(topic, goal)
    st.subheader("📋 생성된 수업안")
    st.markdown(f"**주제:** {plan['주제']}")
    st.markdown(f"**목표:** {plan['목표']}")
    for phase in ["전반부", "중반부", "후반부"]:
        tools = ", ".join(plan[phase]["도구"])
        st.markdown(f"- **{phase}**: {plan[phase]['활동']}  🧰 {tools}")
    st.info(plan["설명"])

    st.header("2️⃣ 수업 피드백 입력")
    st.markdown("활동명을 포함하여 피드백을 작성하세요. 줄 단위로 입력해주세요.")
    feedback_text = st.text_area("✏️ 피드백 입력")
    feedbacks = [line.strip() for line in feedback_text.split("\n") if line.strip()]

    if st.button("피드백 분석 및 수업안 개선"):
        if not feedbacks:
            st.warning("하나 이상의 피드백을 입력해주세요.")
        else:
            phase_feedback, unmatched = analyze_feedback(plan, feedbacks)
            st.subheader("🔍 분석 결과")
            for phase in ["전반부", "중반부", "후반부"]:
                st.markdown(f"#### {phase}")
                pos = [fb for fb, s in phase_feedback[phase] if s == "긍정"]
                neg = [fb for fb, s in phase_feedback[phase] if s == "부정"]
                st.markdown(f"- 긍정 피드백: {len(pos)}개")
                for fb in pos:
                    st.write(f"  - {fb}")
                st.markdown(f"- 부정 피드백: {len(neg)}개")
                for fb in neg:
                    st.write(f"  - {fb}")
            if unmatched:
                st.warning("다음 피드백은 단계와 매칭되지 않았습니다. 수동 선택 필요.")
                for i, fb in enumerate(unmatched):
                    phase = st.selectbox(f"{fb}", ["전반부", "중반부", "후반부"], key=f"unmatched_{i}")
                    sentiment = simple_sentiment_analysis(fb)
                    if sentiment != "중립":
                        phase_feedback[phase].append((fb, sentiment))

            st.subheader("📊 피드백 시각화")
            plot_feedback(phase_feedback)

            new_plan, modified = revise_plan(plan, phase_feedback)
            if modified:
                st.success("🔧 부정 피드백이 많은 활동을 수정한 수업안입니다.")
                for phase in ["전반부", "중반부", "후반부"]:
                    tools = ", ".join(new_plan[phase]["도구"])
                    st.markdown(f"- **{phase}**: {new_plan[phase]['활동']}  🧰 {tools}")
            else:
                st.info("✅ 모든 활동에서 긍정 피드백이 우세하여 수업안을 유지합니다.")
