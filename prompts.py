PROMPTS = {
    # Prompt dịch cơ bản
    'BASIC_TRANSLATION': """Translate this English text to Vietnamese for The Sims 4 game localization. 
Keep the translation casual and friendly, suitable for gaming context. 
Maintain any game-specific terms. Only return the Vietnamese translation, nothing else: {text}""",

    # Prompt dịch với ngữ cảnh game
    'GAMING_CONTEXT': """Translate this English text to Vietnamese, specifically for The Sims 4 game:
- Keep the tone casual and friendly
- Maintain all game mechanics terms
- Use natural Vietnamese gaming language
- Return only the translation
Text to translate: {text}""",

    # Prompt dịch với hướng dẫn chi tiết
    'DETAILED_INSTRUCTION': """Translate to Vietnamese (The Sims 4):
- Use informal pronouns (tôi, bạn, etc.)
- Keep special characters and formatting
- Maintain game terms in original form
- Make it sound natural to Vietnamese gamers
- Only output the translation
Original text: {text}""",

    # Prompt ngắn gọn
    'CONCISE': """Vietnamese translation for Sims 4 (casual tone, gaming context): {text}"""
}

# Prompt mặc định đang sử dụng
DEFAULT_PROMPT = PROMPTS['BASIC_TRANSLATION']

def get_prompt_by_type(prompt_type):
    """
    Lấy prompt theo loại được chọn
    Các loại: 'basic', 'gaming', 'detailed', 'concise'
    """
    prompt_mapping = {
        'basic': PROMPTS['BASIC_TRANSLATION'],
        'gaming': PROMPTS['GAMING_CONTEXT'],
        'detailed': PROMPTS['DETAILED_INSTRUCTION'],
        'concise': PROMPTS['CONCISE']
    }
    return prompt_mapping.get(prompt_type, DEFAULT_PROMPT)

def list_available_prompts():
    """
    Hiển thị danh sách các prompt có sẵn
    """
    print("\nCác loại prompt có sẵn:")
    print("1. basic    - Prompt dịch cơ bản")
    print("2. gaming   - Prompt với ngữ cảnh game")
    print("3. detailed - Prompt với hướng dẫn chi tiết")
    print("4. concise  - Prompt ngắn gọn\n") 