import streamlit as st
import random
from konlpy.tag import Okt
import os

# JAVA 환경 설정 (필요 시 조정)
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
okt = Okt()

# 긍정/부정 키워드 사전
positive_keywords = ["좋", "재미있", "이해되", "유익", "도움", "흥미", "재밌"]
negative_keywords = ["어렵", "지루", "이해못", "싫", "부족", "시간없", "혼란", "복잡", "별로", "재미없"]

# 수업 목표와 태그 (수업 유형 분류용)
lesson_goals_with_tags = {
    "자연 현상과 일상생활에 대한 흥미와 호기심을 바탕으로 문제를 인식하고 해결하는 태도 함양": ["탐구", "흥미"],
    "과학 탐구 방법을 이해하고 문제를 과학적으로 탐구하는 능력 기르기": ["탐구"],
    "생태계의 개념을 이해하고 환경 문제 해결 의지 함양": ["개념", "참여"],
    "과학과 기술 및 사회의 상호 관계를 이해하고 참여적 시민의식 기르기": ["참여", "활동"]
}

# 수업 방법 + 도구 + 태그 (중점 유형별 필터링용)
lesson_methods_with_tags = {
    "전반부": [
        ("흥미 유발 영상 시청", ["프로젝터", "영상 자료"], ["흥미", "탐구"]),
        ("생태계 관련 시각 자료 제공", ["사진 자료", "빔스크린"], ["개념"]),
        ("간단한 퀴즈로 아이스브레이킹", ["퀴즈지", "화이트보드"], ["흥미", "활동"]),
        ("환경 문제 사례 이야기", ["신문 스크랩", "교사용 자료"], ["참여", "개념"])
    ],
    "중반부": [
        ("생태계 오염 실험 활동", ["페트병", "토양 샘플", "비커"], ["탐구"]),
        ("먹이사슬 모형 만들기", ["종이, 가위, 풀", "생물 카드"], ["활동"]),
        ("조사 활동 및 발표", ["탐구 노트", "마이크", "포스트잇"], ["탐구", "참여"]),
        ("환경 보호 아이디어 브레인스토밍", ["칠판", "마인드맵 도구"], ["참여"])
    ],
    "후반부": [
        ("과학 글쓰기", ["학습지", "노트"], ["개념", "활동"]),
        ("환경 캠페인 역할극", ["역할 명찰", "소품"], ["활동", "참여"]),
        ("토론 활동", ["토론 주제 카드", "타이머"], ["참여"]),
        ("퀴즈 또는 게임", ["문제 카드", "스피드 퀴즈 도구"], ["흥미", "활동"])
    ]
}

# 기본 추천 시간 배분 (총 40분)
default_time_allocation = {"전반부": 10, "중반부": 15, "후반부": 15}

def generate_lesson_plan_with_time(topic, focus, time_alloc):
    # 목표 필터링
    filtered_goals = [g for g, tags in lesson_goals_with_tags.items() if focus in tags]
    if not filtered_goals:
        filtered_goals = list(lesson_goals_with_tags.keys())
    goal = random.choice(filtered_goals)

    plan = {
        "주제": topic,
        "목표": goal,
        "시간배분": time_alloc
    }

    for phase in ["전반부", "중반부", "후반부"]:
        candidates = [(m, t) for m, t, tags in lesson_methods_with_tags[phase] if focus in tags]
        if not candidates:
            candidates = [(m, t) for m, t, tags in lesson_methods_with_tags[phase]]
        method, tools = random.choice(candidates)
        plan[phase] = {"활동": method, "도구": tools, "시간(분)": time_alloc[phase]}
    return plan

def analyze_feedback_with_phase(plan, feedbacks):
    results = []
    activity_map = {phase: plan[phase]["활동"] for phase in ["전반부", "중반부", "후반부"]}

    for fb in feedbacks:
        tokens = okt.morphs(fb, stem=True)
        pos = [w for w in tokens if any(pk in w for pk in positive_keywords)]
        neg = [w for w in tokens if any(nk in w for nk in negative_keywords)]

        matched_phase = None
        for phase, activity in activity_map.items():
            # 활동명 또는 도구 중 하나라도 포함되면 매칭
            if activity.replace(" ", "") in fb.replace(" ", ""):
                matched_phase = phase
                break
            else:
                for tool in plan[phase]["도구"]:
                    if tool.replace(" ", "") in fb.replace(" ", ""):
                        matched_phase = phase
                        break
                if matched_phase:
                    break

        if matched_phase is None:
            matched_phase = "미매칭"

        results.append({"피드백": fb, "긍정어": pos, "부정어": neg, "단계": matched_phase})
    return results

