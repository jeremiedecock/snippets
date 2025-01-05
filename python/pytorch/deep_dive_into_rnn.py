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
# # Deep dive into RNNs

# %%
# import itertools
# import matplotlib.pyplot as plt
# import networkx as nx
import torch
from torch.nn import RNN
from torch.nn import LSTM
from torch.nn import GRU

# %%
# # https://networkx.org/documentation/stable/auto_examples/drawing/plot_multipartite_graph.html#


# subset_sizes = [5, 5, 4, 3, 2, 4, 4, 3]
# subset_color = [
#     "gold",
#     "violet",
#     "violet",
#     "violet",
#     "violet",
#     "limegreen",
#     "limegreen",
#     "darkorange",
# ]


# def multilayered_graph(*subset_sizes):
#     extents = nx.utils.pairwise(itertools.accumulate((0,) + subset_sizes))
#     layers = [range(start, end) for start, end in extents]
#     G = nx.Graph()
#     for i, layer in enumerate(layers):
#         G.add_nodes_from(layer, layer=i)
#     for layer1, layer2 in nx.utils.pairwise(layers):
#         G.add_edges_from(itertools.product(layer1, layer2))
#     return G


# G = multilayered_graph(*subset_sizes)
# color = [subset_color[data["layer"]] for v, data in G.nodes(data=True)]
# pos = nx.multipartite_layout(G, subset_key="layer")
# plt.figure(figsize=(8, 8))
# nx.draw(G, pos, node_color=color, with_labels=False)
# plt.axis("equal")
# plt.show()

# %%
# import networkx as nx
# import itertools
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.patches import FancyArrowPatch

# # Taille des sous-ensembles (couches)
# subset_sizes = [3, 2, 3]

# # Couleurs pour les nœuds de chaque couche
# subset_color = [
#     "gold",
#     "violet",
#     "violet",
#     "violet",
#     "violet",
#     "limegreen",
#     "limegreen",
#     "darkorange",
# ]

# def multilayered_graph(*subset_sizes):
#     # Calcul des intervalles pour chaque couche
#     extents = nx.utils.pairwise(itertools.accumulate((0,) + subset_sizes))
#     layers = [range(start, end) for start, end in extents]
#     G = nx.DiGraph()  # Utilisation d'un graphe orienté pour représenter les boucles
#     for i, layer in enumerate(layers):
#         G.add_nodes_from(layer, layer=i)
#         node_list = list(layer)
#         # Ajout des arêtes entre tous les nœuds de la même couche
#         for u, v in itertools.permutations(node_list, 2):
#             G.add_edge(u, v)
#         # Ajout des boucles sur chaque nœud
#         for node in layer:
#             G.add_edge(node, node)
#     # Ajout des arêtes entre les couches adjacentes
#     for layer1, layer2 in nx.utils.pairwise(layers):
#         G.add_edges_from(itertools.product(layer1, layer2))
#     return G

# def draw_curved_edges(G, pos, ax):
#     # Création d'un dictionnaire pour stocker les arêtes entre les mêmes nœuds
#     edge_groups = {}
#     for u, v in G.edges():
#         if u == v:
#             # Boucle sur le même nœud
#             key = (u, v)
#         elif (v, u) in edge_groups:
#             # Arête existante dans l'autre sens
#             key = (v, u)
#         else:
#             key = (u, v)
#         edge_groups.setdefault(key, []).append((u, v))
    
#     for (u, v), edges in edge_groups.items():
#         num_edges = len(edges)
#         # Définition des courbures pour les arêtes multiples
#         if num_edges == 1:
#             rad_list = [0.0]
#         else:
#             rad_list = np.linspace(-0.5, 0.5, num_edges)
#         for (edge, rad) in zip(edges, rad_list):
#             u, v = edge
#             if u == v:
#                 # Boucle sur le même nœud avec une courbure fixe
#                 rad = 0.3
#             elif G.nodes[u]['layer'] == G.nodes[v]['layer']:
#                 # Ajustement de la courbure pour les arêtes dans la même couche
#                 rad *= 1.5
#             else:
#                 # Réduction de la courbure pour les arêtes entre couches
#                 rad *= 0.1
#             # Dessin de l'arête avec la courbure spécifiée
#             arrow = FancyArrowPatch(
#                 posA=pos[u], posB=pos[v],
#                 connectionstyle=f"arc3,rad={rad}",
#                 arrowstyle='-|>',
#                 mutation_scale=10.0,
#                 color='gray',
#                 linewidth=1.0,
#             )
#             ax.add_patch(arrow)

