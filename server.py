#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import json

app = Flask(__name__)

# CORS 허용
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 정적 파일 제공
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# Figma API 호출
def call_figma_api(token, file_key):
    """Figma 파일 정보를 가져오는 함수"""
    if not token or not file_key:
        raise Exception('Figma 토큰과 파일 키가 필요합니다.')
    
    headers = {
        'X-Figma-Token': token
    }
    
    # Figma 파일 정보 가져오기
    file_url = f'https://api.figma.com/v1/files/{file_key}'
    response = requests.get(file_url, headers=headers, timeout=30)
    
    if response.status_code == 403:
        raise Exception('Figma 토큰이 유효하지 않거나 파일에 접근 권한이 없습니다.')
    elif response.status_code == 404:
        raise Exception('Figma 파일을 찾을 수 없습니다. 파일 키를 확인해주세요.')
    elif not response.ok:
        raise Exception(f'Figma API 오류: {response.status_code}')
    
    return response.json()

def extract_figma_design_info(figma_data):
    """Figma 데이터에서 디자인 정보를 추출하는 함수"""
    try:
        file_name = figma_data.get('name', '알 수 없는 파일')
        pages = figma_data.get('document', {}).get('children', [])
        
        design_info = {
            'file_name': file_name,
            'pages': [],
            'components': [],
            'colors': [],
            'text_content': []
        }
        
        def traverse_nodes(nodes, depth=0):
            for node in nodes:
                node_type = node.get('type', '')
                node_name = node.get('name', '')
                
                # 페이지 정보
                if node_type == 'CANVAS':
                    design_info['pages'].append(node_name)
                
                # 컴포넌트 정보
                elif node_type == 'COMPONENT':
                    design_info['components'].append({
                        'name': node_name,
                        'type': node_type
                    })
                
                # 텍스트 내용
                elif node_type == 'TEXT':
                    if 'characters' in node:
                        design_info['text_content'].append(node['characters'])
                
                # 색상 정보
                if 'fills' in node:
                    for fill in node['fills']:
                        if fill.get('type') == 'SOLID' and 'color' in fill:
                            color = fill['color']
                            rgb = f"rgb({int(color.get('r', 0)*255)}, {int(color.get('g', 0)*255)}, {int(color.get('b', 0)*255)})"
                            if rgb not in design_info['colors']:
                                design_info['colors'].append(rgb)
                
                # 자식 노드 탐색
                if 'children' in node:
                    traverse_nodes(node['children'], depth + 1)
        
        traverse_nodes(pages)
        return design_info
        
    except Exception as e:
        raise Exception(f'Figma 데이터 분석 중 오류: {str(e)}')

# OpenAI API 호출
def call_openai(api_key, system_prompt, user_prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        'max_tokens': 1500,
        'temperature': 0.7
    }
    
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 401:
        raise Exception('OpenAI API 키가 유효하지 않습니다.')
    elif response.status_code == 429:
        raise Exception('OpenAI API 사용 한도를 초과했습니다. 잠시 후 다시 시도하거나 다른 AI 모델을 사용해보세요.')
    elif not response.ok:
        error_msg = 'OpenAI 서버 오류가 발생했습니다.'
        try:
            error_data = response.json()
            if 'error' in error_data and 'message' in error_data['error']:
                error_msg = error_data['error']['message']
        except:
            pass
        raise Exception(error_msg)
    
    result = response.json()
    return result['choices'][0]['message']['content']

