import streamlit as st
import random
from transformers import pipeline

# 1) 감정 분석 모델 캐싱해서 로드
@st.cache_resource(show_spinner=True)
def load_sentiment_model():
    return pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

sentiment_model = load_sentiment_model()

# 2) 수업 목표 리스트
lesson_goals = [
    "자연 현상과 일상생활에 대한 흥미와 호기심을 바탕으로 문제를 인식하고 해결하는 태도 함양",
    "과학 탐구 방법을 이해하고 문제를 과학적으로 탐구하는 능력 기르기",
    "생태계의 개념을 이해하고 환경 문제 해결 의지 함양",
    "과학과 기술 및 사회의 상호 관계를 이해하고 참여적 시민의식 기르기"
]

# 3) 수업 활동 사전 (간단화)
lesson_methods = {
    "전반부": [
        ("흥미 유발 영상 시청", "영상 자료와 프로젝터를 활용하여 학생들의 흥미를 끌어냅니다."),
        ("생태계 관련 시각 자료 제공", "사진과 빔스크린으로 시각적 이해를 돕습니다."),
        ("간단한 퀴즈로 아이스브레이킹", "퀴즈지를 사용해 수업 참여를 유도합니다."),
        ("환경 문제 사례 이야기", "신문 스크랩을 활용해 실생활과 연결합니다.")
    ],
    "중반부": [
        ("생태계 오염 실험 활동", "간단한 실험 도구로 직접 체험하며 학습합니다."),
        ("먹이사슬 모형 만들기", "종이와 생물 카드를 사용해 먹이사슬을 이해합니다."),
        ("조사 활동 및 발표", "탐구 노트와 마이크로 조사 내용을 발표합니다."),
        ("환경 보호 아이디어 브레인스토밍", "칠판과 마인드맵으로 아이디어를 확장합니다.")
    ],
    "후반부": [
        ("과학 글쓰기", "학습지와 노트에 학습 내용을 정리합니다."),
        ("환경 캠페인 역할극", "역할 명찰과 소품을 활용해 활동을 생생하게 합니다."),
        ("토론 활동", "토론 주제 카드로 다양한 의견을 교환합니다."),
        ("퀴즈 또는 게임", "문제 카드로 재미있게 학습을 마무리합니다.")
    ]
}

# 4) 수업 설계 생성 함수
def generate_lesson_plan(topic):
    goal = random.choice(lesson_goals)
    plan = {
        "주제": topic,
        "목표": goal,
        "설명": f"이 수업은 '{topic}' 주제를 중심으로 하며, 주요 목표는 '{goal}'입니다. 수업은 도입, 전개, 정리 단계로 구성되어 학생 흥미 유도와 탐구 역량 강화를 목표로 합니다."
    }
    activities = {}
    for phase in ["전반부", "중반부", "후반부"]:
        method, method_desc = random.choice(lesson_methods[phase])
        activities[phase] = {"활동": method, "설명": method_desc}
    plan["활동"] = activities
    return plan

# 5) 웹 UI
st.set_page_config(page_title="AI 수업 설계 및 감정 분석", layout="wide")
st.title("📚 AI 기반 수업 설계 및 감정 분석 도우미")

# 입력: 수업 주제
topic = st.text_input("1️⃣ 수업 주제를 입력하세요 (예: 생물과 환경)")

if topic:
    # 수업 설계 생성
    plan = generate_lesson_plan(topic)

    st.markdown("### ▶️ 생성된 수업 설계")
    st.markdown(f"- **주제:** {plan['주제']}")
    st.markdown(f"- **수업 목표:** {plan['목표']}")
    st.markdown(f"- **수업 설계 근거:** {plan['설명']}")
    
    for phase in ["전반부", "중반부", "후반부"]:
        act = plan["활동"][phase]["활동"]
        desc = plan["활동"][phase]["설명"]
        st.markdown(f"**{phase} 활동:** {act}")
        st.caption(desc)

    st.markdown("---")
    st.markdown("### 2️⃣ 학생 피드백 감정 분석")
    feedback_input = st.text_area("학생 피드백을 여러 줄로 입력하세요 (예: '자료가 너무 어려웠어요', '활동이 재미있었어요')", height=150)

    if st.button("감정 분석 시작"):
        if not feedback_input.strip():
            st.warning("피드백 내용을 입력해주세요.")
        else:
            feedback_list = [fb.strip() for fb in feedback_input.strip().split("\n") if fb.strip()]
            st.markdown(f"총 {len(feedback_list)}개의 피드백 분석 결과:")

            for fb in feedback_list:
                result = sentiment_model(fb)[0]
                label = result['label']
                score = result['score']
                st.markdown(f"- **피드백:** {fb}")
                st.markdown(f"  - 감정 분석 결과: {label} (신뢰도: {score:.2f})")
                st.markdown("---")

# 6) 추가 아이디어
st.sidebar.title("💡 추가 기능 제안")
st.sidebar.markdown("""
- 수업 활동별 피드백 분류 및 개선 제안  
- 학생별 맞춤 수업 설계  
- 다양한 감정 분석 모델 비교  
- 수업 진행 상황 모니터링 대시보드  
- 교사용 요약 리포트 자동 생성  
""")