# G = multilayered_graph(*subset_sizes)
# color = [subset_color[data["layer"]] for v, data in G.nodes(data=True)]
# pos = nx.multipartite_layout(G, subset_key="layer")

# fig, ax = plt.subplots(figsize=(8, 8))
# nx.draw_networkx_nodes(G, pos, node_color=color, ax=ax)
# nx.draw_networkx_labels(G, pos, ax=ax)

# # Dessin des arêtes avec des courbes individuelles
# draw_curved_edges(G, pos, ax)

# plt.axis("equal")
# plt.axis('off')
# plt.show()


# %% [markdown]
# # RNN

# %%
# model.state_dict()
# model.weight_ih_l*   e.g. model.weight_ih_l0
# model.weight_hh_l*   e.g. model.weight_hh_l0
# model.bias_ih_l*   e.g. model.bias_ih_l0
# model.bias_hh_l*   e.g. model.bias_hh_l0
#
# model.all_weights
# model.hidden_size
# model.input_size
#
# list(model.parameters())
# model.get_expected_hidden_size()
# model.get_parameter()
#
# print("model.weight_hh_l0:", model.weight_hh_l0)
# print("model.weight_ih_l0:", model.weight_ih_l0)
# print("model.bias_ih_l0:", model.bias_ih_l0)
# print("model.bias_hh_l0:", model.bias_hh_l0)

# %% [markdown]
# ## One feature, one unit, one layer, no bias

# %% [markdown]
#
# <img src="assets/RNN1.drawio.svg" />

# %%
model = RNN(
    input_size=1,  # number of features in the input x
    hidden_size=1, # number of neurons in hidden layers
    num_layers=1,  # number of recurrent layers
    bias=False     # use bias?
)
model.state_dict() # print the weights and biases of the model

# %%
x = torch.randn(3, 1)    # (seq_len, input_size)
x

# %% [markdown]
# ### Forward pass

# %%
h0 = torch.zeros(model.num_layers, model.hidden_size)   # hidden state at time step 0 (initial hidden state), zeros by default
h0

# %%
y, hn = model(x, h0)
print(f"The hidden state at each time step:\ny = \n{ y }\n\n")
print(f"The hidden state of layer at the final time step:\nhn = \n{ hn }")

# %% [markdown]
# ### Forward computation

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
f = torch.nn.functional.tanh

x_1 = x[0,0]   # input for time step 1
x_2 = x[1,0]   # input for time step 2
x_3 = x[2,0]   # input for time step 3

h1 = f(x_1 * model.weight_ih_l0 + h0 * model.weight_hh_l0)   # hidden state at time step 1
h2 = f(x_2 * model.weight_ih_l0 + h1 * model.weight_hh_l0)   # hidden state at time step 2
h3 = f(x_3 * model.weight_ih_l0 + h2 * model.weight_hh_l0)   # hidden state at time step 3

print(f"Output for time step 1:\nh1 = \n{ h1 }\n\n")
print(f"Output for time step 2:\nh2 = \n{ h2 }\n\n")
print(f"Output for time step 3:\nh3 = \n{ h3 }\n\n")

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# $$
# \boldsymbol{h_t} = \tanh(\boldsymbol{x_t} \boldsymbol{W^{\top}_{ih}} + \boldsymbol{h_{t-1}} \boldsymbol{W^{\top}_{hh}})
# $$

# %%
f = torch.nn.functional.tanh

h1 = f(x[0] @ model.weight_ih_l0 + h0 @ model.weight_hh_l0)   # hidden state at time step 1
h2 = f(x[1] @ model.weight_ih_l0 + h1 @ model.weight_hh_l0)   # hidden state at time step 2
h3 = f(x[2] @ model.weight_ih_l0 + h2 @ model.weight_hh_l0)   # hidden state at time step 3

print(f"Output for time step 1:\nh1 = \n{ h1 }\n\n")
print(f"Output for time step 2:\nh2 = \n{ h2 }\n\n")
print(f"Output for time step 3:\nh3 = \n{ h3 }\n\n")

# %% [markdown]
# ## One feature, one unit, one layer, bias **[TODO]**

# %% [markdown]
#
# <img src="assets/RNN2.drawio.svg" />

# %%
model = RNN(input_size=1, hidden_size=1, num_layers=1, bias=True)
model.state_dict()

