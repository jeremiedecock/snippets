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
import math
import matplotlib.pyplot as plt

# https://github.com/jeremiedecock/neural-network-figures.git
import nnfigs
import numpy as np

import torch

# %% [markdown]
# $
# \newcommand{\cur}{i}
# \newcommand{\prev}{j}
# \newcommand{\prevcur}{{\cur\prev}}
# \newcommand{\next}{k}
# \newcommand{\curnext}{{\next\cur}}
# \newcommand{\ex}{\eta}
# \newcommand{\pot}{\sigma}
# \newcommand{\feature}{x}
# \newcommand{\weight}{{\boldsymbol{w}}}
# \newcommand{\wcur}{{\weight_{\cur\prev}}}
# \newcommand{\activthres}{\theta}
# \newcommand{\activfunc}{f}
# \newcommand{\errfunc}{E}
# \newcommand{\learnrate}{\epsilon}
# \newcommand{\learnit}{n}
# \newcommand{\sigout}{{\boldsymbol{y}}}
# \newcommand{\sigoutdes}{{\boldsymbol{y^*}}}
# \newcommand{\weights}{\boldsymbol{W}}
# \newcommand{\errsig}{\Delta}
# $
#
# Notations:
#
# - $\cur$: couche courante
# - $\prev$: couche immédiatement en amont de la courche courrante (i.e. vers la couche d'entrée du réseau)
# - $\next$: couche immédiatement en aval de la courche courrante (i.e. vers la couche de sortie du réseau)
# - $\ex$: exemple (*sample* ou *feature*) courant (i.e. le vecteur des entrées courantes du réseau)
# - $\pot_\cur$: *Potentiel d'activation* du neurone $i$ pour l'exemple courant
# - $\wcur$: Poids de la connexion entre le neurone $j$ et le neurone $i$
# - $\activthres_\cur$: *Seuil d'activation* du neurone $i$
# - $\activfunc_\cur$: *Fonction d'activation* du neurone $i$
# - $\errfunc$: *Fonction objectif* ou *fonction d'erreur*
# - $\learnrate$: *Pas d'apprentissage* ou *Taux d'apprentissage*
# - $\learnit$: Numéro d'itération (ou cycle ou époque) du processus d'apprentissage
# - $\sigout_\cur$: Signal de sortie du neurone $i$ pour l'exemple courant
# - $\sigoutdes_\cur$: Sortie désirée (*étiquette*) du neurone $i$ pour l'exemple courant
# - $\weights$: Matrice des poids du réseau (en réalité il y a une matrice de taille potentiellement différente par couche)
# - $\errsig_i$: *Signal d'erreur* du neurone $i$ pour l'exemple courant

# %%
STR_CUR = r"i"       # Couche courante
STR_PREV = r"j"      # Couche immédiatement en amont de la courche courrante (i.e. vers la couche d'entrée du réseau)
STR_NEXT = r"k"      # Couche immédiatement en aval de la courche courrante (i.e. vers la couche de sortie du réseau)
STR_EX = r"\eta"     # Exemple (*sample* ou *feature*) courant (i.e. le vecteur des entrées courantes du réseau)
STR_POT = r"\sigma"       # *Potentiel d'activation* du neurone $i$ pour l'exemple $\ex$
STR_POT_CUR = r"x_i"       # *Potentiel d'activation* du neurone $i$ pour l'exemple $\ex$
STR_WEIGHT = r"w"
STR_WEIGHT_CUR = r"w_{ij}"  # Poids de la connexion entre le neurone $j$ et le neurone $i$
STR_ACTIVTHRES = r"\theta"  # *Seuil d'activation* du neurone $i$
STR_ACTIVFUNC = r"f"        # *Fonction d'activation* du neurone $i$
STR_ERRFUNC = r"E"          # *Fonction objectif* ou *fonction d'erreur*
STR_LEARNRATE = r"\epsilon" # *Pas d'apprentissage* ou *Taux d'apprentissage*
STR_LEARNIT = r"n"          # Numéro d'itération (ou cycle ou époque) du processus d'apprentissage
STR_SIGIN = r"x"            # Signal de sortie du neurone $i$ pour l'exemple $\ex$
STR_SIGOUT = r"y"           # Signal de sortie du neurone $i$ pour l'exemple $\ex$
STR_SIGOUT_CUR = r"y_i"
STR_SIGOUT_PREV = r"y_j"
STR_SIGOUT_DES = r"d"           # Sortie désirée (*étiquette*) du neurone $i$ pour l'exemple $\ex$
STR_SIGOUT_DES_CUR = r"d_i"
STR_WEIGHTS = r"W"              # Matrice des poids du réseau (en réalité il y a une matrice de taille potentiellement différente par couche)
STR_ERRSIG = r"\Delta"          # *Signal d'erreur* du neurone $i$ pour l'exemple $\ex$

def tex(tex_str):
    return r"$" + tex_str + r"$"


