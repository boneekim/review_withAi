# 🤖 멀티 AI 체험단 작성 프로그램

## 🚀 자동 시작 설정 완료!

이제 다음 방법들로 서버를 자동으로 시작할 수 있습니다:

### 1. ✅ 시스템 부팅 시 자동 시작 (설정 완료)
- 컴퓨터를 켤 때마다 서버가 자동으로 시작됩니다
- 별도 설정 없이 바로 http://localhost:8081 접속 가능

### 2. 📱 빠른 시작 방법들

#### 방법 1: 스마트 시작 스크립트 (추천)
```bash
./check_and_start.sh
```
- 서버 상태를 확인하고 필요시 자동 시작
- 브라우저까지 자동으로 열어줍니다!

#### 방법 2: 기본 시작 스크립트
```bash
./start_server.sh
```
- 서버를 직접 시작합니다

### 3. 🔧 서비스 관리 명령어

#### 서비스 중지
```bash
launchctl unload ~/Library/LaunchAgents/com.review.withAi.plist
```

#### 서비스 재시작
```bash
launchctl unload ~/Library/LaunchAgents/com.review.withAi.plist
launchctl load ~/Library/LaunchAgents/com.review.withAi.plist
```

#### 서비스 완전 제거
```bash
launchctl unload ~/Library/LaunchAgents/com.review.withAi.plist
rm ~/Library/LaunchAgents/com.review.withAi.plist
```

## 📱 사용 방법

1. **자동 시작**: 컴퓨터를 켜면 자동으로 서버가 시작됩니다
2. **접속**: http://localhost:8081 으로 브라우저에서 접속
3. **모바일 접속**: 같은 WiFi에서 `컴퓨터IP주소:8081`로 접속

## 🛠️ 문제 해결

### 서버가 시작되지 않을 때
1. 터미널에서 확인:
   ```bash
   lsof -i :8081
   ```

2. 로그 확인:
   ```bash
   tail -f server.log
   ```

3. 수동 시작:
   ```bash
   ./check_and_start.sh
   ```

### 포트가 이미 사용 중일 때
```bash
# 기존 프로세스 종료
pkill -f "python.*server.py"
# 다시 시작
./check_and_start.sh
```

## 🎯 주요 기능

- 🧠 **멀티 AI 지원**: OpenAI GPT, Gemini
- ✏️ **다양한 글 유형**: 체험단 응모글, 체험 후기
- 🎨 **깔끔한 UI**: 모바일 친화적 디자인
- 📋 **원클릭 복사**: 생성된 텍스트 바로 복사
- ⚡ **빠른 생성**: 5-15초 내 결과 생성

## 📞 지원

문제가 있으시면 `server.log` 파일을 확인하거나, 터미널에서 직접 `python3 server.py`를 실행해서 오류 메시지를 확인해보세요. 