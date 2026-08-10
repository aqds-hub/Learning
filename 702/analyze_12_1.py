import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('homework_12.1.csv', index_col=0)

# Create treatment indicator: Group==1 AND Time>0
df['treated'] = ((df['Group'] == 1) & (df['Time'] > 0)).astype(int)
df['is_treatment_group'] = (df['Group'] == 1).astype(int)
df['is_post_treatment'] = (df['Time'] > 0).astype(int)

print("Dataset summary:")
print(df.head(10))
print(f"\nDataset shape: {df.shape}")
print(f"\nNumber treated (Group=1 AND Time>0): {df['treated'].sum()}")

# Difference-in-Differences Estimator
# Y = β₀ + β₁*Group + β₂*(Time>0) + β₃*Treated + ε
# where Treated = Group * (Time > 0)

X = np.column_stack([
    np.ones(len(df)),
    df['is_treatment_group'],
    df['is_post_treatment'],
    df['treated']
])

y = df['Y'].values

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

print("\n" + "="*60)
print("DIFFERENCE-IN-DIFFERENCES REGRESSION RESULTS")
print("="*60)
print(f"\nDependent Variable: Y")
print(f"Number of Observations: {n}\n")

labels = ['Constant', 'Group (Treatment Group)', 'Post-Treatment (Time>0)', 'Treatment Effect (DiD)']
for i, label in enumerate(labels):
    print(f"{label:40} {beta[i]:10.6f}  (SE: {se[i]:.6f}, t: {t_stats[i]:7.4f})")

print("\n" + "="*60)
print(f"TREATMENT EFFECT (DiD Estimator): {beta[3]:.6f}")
print(f"Standard Error: {se[3]:.6f}")
print(f"95% CI: [{beta[3] - 1.96*se[3]:.6f}, {beta[3] + 1.96*se[3]:.6f}]")
print("="*60)

# Alternative calculation: Simple DiD
# Effect = (Mean Y for Treatment Post) - (Mean Y for Treatment Pre) - [(Mean Y for Control Post) - (Mean Y for Control Pre)]
treatment_post = df[(df['Group']==1) & (df['Time']>0)]['Y'].mean()
treatment_pre = df[(df['Group']==1) & (df['Time']<=0)]['Y'].mean()
control_post = df[(df['Group']==0) & (df['Time']>0)]['Y'].mean()
control_pre = df[(df['Group']==0) & (df['Time']<=0)]['Y'].mean()

simple_did = (treatment_post - treatment_pre) - (control_post - control_pre)
print(f"\nVerification using simple DiD calculation: {simple_did:.6f}")
print(f"  Treatment group change (pre→post): {treatment_post - treatment_pre:.6f}")
print(f"  Control group change (pre→post): {control_post - control_pre:.6f}")
print(f"  Treatment group means - Pre: {treatment_pre:.6f}, Post: {treatment_post:.6f}")
print(f"  Control group means - Pre: {control_pre:.6f}, Post: {control_post:.6f}")
