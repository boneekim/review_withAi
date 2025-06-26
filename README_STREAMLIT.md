# 🤖 멀티 AI 체험단 작성 프로그램 (Streamlit 버전)

OpenAI GPT와 Google Gemini를 활용하여 체험단 응모글과 리뷰를 자동 생성하는 웹 애플리케이션입니다.

## 🚀 온라인 배포 방법

### 1. Streamlit Cloud 배포 (추천)

1. **GitHub 저장소 생성**
   - 이 프로젝트를 GitHub에 업로드
   - 필수 파일: `app.py`, `requirements.txt`, `.streamlit/config.toml`

2. **Streamlit Cloud 배포**
   - [share.streamlit.io](https://share.streamlit.io) 접속
   - GitHub 계정으로 로그인
   - "New app" 클릭
   - 저장소 선택 후 배포

3. **자동 배포 완료**
   - 몇 분 후 공개 URL 생성
   - 누구나 접속 가능한 웹 서비스 완성

### 2. 기타 배포 플랫폼

#### Heroku
```bash
# Procfile 생성
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# 배포
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### Railway
```bash
# railway.json 생성 후 Railway에 연결
```

#### Render
- GitHub 저장소 연결
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## 💻 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

## 🎯 주요 기능

- 🧠 **멀티 AI 지원**: OpenAI GPT, Google Gemini
- ✏️ **다양한 글 유형**: 체험단 응모글, 체험 후기
- 🎨 **반응형 디자인**: 모바일/데스크톱 최적화
- 📋 **원클릭 복사**: 생성된 텍스트 쉽게 복사
- ⚡ **빠른 생성**: 5-15초 내 결과 생성
- 🔒 **보안**: API 키는 브라우저에서만 처리

## 📱 사용 방법

1. **AI 모델 선택**: Gemini(무료) 또는 OpenAI(고품질)
2. **API 키 입력**: OpenAI 사용 시에만 필요
3. **상품 정보 입력**: 체험하고 싶은 상품/서비스 설명
4. **글 유형 선택**: 응모글 또는 후기
5. **생성 버튼 클릭**: AI가 자동으로 글 작성

## 🔧 설정

### API 키 발급
- **OpenAI**: https://platform.openai.com/api-keys
- **Gemini**: 자동 연결 (무료)

### 비용 안내
- **Gemini**: 완전 무료 (일일 한도 내)
- **OpenAI**: 약 $0.002/요청 (매우 저렴)

## 📂 프로젝트 구조

```
review_withAi/
├── app.py                 # 메인 Streamlit 애플리케이션
├── requirements.txt       # Python 의존성
├── .streamlit/
│   └── config.toml       # Streamlit 설정
├── README_STREAMLIT.md   # 이 파일
└── (기타 기존 파일들)
```

## 🛠️ 개발자 정보

- **프레임워크**: Streamlit
- **AI API**: OpenAI GPT-3.5, Google Gemini
- **언어**: Python 3.8+
- **배포**: Streamlit Cloud, Heroku, Railway, Render

## 📞 지원

문제가 있으시면 GitHub Issues를 통해 문의해주세요.

---

🎉 **이제 전 세계 누구나 접속 가능한 웹 서비스가 됩니다!** 