# %%
# x = torch.randn(10, 1, 1)    # (seq_len=10, batch_size=1, input_size=1)
x = torch.randn(3, 1)    # (seq_len=3, input_size=1)
x

# %%
y, hn = model(x)
print(f"y: {y}")
print(f"hn: {hn}")

# %% [markdown]
# ### Forward computation

# %% [markdown]
# #### Naive detailed computation

# %%
h0 = torch.nn.functional.tanh(model.weight_ih_l0 * x[0,0] + model.bias_ih_l0 + model.bias_hh_l0)
h1 = torch.nn.functional.tanh(model.weight_ih_l0 * x[1,0] + model.weight_hh_l0 * h0 + model.bias_ih_l0 + model.bias_hh_l0)
h2 = torch.nn.functional.tanh(model.weight_ih_l0 * x[2,0] + model.weight_hh_l0 * h1 + model.bias_ih_l0 + model.bias_hh_l0)

print(f"h0: { h0 }\nh1: { h1 }\nh2: { h2 }")

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# $$
# \boldsymbol{h_t} = \tanh(
#     \boldsymbol{x_t} \boldsymbol{W^{\top}_{ih}}
#     + \boldsymbol{b_{ih}}
#     + \boldsymbol{h_{t-1}} \boldsymbol{W^{\top}_{hh}}
#     + \boldsymbol{b_{hh}}
# )
# $$

# %%
h0 = torch.nn.functional.tanh(model.weight_ih_l0 @ x[0] + model.bias_ih_l0 + model.bias_hh_l0)
h1 = torch.nn.functional.tanh(model.weight_ih_l0 @ x[1] + model.weight_hh_l0 @ h0 + model.bias_ih_l0 + model.bias_hh_l0)
h2 = torch.nn.functional.tanh(model.weight_ih_l0 @ x[2] + model.weight_hh_l0 @ h1 + model.bias_ih_l0 + model.bias_hh_l0)

print(f"h0: { h0 }\nh1: { h1 }\nh2: { h2 }")

# %% [markdown]
# ## Three features, one unit, one layer, no bias **[TODO]**

# %% [markdown]
# <img src="assets/RNN3.drawio.svg" />

# %%
model = RNN(input_size=3, hidden_size=1, num_layers=1, bias=False)
model.state_dict()

# %%
x = torch.randn(10, 3)
x

# %%
model(x)

# %% [markdown]
# ## Three features, one unit, one layer, bias **[TODO]**

# %%
model = RNN(input_size=3, hidden_size=1, num_layers=1, bias=False)
model.state_dict()

# %% [markdown]
# ## One feature, two units, one layer, no bias **[TODO]**

# %%
model = RNN(input_size=1, hidden_size=2, num_layers=1, bias=False)
model.state_dict()

# %% [markdown]
# ## One feature, two units, one layer, bias **[TODO]**

# %%
model = RNN(input_size=1, hidden_size=2, num_layers=1, bias=True)
model.state_dict()

# %% [markdown]
# ## Three features, two units, one layer, no bias **[TODO]**

# %% [markdown]
# <img src="assets/RNN4.drawio.svg" />
# <br>
# <img src="assets/rnn_matrix.drawio.svg" />
#
# $$
# \boldsymbol{h_t} = f(
# \color{red}{\boldsymbol{W^{\top}_{ih}}} \color{green}{\boldsymbol{x_t}}
# + \color{orange}{\boldsymbol{W^{\top}_{hh}}} \boldsymbol{h_{t-1}})
# $$

# %%
model = RNN(input_size=3, hidden_size=2, num_layers=1, bias=False)
model.state_dict()

# %%
# x = torch.randn(10, 1, 3)    # (seq_len=10, batch_size=1, input_size=3)
x = torch.randn(4, 3)    # (seq_len=3, input_size=1)
x

# %%
y, hn = model(x)
print(f"y: {y}")
print(f"hn: {hn}")

# %% [markdown]
# ### Forward computation

# %% [markdown]
# #### Naive detailed computation

# %%
h0_0 = torch.nn.functional.tanh(model.weight_ih_l0[0,0] * x[0,0] + model.weight_ih_l0[0,1] * x[0,1] + model.weight_ih_l0[0,2] * x[0,2])
h0_1 = torch.nn.functional.tanh(model.weight_ih_l0[1,0] * x[0,0] + model.weight_ih_l0[1,1] * x[0,1] + model.weight_ih_l0[1,2] * x[0,2])

