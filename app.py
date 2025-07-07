import streamlit as st
import requests
import json
import time

# 페이지 설정
st.set_page_config(
    page_title="🤖 멀티 AI 체험단 작성 프로그램",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.experience-links {
    background: linear-gradient(45deg, #ff6b35, #f7931e);
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
}

.ai-model-section {
    background: #f0f4ff;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #d1d9ff;
    margin-bottom: 1.5rem;
}

.cost-info {
    background: #fffbeb;
    border: 1px solid #fde68a;
    padding: 1rem;
    border-radius: 8px;
    margin-top: 1rem;
    color: #92400e;
}

.result-container {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 1.5rem;
    margin-top: 1rem;
}

.success-message {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #16a34a;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.error-message {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# OpenAI API 호출 함수
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

# Gemini API 호출 함수
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

# 메인 헤더
st.markdown("""
<div class="main-header">
    <h1>🤖 멀티 AI 체험단 작성 프로그램</h1>
    <p>OpenAI, Gemini 중 선택하여 체험단 응모글과 리뷰를 자동 생성합니다</p>
</div>
""", unsafe_allow_html=True)

# 체험단/서평단 링크 섹션
st.markdown("""
<div class="experience-links">
    <h3 style="color: white; margin-bottom: 1rem;">🔗 바로가기 링크</h3>
    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
        <a href="https://shopping.naver.com/plan2/p/experience.nhn" target="_blank" 
           style="background: linear-gradient(45deg, #00d4aa, #00b894); color: white; padding: 1rem 2rem; 
                  border-radius: 25px; text-decoration: none; font-weight: bold;">
            🛍️ 뷰티체험 진행
        </a>
        <a href="https://shopping.naver.com/my/free-trial?isPrizeWinner=yes" target="_blank"
           style="background: linear-gradient(45deg, #fdcb6e, #e17055); color: white; padding: 1rem 2rem; 
                  border-radius: 25px; text-decoration: none; font-weight: bold;">
            🎉 당첨확인
        </a>
        <a href="https://event.yes24.com/reviewerClub" target="_blank"
           style="background: linear-gradient(45deg, #6c5ce7, #a29bfe); color: white; padding: 1rem 2rem; 
                  border-radius: 25px; text-decoration: none; font-weight: bold;">
            📚 서평단 모집
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# AI 모델 선택 (숨김 처리 - 기본값 Gemini 사용)
ai_model = "gemini"  # 기본값으로 Gemini 사용
api_key = "auto"     # Gemini 자동 연결

# 메인 콘텐츠 - 단일 컬럼 레이아웃
# 1. 글 유형 선택 (제일 상단)
st.markdown("### ✏️ 글 유형 선택")
content_type = st.radio(
    "원하는 글 유형을 선택하세요:",
    ["application", "review"],
    format_func=lambda x: "📝 체험단 응모글" if x == "application" else "⭐ 체험 후기/리뷰",
    horizontal=True
)

# 2. 상품 정보 입력
st.markdown("### 📦 상품/서비스 정보")
product_info = st.text_area(
    "체험하고 싶은 상품이나 서비스에 대해 자세히 설명해주세요:",
    placeholder="새로운 스킨케어 제품, 건강식품, 전자제품, 맛집 등\n\n상세할수록 더 좋은 결과를 얻을 수 있습니다!",
    height=120
)

# 3. URL 입력 (체험단 응모글일 때만)
url_content = ""
if content_type == "application":
    st.markdown("### 🔗 URL 입력 (선택)")
    
    # session state 초기화
    if 'url_input' not in st.session_state:
        st.session_state.url_input = ""
    
    url_content = st.text_input(
        "추가하고 싶은 URL이나 링크:",
        value=st.session_state.url_input,
        placeholder="예: https://example.com 또는 기타 링크",
        help="입력한 URL은 생성된 결과 맨 위에 표시됩니다.",
        key="url_input_field"
    )

# 4. 추가 요청사항
st.markdown("### 💡 추가 요청사항 (선택)")

# 글 유형에 따라 다른 기본값 설정
if content_type == "review":
    default_additional_info = '맨앞에 "예스24 리뷰어클럽 서평단 자격으로 도서를 제공받고 작성한 리뷰입니다."를 추가해줘.\n마지막에 "리뷰어클럽리뷰" 를 추가해줘.'
else:
    default_additional_info = '맨앞에 "소식받기, 상품찜, 공유 완료!"를 추가해줘.\n그리고 3-5줄 정도 짧은 글로 간절함과 경험 바탕으로 신청 사유를 작성해줘.\n젊은 말투로 존경어는 써서 정중하게 써줘.'

additional_info = st.text_area(
    "특별한 요구사항이나 포함했으면 하는 내용:",
    value=default_additional_info,
    placeholder="특정 연령대 대상, 특별한 상황, 강조하고 싶은 포인트 등",
    height=100
)

# 5. 생성 버튼
generate_btn = st.button(
    "✨ AI로 생성하기",
    type="primary",
    use_container_width=True
)

# 생성 로직
if generate_btn:
    # 입력 검증
    if ai_model == "openai" and not api_key:
        st.error("❌ OpenAI API 키를 입력해주세요.")
    elif not product_info.strip():
        st.error("❌ 상품/서비스 정보를 입력해주세요.")
    else:
        try:
            # 로딩 표시
            with st.spinner(f'🤖 {ai_model.upper()}가 글을 작성하고 있습니다... (5-15초 소요)'):
                # 시스템 프롬프트 설정
                is_application = content_type == 'application'
                
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

                user_prompt = f"""상품/서비스 정보: {product_info}

{f"추가 요청사항: {additional_info}" if additional_info.strip() else ""}

위 정보를 바탕으로 {"체험단 응모글" if is_application else "체험 후기/리뷰"}을 작성해주세요."""

                # AI 모델별 호출
                if ai_model == 'openai':
                    generated_content = call_openai(api_key, system_prompt, user_prompt)
                else:  # gemini
                    generated_content = call_gemini(api_key, system_prompt, user_prompt)
                
                # 결과 표시
                st.success(f"🎉 {ai_model.upper()}로 성공적으로 생성되었습니다!")
                
                # URL 입력폼 초기화 (체험단 응모글인 경우)
                if content_type == "application" and 'url_input' in st.session_state:
                    st.session_state.url_input = ""
                
                st.markdown("### 📄 생성된 결과")
                
                # URL 내용이 있으면 AI 생성 내용 앞에 추가
                final_content = ""
                if url_content and url_content.strip():
                    final_content = f"{url_content.strip()}\n\n{generated_content}"
                else:
                    final_content = generated_content
                
                # 결과 컨테이너
                result_container = st.container()
                with result_container:
                    st.markdown(f"""
                    <div class="result-container">
                    <div style="color: #666; font-size: 0.9em; margin-bottom: 1rem;">Generated by {ai_model.upper()}</div>
                    <div style="line-height: 1.6; white-space: pre-wrap;">{final_content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 복사 버튼
                    st.markdown("### 📋 복사하기")
                    
                    # Streamlit의 code 컴포넌트를 활용한 복사 기능
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        if st.button("📋 클립보드에 복사", type="primary", use_container_width=True):
                            # JavaScript를 사용한 클립보드 복사
                            copy_script = f"""
                            <script>
                            (function() {{
                                const text = {json.dumps(final_content)};
                                if (navigator.clipboard && window.isSecureContext) {{
                                    navigator.clipboard.writeText(text).then(() => {{
                                        alert('✅ 클립보드에 복사되었습니다!');
                                    }}).catch(() => {{
                                        fallbackCopy(text);
                                    }});
                                }} else {{
                                    fallbackCopy(text);
                                }}
                                
                                function fallbackCopy(text) {{
                                    const textArea = document.createElement('textarea');
                                    textArea.value = text;
                                    textArea.style.position = 'fixed';
                                    textArea.style.left = '-999999px';
                                    textArea.style.top = '-999999px';
                                    document.body.appendChild(textArea);
                                    textArea.focus();
                                    textArea.select();
                                    try {{
                                        document.execCommand('copy');
                                        alert('✅ 클립보드에 복사되었습니다!');
                                    }} catch (err) {{
                                        alert('❌ 복사에 실패했습니다. 내용을 직접 선택해서 복사해주세요.');
                                    }}
                                    document.body.removeChild(textArea);
                                }}
                            }})();
                            </script>
                            """
                            st.markdown(copy_script, unsafe_allow_html=True)
                    
                    # 코드 블록으로 내용 표시 (자동 복사 버튼 포함)
                    st.code(final_content, language=None)
                
        except requests.exceptions.Timeout:
            st.error("❌ API 요청 시간이 초과되었습니다. 다시 시도해주세요.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ 네트워크 오류: {str(e)}")
        except Exception as e:
            st.error(f"❌ {str(e)}")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
🤖 멀티 AI 체험단 작성 프로그램 | 
<a href="https://github.com" target="_blank">GitHub</a> | 
Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True) 