# %%
def display_nn(
    hidden_list: list | None = None,
    highlight_list: list | None = None,
):
    if hidden_list is None:
        hidden_list = []

    if highlight_list is None:
        highlight_list = []

    def color_str(name):
        if name in hidden_list:
            return "lightgray"
        elif name in highlight_list:
            return "red"
        else:
            return "black"

    fig, ax = nnfigs.init_figure(size_x=8, size_y=4)

    HSPACE = 6
    VSPACE = 4

    # Synapse #####################################

    # Layer 1-2
    nnfigs.draw_synapse(
        ax, (0,  VSPACE), (HSPACE,  VSPACE),
        label="" if "w1" in hidden_list else tex(STR_WEIGHT + "_1"),
        label_position=0.4,
        label_color=color_str("w1"),
        color=color_str("w1")
    )
    nnfigs.draw_synapse(
        ax, (0, -VSPACE), (HSPACE,  VSPACE),
        label="" if "w3" in hidden_list else tex(STR_WEIGHT + "_3"),
        label_position=0.25,
        label_offset_y=-0.8,
        label_color=color_str("w3"),
        color=color_str("w3")
    )

    nnfigs.draw_synapse(
        ax, (0,  VSPACE), (HSPACE, -VSPACE),
        label="" if "w2" in hidden_list else tex(STR_WEIGHT + "_2"),
        label_position=0.25,
        label_color=color_str("w2"),
        color=color_str("w2")
    )
    nnfigs.draw_synapse(
        ax, (0, -VSPACE), (HSPACE, -VSPACE),
        label="" if "w4" in hidden_list else tex(STR_WEIGHT + "_4"),
        label_position=0.4,
        label_offset_y=-0.8,
        label_color=color_str("w4"),
        color=color_str("w4")
    )

    # Layer 2-3
    nnfigs.draw_synapse(
        ax, (HSPACE,  VSPACE), (2*HSPACE,  VSPACE),
        label="" if "w5" in hidden_list else tex(STR_WEIGHT + "_5"),
        label_position=0.4,
        label_color=color_str("w5"),
        color=color_str("w5")
    )
    nnfigs.draw_synapse(
        ax, (HSPACE, -VSPACE), (2*HSPACE,  VSPACE),
        label="" if "w7" in hidden_list else tex(STR_WEIGHT + "_7"),
        label_position=0.25,
        label_offset_y=-0.8,
        label_color=color_str("w7"),
        color=color_str("w7")
    )

    nnfigs.draw_synapse(
        ax, (HSPACE,  VSPACE), (2*HSPACE, -VSPACE),
        label="" if "w6" in hidden_list else tex(STR_WEIGHT + "_6"),
        label_position=0.25,
        label_color=color_str("w6"),
        color=color_str("w6")
    )
    nnfigs.draw_synapse(
        ax, (HSPACE, -VSPACE), (2*HSPACE, -VSPACE),
        label="" if "w8" in hidden_list else tex(STR_WEIGHT + "_8"),
        label_position=0.4,
        label_offset_y=-0.8,
        label_color=color_str("w8"),
        color=color_str("w8")
    )

    # Layer 3-4
    nnfigs.draw_synapse(
        ax, (2*HSPACE,  VSPACE), (3*HSPACE, 0),
        label="" if "w9" in hidden_list else tex(STR_WEIGHT + "_9"),
        label_position=0.4,
        label_color=color_str("w9"),
        color=color_str("w9")
    )
    nnfigs.draw_synapse(
        ax, (2*HSPACE, -VSPACE), (3*HSPACE, 0),
        label="" if "w10" in hidden_list else tex(STR_WEIGHT + "_{10}"),
        label_position=0.4,
        label_offset_y=-0.8,
        label_color=color_str("w10"),
        color=color_str("w10")
    )

    nnfigs.draw_synapse(ax, (3*HSPACE, 0), (3*HSPACE + 2, 0))

    # Neuron ######################################

    # Layer 1 (input)
    nnfigs.draw_neuron(
        ax,
        (0,  VSPACE),
        0.5,
        empty=True,
        line_color=color_str("x1")
    )
    nnfigs.draw_neuron(
        ax,
        (0, -VSPACE),
        0.5,
        empty=True,
        line_color=color_str("x2")
    )

    # Layer 2
    nnfigs.draw_neuron(
        ax,
        (HSPACE,  VSPACE),
        1,
        line_color=color_str("n1"),
        ag_func=tex(STR_POT + "_1"),
        tr_func=tex(STR_SIGOUT + "_1"),
        ag_func_color=color_str("s1"),
        tr_func_color=color_str("y1")
    )
    nnfigs.draw_neuron(
        ax,
        (HSPACE, -VSPACE),
        1,
        line_color=color_str("n2"),
        ag_func=tex(STR_POT + "_2"),
        tr_func=tex(STR_SIGOUT + "_2"),
        ag_func_color=color_str("s2"),
        tr_func_color=color_str("y2")
    )

    # Layer 3
    nnfigs.draw_neuron(
        ax,
        (2*HSPACE,  VSPACE),
        1,
        line_color=color_str("n3"),
        ag_func=tex(STR_POT + "_3"),
        tr_func=tex(STR_SIGOUT + "_3"),
        ag_func_color=color_str("s3"),
        tr_func_color=color_str("y3")
    )
    nnfigs.draw_neuron(
        ax,
        (2*HSPACE, -VSPACE),
        1,
        line_color=color_str("n4"),
        ag_func=tex(STR_POT + "_4"),
        tr_func=tex(STR_SIGOUT + "_4"),
        ag_func_color=color_str("s4"),
        tr_func_color=color_str("y4")
    )

    # Layer 4
    nnfigs.draw_neuron(
        ax,
        (3*HSPACE, 0),
        1,
        ag_func=tex(STR_POT + "_o"),
        tr_func=tex(STR_SIGOUT + "_o"),
        ag_func_color=color_str("so"),
        tr_func_color=color_str("yo")
    )

    # Text ########################################

    # Layer 1 (input)
    #plt.text(x=0.5, y=VSPACE+1, s=tex(STR_SIGOUT + "_i"), fontsize=12)
    if "x1" not in hidden_list:
        plt.text(x=-1.7, y=VSPACE, s=tex(STR_SIGIN + "_1"), fontsize=12)
    if "x2" not in hidden_list:
        plt.text(x=-1.7, y=-VSPACE-0.2, s=tex(STR_SIGIN + "_2"), fontsize=12)

    # # Layer 2
    # #plt.text(x=HSPACE-1.25, y=VSPACE+1.5, s=tex(STR_POT + "_1"), fontsize=12)
    # if "y1" not in hidden_list:
    #     plt.text(x=HSPACE+0.4, y=VSPACE+1.5, s=tex(STR_SIGOUT + "_1"), fontsize=12)

    # #plt.text(x=HSPACE-1.25, y=-VSPACE-1.8, s=tex(STR_POT + "_2"), fontsize=12)
    # if "y2" not in hidden_list:
    #     plt.text(x=HSPACE+0.4, y=-VSPACE-1.8, s=tex(STR_SIGOUT + "_2"), fontsize=12)

    # # Layer 3
    # #plt.text(x=2*HSPACE-1.25, y=VSPACE+1.5, s=tex(STR_POT + "_3"), fontsize=12)
    # if "y3" not in hidden_list:
    #     plt.text(x=2*HSPACE+0.4, y=VSPACE+1.5, s=tex(STR_SIGOUT + "_3"), fontsize=12)

    # #plt.text(x=2*HSPACE-1.25, y=-VSPACE-1.8, s=tex(STR_POT + "_4"), fontsize=12)
    # if "y4" not in hidden_list:
    #     plt.text(x=2*HSPACE+0.4, y=-VSPACE-1.8, s=tex(STR_SIGOUT + "_4"), fontsize=12)

    # Layer 4
    #plt.text(x=3*HSPACE-1.25, y=1.5, s=tex(STR_POT + "_o"), fontsize=12)
    #plt.text(x=3*HSPACE+0.4,  y=1.5, s=tex(STR_SIGOUT + "_o"), fontsize=12)


    # plt.text(
    #     x=3*HSPACE-0.3,
    #     y=-1.8,
    #     s=tex(STR_POT),
    #     fontsize=12
    # )
    # plt.text(
    #     x=3*HSPACE+2.5,
    #     y=-0.3,
    #     s=tex(STR_SIGOUT),
    #     fontsize=12
    # )

    plt.show()