h1_0 = torch.nn.functional.tanh(model.weight_ih_l0[0,0] * x[1,0] + model.weight_ih_l0[0,1] * x[1,1] + model.weight_ih_l0[0,2] * x[1,2] + model.weight_hh_l0[0,0] * h0_0 + model.weight_hh_l0[0,1] * h0_1)
h1_1 = torch.nn.functional.tanh(model.weight_ih_l0[1,0] * x[1,0] + model.weight_ih_l0[1,1] * x[1,1] + model.weight_ih_l0[1,2] * x[1,2] + model.weight_hh_l0[1,0] * h0_0 + model.weight_hh_l0[1,1] * h0_1)

h2_0 = torch.nn.functional.tanh(model.weight_ih_l0[0,0] * x[2,0] + model.weight_ih_l0[0,1] * x[2,1] + model.weight_ih_l0[0,2] * x[2,2] + model.weight_hh_l0[0,0] * h1_0 + model.weight_hh_l0[0,1] * h1_1)
h2_1 = torch.nn.functional.tanh(model.weight_ih_l0[1,0] * x[2,0] + model.weight_ih_l0[1,1] * x[2,1] + model.weight_ih_l0[1,2] * x[2,2] + model.weight_hh_l0[1,0] * h1_0 + model.weight_hh_l0[1,1] * h1_1)

h3_0 = torch.nn.functional.tanh(model.weight_ih_l0[0,0] * x[3,0] + model.weight_ih_l0[0,1] * x[3,1] + model.weight_ih_l0[0,2] * x[3,2] + model.weight_hh_l0[0,0] * h2_0 + model.weight_hh_l0[0,1] * h2_1)
h3_1 = torch.nn.functional.tanh(model.weight_ih_l0[1,0] * x[3,0] + model.weight_ih_l0[1,1] * x[3,1] + model.weight_ih_l0[1,2] * x[3,2] + model.weight_hh_l0[1,0] * h2_0 + model.weight_hh_l0[1,1] * h2_1)

print(f"h0: ({ h0_0 }, { h0_1 })\nh1: ({ h1_0 }, { h1_1 })\nh2: ({ h2_0 }, { h2_1 })\nh3: ({ h3_0 }, { h3_1 })")

# %% [markdown]
# #### Algebraic computation

# %%
h0 = torch.nn.functional.tanh(model.weight_ih_l0 @ x[0])
h1 = torch.nn.functional.tanh(model.weight_ih_l0 @ x[1] + model.weight_hh_l0 @ h0)
h2 = torch.nn.functional.tanh(model.weight_ih_l0 @ x[2] + model.weight_hh_l0 @ h1)
h3 = torch.nn.functional.tanh(model.weight_ih_l0 @ x[3] + model.weight_hh_l0 @ h2)

print(f"h0: { h0 }\nh1: { h1 }\nh2: { h2 }\nh3: { h3 }")

# %% [markdown]
# ## One feature, one units, one layer, bias **[TODO]**

# %% [markdown]
#
# <img src="assets/RNN4b.drawio.svg" />

# %%
model = RNN(input_size=3, hidden_size=2, num_layers=1, bias=True)
model.state_dict()

# %%
# x = torch.randn(10, 1, 3)    # (seq_len=10, batch_size=1, input_size=3)
x = torch.randn(4, 3)    # (seq_len=3, input_size=1)
x

# %%
y, hn = model(x)
print(f"y: {y}")
print(f"hn: {hn}")

# %% [markdown]
# ### Forward computation

# %% [markdown]
# #### Naive detailed computation

# %%
h0_0 = torch.nn.functional.tanh(model.weight_ih_l0[0,0] * x[0,0] + model.weight_ih_l0[0,1] * x[0,1] + model.weight_ih_l0[0,2] * x[0,2] + model.bias_ih_l0[0] + model.bias_hh_l0[0])
h0_1 = torch.nn.functional.tanh(model.weight_ih_l0[1,0] * x[0,0] + model.weight_ih_l0[1,1] * x[0,1] + model.weight_ih_l0[1,2] * x[0,2] + model.bias_ih_l0[1] + model.bias_hh_l0[1])

h1_0 = torch.nn.functional.tanh(model.weight_ih_l0[0,0] * x[1,0] + model.weight_ih_l0[0,1] * x[1,1] + model.weight_ih_l0[0,2] * x[1,2] + model.weight_hh_l0[0,0] * h0_0 + model.weight_hh_l0[0,1] * h0_1 + model.bias_ih_l0[0] + model.bias_hh_l0[0])
h1_1 = torch.nn.functional.tanh(model.weight_ih_l0[1,0] * x[1,0] + model.weight_ih_l0[1,1] * x[1,1] + model.weight_ih_l0[1,2] * x[1,2] + model.weight_hh_l0[1,0] * h0_0 + model.weight_hh_l0[1,1] * h0_1 + model.bias_ih_l0[1] + model.bias_hh_l0[1])