# Gemini API 호출
def call_gemini(api_key, system_prompt, user_prompt):
    # 자동 Gemini API 키 사용
    if not api_key or api_key == 'auto':
        api_key = 'AIzaSyCF7cH-42NtbuDlDKllA_K9U-cbo4B0c6k'
    
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = {
        'contents': [
            {
                'parts': [
                    {'text': f'{system_prompt}\n\n{user_prompt}'}
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.7,
            'maxOutputTokens': 1500
        }
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 403:
        raise Exception('Gemini API 키가 유효하지 않거나 권한이 없습니다.')
    elif response.status_code == 429:
        raise Exception('Gemini API 사용 한도를 초과했습니다.')
    elif not response.ok:
        error_msg = 'Gemini 서버 오류가 발생했습니다.'
        try:
            error_data = response.json()
            if 'error' in error_data and 'message' in error_data['error']:
                error_msg = error_data['error']['message']
        except:
            pass
        raise Exception(error_msg)
    
    result = response.json()
    
    if 'candidates' not in result or len(result['candidates']) == 0:
        raise Exception('Gemini에서 응답을 생성하지 못했습니다.')
    
    return result['candidates'][0]['content']['parts'][0]['text']

# Figma 파일 정보 가져오기 API
@app.route('/api/figma-info', methods=['POST', 'OPTIONS'])
def get_figma_info():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.json
        figma_token = data.get('figmaToken')
        figma_file_key = data.get('figmaFileKey')
        
        if not figma_token or not figma_file_key:
            return jsonify({'error': 'Figma 토큰과 파일 키가 필요합니다.'}), 400
        
        # Figma API 호출
        figma_data = call_figma_api(figma_token, figma_file_key)
        
        # 디자인 정보 추출
        design_info = extract_figma_design_info(figma_data)
        
        return jsonify(design_info)
        
    except Exception as e:
        print(f"Figma API 오류: {e}")
        return jsonify({'error': str(e)}), 500

# 멀티 AI API 프록시
@app.route('/api/generate', methods=['POST', 'OPTIONS'])
def generate():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.json
        ai_model = data.get('aiModel', 'openai')
        api_key = data.get('apiKey')
        product_info = data.get('productInfo')
        content_type = data.get('contentType')
        additional_info = data.get('additionalInfo', '')
        
        # Figma 관련 데이터
        figma_info = data.get('figmaInfo')
        use_figma = data.get('useFigma', False)

        if not api_key or not product_info:
            return jsonify({'error': 'API 키와 상품 정보는 필수입니다.'}), 400

        is_application = content_type == 'application'
        
        # 기본 시스템 프롬프트
        if is_application:
            system_prompt = """당신은 체험단 응모글 작성 전문가입니다. 사용자가 제공한 상품/서비스 정보를 바탕으로 간결하고 진정성 있는 체험단 응모글을 작성해주세요. 

작성 가이드라인:
- 3-5줄 정도의 짧고 간결한 길이
- 간절함과 경험을 바탕으로 한 신청 사유
- 제품에 대한 관심과 열정을 간결하게 표현
- 체험 후 상세한 리뷰 작성 의지를 간략히 언급
- 정중하고 진실한 어조 사용
- 개인적인 경험이나 관심사를 자연스럽게 포함
- 한국어로 작성"""
        else:
            system_prompt = """당신은 체험 후기/리뷰 작성 전문가입니다. 사용자가 제공한 상품/서비스 정보를 바탕으로 상세하고 유용한 체험 후기를 작성해주세요.

작성 가이드라인:
- 제목, 첫인상, 사용 경험, 장단점, 총평 형식으로 구성
- 구체적이고 실질적인 정보 포함
- 마크다운 형식 사용 (제목은 #, ## 사용)
- 읽는 사람에게 도움이 되는 솔직한 후기
- 800-1200자 정도의 충분한 분량
- 한국어로 작성"""

        # Figma 정보가 있으면 시스템 프롬프트에 추가
        if use_figma and figma_info:
            figma_context = f"""

추가 디자인 정보 (Figma에서 가져온 정보):
- 파일명: {figma_info.get('file_name', '')}
- 페이지: {', '.join(figma_info.get('pages', []))}
- 컴포넌트: {', '.join([comp.get('name', '') for comp in figma_info.get('components', [])])}
- 주요 색상: {', '.join(figma_info.get('colors', [])[:5])}
- 텍스트 내용: {' / '.join(figma_info.get('text_content', [])[:3])}

위 디자인 정보를 참고하여 더욱 구체적이고 현실적인 글을 작성해주세요."""
            system_prompt += figma_context

        user_prompt = f"""상품/서비스 정보: {product_info}

{f"추가 요청사항: {additional_info}" if additional_info else ""}

위 정보를 바탕으로 {"체험단 응모글" if is_application else "체험 후기/리뷰"}을 작성해주세요."""

        # AI 모델별 호출
        if ai_model == 'openai':
            generated_content = call_openai(api_key, system_prompt, user_prompt)
        elif ai_model == 'gemini':
            generated_content = call_gemini(api_key, system_prompt, user_prompt)
        else:
            return jsonify({'error': '지원하지 않는 AI 모델입니다.'}), 400
        
        return jsonify({'content': generated_content})

    except requests.exceptions.Timeout:
        return jsonify({'error': 'API 요청 시간이 초과되었습니다. 다시 시도해주세요.'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'네트워크 오류: {str(e)}'}), 500
    except Exception as e:
        print(f"오류 발생: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🎯 멀티 AI 체험단 작성 프로그램 서버를 시작합니다...")
    print("📱 브라우저에서 http://localhost:8081 으로 접속하세요!")
    print("📱 모바일에서는 컴퓨터의 IP 주소:8081 으로 접속하세요!")
    print("⏹️  종료하려면 Ctrl+C를 누르세요.")
    print("=" * 50)
    
    # 네트워크 접근 가능하도록 host='0.0.0.0' 설정
    # debug=False로 설정하여 이중 프로세스 문제 방지
    app.run(host='0.0.0.0', port=8081, debug=False) 