# display_nn(
#     hidden_list=["w1", "y1", "s2", "y3"],
#     highlight_list=["w3", "s4"]
# )

# %% [markdown]
# ## Make the model in PyTorch

# %% [markdown]
# **Remark**: The model is a simple feedforward neural network with two hidden layers. To simplify computations, we don't use any bias.

# %%
model = torch.nn.Sequential(
    torch.nn.Linear(2, 2, bias=False),
    torch.nn.Tanh(),
    torch.nn.Linear(2, 2, bias=False),
    torch.nn.Tanh(),
    torch.nn.Linear(2, 1, bias=False)
)
model.state_dict() # print the weights and biases of the model

# %%
x = torch.randn(2)
x

# %%
y_true = torch.randn(1)
y_true

# %%
loss_fn = torch.nn.MSELoss()

# %% [markdown]
# ## Compute the forward pass

# %%
display_nn()

# %% [markdown]
# $
# \newcommand{\yone}{\underbrace{\activfunc   \left( \overbrace{\weight_1 \feature_1 + \weight_3 \feature_2}^{\pot_1} \right)}_{\sigout_1}}
# \newcommand{\ytwo}{\underbrace{\activfunc   \left( \overbrace{\weight_2 \feature_1 + \weight_4 \feature_2}^{\pot_2} \right)}_{\sigout_2}}
# \newcommand{\ythree}{\underbrace{\activfunc \left( \overbrace{\weight_5 \yone + \weight_7 \ytwo}^{\pot_3} \right)}_{\sigout_3}}
# \newcommand{\yfour}{\underbrace{\activfunc  \left( \overbrace{\weight_6 \yone + \weight_8 \ytwo}^{\pot_4} \right)}_{\sigout_4}}
# $
#
# $$
# \sigout_o =
# \activfunc \left(
# \overbrace{
#  \weight_9 ~ \ythree
#  +
#  \weight_{10} ~ \yfour
# }^{\pot_o}
# \right)
# $$

# %%
x1 = x[0].item()
x2 = x[1].item()

w1 = model[0].weight[0, 0].item()
w2 = model[0].weight[1, 0].item()
w3 = model[0].weight[0, 1].item()
w4 = model[0].weight[1, 1].item()

w5 = model[2].weight[0, 0].item()
w6 = model[2].weight[1, 0].item()
w7 = model[2].weight[0, 1].item()
w8 = model[2].weight[1, 1].item()

w9 = model[4].weight[0, 0].item()
w10 = model[4].weight[0, 1].item()

# f = torch.nn.functional.tanh
f = math.tanh

def df(x):
    """Derivative of the tanh function
    $\tanh '= \frac{1}{\cosh^{2}} = 1-\tanh^{2}$
    """
    y = 1. - math.tanh(x) ** 2
    return y


