# Stable Diffusion


C.f. :
- https://huggingface.co/stabilityai/stable-diffusion-2-1-base#examples
- https://github.com/huggingface/diffusers


## Install requirements

```
mkdir stablediffusion
cd stablediffusion
conda deactivate
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
pip install diffusers transformers accelerate scipy safetensors xformers
```
