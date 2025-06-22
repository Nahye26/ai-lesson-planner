import streamlit as st
import random
from matplotlib import pyplot as plt

# 1. set_page_config은 가장 첫번째 Streamlit 함수 호출로 가장 위에 위치
st.set_page_config(page_title="AI 수업 설계 및 감정 분석", layout="wide")

# --- 수업 목표 ---
lesson_goals = [
    "자연 현상과 일상생활에 대한 흥미와 호기심을 바탕으로 문제를 인식하고 해결하는 태도 함양",
    "과학 탐구 방법을 이해하고 문제를 과학적으로 탐구하는 능력 기르기",
    "생태계의 개념을 이해하고 환경 문제 해결 의지 함양",
    "과학과 기술 및 사회의 상호 관계를 이해하고 참여적 시민의식 기르기"
]

# --- 수업 방법 + 도구 ---
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

# --- 수업 설계 근거 및 이유 ---
def generate_rationale(topic, goal, activities):
    rationale = f"이번 수업 주제는 '{topic}'입니다. 주요 학습 목표는 '{goal}'이며, 이는 학생들이 과학 탐구 능력과 환경 문제에 대한 참여 의식을 기르도록 돕기 위함입니다.\n\n"
    rationale += "수업은 전반부, 중반부, 후반부로 나누어 구성하였고, 각 단계별 활동 선정에는 다음과 같은 이유가 있습니다:\n"
    for phase in ["전반부", "중반부", "후반부"]:
        activity = activities[phase]['활동']
        tools = ", ".join(activities[phase]['도구'])
        rationale += f"- [{phase}] '{activity}' 활동은 학생들의 흥미와 참여를 유도하고 학습 효과를 높이기 위해 '{tools}' 도구를 사용합니다.\n"
    rationale += "\n이러한 구성은 학생들의 집중력과 참여도를 높이고, 단계별로 학습 목표를 효과적으로 달성할 수 있도록 설계되었습니다."
    return rationale

# --- 수업 계획 생성 ---
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
    plan["설명"] = generate_rationale(topic, goal, plan)
    return plan

# --- Streamlit UI ---
st.title("📘 AI 수업 설계 및 감정 분석")

st.header("1️⃣ 수업 주제 입력")
topic = st.text_input("수업 주제를 입력하세요 (예: 생물과 환경)")

if topic:
    plan = generate_lesson_plan(topic)
    st.subheader("📋 생성된 수업안")
    st.markdown(f"**주제:** {plan['주제']}")
    st.markdown(f"**목표:** {plan['목표']}")
    for phase in ["전반부", "중반부", "후반부"]:
        tools_str = ", ".join(plan[phase]["도구"])
        st.markdown(f"- **{phase}**: {plan[phase]['활동']}  🧰 도구: {tools_str}")

    st.info(plan["설명"])

else:
    st.info("👈 위 입력란에 수업 주제를 입력해주세요.")