# %%
sigma1 = w1 * x1 + w3 * x2  # (x @ model[0].weight)[0].item()
y1 = f(sigma1)              # torch.nn.functional.tanh(x @ model[0].weight)[0]

sigma2 = w2 * x1 + w4 * x2  # (x @ model[0].weight)[1]
y2 = f(sigma2)              # torch.nn.functional.tanh(x @ model[0].weight)[1]

sigma3 = w5 * y1 + w7 * y2  # (torch.nn.functional.tanh(x @ model[0].weight) @ model[2].weight)[0]
y3 = f(sigma3)              # torch.nn.functional.tanh(torch.nn.functional.tanh(x @ model[0].weight) @ model[2].weight)[0].item()

sigma4 = w6 * y1 + w8 * y2  # (torch.nn.functional.tanh(x @ model[0].weight) @ model[2].weight)[1].item()
y4 = f(sigma4)              # torch.nn.functional.tanh(torch.nn.functional.tanh(x @ model[0].weight) @ model[2].weight)[1].item()

sigma = w9 * y3 + w10 * y4  # (torch.nn.functional.tanh(torch.nn.functional.tanh(x @ model[0].weight) @ model[2].weight) @ model[4].weight.T)[0].item()
y_pred = sigma              # torch.nn.functional.tanh(torch.nn.functional.tanh(x @ model[0].weight) @ model[2].weight) @ model[4].weight.T

y_pred

# %%
# The loss is the mean squared error between the predicted and true values
(y_pred - y_true)**2

# %% [markdown]
# ### Let's check with PyTorch

# %%
y_pred = model(x)
y_pred

# %%
error = loss_fn(y_pred, y_true)
error

# %% [markdown]
# ## Compute the backward pass

# %% [markdown]
# ### Backward computation of $\frac{\partial \errfunc}{\partial \weight_{10}}$

# %%
display_nn(
    hidden_list=["x1", "x2", "y1", "y2", "y3", "s1", "s2", "s3", "s4", "n1", "n2", "n3", "w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w9"],
    highlight_list=["w10"]
)

# %% [markdown]
# $$
# \sigout_o =
# \activfunc \left(
# \overbrace{
#  \weight_9 ~ \ythree
#  +
#  \weight_{10} ~ \yfour
# }^{\pot_o}
# \right)
# $$

# %% [markdown]
# Using the chain rule:
#
# $$
# \frac{\partial \errfunc}{\partial \color{red}{\weight_{10}}}
# =
# \underbrace{
#  \frac{\partial \errfunc}{\partial \color{orange}{\sigout_o}}
#  \frac{\partial \color{orange}{\sigout_o}}{\partial \color{green}{\pot_o}} ~
# }_{\errsig_o}
# \frac{\partial \color{green}{\pot_o}}{\partial \color{red}{\weight_{10}}}
# =
# \errsig_o
# \frac{\partial \color{green}{\pot_o}}{\partial \color{red}{\weight_{10}}}
# $$
#
# knowing that:
#
# $$
# \begin{align}
# \frac{\partial \errfunc}{\partial \color{orange}{\sigout_o}}              &= 2 (\sigout_o - \sigoutdes) \\
# \frac{\partial \color{orange}{\sigout_o}}{\partial \color{green}{\pot_o}}   &= f'(\pot_o) = 1 \\
# \frac{\partial \color{green}{\pot_o}}{\partial \color{red}{\weight_{10}}}           &= \sigout_4 \\
# \end{align}
# $$
#
# we can write:
#
# $$
# \frac{\partial \errfunc}{\partial \color{red}{\weight_{10}}} = 2(\sigout_o - \sigoutdes) \cdot f'(\pot_o) \cdot \sigout_4 = 2(\sigout_o - \sigoutdes) \cdot \sigout_4
# $$

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
grad_E_w10 = 2 * (y_pred - y_true) * y4
grad_E_w10

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# TODO...

# %%
# f = torch.nn.functional.tanh

# h1 = f(x[0] @ model.weight_ih_l0 + h0 @ model.weight_hh_l0)   # hidden state at time step 1
# h2 = f(x[1] @ model.weight_ih_l0 + h1 @ model.weight_hh_l0)   # hidden state at time step 2
# h3 = f(x[2] @ model.weight_ih_l0 + h2 @ model.weight_hh_l0)   # hidden state at time step 3

# print(f"Output for time step 1:\nh1 = \n{ h1 }\n\n")
# print(f"Output for time step 2:\nh2 = \n{ h2 }\n\n")
# print(f"Output for time step 3:\nh3 = \n{ h3 }\n\n")

# %% [markdown]
# ### Backward computation of $\frac{\partial \errfunc}{\partial \weight_9}$

# %%
display_nn(
    hidden_list=["x1", "x2", "y1", "y2", "y4", "s1", "s2", "s3", "s4", "n1", "n2", "n4", "w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w10"],
    highlight_list=["w9"]
)

# %% [markdown]
# $$
# \sigout_o =
# \activfunc \left(
# \overbrace{
#  \weight_9 ~ \ythree
#  +
#  \weight_{10} ~ \yfour
# }^{\pot_o}
# \right)
# $$

