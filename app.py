import streamlit as st
import random

# -------------------
# 수업 목표
lesson_goals = [
    "자연 현상과 일상생활에 대한 흥미와 호기심을 바탕으로 문제를 인식하고 해결하는 태도 함양",
    "과학 탐구 방법을 이해하고 문제를 과학적으로 탐구하는 능력 기르기",
    "생태계의 개념을 이해하고 환경 문제 해결 의지 함양",
    "과학과 기술 및 사회의 상호 관계를 이해하고 참여적 시민의식 기르기"
]

# 수업 방식별 활동 예시 (탐구, 활동, 개념)
lesson_activities = {
    "탐구": {
        "전반부": [("흥미 유발 영상 시청", ["프로젝터", "영상 자료"]), ("환경 문제 사례 이야기", ["신문 스크랩", "교사용 자료"])],
        "중반부": [("생태계 오염 실험 활동", ["페트병", "토양 샘플", "비커"]), ("조사 활동 및 발표", ["탐구 노트", "마이크", "포스트잇"])],
        "후반부": [("환경 캠페인 역할극", ["역할 명찰", "소품"]), ("토론 활동", ["토론 주제 카드", "타이머"])]
    },
    "활동": {
        "전반부": [("간단한 퀴즈로 아이스브레이킹", ["퀴즈지", "화이트보드"]), ("생태계 관련 시각 자료 제공", ["사진 자료", "빔스크린"])],
        "중반부": [("먹이사슬 모형 만들기", ["종이, 가위, 풀", "생물 카드"]), ("환경 보호 아이디어 브레인스토밍", ["칠판", "마인드맵 도구"])],
        "후반부": [("퀴즈 또는 게임", ["문제 카드", "스피드 퀴즈 도구"]), ("과학 글쓰기", ["학습지", "노트"])]
    },
    "개념": {
        "전반부": [("생태계 관련 시각 자료 제공", ["사진 자료", "빔스크린"]), ("흥미 유발 영상 시청", ["프로젝터", "영상 자료"])],
        "중반부": [("과학 원리 설명", ["교사용 자료", "화이트보드"]), ("개념 정리 퀴즈", ["퀴즈지"])],
        "후반부": [("과학 글쓰기", ["학습지", "노트"]), ("토론 활동", ["토론 주제 카드", "타이머"])]
    }
}

# 기본 추천 시간 배분 (단위: 분)
default_time_distribution = {
    "전반부": 10,
    "중반부": 15,
    "후반부": 15
}

# -------------------
# 수업 계획 생성 함수
def generate_lesson_plan(topic, approach, time_dist):
    goal = random.choice(lesson_goals)
    plan = {
        "주제": topic,
        "목표": goal,
        "시간배분": time_dist
    }
    for phase in ["전반부", "중반부", "후반부"]:
        methods_tools = lesson_activities[approach][phase]
        method, tools = random.choice(methods_tools)
        plan[phase] = {
            "활동": method,
            "도구": tools
        }
    return plan

# -------------------
# 수업 설계 근거 및 이유 자동 생성 함수
def generate_rationale(topic, goal, activities, time_dist):
    rationale = f"이번 수업 주제는 '{topic}'입니다. 주요 학습 목표는 '{goal}'이며, 이는 학생들이 과학 탐구 능력과 환경 문제에 대한 참여 의식을 기르도록 돕기 위함입니다.\n\n"
    rationale += "수업은 전반부, 중반부, 후반부로 나누어 구성하였고, 각 단계별 활동 선정에는 다음과 같은 이유가 있습니다:\n"
    for phase in ["전반부", "중반부", "후반부"]:
        activity = activities[phase]['활동']
        tools = ", ".join(activities[phase]['도구'])
        rationale += f"- [{phase} ({time_dist[phase]}분)] '{activity}' 활동은 학생들의 흥미와 참여를 유도하고 학습 효과를 높이기 위해 '{tools}' 도구를 사용합니다.\n"
    rationale += "\n이러한 구성은 학생들의 집중력과 참여도를 높이고, 단계별로 학습 목표를 효과적으로 달성할 수 있도록 설계되었습니다."
    return rationale

# -------------------
# Streamlit UI 시작
st.set_page_config(page_title="AI 수업 설계기 - 탐구/활동/개념 선택 및 시간배분", layout="wide")
st.title("📘 AI 수업 설계기")

st.header("1️⃣ 수업 주제 입력")
topic = st.text_input("수업 주제를 입력하세요 (예: 생물과 환경)")

st.header("2️⃣ 수업 방식 선택")
approach = st.radio("주로 어떤 방식으로 수업할까요?", options=["탐구", "활동", "개념"])

st.header("3️⃣ 시간 배분 선택")
time_option = st.radio("시간 배분을 선택하세요", options=["추천 시간 배분 사용", "직접 시간 배분 입력"])

if time_option == "추천 시간 배분 사용":
    time_dist = default_time_distribution
else:
    st.write("단위: 분")
    t1 = st.number_input("전반부 시간", min_value=1, max_value=40, value=10)
    t2 = st.number_input("중반부 시간", min_value=1, max_value=40, value=15)
    t3 = st.number_input("후반부 시간", min_value=1, max_value=40, value=15)
    total = t1 + t2 + t3
    if total > 40:
        st.error("총 시간은 40분을 넘을 수 없습니다!")
        st.stop()
    time_dist = {"전반부": t1, "중반부": t2, "후반부": t3}

if topic:
    plan = generate_lesson_plan(topic, approach, time_dist)
    rationale = generate_rationale(topic, plan["목표"], plan, time_dist)

    st.subheader("📋 생성된 수업안")
    st.markdown(f"**주제:** {plan['주제']}")
    st.markdown(f"**목표:** {plan['목표']}")
    for phase in ["전반부", "중반부", "후반부"]:
        tools_str = ", ".join(plan[phase]["도구"])
        st.markdown(f"- **{phase}** ({time_dist[phase]}분): {plan[phase]['활동']}  🧰 도구: {tools_str}")

    st.info(rationale)
else:
    st.info("👈 위 입력란에 수업 주제를 입력해주세요.")