h2_0 = torch.nn.functional.tanh(model.weight_ih_l0[0,0] * x[2,0] + model.weight_ih_l0[0,1] * x[2,1] + model.weight_ih_l0[0,2] * x[2,2] + model.weight_hh_l0[0,0] * h1_0 + model.weight_hh_l0[0,1] * h1_1 + model.bias_ih_l0[0] + model.bias_hh_l0[0])
h2_1 = torch.nn.functional.tanh(model.weight_ih_l0[1,0] * x[2,0] + model.weight_ih_l0[1,1] * x[2,1] + model.weight_ih_l0[1,2] * x[2,2] + model.weight_hh_l0[1,0] * h1_0 + model.weight_hh_l0[1,1] * h1_1 + model.bias_ih_l0[1] + model.bias_hh_l0[1])

h3_0 = torch.nn.functional.tanh(model.weight_ih_l0[0,0] * x[3,0] + model.weight_ih_l0[0,1] * x[3,1] + model.weight_ih_l0[0,2] * x[3,2] + model.weight_hh_l0[0,0] * h2_0 + model.weight_hh_l0[0,1] * h2_1 + model.bias_ih_l0[0] + model.bias_hh_l0[0])
h3_1 = torch.nn.functional.tanh(model.weight_ih_l0[1,0] * x[3,0] + model.weight_ih_l0[1,1] * x[3,1] + model.weight_ih_l0[1,2] * x[3,2] + model.weight_hh_l0[1,0] * h2_0 + model.weight_hh_l0[1,1] * h2_1 + model.bias_ih_l0[1] + model.bias_hh_l0[1])

print(f"h0: ({ h0_0 }, { h0_1 })\nh1: ({ h1_0 }, { h1_1 })\nh2: ({ h2_0 }, { h2_1 })\nh3: ({ h3_0 }, { h3_1 })")

# %% [markdown]
# #### Algebraic computation

# %%
h0 = torch.nn.functional.tanh(model.weight_ih_l0 @ x[0] + model.bias_ih_l0 + model.bias_hh_l0)
h1 = torch.nn.functional.tanh(model.weight_ih_l0 @ x[1] + model.weight_hh_l0 @ h0 + model.bias_ih_l0 + model.bias_hh_l0)
h2 = torch.nn.functional.tanh(model.weight_ih_l0 @ x[2] + model.weight_hh_l0 @ h1 + model.bias_ih_l0 + model.bias_hh_l0)
h3 = torch.nn.functional.tanh(model.weight_ih_l0 @ x[3] + model.weight_hh_l0 @ h2 + model.bias_ih_l0 + model.bias_hh_l0)

print(f"h0: { h0 }\nh1: { h1 }\nh2: { h2 }\nh3: { h3 }")

# %% [markdown]
# ## One feature, one unit, two layers (stacked RNN), no bias

# %%
model = RNN(
    input_size=1,  # number of features in the input x
    hidden_size=1, # number of neurons in hidden layers
    num_layers=2,  # number of recurrent layers
    bias=False     # use bias?
)
model.state_dict() # print the weights and biases of the model

# %%
x = torch.randn(3, 1)    # (seq_len, input_size)
x

# %% [markdown]
# ### Forward pass

# %%
h0 = torch.zeros(model.num_layers, model.hidden_size)   # hidden state at time step 0 (initial hidden state), zeros by default
h0

# %%
y, hn = model(x, h0)
print(f"The hidden state at each time step:\ny = \n{ y }\n\n")
print(f"The hidden state of layer at the final time step:\nhn = \n{ hn }")

# %% [markdown]
# ### Forward computation

# %% [markdown]
# Forward pseudo code:
#
# ```python
# def forward(x, h_0=None):
#     h_t_minus_1 = h_0
#     h_t = h_0
#     output = []
#     for t in range(seq_len):
#
#         input_t = x[t]
#         for layer in range(num_layers):
#             h_t[layer] = torch.tanh(
#                 input_t @ weight_ih[layer].T
#                 + h_t_minus_1[layer] @ weight_hh[layer].T
#             )
#             input_t = h_t[layer]    # The output of the current layer is the input of the next layer
#
#         output.append(h_t[-1])
#         h_t_minus_1 = h_t
#
#     output = torch.stack(output)
#     return output, h_t
# ```

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
f = torch.nn.functional.tanh

