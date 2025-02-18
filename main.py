import xml.etree.ElementTree as ET
import google.generativeai as genai
import os
import time
import json
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# Cấu hình cho model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

def init_chat():
    """Khởi tạo chat session với lịch sử mẫu"""
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config
    )
    
    chat = model.start_chat(history=[
    {
      "role": "user",
      "parts": [
        "You are a Vietnamese translator for The Sims 4.\nRETURN ONLY THE VIETNAMESE TRANSLATION.\n- Keep all tags and placeholders unchanged\n- Use casual Vietnamese tone\n\nTranslate to Vietnamese: This abstract sculpture doesn't have a specific shape intended. It's made to let you imagine what you want. Apparently some people see a llama in it.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Cái tượng trừu tượng này không có hình dáng cụ thể nào cả. Nó được làm ra để bạn tha hồ tưởng tượng đó. Nghe đâu có người còn nhìn ra con lạc đà không bướu trong đó nữa cơ.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "When translating nouns, avoid adding particles such as \"nè\", \"hả\", \"á\" at the end. For example, \"Ancient Bust\" should be translated as \"Tượng Cổ\", not \"Tượng Cổ nè\"\nTranslate to Vietnamese: Wishmaker",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Người Ước Nguyện\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "With the format (From...) when translating, keep it as (Từ...) for example: (From Designing Jewelry) -> (Từ Việc Thiết Kế Trang Sức)\nTranslate to Vietnamese: (From Crystal Crafter Aspiration)",
      ],
    },
    {
      "role": "model",
      "parts": [
        "(Từ Nguyện Vọng Chế Tạo Pha Lê)\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "All forms such as {M0.he}{F0.she} or {M0.his}{F0.her} or {F0.Lady}{M0.Lord} and other {M0.}, {F0.} MUST BE KEPT UNCHANGED.\nTranslate to Vietnamese: {0.SimFirstName} befriended a Dust Bunny! Since {M0.he}{F0.she} made {M0.his}{F0.her} fluffy companion feel so welcomed and cared for in {M0.his}{F0.her} house, this dust bunny will behave a bit differently. It can now survive in even the cleanest environments and will no longer be destroyed by cleaning around the house - it's here to stay. \\n\\nBefriended Dust Bunnies will also show their appreciation by finding rarer items and occasionally even digging up substantial piles of Simoleons. ",
      ],
    },
    {
      "role": "model",
      "parts": [
        "{0.SimFirstName} đã kết bạn với Thỏ Bụi! Vì {M0.he}{F0.she} đã làm cho người bạn lông xù của {M0.his}{F0.her} cảm thấy được chào đón và chăm sóc trong nhà của {M0.his}{F0.her}, nên thỏ bụi này sẽ cư xử hơi khác một chút. Giờ nó có thể sống sót ngay cả trong môi trường sạch sẽ nhất và sẽ không còn bị tiêu diệt khi dọn dẹp nhà cửa nữa - nó sẽ ở lại đây. \\n\\nThỏ Bụi đã kết bạn cũng sẽ thể hiện sự cảm kích bằng cách tìm kiếm những vật phẩm hiếm hơn và đôi khi thậm chí còn đào được những đống Simoleon đáng kể.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        " If there are multiple pieces of content to translate, return them as key-value pairs (KEY1, KEY2, etc.) according to the number of contents.\nKEY1-Translate to Vietnamese: Thank you for your hat donation. This will surely keep someone's head warm!\nKEY2-Translate to Vietnamese: {0.SimFirstName} befriended a Dust Bunny! Since {M0.he}{F0.she} made {M0.his}{F0.her} fluffy companion feel so welcomed and cared for in {M0.his}{F0.her} house, this dust bunny will behave a bit differently. It can now survive in even the cleanest environments and will no longer be destroyed by cleaning around the house - it's here to stay. \\n\\nBefriended Dust Bunnies will also show their appreciation by finding rarer items and occasionally even digging up substantial piles of Simoleons.\nKEY3-Translate to Vietnamese: (From Crystal Crafter Aspiration)\nKEY4-Translate to Vietnamese: Wishmaker\nKEY5-Translate to Vietnamese: {0.SimFirstName} befriended a Dust Bunny! Since {M0.he}{F0.she} made {M0.his}{F0.her} fluffy companion feel so welcomed and cared for in {M0.his}{F0.her} house, this dust bunny will behave a bit differently. It can now survive in even the cleanest environments and will no longer be destroyed by cleaning around the house - it's here to stay. \\n\\nBefriended Dust Bunnies will also show their appreciation by finding rarer items and occasionally even digging up substantial piles of Simoleons.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n\"KEY1\": \"Cảm ơn bạn đã quyên góp mũ. Chắc chắn nó sẽ giúp ai đó giữ ấm đầu!\",\n\"KEY2\": \"{0.SimFirstName} đã kết bạn với Thỏ Bụi! Vì {M0.he}{F0.she} đã làm cho người bạn lông xù của {M0.his}{F0.her} cảm thấy được chào đón và chăm sóc trong nhà của {M0.his}{F0.her}, nên thỏ bụi này sẽ cư xử hơi khác một chút. Giờ nó có thể sống sót ngay cả trong môi trường sạch sẽ nhất và sẽ không còn bị tiêu diệt khi dọn dẹp nhà cửa nữa - nó sẽ ở lại đây. \\n\\nThỏ Bụi đã kết bạn cũng sẽ thể hiện sự cảm kích bằng cách tìm kiếm những vật phẩm hiếm hơn và đôi khi thậm chí còn đào được những đống Simoleon đáng kể.\",\n\"KEY3\": \"(Từ Nguyện Vọng Chế Tạo Pha Lê)\",\n\"KEY4\": \"Người Ước Nguyện\",\n\"KEY5\": \"{0.SimFirstName} đã kết bạn với Thỏ Bụi! Vì {M0.he}{F0.she} đã làm cho người bạn lông xù của {M0.his}{F0.her} cảm thấy được chào đón và chăm sóc trong nhà của {M0.his}{F0.her}, nên thỏ bụi này sẽ cư xử hơi khác một chút. Giờ nó có thể sống sót ngay cả trong môi trường sạch sẽ nhất và sẽ không còn bị tiêu diệt khi dọn dẹp nhà cửa nữa - nó sẽ ở lại đây. \\n\\nThỏ Bụi đã kết bạn cũng sẽ thể hiện sự cảm kích bằng cách tìm kiếm những vật phẩm hiếm hơn và đôi khi thậm chí còn đào được những đống Simoleon đáng kể.\"\n}\n```",
      ],
    },
  ])
    
    return chat

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

