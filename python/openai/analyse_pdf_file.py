#!/usr/bin/env python3

# https://platform.openai.com/docs/overview

from openai import OpenAI
client = OpenAI()

file = client.files.create(
    file=open("test.pdf", "rb"),
    purpose="user_data"
)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "file",
                    "file": {
                        "file_id": file.id,
                    }
                },
                {
                    "type": "text",
                    "text": "What is the title of this paper?",
                },
            ]
        }
    ]
)

print(completion.choices[0].message.content)