x_1 = x[0,0]   # input for time step 1
x_2 = x[1,0]   # input for time step 2
x_3 = x[2,0]   # input for time step 3

h0_l0 = h0[0,0]   # hidden state at time step 0 for layer 0
h0_l1 = h0[1,0]   # hidden state at time step 0 for layer 1

# Hidden state at time step 1
h1_l0 = f(  x_1 * model.weight_ih_l0 + h0_l0 * model.weight_hh_l0)
h1_l1 = f(h1_l0 * model.weight_ih_l1 + h0_l1 * model.weight_hh_l1)
h1 = torch.tensor([[h1_l0], [h1_l1]])

# Hidden state at time step 2
h2_l0 = f(  x_2 * model.weight_ih_l0 + h1_l0 * model.weight_hh_l0)
h2_l1 = f(h2_l0 * model.weight_ih_l1 + h1_l1 * model.weight_hh_l1)
h2 = torch.tensor([[h2_l0], [h2_l1]])

# Hidden state at time step 3
h3_l0 = f(  x_3 * model.weight_ih_l0 + h2_l0 * model.weight_hh_l0)
h3_l1 = f(h3_l0 * model.weight_ih_l1 + h2_l1 * model.weight_hh_l1)
h3 = torch.tensor([[h3_l0], [h3_l1]])

print(f"Output for time step 1:\nh1 = \n{ h1 }\n\n")
print(f"Output for time step 2:\nh2 = \n{ h2 }\n\n")
print(f"Output for time step 3:\nh3 = \n{ h3 }\n\n")

print(f"The hidden state at each time step:\ny = \n{ torch.tensor([h1_l1, h2_l1, h3_l1]).unsqueeze(1) }\n\n")
print(f"The hidden state of layer at the final time step:\nhn = \n{ h3 }")

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# - First layer ($l = 0$):
# $$
# \boldsymbol{h}^{(0)}_t = \tanh\left( \boldsymbol{x}_t \boldsymbol{W}^{(0)}_{ih} + \boldsymbol{h}^{(0)}_{t-1} \boldsymbol{W}^{(0)}_{hh} \right)
# $$
#
# - Next layers ($l \geq 1$):
# $$
# \boldsymbol{h}^{(l)}_t = \tanh\left(\boldsymbol{h}^{(l-1)}_t \boldsymbol{W}^{(l)}_{ih} + \boldsymbol{h}^{(l)}_{t-1} \boldsymbol{W}^{(l)}_{hh} \right)
# $$

# %%
f = torch.nn.functional.tanh

# Time step 1 (h1)
h1_l0 = f( x[0] @ model.weight_ih_l0 + h0[0] @ model.weight_hh_l0)
h1_l1 = f(h1_l0 @ model.weight_ih_l1 + h0[1] @ model.weight_hh_l1)
h1 = torch.stack([h1_l0, h1_l1])

# Time step 2 (h2)
h2_l0 = f( x[1] @ model.weight_ih_l0 + h1[0] @ model.weight_hh_l0)
h2_l1 = f(h2_l0 @ model.weight_ih_l1 + h1[1] @ model.weight_hh_l1)
h2 = torch.stack([h2_l0, h2_l1])

# Time step 3 (h3)
h3_l0 = f( x[2] @ model.weight_ih_l0 + h2[0] @ model.weight_hh_l0)
h3_l1 = f(h3_l0 @ model.weight_ih_l1 + h2[1] @ model.weight_hh_l1)
h3 = torch.stack([h3_l0, h3_l1])

print(f"Output for time step 1:\nh1 = \n{ h1 }\n\n")
print(f"Output for time step 2:\nh2 = \n{ h2 }\n\n")
print(f"Output for time step 3:\nh3 = \n{ h3 }\n\n")

print(f"The hidden state at each time step:\ny = \n{ torch.tensor([h1_l1, h2_l1, h3_l1]).unsqueeze(1) }\n\n")
print(f"The hidden state of layers at the final time step:\nhn = \n{ h3 }")

# %% [markdown]
# ## Three features, two units, two layers (stacked RNN), no bias **[TODO]**

