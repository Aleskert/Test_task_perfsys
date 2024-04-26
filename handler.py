# handler.py

import json
import uuid
import textract

def extract_text_from_file(file_path):
    try:
        # Витягуємо текст з файлу
        text = textract.process(file_path, encoding='utf-8')
        return text.decode('utf-8')
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def files_post(event, context):
    callback_url = event['body'].get('callback_url')
    file_id = str(uuid.uuid4())
    upload_url = f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}/files/{file_id}"
    file_content = event['body'].get('file_content')
    file_name = f"{file_id}.pdf"
    with open(file_name, 'wb') as f:
        f.write(file_content)
    
    extracted_text = extract_text_from_file(file_name)
    
    import os
    os.remove(file_name)
    
    if extracted_text is not None:
        import requests
        callback_data = {'file_id': file_id, 'extracted_text': extracted_text}
        requests.post(callback_url, json=callback_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'upload_url': upload_url})
    }

def files_get(event, context):
    file_id = event['pathParameters']['file_id']
    
    # Отримуємо текст з файлу за file_id (якщо текст уже вилучено)
    # У цьому прикладі я не зберігаю вилучений текст, тому просто повертаємо статус "in_progress"
    response = {
        'file_id': file_id,
        'status': 'in_progress'
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

