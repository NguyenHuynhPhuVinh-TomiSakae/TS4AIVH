import xml.etree.ElementTree as ET
import google.generativeai as genai
import os
import time
import json
from dotenv import load_dotenv
from prompts import DEFAULT_PROMPT, get_prompt_by_type, list_available_prompts

# Tải biến môi trường từ file .env
load_dotenv()

# Cấu hình Gemini API sử dụng key từ env
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

def load_translation_cache(cache_file):
    """Đọc cache từ file JSON"""
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_translation_cache(cache_file, cache):
    """Lưu cache vào file JSON"""
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def load_request_count(count_file):
    """Đọc số request đã thực hiện"""
    if os.path.exists(count_file):
        with open(count_file, 'r') as f:
            return int(f.read().strip())
    return 0

def save_request_count(count_file, count):
    """Lưu số request đã thực hiện"""
    with open(count_file, 'w') as f:
        f.write(str(count))

def translate_text(text, translation_cache, cache_file, count_file, request_count, prompt_type='basic'):
    """Dịch văn bản sử dụng Gemini với retry và delay"""
    if text in translation_cache:
        print(f"Đã tìm thấy trong cache: {text}")
        return translation_cache[text], request_count

    if request_count >= 1500:
        raise Exception("Đã đạt giới hạn 1500 request. Dừng chương trình.")

    max_retries = 3
    retry_delay = 5
    
    time.sleep(4)

    for attempt in range(max_retries):
        try:
            print(f"\nRequest số {request_count + 1}")
            print(f"Đang dịch: {text}")
            prompt = get_prompt_by_type(prompt_type).format(text=text)
            
            response = model.generate_content(prompt)
            translated = response.text.strip()
            print(f"Bản dịch: {translated}")
            
            request_count += 1
            save_request_count(count_file, request_count)
            
            translation_cache[text] = translated
            save_translation_cache(cache_file, translation_cache)
            
            return translated, request_count
        except Exception as e:
            if "Đã đạt giới hạn 1500 request" in str(e):
                raise e
            if attempt < max_retries - 1:
                print(f"Lỗi: {e}. Thử lại sau {retry_delay} giây...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print(f"Không thể dịch text sau {max_retries} lần thử. Dừng chương trình.")
                raise e

def process_xml(input_file, output_file, cache_file, count_file):
    """
    Các tham số đã được đổi tên để khớp với cách gọi:
    - input_file thay vì input_path
    - output_file thay vì output_path
    """
    print(f"\nBắt đầu xử lý file {input_file}")
    
    # Tải cache và số request
    translation_cache = load_translation_cache(cache_file)
    request_count = load_request_count(count_file)
    print(f"Số request đã thực hiện: {request_count}")
    
    if request_count >= 1500:
        print("Đã đạt giới hạn 1500 request. Không thể tiếp tục.")
        return
    
    # Kiểm tra file output đã tồn tại
    if os.path.exists(output_file):
        print(f"Đọc file output hiện có: {output_file}")
        existing_tree = ET.parse(output_file)
        existing_root = existing_tree.getroot()
        # Tạo dict các bản dịch đã có
        existing_translations = {elem.get('Key'): elem.text for elem in existing_root.findall('Text')}
    else:
        existing_translations = {}

    # Đọc file input
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Tạo root mới cho output
    new_root = ET.Element('STBLKeyStringList')
    
    total_elements = len(root.findall('Text'))
    print(f"Tổng số phần tử cần dịch: {total_elements}")
    
    try:
        for index, text_elem in enumerate(root.findall('Text'), 1):
            key = text_elem.get('Key')
            original_text = text_elem.text
            
            print(f"\nXử lý phần tử {index}/{total_elements}")
            
            if key in existing_translations:
                translated_text = existing_translations[key]
                print(f"Đã có bản dịch cho key {key}")
            else:
                translated_text, request_count = translate_text(
                    original_text, 
                    translation_cache, 
                    cache_file,
                    count_file,
                    request_count
                )
            
            new_elem = ET.Element('Text')
            new_elem.set('Key', key)
            new_elem.text = translated_text
            new_root.append(new_elem)
            
            # Lưu file sau mỗi lần dịch thành công
            tree = ET.ElementTree(new_root)
            tree.write(output_file, encoding='UTF-8', xml_declaration=True)
            
    except Exception as e:
        print(f"Lỗi nghiêm trọng: {e}")
        print("Đã lưu các bản dịch đã hoàn thành. Có thể chạy lại để tiếp tục.")
        return

    print(f"\nĐã hoàn thành! Kết quả được lưu vào {output_file}")

def get_file_paths(package_name):
    """Tạo đường dẫn cho các file dựa trên tên gói"""
    base_path = f"{package_name}/{package_name}"
    return {
        'input': f"{base_path}.xml",
        'output': f"{base_path}_vietnamese.xml",
        'cache': f"{package_name}/translation_cache.json",
        'count': "total_request_count.txt"
    }

def main():
    list_available_prompts()
    prompt_type = input("Chọn loại prompt (nhập tên hoặc số thứ tự): ").lower()
    
    # Chuyển đổi số thứ tự sang tên prompt
    prompt_number_mapping = {
        '1': 'basic',
        '2': 'gaming',
        '3': 'detailed',
        '4': 'concise'
    }
    
    if prompt_type in prompt_number_mapping:
        prompt_type = prompt_number_mapping[prompt_type]
    
    package_name = input("Nhập tên gói (ví dụ: SP58): ").strip()
    paths = get_file_paths(package_name)
    
    # Sửa lại tên tham số khi gọi hàm để khớp với định nghĩa
    process_xml(
        input_file=paths['input'],
        output_file=paths['output'],
        cache_file=paths['cache'],
        count_file=paths['count']
    )

if __name__ == "__main__":
    main()
