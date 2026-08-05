import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('homework_12.2.csv', index_col=0)

# Filter to pre-treatment period (Time < 0)
df_pre = df[df['Time'] < 0].copy()

print(f"Dataset 12.2 - Pre-Treatment Period Analysis (Time < 0)")
print(f"Number of observations: {len(df_pre)}")
print(f"Treatment group (Group=1): {(df_pre['Group']==1).sum()}")
print(f"Control group (Group=0): {(df_pre['Group']==0).sum()}\n")

# Create interaction term
df_pre['group_time'] = df_pre['Group'] * df_pre['Time']

# Set up regression: Y = β₀ + β₁*Group + β₂*Time + β₃*Group*Time + ε
X = np.column_stack([
    np.ones(len(df_pre)),
    df_pre['Group'],
    df_pre['Time'],
    df_pre['group_time']
])

y = df_pre['Y'].values

# OLS regression
beta = np.linalg.lstsq(X, y, rcond=None)[0]

# Calculate standard errors
residuals = y - X @ beta
n = len(y)
k = X.shape[1]
residual_variance = (residuals ** 2).sum() / (n - k)
var_covar_matrix = residual_variance * np.linalg.inv(X.T @ X)
se = np.sqrt(np.diag(var_covar_matrix))

# T-statistics
t_stats = beta / se

print("="*70)
print("PARALLEL TRENDS TEST (PRE-TREATMENT PERIOD)")
print("="*70)
print(f"Regression: Y ~ Constant + Group + Time + Group*Time\n")

labels = ['Constant', 'Group', 'Time', 'Group x Time (Interaction)']
for i, label in enumerate(labels):
    print(f"{label:35} {beta[i]:10.6f}  (SE: {se[i]:.6f}, t: {t_stats[i]:8.4f})")

print("\n" + "="*70)
print(f"INTERACTION TERM (Group x Time) T-VALUE: {t_stats[3]:.4f}")
print("="*70)
print("\nInterpretation: A t-value close to 0 suggests parallel trends")
print("(similar pre-treatment trends between groups)")