# %% [markdown]
# Using the chain rule:
#
# $$
# \frac{\partial \errfunc}{\partial \color{red}{\weight_9}}
# =
# \underbrace{
#  \frac{\partial \errfunc}{\partial \color{orange}{\sigout_o}}
#  \frac{\partial \color{orange}{\sigout_o}}{\partial \color{green}{\pot_o}} ~
# }_{\errsig_o}
# \frac{\partial \color{green}{\pot_o}}{\partial \color{red}{\weight_9}}
# =
# \errsig_o
# \frac{\partial \color{green}{\pot_o}}{\partial \color{red}{\weight_9}}
# $$
#
# knowing that:
#
# $$
# \begin{align}
# \frac{\partial \errfunc}{\partial \color{orange}{\sigout_o}}              &= 2 (\sigout_o - \sigoutdes) \\
# \frac{\partial \color{orange}{\sigout_o}}{\partial \color{green}{\pot_o}}   &= f'(\pot_o) = 1 \\
# \frac{\partial \color{green}{\pot_o}}{\partial \weight_9}           &= \sigout_3 \\
# \end{align}
# $$
#
# we can write:
#
# $$
# \frac{\partial \errfunc}{\partial \weight_9} = 2(\sigout_o - \sigoutdes) \cdot f'(\pot_o) \cdot \sigout_3 = 2(\sigout_o - \sigoutdes) \cdot \sigout_3
# $$

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
grad_E_w9 = 2 * (y_pred - y_true) * y3
grad_E_w9

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# TODO...

# %% [markdown]
# ### Backward computation of $\frac{\partial \errfunc}{\partial \weight_8}$

# %%
display_nn(
    hidden_list=["x1", "x2", "y1", "y3", "s1", "s2", "s3", "n1", "n3", "w1", "w2", "w3", "w4", "w5", "w6", "w7", "w9"],
    highlight_list=["w8"]
)

# %% [markdown]
# $$
# \sigout_o =
# \activfunc \left(
# \overbrace{
#  \weight_9 ~ \ythree
#  +
#  \weight_{10} ~ \yfour
# }^{\pot_o}
# \right)
# $$

# %% [markdown]
# Using the chain rule:
#
# $$
# \frac{\partial \errfunc}{\partial \color{red}{\weight_8}}
# =
# \underbrace{
#  \underbrace{
#   \frac{\partial \errfunc}{\partial \sigout_o}
#   \frac{\partial \sigout_o}{\partial \pot_o} ~
#  }_{\errsig_o}
#  \frac{\partial \pot_o}{\partial \sigout_4} ~
#  \frac{\partial \sigout_4}{\partial \pot_4} ~
# }_{\errsig_4}
# \frac{\partial \pot_4}{\partial \color{red}{\weight_8}}
# =
# \errsig_4
# \frac{\partial \pot_4}{\partial \color{red}{\weight_8}}
# $$

# %% [markdown]
# knowing that:
#
# $$
# \begin{align}
# \frac{\partial \errfunc}{\partial \sigout_o} &= 2 (\sigout_o - \sigoutdes) \\
# \frac{\partial \sigout_o}{\partial \pot_o}   &= f'(\pot_o) = 1 \\
# \frac{\partial \pot_o}{\partial \sigout_4}   &= \weight_{10} \\
# \frac{\partial \sigout_4}{\partial \pot_4}   &= f'(\pot_4) \\
# \frac{\partial \pot_4}{\partial \weight_8}   &= \sigout_2 \\
# \end{align}
# $$

# %% [markdown]
# we can write:
#
# $$
# \frac{\partial \errfunc}{\partial \weight_8} = 2(\sigout_o - \sigoutdes) \cdot \weight_{10} \cdot f'(\pot_4) \cdot \sigout_2
# $$

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
grad_E_w8 = 2 * (y_pred - y_true) * w10 * df(sigma4) * y2
grad_E_w8

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# TODO...

# %% [markdown]
# ### Backward computation of $\frac{\partial \errfunc}{\partial \weight_7}$

# %%
display_nn(
    hidden_list=["x1", "x2", "y1", "y4", "s1", "s2", "s4", "n1", "n4", "w1", "w2", "w3", "w4", "w5", "w6", "w8", "w10"],
    highlight_list=["w7"]
)

# %% [markdown]
# $$
# \sigout_o =
# \activfunc \left(
# \overbrace{
#  \weight_9 ~ \ythree
#  +
#  \weight_{10} ~ \yfour
# }^{\pot_o}
# \right)
# $$

# %% [markdown]
# Using the chain rule:
#
# $$
# \frac{\partial \errfunc}{\partial \color{red}{\weight_7}}
# =
# \underbrace{
#  \underbrace{
#   \frac{\partial \errfunc}{\partial \sigout_o}
#   \frac{\partial \sigout_o}{\partial \pot_o} ~
#  }_{\errsig_o}
#  \frac{\partial \pot_o}{\partial \sigout_3} ~
#  \frac{\partial \sigout_3}{\partial \pot_3} ~
# }_{\errsig_3}
# \frac{\partial \pot_3}{\partial \color{red}{\weight_7}}
# =
# \errsig_3
# \frac{\partial \pot_3}{\partial \color{red}{\weight_7}}
# $$

# %% [markdown]
# knowing that:
#
# $$
# \begin{align}
# \frac{\partial \errfunc}{\partial \sigout_o} &= 2 (\sigout_o - \sigoutdes) \\
# \frac{\partial \sigout_o}{\partial \pot_o}   &= f'(\pot_o) = 1 \\
# \frac{\partial \pot_o}{\partial \sigout_3}   &= \weight_9 \\
# \frac{\partial \sigout_3}{\partial \pot_3}   &= f'(\pot_3) \\
# \frac{\partial \pot_3}{\partial \color{red}{\weight_7}}   &= \sigout_2 \\
# \end{align}
# $$

