import streamlit as st
import random
from konlpy.tag import Okt
from matplotlib import pyplot as plt

# Okt 초기화 (konlpy는 JVM 필요, 로컬환경에서만 가능)
try:
    okt = Okt()
except Exception as e:
    st.error("Konlpy Okt 초기화 실패: JVM 환경 문제일 수 있습니다. 로컬 환경에서 실행해 주세요.")
    st.stop()

# 키워드 사전
positive_keywords = ["좋", "재미있", "이해되", "유익", "도움", "흥미", "재밌"]
negative_keywords = ["어렵", "지루", "이해못", "싫", "부족", "시간없", "혼란", "복잡", "별로", "재미없"]

# 수업 목표
lesson_goals = [
    "자연 현상과 일상생활에 대한 흥미와 호기심을 바탕으로 문제를 인식하고 해결하는 태도 함양",
    "과학 탐구 방법을 이해하고 문제를 과학적으로 탐구하는 능력 기르기",
    "생태계의 개념을 이해하고 환경 문제 해결 의지 함양",
    "과학과 기술 및 사회의 상호 관계를 이해하고 참여적 시민의식 기르기"
]

# 수업 방법 + 도구
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

# 수업 계획 생성 함수
def generate_lesson_plan(goal):
    plan = {"목표": goal}
    for phase in ["전반부", "중반부", "후반부"]:
        method, tools = random.choice(lesson_methods[phase])
        plan[phase] = {
            "활동": method,
            "도구": tools
        }
    return plan

# 수업 설계 출력 함수
def display_lesson_plan(plan):
    st.markdown(f"### 🎯 학습 목표: {plan['목표']}")
    for phase in ["전반부", "중반부", "후반부"]:
        tools_str = ", ".join(plan[phase]["도구"])
        st.markdown(f"- **{phase}**: {plan[phase]['활동']}  🧰 도구: {tools_str}")

# 피드백 분석 함수
def analyze_feedback(plan, feedback_list):
    phase_feedback = {"전반부": [], "중반부": [], "후반부": []}
    activity_map = {phase: plan[phase]["활동"] for phase in ["전반부", "중반부", "후반부"]}
    results = []

    for feedback in feedback_list:
        tokens = okt.morphs(feedback, stem=True)
        pos = [w for w in tokens if any(p in w for p in positive_keywords)]
        neg = [w for w in tokens if any(n in w for n in negative_keywords)]

        matched_phase = None
        for phase, activity in activity_map.items():
            # 활동명 혹은 도구 중 하나라도 있으면 매칭 시도
            if activity.replace(" ", "") in feedback.replace(" ", "") or any(tool in feedback for tool in plan[phase]["도구"]):
                matched_phase = phase
                break

        if matched_phase is None:
            matched_phase = st.selectbox(
                f"피드백 내용: \"{feedback}\"\n어느 단계(전반부/중반부/후반부)에 해당하나요?",
                options=["전반부", "중반부", "후반부"],
                key=feedback
            )
            if not matched_phase:
                matched_phase = "전반부"  # 기본값

        results.append((feedback, pos, neg, matched_phase))
        phase_feedback[matched_phase].append((pos, neg))

    return results, phase_feedback

# 피드백 기반 수업 수정 함수
def apply_feedback(plan, phase_feedback):
    new_plan = plan.copy()
    modified = False

    for phase in ["전반부", "중반부", "후반부"]:
        pos_count = sum(len(p[0]) for p in phase_feedback[phase])
        neg_count = sum(len(p[1]) for p in phase_feedback[phase])
        st.write(f"### [{phase}] 긍정 피드백: {pos_count}, 부정 피드백: {neg_count}")

        if neg_count > pos_count:
            st.warning(f"🔧 {phase} 활동을 수정합니다.")
            current = plan[phase]["활동"]
            options = [m for m, _ in lesson_methods[phase] if m != current]
            if options:
                new_method = random.choice(options)
                new_tools = [t for m, t in lesson_methods[phase] if m == new_method][0]
                new_plan[phase] = {"활동": new_method, "도구": new_tools}
                modified = True

    if modified:
        st.success("✅ 일부 단계가 부정 피드백에 따라 수정되었습니다.")
    else:
        st.success("✅ 모든 단계에서 긍정 피드백이 우세하여 수업을 유지합니다.")

    return new_plan

# 피드백 시각화 함수
def visualize_feedback(phase_feedback):
    phases = ["전반부", "중반부", "후반부"]
    pos_counts = [sum(len(p[0]) for p in phase_feedback[phase]) for phase in phases]
    neg_counts = [sum(len(p[1]) for p in phase_feedback[phase]) for phase in phases]

    fig, ax = plt.subplots()
    x = range(len(phases))
    ax.bar(x, pos_counts, width=0.4, label="긍정 피드백", color='green', align='center')
    ax.bar(x, neg_counts, width=0.4, label="부정 피드백", color='red', bottom=pos_counts, align='center')
    ax.set_xticks(x)
    ax.set_xticklabels(phases)
    ax.set_ylabel("피드백 개수")
    ax.set_title("단계별 긍정/부정 피드백 분포")
    ax.legend()
    st.pyplot(fig)

# Streamlit UI
st.title("📚 AI 기반 수업 설계 및 피드백 분석기")

st.header("1️⃣ 학습 목표 선택")
goal = st.selectbox("학습 목표를 선택하세요", lesson_goals)

if goal:
    plan = generate_lesson_plan(goal)

    st.header("2️⃣ 생성된 수업안")
    display_lesson_plan(plan)

    st.header("3️⃣ 수업 피드백 입력 (빈 줄 없이 Enter만 누르면 종료)")
    feedbacks = []
    while True:
        feedback = st.text_input(f"피드백 {len(feedbacks)+1}", key=f"fb_{len(feedbacks)}")
        if feedback == "":
            break
        feedbacks.append(feedback)

    if feedbacks:
        results, phase_feedback = analyze_feedback(plan, feedbacks)

        st.header("4️⃣ 피드백 분석 결과")
        for f, pos, neg, phase in results:
            st.markdown(f"- \"{f}\"  → 단계: **{phase}**, 긍정 키워드: {pos}, 부정 키워드: {neg}")

        visualize_feedback(phase_feedback)

        st.header("5️⃣ 피드백 반영 수업안 수정")
        new_plan = apply_feedback(plan, phase_feedback)

        st.header("6️⃣ 최종 수업안")
        display_lesson_plan(new_plan)
    else:
        st.info("피드백이 없습니다. 수업안을 수정할 수 없습니다.")
else:
    st.info("학습 목표를 선택해주세요.")