def show_lesson_plan(plan):
    st.markdown(f"### 📘 수업 주제: {plan['주제']}")
    st.markdown(f"**수업 목표:** {plan['목표']}")
    st.markdown(f"**시간 배분:** 전반부 {plan['시간배분']['전반부']}분 / 중반부 {plan['시간배분']['중반부']}분 / 후반부 {plan['시간배분']['후반부']}분")
    for phase in ["전반부", "중반부", "후반부"]:
        info = plan[phase]
        st.markdown(f"- **{phase}** ({info['시간(분)']}분): {info['활동']} (도구: {', '.join(info['도구'])})")

def explain_design_rationale(focus, time_alloc):
    rationale = f"""
    ### 수업 설계 근거 설명
    - **수업 유형 '{focus}'를 중심**으로 목표와 활동을 선정하여 학생들의 {focus} 능력 및 참여를 극대화하고자 하였습니다.
    - **시간 배분**은 총 40분 수업 기준으로, 전반부 {time_alloc['전반부']}분, 중반부 {time_alloc['중반부']}분, 후반부 {time_alloc['후반부']}분으로 계획하여 집중도와 흥미를 유지하도록 설계하였습니다.
    - 전반부에는 흥미 유발 및 개념 소개, 중반부에는 심화 탐구 활동, 후반부에는 정리 및 적용 활동을 배치하였습니다.
    """
    st.markdown(rationale)

# Streamlit UI 시작
st.title("📗 AI 수업 설계 및 피드백 분석기")

topic = st.text_input("🧪 수업 주제를 입력하세요")
focus = st.radio("수업 유형을 선택하세요", options=["탐구", "개념", "활동"], index=0)

use_default_time = st.checkbox("추천 시간 배분 사용 (전반부:10분, 중반부:15분, 후반부:15분)", value=True)

if use_default_time:
    time_alloc = default_time_allocation
else:
    st.markdown("### 직접 시간 배분 입력 (총합 40분 권장)")
    t1 = st.number_input("전반부 시간 (분)", min_value=0, max_value=40, value=10)
    t2 = st.number_input("중반부 시간 (분)", min_value=0, max_value=40, value=15)
    t3 = st.number_input("후반부 시간 (분)", min_value=0, max_value=40, value=15)
    total = t1 + t2 + t3
    if total != 40:
        st.warning(f"⚠️ 총합이 40분이 아닙니다. 현재 총합: {total}분")
    time_alloc = {"전반부": t1, "중반부": t2, "후반부": t3}

if st.button("수업안 생성하기"):
    if not topic.strip():
        st.warning("수업 주제를 입력하세요.")
    else:
        lesson_plan = generate_lesson_plan_with_time(topic.strip(), focus, time_alloc)
        show_lesson_plan(lesson_plan)
        explain_design_rationale(focus, time_alloc)

        st.markdown("---")
        st.header("💬 학생 피드백 입력 및 감정 분석 (키워드 기반)")

        feedback_input = st.text_area("학생 피드백을 입력하세요. 여러 개 입력 시 줄바꿈으로 구분하세요.", height=150)

        if st.button("피드백 분석하기"):
            if not feedback_input.strip():
                st.warning("피드백을 입력하세요.")
            else:
                feedbacks = [f.strip() for f in feedback_input.strip().split("\n") if f.strip()]
                analysis_results = analyze_feedback_with_phase(lesson_plan, feedbacks)
                for res in analysis_results:
                    st.markdown(f"**피드백:** {res['피드백']}")
                    st.markdown(f"- 감정 키워드: 긍정 {res['긍정어']} / 부정 {res['부정어']}")
                    st.markdown(f"- 관련 단계: {res['단계']}")
                    st.markdown("---")