# %% [markdown]
# we can write:
#
# $$
# \frac{\partial \errfunc}{\partial \weight_8}
# =
# 2(\sigout_o - \sigoutdes) \cdot
# \weight_9 \cdot
# f'(\pot_3) \cdot
# \sigout_2
# $$

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
grad_E_w7 = 2 * (y_pred - y_true) * w9 * df(sigma3) * y2
grad_E_w7

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# TODO...

# %% [markdown]
# ### Backward computation of $\frac{\partial \errfunc}{\partial \weight_6}$

# %%
display_nn(
    hidden_list=["x1", "x2", "y2", "y3", "s1", "s2", "s3", "n3", "n2", "w1", "w2", "w3", "w4", "w5", "w8", "w7", "w9"],
    highlight_list=["w6"]
)

# %% [markdown]
# $$
# \sigout_o =
# \activfunc \left(
# \overbrace{
#  \weight_9 ~ \ythree
#  +
#  \weight_{10} ~ \yfour
# }^{\pot_o}
# \right)
# $$

# %% [markdown]
# Using the chain rule:
#
# $$
# \frac{\partial \errfunc}{\partial \color{red}{\weight_6}}
# =
# \underbrace{
#  \underbrace{
#   \frac{\partial \errfunc}{\partial \sigout_o}
#   \frac{\partial \sigout_o}{\partial \pot_o} ~
#  }_{\errsig_o}
#  \frac{\partial \pot_o}{\partial \sigout_4} ~
#  \frac{\partial \sigout_4}{\partial \pot_4} ~
# }_{\errsig_4}
# \frac{\partial \pot_4}{\partial \color{red}{\weight_6}}
# =
# \errsig_4
# \frac{\partial \pot_4}{\partial \color{red}{\weight_6}}
# $$

# %% [markdown]
# knowing that:
#
# $$
# \begin{align}
# \frac{\partial \errfunc}{\partial \sigout_o} &= 2 (\sigout_o - \sigoutdes) \\
# \frac{\partial \sigout_o}{\partial \pot_o}   &= f'(\pot_o) = 1 \\
# \frac{\partial \pot_o}{\partial \sigout_4}   &= \weight_{10} \\
# \frac{\partial \sigout_4}{\partial \pot_4}   &= f'(\pot_4) \\
# \frac{\partial \pot_4}{\partial \color{red}{\weight_6}}   &= \sigout_1 \\
# \end{align}
# $$

# %% [markdown]
# we can write:
#
# $$
# \frac{\partial \errfunc}{\partial \weight_8}
# =
# 2(\sigout_o - \sigoutdes) \cdot
# \weight_{10} \cdot
# f'(\pot_4) \cdot
# \sigout_1
# $$

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
grad_E_w6 = 2 * (y_pred - y_true) * w10 * df(sigma4) * y1
grad_E_w6

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# TODO...

# %% [markdown]
# ### Backward computation of $\frac{\partial \errfunc}{\partial \weight_5}$

# %%
display_nn(
    hidden_list=["x1", "x2", "y2", "y4", "s1", "s2", "s4", "n2", "n4", "w1", "w2", "w3", "w4", "w8", "w6", "w7", "w10"],
    highlight_list=["w5"]
)

# %% [markdown]
# $$
# \sigout_o =
# \activfunc \left(
# \overbrace{
#  \weight_9 ~ \ythree
#  +
#  \weight_{10} ~ \yfour
# }^{\pot_o}
# \right)
# $$

# %% [markdown]
# Using the chain rule:
#
# $$
# \frac{\partial \errfunc}{\partial \color{red}{\weight_5}}
# =
# \underbrace{
#  \underbrace{
#   \frac{\partial \errfunc}{\partial \sigout_o}
#   \frac{\partial \sigout_o}{\partial \pot_o} ~
#  }_{\errsig_o}
#  \frac{\partial \pot_o}{\partial \sigout_3} ~
#  \frac{\partial \sigout_3}{\partial \pot_3} ~
# }_{\errsig_3}
# \frac{\partial \pot_3}{\partial \color{red}{\weight_5}}
# =
# \errsig_3
# \frac{\partial \pot_3}{\partial \color{red}{\weight_5}}
# $$

# %% [markdown]
# knowing that:
#
# $$
# \begin{align}
# \frac{\partial \errfunc}{\partial \sigout_o} &= 2 (\sigout_o - \sigoutdes) \\
# \frac{\partial \sigout_o}{\partial \pot_o}   &= f'(\pot_o) = 1 \\
# \frac{\partial \pot_o}{\partial \sigout_3}   &= \weight_9 \\
# \frac{\partial \sigout_3}{\partial \pot_3}   &= f'(\pot_3) \\
# \frac{\partial \pot_3}{\partial \color{red}{\weight_5}}   &= \sigout_1 \\
# \end{align}
# $$

# %% [markdown]
# we can write:
#
# $$
# \frac{\partial \errfunc}{\partial \weight_5}
# =
# 2(\sigout_o - \sigoutdes) \cdot
# \weight_9 \cdot
# f'(\pot_3) \cdot
# \sigout_1
# $$

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
grad_E_w5 = 2 * (y_pred - y_true) * w9 * df(sigma3) * y1
grad_E_w5

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# TODO...

