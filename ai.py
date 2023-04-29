import os
import openai
from dotenv import load_dotenv
import requests
import uuid
import time
import json

load_dotenv()

# Openai set
openai.api_key = os.getenv('OPENAI_API_KEY')  

# Naver clova set
clova_ocr_apigw_url = os.getenv('CLOVA_OCR_APIGW_URL')
clova_ocr_secret_key = os.getenv('CLOVA_OCR_SECRET_KEY')

class SigonganAI:
    def __init__(self, imageUrl):
        self._imageUrl = imageUrl
        self._messages = []

    def imgOCR(self, type):
        # Naver clova OCR
        if(type=="url"):
            request_json = {
                'images': [
                    {
                        'format': 'jpg',
                        'name': 'demo',
                        'url': self._imageUrl
                    }
                ],
                'requestId': str(uuid.uuid4()),
                'version': 'V2',
                'timestamp': int(round(time.time()*1000))
            }
        else: 
            request_json = {
                'images': [
                    {
                        'format': 'jpg',
                        'name': 'demo',
                        'data': self._imageUrl.decode('utf8')
                    }
                ],
                'requestId': str(uuid.uuid4()),
                'version': 'V2',
                'timestamp': int(round(time.time()*1000))
            }
        payload = json.dumps(request_json).encode('UTF-8')
        headers = {
            'X-OCR-SECRET': clova_ocr_secret_key,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", clova_ocr_apigw_url, headers=headers, data = payload)
        result = response.json()
        texts = result['images'][0]['fields']
        context = ''
        for text in texts:
            context += text['inferText']
            if (text['lineBreak']):
                context += '\n'
            else: 
                context += ' '
        return context
        
    def appendMessage(self, role, content):
        self._messages.append({"role":role, "content":content})

    def initMessage(self, messages):
        self._messages = messages
    
    def getGPT(self):
        try:
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = self._messages
            )
        except:
            return False, False
        answer = response.choices[0].message.content.strip()
        tokens = response.usage.total_tokens
        self.appendMessage("assistant", answer)
        return answer, tokens