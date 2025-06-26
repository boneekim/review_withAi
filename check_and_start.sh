#!/bin/bash

# 🔍 서버 상태 확인 및 자동 시작 스크립트
echo "🔍 서버 상태를 확인합니다..."

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# 포트 8081이 사용 중인지 확인
if lsof -Pi :8081 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ 서버가 이미 실행 중입니다!"
    echo "📱 브라우저에서 http://localhost:8081 으로 접속하세요!"
    
    # 브라우저 자동 열기 (선택사항)
    open http://localhost:8081 2>/dev/null || true
else
    echo "❌ 서버가 실행되지 않고 있습니다."
    echo "🚀 서버를 시작합니다..."
    
    # 백그라운드에서 서버 시작
    nohup python3 server.py > server.log 2>&1 &
    
    # 서버 시작 대기
    echo "⏳ 서버 시작을 기다리는 중..."
    for i in {1..10}; do
        sleep 1
        if lsof -Pi :8081 -sTCP:LISTEN -t >/dev/null ; then
            echo "✅ 서버가 성공적으로 시작되었습니다!"
            echo "📱 브라우저에서 http://localhost:8081 으로 접속하세요!"
            
            # 브라우저 자동 열기
            open http://localhost:8081 2>/dev/null || true
            exit 0
        fi
        echo "   $i초 경과..."
    done
    
    echo "❌ 서버 시작에 실패했습니다. server.log를 확인해주세요."
    exit 1
fi 