# %% [markdown]
# ### Backward computation of $\frac{\partial \errfunc}{\partial \weight_4}$

# %%
display_nn(
    hidden_list=["x1", "y1", "s1", "n1", "w1", "w2", "w3", "w5", "w6"],
    highlight_list=["w4"]
)

# %% [markdown]
# $$
# \sigout_o =
# \activfunc \left(
# \overbrace{
#     \weight_9 ~
#     \underbrace{
#         \activfunc \left(
#             \overbrace{
#                 \weight_5 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_1 \feature_1 + \weight_3 \feature_2
#                         }^{\pot_1}
#                     \right)
#                 }_{\sigout_1}
#                 +
#                 \weight_7 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_2 \feature_1 + {\color{red}{\weight_4}} \feature_2
#                         }^{\pot_2}
#                     \right)
#                 }_{\sigout_2}
#             }^{\pot_3}
#         \right)
#     }_{\sigout_3}
#     +
#     \weight_{10} ~ \underbrace{
#         \activfunc \left(
#             \overbrace{
#                 \weight_6 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_1 \feature_1 + \weight_3 \feature_2
#                         }^{\pot_1}
#                     \right)
#                 }_{\sigout_1}
#                 +
#                 \weight_8 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_2 \feature_1 + {\color{red}{\weight_4}} \feature_2
#                         }^{\pot_2}
#                     \right)
#                 }_{\sigout_2}
#             }^{\pot_4}
#         \right)
#     }_{\sigout_4}
# }^{\pot_o}
# \right)
# $$

# %% [markdown]
# Using the chain rule:
#
# $$
# \frac{\partial \errfunc}{\partial \color{red}{\weight_4}}
# =
# \underbrace{
#     \left(
#         \underbrace{
#             \underbrace{
#                 \frac{\partial \errfunc}{\partial \sigout_o}
#                 \frac{\partial \sigout_o}{\partial \pot_o} ~
#             }_{\errsig_o}
#             \frac{\partial \pot_o}{\partial \sigout_4} ~
#             \frac{\partial \sigout_4}{\partial \pot_4} ~
#         }_{\errsig_4}
#         \frac{\partial \pot_4}{\partial \sigout_2} ~
#         +
#         \underbrace{
#             \underbrace{
#                 \frac{\partial \errfunc}{\partial \sigout_o}
#                 \frac{\partial \sigout_o}{\partial \pot_o} ~
#             }_{\errsig_o}
#             \frac{\partial \pot_o}{\partial \sigout_3} ~
#             \frac{\partial \sigout_3}{\partial \pot_3} ~
#         }_{\errsig_3}
#         \frac{\partial \pot_3}{\partial \sigout_2} ~
#     \right)
#     \frac{\partial \sigout_2}{\partial \pot_2} ~
# }_{\errsig_2}
# \frac{\partial \pot_2}{\partial \color{red}{\weight_4}}
# =
# \errsig_2
# \frac{\partial \pot_2}{\partial \color{red}{\weight_4}}
# $$

# %% [markdown]
# knowing that:
#
# $$
# \begin{align}
# \frac{\partial \errfunc}{\partial \sigout_o} &= 2 (\sigout_o - \sigoutdes) \\
# \frac{\partial \sigout_o}{\partial \pot_o}   &= f'(\pot_o) = 1 \\
# \frac{\partial \pot_o}{\partial \sigout_4}   &= \weight_{10} \\
# \frac{\partial \sigout_4}{\partial \pot_4}   &= f'(\pot_4) \\
# \frac{\partial \pot_4}{\partial \sigout_2}   &= \weight_8 \\
# \frac{\partial \pot_o}{\partial \sigout_3}   &= \weight_9 \\
# \frac{\partial \sigout_3}{\partial \pot_3}   &= f'(\pot_3) \\
# \frac{\partial \pot_3}{\partial \sigout_2}   &= \weight_7 \\
# \frac{\partial \sigout_2}{\partial \pot_2}   &= f'(\pot_2) \\
# \frac{\partial \pot_2}{\partial \color{red}{\weight_4}} &= \feature_2
#  \\
# \end{align}
# $$

# %% [markdown]
# we can write:
#
# $$
# \frac{\partial \errfunc}{\partial \weight_4}
# =
# 2(\sigout_o - \sigoutdes) \cdot
# f'(\pot_2) \cdot
# \weight_2
# \left(
#     \weight_{10} \cdot
#     f'(\pot_4) \cdot
#     \weight_8
#     +
#     \weight_9 \cdot
#     f'(\pot_3) \cdot
#     \weight_7
# \right)
# $$

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
grad_E_w4 = 2 * (y_pred - y_true) * df(sigma2) * x2 * (w10 * df(sigma4) * w8 + w9 * df(sigma3) * w7)
grad_E_w4

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# TODO...

# %% [markdown]
# ### Backward computation of $\frac{\partial \errfunc}{\partial \weight_3}$

# %%
display_nn(
    hidden_list=["x1", "y2", "s2", "n2", "w1", "w2", "w4", "w7", "w8"],
    highlight_list=["w3"]
)

