#!/bin/bash

# 🚀 멀티 AI 체험단 서버 시작 스크립트
echo "🎯 멀티 AI 체험단 서버를 시작합니다..."

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# 기존 서버 프로세스 종료
echo "🔄 기존 서버 프로세스 확인 중..."
pkill -f "python.*server.py" 2>/dev/null || true

# 잠시 대기
sleep 2

# 서버 시작
echo "🚀 서버 시작 중..."
python3 server.py

echo "✅ 서버가 시작되었습니다!"
echo "📱 브라우저에서 http://localhost:8081 으로 접속하세요!" 