#!/usr/bin/env python3

# https://huggingface.co/mistralai/Ministral-3-3B-Reasoning-2512

import torch
from transformers import Mistral3ForConditionalGeneration, MistralCommonBackend

model_id = "mistralai/Ministral-3-3B-Reasoning-2512"

tokenizer = MistralCommonBackend.from_pretrained(model_id)
model = Mistral3ForConditionalGeneration.from_pretrained(
    model_id, torch_dtype=torch.bfloat16, device_map="auto"
)

image_url = "https://static.wikia.nocookie.net/essentialsdocs/images/7/70/Battle.png/revision/latest?cb=20220523172438"

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What action do you think I should take in this situation? List all the possible actions and explain why you think they are good or bad.",
            },
            {"type": "image_url", "image_url": {"url": image_url}},
        ],
    },
]

tokenized = tokenizer.apply_chat_template(messages, return_tensors="pt", return_dict=True)

tokenized["input_ids"] = tokenized["input_ids"].to(device="cuda")
tokenized["pixel_values"] = tokenized["pixel_values"].to(dtype=torch.bfloat16, device="cuda")
image_sizes = [tokenized["pixel_values"].shape[-2:]]

output = model.generate(
    **tokenized,
    # image_sizes=image_sizes,
    max_new_tokens=8092,
)[0]

decoded_output = tokenizer.decode(output[len(tokenized["input_ids"][0]):])
print(decoded_output)