# %% [markdown]
# $$
# \sigout_o =
# \activfunc \left(
# \overbrace{
#     \weight_9 ~
#     \underbrace{
#         \activfunc \left(
#             \overbrace{
#                 \weight_5 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_1 \feature_1 + {\color{red}{\weight_3}} \feature_2
#                         }^{\pot_1}
#                     \right)
#                 }_{\sigout_1}
#                 +
#                 \weight_7 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_2 \feature_1 + \weight_4 \feature_2
#                         }^{\pot_2}
#                     \right)
#                 }_{\sigout_2}
#             }^{\pot_3}
#         \right)
#     }_{\sigout_3}
#     +
#     \weight_{10} ~ \underbrace{
#         \activfunc \left(
#             \overbrace{
#                 \weight_6 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_1 \feature_1 + {\color{red}{\weight_3}} \feature_2
#                         }^{\pot_1}
#                     \right)
#                 }_{\sigout_1}
#                 +
#                 \weight_8 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_2 \feature_1 + \weight_4 \feature_2
#                         }^{\pot_2}
#                     \right)
#                 }_{\sigout_2}
#             }^{\pot_4}
#         \right)
#     }_{\sigout_4}
# }^{\pot_o}
# \right)
# $$

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
grad_E_w3 = 0
grad_E_w3

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# TODO...

# %% [markdown]
# ### Backward computation of $\frac{\partial \errfunc}{\partial \weight_2}$

# %%
display_nn(
    hidden_list=["x2", "y1", "s1", "n1", "w1", "w4", "w3", "w5", "w6"],
    highlight_list=["w2"]
)

# %% [markdown]
# $$
# \sigout_o =
# \activfunc \left(
# \overbrace{
#     \weight_9 ~
#     \underbrace{
#         \activfunc \left(
#             \overbrace{
#                 \weight_5 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_1 \feature_1 + \weight_3 \feature_2
#                         }^{\pot_1}
#                     \right)
#                 }_{\sigout_1}
#                 +
#                 \weight_7 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             {\color{red}{\weight_2}} \feature_1 + \weight_4 \feature_2
#                         }^{\pot_2}
#                     \right)
#                 }_{\sigout_2}
#             }^{\pot_3}
#         \right)
#     }_{\sigout_3}
#     +
#     \weight_{10} ~ \underbrace{
#         \activfunc \left(
#             \overbrace{
#                 \weight_6 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_1 \feature_1 + \weight_3 \feature_2
#                         }^{\pot_1}
#                     \right)
#                 }_{\sigout_1}
#                 +
#                 \weight_8 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             {\color{red}{\weight_2}} \feature_1 + \weight_4 \feature_2
#                         }^{\pot_2}
#                     \right)
#                 }_{\sigout_2}
#             }^{\pot_4}
#         \right)
#     }_{\sigout_4}
# }^{\pot_o}
# \right)
# $$

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
grad_E_w2 = 0
grad_E_w2

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# TODO...

# %% [markdown]
# ### Backward computation of $\frac{\partial \errfunc}{\partial \weight_1}$

# %%
display_nn(
    hidden_list=["x2", "y2", "s2", "n2", "w4", "w2", "w3", "w7", "w8"],
    highlight_list=["w1"]
)

# %% [markdown]
# $$
# \sigout_o =
# \activfunc \left(
# \overbrace{
#     \weight_9 ~
#     \underbrace{
#         \activfunc \left(
#             \overbrace{
#                 \weight_5 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             {\color{red}{\weight_1}} \feature_1 + \weight_3 \feature_2
#                         }^{\pot_1}
#                     \right)
#                 }_{\sigout_1}
#                 +
#                 \weight_7 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_2 \feature_1 + \weight_4 \feature_2
#                         }^{\pot_2}
#                     \right)
#                 }_{\sigout_2}
#             }^{\pot_3}
#         \right)
#     }_{\sigout_3}
#     +
#     \weight_{10} ~ \underbrace{
#         \activfunc \left(
#             \overbrace{
#                 \weight_6 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             {\color{red}{\weight_1}} \feature_1 + \weight_3 \feature_2
#                         }^{\pot_1}
#                     \right)
#                 }_{\sigout_1}
#                 +
#                 \weight_8 \underbrace{
#                     \activfunc \left(
#                         \overbrace{
#                             \weight_2 \feature_1 + \weight_4 \feature_2
#                         }^{\pot_2}
#                     \right)
#                 }_{\sigout_2}
#             }^{\pot_4}
#         \right)
#     }_{\sigout_4}
# }^{\pot_o}
# \right)
# $$

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
grad_E_w1 = 0
grad_E_w1

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# TODO...

# %% [markdown]
# ## Check backward computations result with PyTorch

# %%
error.backward()

# %%
# Get gradients
for name, param in model.named_parameters():
    if param.requires_grad:
        print(f"Gradient for {name}:")
        print(param.grad)
        print()

# %% [markdown]
# Let's compare with what we have manually computed:

# %%
grad_layer_0 = torch.tensor([[grad_E_w1, grad_E_w3], [grad_E_w2, grad_E_w4]])
print("Gradient for 0.weight:")
print(grad_layer_0)
print()

grad_layer_2 = torch.tensor([[grad_E_w5, grad_E_w7], [grad_E_w6, grad_E_w8]])
print("Gradient for 2.weight:")
print(grad_layer_2)
print()

grad_layer_4 = torch.tensor([[grad_E_w9, grad_E_w10]])
print("Gradient for 4.weight:")
print(grad_layer_4)
