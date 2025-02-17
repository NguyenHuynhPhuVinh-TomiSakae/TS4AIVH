PROMPTS = {
    # Prompt dịch cơ bản
    'BASIC_TRANSLATION': """You are a Vietnamese translator for The Sims 4 game.
IMPORTANT: YOU MUST ONLY RETURN THE VIETNAMESE TRANSLATION, NOTHING ELSE.
DO NOT:
- Repeat the English text
- Explain your translation
- Add any comments
- Add any analysis
- Add any notes

Rules:
- Keep all HTML-like tags exactly as they appear
- Preserve all placeholders and object references
- Do not translate content inside tags/placeholders
- Use casual and friendly tone

Text to translate: <<text>>""",

    # Prompt dịch với ngữ cảnh game
    'GAMING_CONTEXT': """You are translating for The Sims 4 game.
YOUR RESPONSE MUST CONTAIN ONLY THE VIETNAMESE TRANSLATION.
DO NOT INCLUDE:
- The original English text
- Any explanations
- Any comments
- Any analysis

Rules:
- Keep all tags and placeholders unchanged
- Use gaming-appropriate language
- Keep casual tone
- Preserve all formatting

Text: <<text>>""",

    # Prompt dịch với hướng dẫn chi tiết
    'DETAILED_INSTRUCTION': """You are a Sims 4 Vietnamese translator.
RESPOND WITH THE VIETNAMESE TRANSLATION ONLY.
DO NOT ADD:
- Original text
- Explanations
- Comments
- Notes
- Analysis

Rules:
- Keep all HTML tags and formatting
- Preserve all placeholders
- Use informal pronouns
- Natural gaming language

Text: <<text>>""",

    # Prompt ngắn gọn
    'CONCISE': """RETURN ONLY VIETNAMESE TRANSLATION, NO OTHER TEXT. Keep tags/placeholders: <<text>>"""
}

# Prompt mặc định đang sử dụng
DEFAULT_PROMPT = PROMPTS['BASIC_TRANSLATION']

def get_prompt_by_type(prompt_type):
    """
    Lấy prompt theo loại được chọn và thay thế text an toàn
    """
    prompt_mapping = {
        'basic': PROMPTS['BASIC_TRANSLATION'],
        'gaming': PROMPTS['GAMING_CONTEXT'],
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
    print("2. gaming   - Prompt với ngữ cảnh game")
    print("3. detailed - Prompt với hướng dẫn chi tiết")
    print("4. concise  - Prompt ngắn gọn\n") 