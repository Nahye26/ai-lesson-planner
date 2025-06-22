import streamlit as st
import random
from collections import Counter
from matplotlib import pyplot as plt

# ---------- 키워드 사전 ----------
positive_keywords = ["좋", "재미있", "이해되", "유익", "도움", "흥미", "재밌", "만족", "좋았"]
negative_keywords = ["어렵", "지루", "이해못", "싫", "부족", "시간없", "혼란", "복잡", "별로", "재미없", "불편"]

# ---------- 수업 목표 ----------
lesson_goals = [
    "자연 현상과 일상생활에 대한 흥미와 호기심을 바탕으로 문제를 인식하고 해결하는 태도 함양",
    "과학 탐구 방법을 이해하고 문제를 과학적으로 탐구하는 능력 기르기",
    "생태계의 개념을 이해하고 환경 문제 해결 의지 함양",
    "과학과 기술 및 사회의 상호 관계를 이해하고 참여적 시민의식 기르기"
]

# ---------- 수업 방법 + 도구 ----------
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

# ---------- 수업 계획 생성 ----------
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

# ---------- 피드백 텍스트 감정 분석 ----------
def analyze_sentiment(text):
    # 긍정, 부정 키워드 포함여부 확인
    pos_count = sum(text.count(p) for p in positive_keywords)
    neg_count = sum(text.count(n) for n in negative_keywords)

    # 중립 없음 - 긍정과 부정이 같으면 부정 우선 (or 중립으로 처리 안함)
    if pos_count > neg_count:
        return "긍정"
    else:
        return "부정"

# ---------- 피드백 리스트 단계 매칭 및 분석 ----------
def analyze_feedback(plan, feedback_list):
    phase_feedback = {"전반부": [], "중반부": [], "후반부": []}
    activity_map = {phase: plan[phase]["활동"] for phase in ["전반부", "중반부", "후반부"]}
    results = []

    for fb in feedback_list:
        matched_phase = None
        # 활동명 포함으로 단계 자동 판단
        for phase, activity in activity_map.items():
            if activity.replace(" ", "") in fb.replace(" ", ""):
                matched_phase = phase
                break

        # 매칭 안 되면 사용자에게 선택 요청
        if matched_phase is None:
            st.warning(f"아래 피드백에 대해 단계가 자동 매칭되지 않았습니다:\n\n'{fb}'")
            matched_phase = st.radio("이 피드백은 어느 단계에 해당합니까?", options=["전반부", "중반부", "후반부"], key=fb)

        sentiment = analyze_sentiment(fb)
        phase_feedback[matched_phase].append(sentiment)
        results.append((fb, matched_phase, sentiment))

    return results, phase_feedback

# ---------- 부정 많은 단계 활동 교체 ----------
def apply_feedback(plan, phase_feedback):
    new_plan = plan.copy()
    modified = False

    st.subheader("📊 단계별 피드백 요약")
    phases = ["전반부", "중반부", "후반부"]
    counts_pos = []
    counts_neg = []

    for phase in phases:
        pos = phase_feedback[phase].count("긍정")
        neg = phase_feedback[phase].count("부정")
        counts_pos.append(pos)
        counts_neg.append(neg)
        st.write(f"- **{phase}**: 긍정 {pos}개, 부정 {neg}개")

        if neg > pos:
            st.warning(f"{phase} 활동에 부정 피드백이 많아 활동을 교체합니다.")
            current_act = plan[phase]["활동"]
            options = [m for m, _ in lesson_methods[phase] if m != current_act]
            new_act = random.choice(options)
            new_tools = [t for m, t in lesson_methods[phase] if m == new_act][0]
            new_plan[phase] = {"활동": new_act, "도구": new_tools}
            modified = True

    # 막대그래프 그리기
    fig, ax = plt.subplots()
    x = phases
    ax.bar(x, counts_pos, label="긍정", color="skyblue")
    ax.bar(x, counts_neg, bottom=counts_pos, label="부정", color="salmon")
    ax.set_ylabel("피드백 개수")
    ax.set_title("단계별 긍정/부정 피드백 분포")
    ax.legend()
    st.pyplot(fig)

    if modified:
        st.success("부정 피드백이 많은 단계의 활동을 교체한 최종 수업안입니다.")
    else:
        st.success("모든 단계에서 긍정 피드백이 우세하여 수업안을 유지합니다.")

    return new_plan

# ---------- 수업안 출력 ----------
def display_plan(plan):
    st.markdown(f"### 수업 주제: {plan['주제']}")
    st.markdown(f"**수업 목표:** {plan['목표']}")
    for phase in ["전반부", "중반부", "후반부"]:
        tools_str = ", ".join(plan[phase]["도구"])
        st.markdown(f"- **{phase}**: {plan[phase]['활동']}  🧰 도구: {tools_str}")

# ---------- Streamlit 앱 UI ----------
def main():
    st.title("📚 AI 수업 설계 및 피드백 분석기")
    st.markdown("---")

    topic = st.text_input("수업 주제를 입력하세요", placeholder="예) 생물과 환경")

    if topic:
        plan = generate_lesson_plan(topic)
        st.header("1️⃣ 생성된 수업안")
        display_plan(plan)

        st.header("2️⃣ 수업에 대한 교사 피드백 입력")
        st.info("각 피드백에는 가능한 활동명(예: 흥미 유발 영상 시청)을 포함해 주세요.\n"
                "만약 단계가 자동으로 매칭되지 않으면 단계 선택을 요청합니다.\n"
                "중립 감정은 없으며 긍정/부정으로만 분석합니다.")

        feedback_input = st.text_area("피드백을 한 줄씩 입력하세요(한 줄에 하나씩 입력). 빈 줄로 구분됨", height=150)
        feedback_list = [line.strip() for line in feedback_input.split("\n") if line.strip()]

        if st.button("▶️ 피드백 분석 및 수업안 수정"):
            if not feedback_list:
                st.error("피드백을 입력하세요!")
            else:
                results, phase_feedback = analyze_feedback(plan, feedback_list)
                st.header("3️⃣ 피드백 분석 결과")
                for fb, phase, senti in results:
                    st.write(f"- \"{fb}\" → 단계: **{phase}**, 감정: **{senti}**")

                new_plan = apply_feedback(plan, phase_feedback)

                st.header("4️⃣ 최종 수업안")
                display_plan(new_plan)

if __name__ == "__main__":
    main()
