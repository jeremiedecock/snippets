#!/bin/sh

# Make a virtual environment for the TensorFlow backend

rm -rf env_tensorflow_cpu
python3 -m venv env_tensorflow_cpu
./env_tensorflow_cpu/bin/python3 -m pip install --upgrade pip
./env_tensorflow_cpu/bin/python3 -m pip install -r requirements-tensorflow-cpu.txt
./env_tensorflow_cpu/bin/python3 -m pip install -r requirements-dev.txt
# TODO: SET "KERAS_BACKEND" IN env_*/bin/activate ; c.f. https://medium.com/@dataproducts/python-three-different-ways-to-store-environment-variables-15224952f31b

# Make a virtual environment for the PyTorch backend

rm -rf env_pytorch_cpu
python3 -m venv env_pytorch_cpu
./env_pytorch_cpu/bin/python3 -m pip install --upgrade pip
./env_pytorch_cpu/bin/python3 -m pip install -r requirements-pytorch-cpu.txt
./env_pytorch_cpu/bin/python3 -m pip install -r requirements-dev.txt
# TODO: SET "KERAS_BACKEND" IN env_*/bin/activate ; c.f. https://medium.com/@dataproducts/python-three-different-ways-to-store-environment-variables-15224952f31b

# Make a virtual environment for the JAX backend

rm -rf env_jax_cpu
python3 -m venv env_jax_cpu
./env_jax_cpu/bin/python3 -m pip install --upgrade pip
./env_jax_cpu/bin/python3 -m pip install -r requirements-jax-cpu.txt
./env_jax_cpu/bin/python3 -m pip install -r requirements-dev.txt
# TODO: SET "KERAS_BACKEND" IN env_*/bin/activate ; c.f. https://medium.com/@dataproducts/python-three-different-ways-to-store-environment-variables-15224952f31b
