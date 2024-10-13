import tomllib

with open("hello.toml", "rb") as f:
    data = tomllib.load(f)

print(data)