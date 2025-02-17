PROMPTS = {
    # Prompt dịch cơ bản
    'BASIC_TRANSLATION': """You are a Vietnamese translator for The Sims 4.
RETURN ONLY THE VIETNAMESE TRANSLATION.
- Keep all tags and placeholders unchanged
- Use casual Vietnamese tone

<<text>>""",

    # Prompt dịch với ngữ cảnh game
    'BASIC_TRANSLATION_FROM': """You are a Vietnamese translator for The Sims 4.
RETURN ONLY THE VIETNAMESE TRANSLATION.
- Keep all tags and placeholders unchanged
- Keep (FROM...) structure unchanged
- Use casual Vietnamese tone

<<text>>""",

    # Prompt dịch với hướng dẫn chi tiết
    'DETAILED_INSTRUCTION': """RETURN ONLY THE VIETNAMESE TRANSLATION.
- Keep all tags and placeholders unchanged
- Keep (FROM...) structure unchanged
- Use casual Vietnamese gaming tone
- No explanations or English text

<<text>>""",

    # Prompt ngắn gọn
    'CONCISE': """VIETNAMESE TRANSLATION ONLY. Keep tags/placeholders/FROM: <<text>>"""
}

# Prompt mặc định đang sử dụng
DEFAULT_PROMPT = PROMPTS['BASIC_TRANSLATION_FROM']

def get_prompt_by_type(prompt_type):
    """
    Lấy prompt theo loại được chọn và thay thế text an toàn
    """
    prompt_mapping = {
        'basic': PROMPTS['BASIC_TRANSLATION'],
        'basic_from': PROMPTS['BASIC_TRANSLATION_FROM'],
        'detailed': PROMPTS['DETAILED_INSTRUCTION'],
        'concise': PROMPTS['CONCISE']
    }
    prompt_template = prompt_mapping.get(prompt_type, DEFAULT_PROMPT)
    return prompt_template.replace('<<text>>', '{text}')

def list_available_prompts():
    """
    Hiển thị danh sách các prompt có sẵn
    """
    print("\nCác loại prompt có sẵn:")
    print("1. basic    - Prompt dịch cơ bản")
    print("2. basic_from - Prompt dịch cơ bản fix (FROM...)")
    print("3. detailed - Prompt với hướng dẫn chi tiết")
    print("4. concise  - Prompt ngắn gọn\n") 