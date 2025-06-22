import streamlit as st
import json
from datetime import datetime
from transformers import pipeline

# 페이지 기본 설정
st.set_page_config(page_title="AI 수업 설계 도우미", layout="wide")
st.title("📘 AI 기반 수업 설계 자동화 시스템 (고급형)")
st.markdown("---")

with st.expander("❓ 사용법 안내 보기"):
    st.markdown("""
    - 1단계: 과목, 주제, 학년, 수업 유형 선택
    - 2단계: 자동 생성된 수업 목표 및 자료 확인
    - 3단계: 수업 설계안 및 교사용 설명 확인
    - 4단계: 학생 피드백 입력 및 감정 분석 → 개선안 확인
    """)

# 감정 분석 파이프라인 캐시로 로드
@st.cache_resource
def load_sentiment_pipeline():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

classifier = load_sentiment_pipeline()

# 내장된 학습 목표 데이터
goal_bank = {
    "과학": {
        "생물과 환경": {
            "초등": ["생물 간 상호작용을 설명할 수 있다.", "생태계 구성 요소를 관찰할 수 있다."],
            "중등": ["생태계의 에너지 흐름을 설명할 수 있다.", "물질 순환 과정을 설명할 수 있다."],
            "고등": ["생태계 평형 가능성을 이해하고 예측할 수 있다."]
        },
        "물질의 성질": {
            "초등": ["물질의 상태변화를 관찰할 수 있다."],
            "중등": ["혼합물과 순물질을 구별할 수 있다."],
            "고등": ["화학 반응의 법칙을 설명할 수 있다."]
        }
    },
    "사회": {
        "지리와 환경": {
            "초등": ["지역의 자연환경을 설명할 수 있다."],
            "중등": ["기후에 따른 생활 모습을 설명할 수 있다."],
            "고등": ["인간과 환경의 상호작용을 분석할 수 있다."]
        }
    },
    "국어": {
        "설명문 읽기": {
            "초등": ["중심 생각을 파악할 수 있다."],
            "중등": ["설명 방식의 특징을 이해할 수 있다."],
            "고등": ["논리적 전개 방식의 효과를 분석할 수 있다."]
        }
    },
    "영어": {
        "자기소개": {
            "초등": ["자기소개 문장을 말할 수 있다."],
            "중등": ["자신을 영어로 소개할 수 있다."],
            "고등": ["자기소개서를 영어로 작성할 수 있다."]
        }
    }
}

# 수업 자료 추천 데이터
materials = {
    "생물과 환경": ["생태계 시뮬레이션 활동지", "먹이사슬 보드게임", "생물 관찰 영상"],
    "물질의 성질": ["상태 변화 관찰 실험 도구", "혼합물 실험 키트", "화학 반응 시뮬레이터"],
    "지리와 환경": ["세계 기후 지도", "환경 다큐 영상", "지역 탐구 활동지"],
    "설명문 읽기": ["설명문 예문 모음", "중심 생각 찾기 활동지"],
    "자기소개": ["영어 자기소개 템플릿", "스피킹 연습 카드", "발표 영상 예시"]
}

def get_goals_ai(subject, topic, grade):
    return goal_bank.get(subject, {}).get(topic, {}).get(grade, ["(선택한 항목에 대한 성취기준 정보 없음)"])

def recommend_materials(topic):
    return materials.get(topic, ["추천 자료 없음"])

def generate_teacher_note(subject, topic, grade, goals, materials):
    goal_text = ", ".join(goals)
    materials_text = ", ".join(materials)
    note = (
        f"본 수업은 {subject} 과목의 '{topic}' 단원을 대상으로 하며, {grade} 학년 수준에 맞추어 설계되었습니다.\n"
        f"주요 학습 목표는 {goal_text}이며, 이는 교육과정 성취기준과 연계되어 있습니다.\n"
        f"효과적인 수업 진행을 위해 다음과 같은 자료를 활용할 것을 권장합니다: {materials_text}.\n"
        f"이 자료들은 학습자의 이해를 돕고 흥미를 높이기 위해 엄선되었습니다.\n"
        f"이 수업안을 통해 학생들의 적극적인 참여와 깊은 이해를 기대할 수 있습니다."
    )
    return note

type_explain = {
    "탐구 중심": "스스로 탐구하며 개념을 발견하도록 구성합니다.",
    "토의 중심": "주제에 대한 협력적 토의를 중심으로 전개합니다.",
    "개념 설명형": "명확한 설명과 예시 중심으로 수업을 전개합니다.",
    "프로젝트형": "문제 해결 프로젝트를 통해 협력을 강화합니다."
}

