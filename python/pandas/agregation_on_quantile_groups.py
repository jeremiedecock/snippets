# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import pandas as pd

# %% [markdown]
# # Example of a NumPy array

# %%
df = pd.DataFrame(np.random.rand(10000), columns=['x'])

# %% [markdown]
# # Define the quantile intervals

# %%
quantile_intervals = [0, 0.25, 0.5, 0.75, 1.0]

# %% [markdown]
# # Use pd.qcut to create quantile groups

# %%
df['quantile_group'] = pd.qcut(df['x'], q=quantile_intervals, labels=["0-25%", "25-50%", "50-75%", "75-100%"])
print(df)

# %% [markdown]
# # Aggregate data by quantile groups

# %%
agg_result = df.groupby('quantile_group')['x'].agg(['mean', 'sum', 'count', 'min', 'max'])

# %% [markdown]
# # Print results

# %%
print(agg_result)

# %% [markdown]
# # Check results

# %%
quantile = df.x.quantile(0.25)
print(quantile)

# %%
df.loc[df.x <= quantile, ["x"]].mean()

# %%
df.loc[df.x <= quantile, ["x"]].sum()

# %%
df.loc[df.x <= quantile, ["x"]].count()

# %%
df.loc[df.x <= quantile, ["x"]].min()

# %%
df.loc[df.x <= quantile, ["x"]].max()
