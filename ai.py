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
import asyncio
import aiohttp
import math

load_dotenv()

# Openai set
openai.api_key = os.getenv('OPENAI_API_KEY')  

# Naver clova set
clova_ocr_apigw_url = os.getenv('CLOVA_OCR_APIGW_URL')
clova_ocr_secret_key = os.getenv('CLOVA_OCR_SECRET_KEY')

class SigonganAI:
    def __init__(self):
        self._messages = []

    async def imgOCR(self, url, session, type = ''):
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
        async with session.post(clova_ocr_apigw_url, headers=headers, data = payload) as response:
            result = await response.json()
            texts = result['images'][0]['fields']
            context = ''
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
            return context, chunks

    async def loadImage(self, session, url):
        async with session.get(url) as response:
            return await response.content.read()

    async def imageProcessor(self, imgUrl=[]):
        context = ''
        cluster = []
        cnt = 0
        strings = []

        start = time.time()
        async with aiohttp.ClientSession() as session:
            imgs = await asyncio.gather(*(self.loadImage(session, url) for url in imgUrl))
            for _img in imgs:
                # load image
                img = Image.open(BytesIO(_img))

                # process iamge
                hw_ratio = 5
                n = math.ceil(img.height / (img.width * hw_ratio))
                list = []
                for i in range(0, n):
                    if (i==n-1):
                        list.append(img.crop((0, i*hw_ratio*img.width, img.width, img.height)))
                    else:
                        list.append(img.crop((0, i*hw_ratio*img.width, img.width, (i+1)*hw_ratio*img.width)))
                    cnt += 1

                # OCR
                for el in list:
                    buffer = io.BytesIO()
                    el.save(buffer, format='PNG')
                    el = buffer.getvalue()
                    string = base64.b64encode(el)
                    strings.append(string)
        mid = time.time()
        print('img load: ', mid-start)

        async with aiohttp.ClientSession() as session:
            context = ''
            cluster = []
            for j in range(math.ceil(len(strings) / 5)):
                results = await asyncio.gather(*(self.imgOCR(_str, session, 'data') for _str in strings[5*j : 5*(j+1)]))
                for result in results:
                    context += result[0]
                    cluster += result[1]
            end = time.time()
            print('ocr: ', end-mid)
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
                model = model,
                messages = self._messages,
                temperature = 0.1
            )
        except:
            return False, False
        answer = response.choices[0].message.content.strip()
        tokens = response.usage.total_tokens
        self.appendMessage("assistant", answer)
        return answer, tokens
    
