import base64
import requests
from openai import OpenAI

def design_description(base64Image, api_key):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?, Understand the image thoroughly and provide a detailed description about this image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64Image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # print(response.json())
    return response.json()


def design_generation(prompt, APIKEY):
    client = OpenAI(api_key=APIKEY)

    response = client.images.generate(
        model="dall-e-3",
        prompt=f'Create an design with this description: {prompt}, [!IMPORTANT]  make the image as a desgin and make sure the text/label is clearly visible',
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    return image_url