from transformers import AutoModelForCausalLM, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("stabilityai/stablecode-instruct-alpha-3b")
model = AutoModelForCausalLM.from_pretrained(
  "stabilityai/stablecode-instruct-alpha-3b",
  trust_remote_code=True,
  torch_dtype="auto",
)
model.cuda()
inputs = tokenizer("###Instruction\nGenerate a python function to find number of CPU cores###Response\n", return_tensors="pt").to("cuda")
tokens = model.generate(
  **inputs,
  max_new_tokens=48,
  temperature=0.2,
  do_sample=True,
)
print(tokenizer.decode(tokens[0], skip_special_tokens=True))

