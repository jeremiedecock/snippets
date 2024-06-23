#!/bin/sh

# Make a virtual environment for the TensorFlow backend

rm -rf env_tensorflow_gpu
python3 -m venv env_tensorflow_gpu
./env_tensorflow_gpu/bin/python3 -m pip install --upgrade pip
./env_tensorflow_gpu/bin/python3 -m pip install -r requirements-tensorflow-gpu.txt
./env_tensorflow_gpu/bin/python3 -m pip install -r requirements-dev.txt
echo -e "\nexport KERAS_BACKEND=tensorflow" >> ./env_tensorflow_gpu/bin/activate

# Make a virtual environment for the PyTorch backend

rm -rf env_pytorch_gpu
python3 -m venv env_pytorch_gpu
./env_pytorch_gpu/bin/python3 -m pip install --upgrade pip
./env_pytorch_gpu/bin/python3 -m pip install -r requirements-pytorch-gpu.txt
./env_pytorch_gpu/bin/python3 -m pip install -r requirements-dev.txt
echo -e "\nexport KERAS_BACKEND=torch" >> ./env_pytorch_gpu/bin/activate

# Make a virtual environment for the JAX backend

rm -rf env_jax_gpu
python3 -m venv env_jax_gpu
./env_jax_gpu/bin/python3 -m pip install --upgrade pip
./env_jax_gpu/bin/python3 -m pip install -r requirements-jax-gpu.txt
./env_jax_gpu/bin/python3 -m pip install -r requirements-dev.txt
echo -e "\nexport KERAS_BACKEND=jax" >> ./env_jax_gpu/bin/activate