def translate_text(text, translation_cache, cache_file, count_file, request_count, chat_session):
    """Dịch văn bản sử dụng chat session"""
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
            
            response = chat_session.send_message(f"Translate to Vietnamese: {text}")
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

def translate_multiple_texts(texts, translation_cache, cache_file, count_file, request_count, chat_session):
    """Dịch nhiều văn bản cùng lúc và trả về dạng JSON"""
    prompt = "\n".join([f"KEY{i+1}-Translate to Vietnamese: {text}" for i, text in enumerate(texts)])
    
    if request_count >= 1500:
        raise Exception("Đã đạt giới hạn 1500 request. Dừng chương trình.")

    max_retries = 3
    retry_delay = 5
    time.sleep(4)

    for attempt in range(max_retries):
        try:
            print(f"\nRequest số {request_count + 1}")
            print(f"Đang dịch {len(texts)} văn bản")
            
            response = chat_session.send_message(prompt)
            # Chuyển đổi response text thành dict
            response_text = response.text.strip()
            try:
                translations = json.loads(response_text)
            except json.JSONDecodeError:
                raise Exception("Không thể parse JSON từ phản hồi của AI")
            
            # Cập nhật cache cho từng bản dịch
            for i, text in enumerate(texts):
                key = f"KEY{i+1}"
                if key in translations:
                    translation_cache[text] = translations[key]
            
            save_translation_cache(cache_file, translation_cache)
            
            request_count += 1
            save_request_count(count_file, request_count)
            
            return translations, request_count
            
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

def process_xml(input_file, output_file, cache_file, count_file, chat_session, batch_size=1):
    """
    Xử lý file XML với khả năng dịch nhiều phần tử cùng lúc
    batch_size: số lượng phần tử cần dịch trong một lần
    """
    print(f"\nBắt đầu xử lý file {input_file}")
    
    translation_cache = load_translation_cache(cache_file)
    request_count = load_request_count(count_file)
    print(f"Số request đã thực hiện: {request_count}")
    
    if request_count >= 1500:
        print("Đã đạt giới hạn 1500 request. Không thể tiếp tục.")
        return
    
    if os.path.exists(output_file):
        print(f"Đọc file output hiện có: {output_file}")
        existing_tree = ET.parse(output_file)
        existing_root = existing_tree.getroot()
        existing_translations = {elem.get('Key'): elem.text for elem in existing_root.findall('Text')}
    else:
        existing_translations = {}

    tree = ET.parse(input_file)
    root = tree.getroot()
    new_root = ET.Element('STBLKeyStringList')
    
    elements = root.findall('Text')
    total_elements = len(elements)
    print(f"Tổng số phần tử cần dịch: {total_elements}")
    
    try:
        # Xử lý theo batch
        for i in range(0, total_elements, batch_size):
            batch_elements = elements[i:i + batch_size]
            texts_to_translate = []
            keys = []
            
            for elem in batch_elements:
                key = elem.get('Key')
                if key in existing_translations:
                    # Thêm phần tử đã có vào output
                    new_elem = ET.Element('Text')
                    new_elem.set('Key', key)
                    new_elem.text = existing_translations[key]
                    new_root.append(new_elem)
                    print(f"Đã có bản dịch cho key {key}")
                else:
                    texts_to_translate.append(elem.text)
                    keys.append(key)
            
            if texts_to_translate:
                translations, request_count = translate_multiple_texts(
                    texts_to_translate,
                    translation_cache,
                    cache_file,
                    count_file,
                    request_count,
                    chat_session
                )
                
                # Thêm các bản dịch mới vào output
                for j, key in enumerate(keys):
                    new_elem = ET.Element('Text')
                    new_elem.set('Key', key)
                    new_elem.text = translations[f"KEY{j+1}"]
                    new_root.append(new_elem)
            
            # Lưu file sau mỗi batch
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
    package_name = input("Nhập tên gói (ví dụ: SP58): ").strip()
    batch_size = int(input("Nhập số lượng KEY cần dịch cùng lúc (1-5): ").strip())
    
    # Giới hạn batch_size từ 1-5
    batch_size = max(1, min(5, batch_size))
    
    paths = get_file_paths(package_name)
    chat_session = init_chat()
    
    process_xml(
        input_file=paths['input'],
        output_file=paths['output'],
        cache_file=paths['cache'],
        count_file=paths['count'],
        chat_session=chat_session,
        batch_size=batch_size
    )

if __name__ == "__main__":
    main()
