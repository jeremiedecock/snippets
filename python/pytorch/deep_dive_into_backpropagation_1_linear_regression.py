# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Deep dive into backpropagation

# %%
import torch

# %% [markdown]
# <img src="assets/regression_1d.drawio.svg" width="500">

# %%
model = torch.nn.Linear(
    in_features=1,
    out_features=1,
    bias=True
)
model.state_dict() # print the weights and biases of the model

# %%
x = torch.randn(1)
x

# %%
w = 3.0
b = 2.0

y_true = w * x + b
y_true

# %%
loss_fn = torch.nn.MSELoss()

# %% [markdown]
# ### Forward pass

# %%
y_pred = model(x)
y_pred

# %%
error = loss_fn(y_pred, y_true)
error

# %% [markdown]
# Let's manually compute the error and compare it with the error computed above:

# %%
# The loss is the mean squared error between the predicted and true values
(y_pred - y_true)**2

# %% [markdown]
# $$
# E =
# \left(
# \underbrace{
# f(
# \overbrace{
# w \cdot x + b
# }^{\sigma}
# )
# }_{y}
# - y^*
# \right)^2
# $$
#
# $$
# \begin{align}
# E &= \left( y - y^* \right)^2 \\
# y &= f(\sigma) \\
# \sigma &= w \cdot x + b \\
# \end{align}
# $$

# %% [markdown]
# ### Backward pass

# %% [markdown]
# #### Computation $\frac{\partial E}{\partial w}$ with PyTorch autograd

# %%
error.backward()

# %%
# Get gradients
for name, param in model.named_parameters():
    if param.requires_grad:
        print(f"Gradient for {name}: {param.grad}")

# %%
model.state_dict()

# %% [markdown]
# This is our reference computation. We will use it to validate the manual computation that follows.

# %% [markdown]
# #### Manual computation of $\frac{\partial E}{\partial w}$

# %% [markdown]
# Let's rewrite the computation of $\frac{\partial E}{\partial w}$ manually.

# %% [markdown]
# Using the chain rule:
#
# $$
# \frac{\partial E}{\partial w} =
# \frac{\partial E}{\partial \color{green}{\sigma}} ~
# \frac{\partial \color{green}{\sigma}}{\partial w} ~
# $$
#
# knowing that:
#
# $$
# \begin{align}
# \frac{\partial E}{\partial \color{green}{\sigma}} &= 2 (\sigma - y^*) \\
# \frac{\partial \color{green}{\sigma}}{\partial w} &= x \\
# \end{align}
# $$
#
# we can write:
#
# $$
# \frac{\partial E}{\partial w} = 2(\sigma - y^*) \cdot x
# $$

# %% [markdown]
# Let's apply this formula to the previous example:

# %%
sigma = y_pred

grad_E_w = 2 * (sigma - y_true) * x
grad_E_w

# %% [markdown]
# Ok, we obtain the same result than with PyTorch autograd.

# %% [markdown]
# #### Manual computation of $\frac{\partial E}{\partial b}$

# %% [markdown]
# Let's rewrite the computation of $\frac{\partial E}{\partial b}$ manually.

# %% [markdown]
# Using the chain rule:
#
# $$
# \frac{\partial E}{\partial b} =
# \frac{\partial E}{\partial \color{green}{\sigma}} ~
# \frac{\partial \color{green}{\sigma}}{\partial b} ~
# $$
#
# knowing that:
#
# $$
# \begin{align}
# \frac{\partial E}{\partial \color{green}{\sigma}} &= 2 (\sigma - y^*) \\
# \frac{\partial \color{green}{\sigma}}{\partial b} &= 1 \\
# \end{align}
# $$
#
# we can write:
#
# $$
# \frac{\partial E}{\partial w} = 2(\sigma - y^*)
# $$

# %% [markdown]
# Let's apply this formula to the previous example:

# %%
f = torch.nn.functional.tanh

sigma = y_pred

grad_b = 2 * (sigma - y_true)
grad_b

# %% [markdown]
# Ok, we obtain the same result than with PyTorch autograd.
