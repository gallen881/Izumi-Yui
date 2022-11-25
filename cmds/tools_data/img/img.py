from PIL import Image
import pytesseract
import requests
import function
import os

import openai
openai.api_key = function.open_json('data.json')['openai_token']


IMG_PATH = './cmds/tools_data/img/temp.png'

def ocr(img_url: str, lang: str) -> list:

    with open(IMG_PATH, 'wb') as file:
        file.write(requests.get(img_url, headers={'user-agent': 'Mozilla/5.0'}).content)
    function.print_detail(memo='INFO', obj='Saved temp.png successfully')

    text = pytesseract.image_to_string(Image.open(IMG_PATH), lang=lang)
    function.print_detail(memo='INFO', obj=f'Form string: "{text}"')

    text_list = function.split_str_to_list(text, 2000)
    if text_list != ['']:
        function.print_detail(memo='INFO', obj='Ocr successfully')
        return text_list
    else:
        function.print_detail(memo='INFO', obj='Character not found')
        return ['***Character not found***']

def rotate(img_url: str, angle: str) -> None:
    with open(IMG_PATH, 'wb') as file:
        file.write(requests.get(img_url, headers={'user-agent': 'Mozilla/5.0'}).content)

    Image.open(IMG_PATH).rotate(angle, expand=1).save(IMG_PATH, quality=100)
    function.print_detail(memo='INFO', obj='Saved temp.png successfully')
    for i in range(95, 0, -5):
        if os.path.getsize(IMG_PATH) >= 8388608:
            function.print_detail(memo='WARN', obj=f'Picture size is larger than 8MB, resave it with quality {i}')
            Image.open(IMG_PATH).rotate(angle, expand=1).save(IMG_PATH, quality=i)
            function.print_detail(memo='INFO', obj='Saved temp.png successfully')
        else:
            break


def generate(prompts: str) -> str:
    response = openai.Image.create(prompt=prompts, n=1, size='1024x1024')
    image_url = response['data'][0]['url']
    function.print_detail(memo='INFO', obj=f'Form image: "{image_url}"')
    return image_url
