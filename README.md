# 📚 AI 학습 자동화 시스템

Streamlit 기반의 AI 학습 지원 도구입니다. PDF 및 문서 요약, 다국어 번역, GPT 노트 자동화, 진도 관리, Hugging Face 챗봇 기능을 포함합니다.

## 🚀 실행 방법

### 1. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. API 키 설정

#### ▶️ 로컬 실행
`.env` 파일에 다음과 같이 작성:
```env
OPENAI_API_KEY=your-openai-api-key
HF_API_TOKEN=your-huggingface-token (선택)
```

#### ▶️ Streamlit Cloud 배포
`.streamlit/secrets.toml` 파일 생성:
```toml
OPENAI_API_KEY = "your-openai-api-key"
HF_API_TOKEN = "your-huggingface-token"  # optional
```

### 3. 앱 실행
```bash
streamlit run app.py
```

## 📦 기능 요약

- 📘 GPT 번역기 (한글 ↔ 영어 ↔ 한자)
- 📤 파일 업로드 → 자동 요약 및 노트 저장
- 📒 노트 작성/편집/검색
- 📊 진도 관리 대시보드
- 🤖 Hugging Face 무료 챗봇 통합
- 📚 PDF 개념/사례 추출기

---

## 🔐 보안 주의
- `.env`와 `.streamlit/secrets.toml`은 `.gitignore`에 포함되어야 합니다.