# %% [markdown]
# <img src="assets/RNN5.drawio.svg" />
# <br>
# <img src="assets/stacked_rnn_matrix.drawio.svg" />
#
# - First layer ($l = 0$):
# $$
# \Large
# \boldsymbol{h}^{(0)}_t = f\left( \boldsymbol{W}^{(0)\top}_{ih} \boldsymbol{x}_t + \boldsymbol{W}^{(0)\top}_{hh} \boldsymbol{h}^{(0)}_{t-1} \right)
# $$
#
# - Next layers ($l \geq 1$):
# $$
# \Large
# \boldsymbol{h}^{(l)}_t = f\left(\boldsymbol{W}^{(l)\top}_{ih} \boldsymbol{h}^{(l\color{red}{-1})}_{\color{red}{t}} + \boldsymbol{W}^{(l)\top}_{hh} \boldsymbol{h}^{(l)}_{t\color{red}{-1}} \right)
# $$

# %%
model = RNN(input_size=3, hidden_size=2, num_layers=2, bias=False)
model.state_dict()

# %%
x = torch.randn(10, 1, 3)    # (seq_len=10, batch_size=1, input_size=3)
x

# %%
y = model(x)
y

# %% [markdown]
# ## Three features, two units, four layers (stacked RNN), no bias **[TODO]**

# %% [markdown]
#
# <img src="assets/RNN6.drawio.svg" />

# %%
model = RNN(input_size=3, hidden_size=2, num_layers=4, bias=False)
model.state_dict()

# %%
x = torch.randn(10, 3)
x

# %%
model(x)

# %% [markdown]
# ## One feature, one unit, one layer, no bias, bidirectionnal

# %%
model = RNN(
    input_size=1,       # number of features in the input x
    hidden_size=1,      # number of neurons in hidden layers
    num_layers=1,       # number of recurrent layers
    bias=False,         # don't use bias
    bidirectional=True  # bidirectional RNN
)
model.state_dict()      # print the weights and biases of the model

# %%
x = torch.randn(3, 1)    # (seq_len, input_size)
x

# %% [markdown]
# ### Forward pass

# %%
num_directions = 2 if model.bidirectional else 1

h0 = torch.zeros(model.num_layers * num_directions, model.hidden_size)   # hidden state at time step 0 (initial hidden state), zeros by default
h0

# %%
y, hn = model(x, h0)
print(f"y (hidden states at each time step):\ny = \n{ y }\n\n")
print(f"hn (final hidden states):\nhn = \n{ hn }")

# %% [markdown]
# ### Forward computation

# %% [markdown]
# #### Naive detailed computation

# %% [markdown]
# Let's write the forward computation in a (naive) detailed way.

# %%
f = torch.nn.functional.tanh

x_1 = x[0,0]   # input for time step 1
x_2 = x[1,0]   # input for time step 2
x_3 = x[2,0]   # input for time step 3

# Forward weights
W_ih_f = model.weight_ih_l0      # shape (hidden_size, input_size)
W_hh_f = model.weight_hh_l0      # shape (hidden_size, hidden_size)

# Backward weights
W_ih_b = model.weight_ih_l0_reverse
W_hh_b = model.weight_hh_l0_reverse

# Extract initial forward and backward hidden states
h0_f = h0[0]  # forward initial hidden state
h0_b = h0[1]  # backward initial hidden state

# Forward computation over time
h1_f = f(x_1 * W_ih_f + h0_f * W_hh_f)
h2_f = f(x_2 * W_ih_f + h1_f * W_hh_f)
h3_f = f(x_3 * W_ih_f + h2_f * W_hh_f)

# Backward computation (reverse time order)
# Start from the end (x[2]) with h0_b
h1_b = f(x_3 * W_ih_b + h0_b * W_hh_b)
h2_b = f(x_2 * W_ih_b + h1_b * W_hh_b)
h3_b = f(x_1 * W_ih_b + h2_b * W_hh_b)

# The output at time t is the concatenation of the forward state at t
# and the backward state at (seq_len - t - 1).
y = torch.tensor([
    [h1_f, h3_b],  # at t=0, forward is h1_f, backward is h3_b (from end)
    [h2_f, h2_b],  # at t=1, forward is h2_f, backward is h2_b
    [h3_f, h1_b]   # at t=2, forward is h3_f, backward is h1_b (from start)
])

# The final hidden state hn consists of the last forward state (h3_f)
# and the first backward state computed (h1_b).
hn = torch.tensor([[h3_f], [h1_b]])

print(f"y (hidden states at each time step):\ny = \n{ y }\n\n")
print(f"hn (final hidden states):\nhn = \n{ hn }")