def generate_template(topic, lesson_type, goals, intro_time, main_time, outro_time, custom_activity):
    goal_text = "- " + "\n- ".join(goals)
    materials_list = recommend_materials(topic)
    materials_text = "- " + "\n- ".join(materials_list)
    teacher_note = generate_teacher_note(subject, topic, grade, goals, materials_list)
    return f"""
### 📘 수업 주제: {topic}

#### 🎯 학습 목표:
{goal_text}

#### 🧭 수업 유형: {lesson_type}
- {type_explain.get(lesson_type, "")}

#### ⏱️ 수업 구성:
- **도입 ({intro_time}분)**: 동기 유발 자극 제시 및 집중 유도
- **전개 ({main_time}분)**: {custom_activity or lesson_type} 활동 전개
- **정리 ({outro_time}분)**: 퀴즈 또는 마인드맵 정리

#### 📦 수업 자료 추천:
{materials_text}

---

#### 📝 교사용 설명
{teacher_note}
"""

# UI 시작
st.subheader("1️⃣ 수업 기본 정보 입력")
subject = st.selectbox("과목 선택", list(goal_bank.keys()))
topic_list = list(goal_bank.get(subject, {}).keys())
topic = st.selectbox("단원명 선택", topic_list) if topic_list else st.text_input("단원명 입력")
grade = st.selectbox("학년 수준 선택", ["초등", "중등", "고등"])
lesson_type = st.radio("수업 유형", list(type_explain.keys()))

st.markdown("---")
st.subheader("2️⃣ 수업 시간 및 활동 설정")

intro_time = st.number_input("도입 시간(분)", min_value=1, max_value=30, value=5)
main_time = st.number_input("전개 시간(분)", min_value=5, max_value=60, value=15)
outro_time = st.number_input("정리 시간(분)", min_value=1, max_value=30, value=5)
custom_activity = st.text_input("전개 활동 설명 (선택사항)", "")

if st.button("🚀 수업안 생성하기"):
    goals = get_goals_ai(subject, topic, grade)
    lesson_plan = generate_template(topic, lesson_type, goals, intro_time, main_time, outro_time, custom_activity)
    st.markdown(lesson_plan)
    st.session_state["current_plan"] = lesson_plan
    st.success("✅ 수업안이 성공적으로 생성되었습니다.")

st.markdown("---")
st.subheader("3️⃣ 학생 피드백 입력 및 수업 개선")

feedback = st.text_area("학생 피드백 입력 (예: 지루했어요, 너무 어려웠어요 등)", height=150)

if st.button("🧠 피드백 분석 및 수업 개선 제안"):
    if "current_plan" not in st.session_state:
        st.warning("먼저 수업안을 생성해주세요.")
    else:
        sentiment_result = classifier(feedback)
        st.markdown("### ✅ 감정 분석 결과")
        st.write(sentiment_result)

        modified_plan = st.session_state["current_plan"]
        label = sentiment_result[0]['label']

        if label == "NEGATIVE":
            if any(kw in feedback for kw in ["지루", "흥미없"]):
                modified_plan += "\n\n🎯 흥미 개선 제안: 게임 요소, 역할극, 실험 활동을 추가해보세요."
            if any(kw in feedback for kw in ["어렵", "이해 못"]):
                modified_plan += "\n\n🎯 난이도 조절: 쉬운 예시와 시각 자료(PPT, 영상 등)를 보완하고, 개별 질문 시간을 포함하세요."
            if any(kw in feedback for kw in ["시간 낭비", "비효율"]):
                modified_plan += "\n\n🎯 시간 개선 제안: 활동 전 목표 명확화, 활동 시간 최적화 검토."
            if any(kw in feedback for kw in ["자료 이해", "자료 어렵"]):
                modified_plan += "\n\n🎯 자료 보완 제안: 학습 자료를 그림, 도식화하여 시각적으로 구성해보세요."

        st.markdown("### 🔧 개선된 수업안")
        st.markdown(modified_plan)

        log = {
            "date": str(datetime.now()),
            "subject": subject,
            "topic": topic,
            "grade": grade,
            "lesson_type": lesson_type,
            "feedback": feedback,
            "plan": modified_plan
        }
        with open("lesson_history.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")

        st.success("💾 개선된 수업안이 저장되었습니다.")

