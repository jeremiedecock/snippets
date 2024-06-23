#!/bin/sh

# Make a virtual environment for the TensorFlow backend

rm -rf env_tensorflow_cpu
python3 -m venv env_tensorflow_cpu
./env_tensorflow_cpu/bin/python3 -m pip install --upgrade pip
./env_tensorflow_cpu/bin/python3 -m pip install -r requirements-tensorflow-cpu.txt
./env_tensorflow_cpu/bin/python3 -m pip install -r requirements-dev.txt
echo -e "\nexport KERAS_BACKEND=tensorflow" >> ./env_tensorflow_cpu/bin/activate

# Make a virtual environment for the PyTorch backend

rm -rf env_pytorch_cpu
python3 -m venv env_pytorch_cpu
./env_pytorch_cpu/bin/python3 -m pip install --upgrade pip
./env_pytorch_cpu/bin/python3 -m pip install -r requirements-pytorch-cpu.txt
./env_pytorch_cpu/bin/python3 -m pip install -r requirements-dev.txt
echo -e "\nexport KERAS_BACKEND=torch" >> ./env_pytorch_cpu/bin/activate

# Make a virtual environment for the JAX backend

rm -rf env_jax_cpu
python3 -m venv env_jax_cpu
./env_jax_cpu/bin/python3 -m pip install --upgrade pip
./env_jax_cpu/bin/python3 -m pip install -r requirements-jax-cpu.txt
./env_jax_cpu/bin/python3 -m pip install -r requirements-dev.txt
echo -e "\nexport KERAS_BACKEND=jax" >> ./env_jax_cpu/bin/activate