# %% [markdown]
# #### Algebraic computation

# %% [markdown]
# Let's rewrite the forward computation in a less naive way (using linear algebra).

# %% [markdown]
# - Direction forward ($\color{red}{\text{from } t=1 \text{ to } t=T}$) :
#
# $$
# \boldsymbol{h}_t^{(f)} = \tanh\left( \boldsymbol{x}_t \boldsymbol{W}_{ih}^{(f)} + \boldsymbol{h}_{t-1}^{(f)} \boldsymbol{W}_{hh}^{(f)} \right), \quad\quad \text{with } \boldsymbol{h}_0^{(f)} = \boldsymbol{0}
# $$
#
# - Direction backward ($\color{red}{\text{from } t=T \text{ to } t=1}$) :
#
# $$
# \boldsymbol{h}_t^{(b)} = \tanh\left( \boldsymbol{x}_t \boldsymbol{W}_{ih}^{(b)} + \boldsymbol{h}_{t+1}^{(b)} \boldsymbol{W}_{hh}^{(b)} \right), \quad\quad \text{with } \boldsymbol{h}_{T+1}^{(b)} = \boldsymbol{0}
# $$
#
# The representation of the bidirectional hidden state at time t is then the concatenation of the two:
#
# $$
# \boldsymbol{h}_t = 
# \begin{bmatrix}
# \boldsymbol{h}_t^{(f)} \\
# \boldsymbol{h}_t^{(b)}
# \end{bmatrix}^{\top}
# $$

# %%
f = torch.nn.functional.tanh

# Forward weights
W_ih_f = model.weight_ih_l0      # shape (hidden_size, input_size)
W_hh_f = model.weight_hh_l0      # shape (hidden_size, hidden_size)

# Backward weights
W_ih_b = model.weight_ih_l0_reverse
W_hh_b = model.weight_hh_l0_reverse

# Extract initial forward and backward hidden states
h0_f = h0[0]  # forward initial hidden state
h0_b = h0[1]  # backward initial hidden state

# Forward computation over time
h1_f = f(x[0] @ W_ih_f.T + h0_f @ W_hh_f.T)
h2_f = f(x[1] @ W_ih_f.T + h1_f @ W_hh_f.T)
h3_f = f(x[2] @ W_ih_f.T + h2_f @ W_hh_f.T)

# Backward computation (reverse time order)
# Start from the end (x[2]) with h0_b
h1_b = f(x[2] @ W_ih_b.T + h0_b @ W_hh_b.T)
h2_b = f(x[1] @ W_ih_b.T + h1_b @ W_hh_b.T)
h3_b = f(x[0] @ W_ih_b.T + h2_b @ W_hh_b.T)

# The output at time t is the concatenation of the forward state at t
# and the backward state at (seq_len - t - 1).
y = torch.tensor([
    [h1_f, h3_b],  # at t=0, forward is h1_f, backward is h3_b (from end)
    [h2_f, h2_b],  # at t=1, forward is h2_f, backward is h2_b
    [h3_f, h1_b]   # at t=2, forward is h3_f, backward is h1_b (from start)
])

# The final hidden state hn consists of the last forward state (h3_f)
# and the first backward state computed (h1_b).
hn = torch.tensor([[h3_f], [h1_b]])

print(f"y (hidden states at each time step):\ny = \n{ y }\n\n")
print(f"hn (final hidden states):\nhn = \n{ hn }")

# %% [markdown]
# ## One feature, one unit, one layer, bias, bidirectionnal **[TODO]**

# %%
model = RNN(input_size=1, hidden_size=1, num_layers=1, bias=True, bidirectional=True)
model.state_dict()

# %% [markdown]
# Forward pseudo code (see https://pytorch.org/docs/stable/generated/torch.nn.RNN.html#torch.nn.RNN):
#
# ```python
# def forward(x, h_0=None):
#     h_t_minus_1 = h_0
#     h_t = h_0
#     output = []
#     for t in range(seq_len):
#
#         for layer in range(num_layers):
#             h_t[layer] = torch.tanh(
#                 x[t] @ weight_ih[layer].T
#                 + bias_ih[layer]
#                 + h_t_minus_1[layer] @ weight_hh[layer].T
#                 + bias_hh[layer]
#             )
#         output.append(h_t[-1])
#         h_t_minus_1 = h_t
#
#     output = torch.stack(output)
#     return output, h_t
# ```

# %% [markdown]
# # LSTM
