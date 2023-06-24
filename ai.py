import os
import openai
from dotenv import load_dotenv
import requests
import uuid
import time
import json
from PIL import Image
from io import BytesIO
import base64
import math
import io
import time

load_dotenv()

# Openai set
openai.api_key = os.getenv('OPENAI_API_KEY')  

# Naver clova set
clova_ocr_apigw_url = os.getenv('CLOVA_OCR_APIGW_URL')
clova_ocr_secret_key = os.getenv('CLOVA_OCR_SECRET_KEY')

class SigonganAI:
    def __init__(self):
        self._messages = []

    def imgOCR(self, url, type = ''):
        # Naver clova OCR
        if(type=="url"):
            request_json = {
                'images': [
                    {
                        'format': 'jpg',
                        'name': 'demo',
                        'url': url
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
                        'data': url.decode('utf8')
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

        start = time.time()
        cluster = []
        for text in texts:
            ### whole
            context += text['inferText']
            if (text['lineBreak']):
                context += '\n'
            else: 
                context += ' '
            
            ### cluster
            dist = []
            vertices = text['boundingPoly']['vertices']
            if cluster == []:
                cluster.append([text])
                continue
            prev_chunks = cluster[-3:]
            for chunk in prev_chunks:
                dx = 0
                dy = 0
                prev_vertices = chunk[-1]['boundingPoly']['vertices']
                for i in range(0,4):
                    dx += (vertices[i]['x'] - prev_vertices[i]['x']) / 16
                    dy += (vertices[i]['y'] - prev_vertices[i]['y']) / 4
                dx = abs(dx)
                dy = abs(dy)
                dist.append((dx**2 + dy**2)**0.5)
            min_dist = min(dist)
            if(min_dist > 200):
                cluster.append([text])
            else:
                idx = len(cluster) + dist.index(min_dist) - min([len(cluster), 3])
                cluster[idx].append(text)
        chunks = []
        for chunk in cluster:
            chunk_ctx = ''
            for text in chunk:
                chunk_ctx += text['inferText']
                if text['lineBreak']: chunk_ctx += '\n'
                else: chunk_ctx += ' '
            chunks.append(chunk_ctx)
        end = time.time()
        print(end - start)

        return context, chunks
    
    def imageProcessor(self, imgUrl=[]):
        context = ''
        cluster = []
        cnt = 0
        load_latency = []
        process_latency = []
        ocr_latency = []
        for url in imgUrl:
            '''
            if cnt > 7: # 7장으로 제한
                break
            '''
            # load image
            start = time.time()
            content = requests.get(url).content
            img = Image.open(BytesIO(content))
            end = time.time()
            load_latency.append(end-start)

            # process iamge
            start = time.time()
            hw_ratio = 4
            n = math.ceil(img.height / (img.width * hw_ratio))
            list = []
            for i in range(0, n):
                if (i==n-1):
                    list.append(img.crop((0, i*hw_ratio*img.width, img.width, img.height)))
                else:
                    list.append(img.crop((0, i*hw_ratio*img.width, img.width, (i+1)*hw_ratio*img.width)))
                cnt += 1
            end = time.time()
            process_latency.append(end - start)

            # OCR
            for el in list:
                start = time.time()
                buffer = io.BytesIO()
                el.save(buffer, format='PNG')
                el = buffer.getvalue()
                string = base64.b64encode(el)
                _ctx, _cluster = self.imgOCR(string)
                context += _ctx
                context += "\n"
                cluster += _cluster
                end = time.time()
                ocr_latency.append(end - start)
        '''
        if len(ocr)>2000:
            ocr = ocr[:2000]
        alert = ''
        if len(ocr) == 2000:
            alert = '2000자 이상의 텍스트가 인식되었습니다'
        else :
            alert = f'{len(ocr)}자의 텍스트가 인식되었습니다'
        '''
        print(load_latency, process_latency, ocr_latency, len(context))
        return context, cluster
        
    def appendMessage(self, role, content):
        self._messages.append({"role":role, "content":content})
        
    def appendMessages(self, messages):
        self._messages += messages

    def initMessage(self, messages):
        self._messages = messages
    
    def getGPT(self, model = 'gpt-3.5-turbo-0613'):
        try:
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo-0613",
                messages = self._messages,
                temperature = 0.1
            )
        except:
            return False, False
        answer = response.choices[0].message.content.strip()
        tokens = response.usage.total_tokens
        self.appendMessage("assistant", answer)
        return answer, tokens