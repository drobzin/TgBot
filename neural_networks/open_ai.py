from decouple import config
import logging
from openai import AsyncOpenAI

aclient = AsyncOpenAI(api_key=config('O_SECRET_KEY'))


async def generate_text(prompt) -> dict:
    try:
        response = await aclient.chat.completions.create(model="gpt-3.5-turbo",
                                                         messages=[
                                                             {"role": "user",
                                                                 "content": prompt}
                                                         ])
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)


async def generate_image(prompt, n=1, size="1024x1024") -> list[str]:
    try:
        response = await aclient.images.generate(prompt=prompt,
                                                 n=n,
                                                 size=size)
        urls = []
        logging.error(response)
        for i in response['data']:
            urls.append(i['url'])
    except Exception as e:
        logging.error(e)
        return []
    else:
        return urls
