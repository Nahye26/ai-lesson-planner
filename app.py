import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"

from konlpy.tag import Okt
# 나머지 코드... import streamlit as st
import random
from konlpy.tag import Okt
import os

# 1. JAVA 환경 설정 (konlpy Okt가 제대로 작동하려면)
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"  # 환경에 맞게 수정하세요
okt = Okt()

# 2. 키워드 사전 정의
positive_keywords = ["좋", "재미있", "이해되", "유익", "도움", "흥미", "재밌"]
negative_keywords = ["어렵", "지루", "이해못", "싫", "부족", "시간없", "혼란", "복잡", "별로", "재미없"]

# 3. 수업 목표 리스트
lesson_goals = [
    "자연 현상과 일상생활에 대한 흥미와 호기심을 바탕으로 문제를 인식하고 해결하는 태도 함양",
    "과학 탐구 방법을 이해하고 문제를 과학적으로 탐구하는 능력 기르기",
    "생태계의 개념을 이해하고 환경 문제 해결 의지 함양",
    "과학과 기술 및 사회의 상호 관계를 이해하고 참여적 시민의식 기르기"
]

# 4. 수업 방법과 도구 사전
lesson_methods = {
    "전반부": [
        ("흥미 유발 영상 시청", ["프로젝터", "영상 자료"]),
        ("생태계 관련 시각 자료 제공", ["사진 자료", "빔스크린"]),
        ("간단한 퀴즈로 아이스브레이킹", ["퀴즈지", "화이트보드"]),
        ("환경 문제 사례 이야기", ["신문 스크랩", "교사용 자료"])
    ],
    "중반부": [
        ("생태계 오염 실험 활동", ["페트병", "토양 샘플", "비커"]),
        ("먹이사슬 모형 만들기", ["종이, 가위, 풀", "생물 카드 출력"]),
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

# 5. 수업 계획 생성 함수
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

# 6. 감정 및 단계별 피드백 분석 함수
def analyze_feedback_with_phase(plan, feedback):
    tokens = okt.morphs(feedback, stem=True)
    pos = [w for w in tokens if any(p in w for p in positive_keywords)]
    neg = [w for w in tokens if any(n in w for n in negative_keywords)]

    # 단계 자동 매칭
    matched_phase = None
    for phase, activity in {p: plan[p]["활동"] for p in ["전반부", "중반부", "후반부"]}.items():
        if activity.replace(" ", "") in feedback.replace(" ", ""):
            matched_phase = phase
            break

    # 감정 판정
    if pos and not neg:
        sentiment = "긍정"
    elif neg and not pos:
        sentiment = "부정"
    elif pos and neg:
        sentiment = "혼합"
    else:
        sentiment = "중립"

    return {
        "피드백": feedback,
        "긍정어": pos,
        "부정어": neg,
        "감정": sentiment,
        "단계": matched_phase or "(자동 인식 실패)"
    }

# 7. 수업 설계 근거 설명 함수 추가
def lesson_plan_rationale():
    rationale = """
    이 수업 설계는 학생의 흥미를 유발하는 시각 자료와 활동을 전반부에 배치하여 집중도를 높이고,
    중반부에 실험과 탐구 활동을 통해 과학적 탐구 능력을 강화하며,
    후반부에는 토론과 글쓰기를 통해 학습 내용을 정리하고 심화하는 구조로 설계되었습니다.
    이러한 단계별 접근은 주의 집중의 흐름을 고려한 효과적인 교수 전략입니다.
    """
    return rationale

# 8. Streamlit 웹앱 UI 구성
def main():
    st.title("📘 AI 기반 초등 과학 수업 설계 및 피드백 분석기")

    st.header("1️⃣ 수업 주제 입력")
    topic = st.text_input("수업 주제를 입력하세요 (예: 생물과 환경)")

    if topic:
        plan = generate_lesson_plan(topic)

        st.subheader("📋 생성된 수업 계획")
        st.markdown(f"**주제:** {plan['주제']}")
        st.markdown(f"**목표:** {plan['목표']}")
        for phase in ["전반부", "중반부", "후반부"]:
            st.markdown(f"- **{phase}** 활동: {plan[phase]['활동']}  \n  도구: {', '.join(plan[phase]['도구'])}")

        st.subheader("💡 수업 설계 근거")
        st.info(lesson_plan_rationale())

        st.header("2️⃣ 학생 피드백 입력 및 분석")
        feedback_input = st.text_area("학생 피드백을 여러 줄로 입력하세요 (예: 너무 지루했어요. / 활동이 재미있었어요.)", height=150)

        if st.button("🔍 피드백 분석 시작"):
            if not feedback_input.strip():
                st.warning("피드백을 입력해 주세요.")
            else:
                feedbacks = [fb.strip() for fb in feedback_input.strip().split("\n") if fb.strip()]
                st.subheader("📊 피드백 분석 결과")
                for fb in feedbacks:
                    analysis = analyze_feedback_with_phase(plan, fb)
                    st.markdown(f"**피드백:** {analysis['피드백']}")
                    st.markdown(f"- 감정: {analysis['감정']}")
                    st.markdown(f"- 긍정어: {analysis['긍정어']}")
                    st.markdown(f"- 부정어: {analysis['부정어']}")
                    st.markdown(f"- 매칭된 단계: {analysis['단계']}")
                    st.markdown("---")

if __name__ == "__main__":
    main()
 
