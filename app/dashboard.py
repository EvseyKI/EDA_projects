import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from explainerdashboard import RegressionExplainer, ExplainerDashboard
from sklearn.model_selection import train_test_split

link_to_dataset = 'https://raw.githubusercontent.com/aiedu-courses/eda_and_dev_tools/refs/heads/main/datasets/abalone.csv'

df  = pd.read_csv(link_to_dataset)

df.fillna({
    'Diameter': df['Diameter'].median(),
    'Whole weight': df['Whole weight'].median(),
    'Shell weight': df['Shell weight'].median()
}, inplace=True)
df = df[df['Height'] > 0]
df['Sex'] = df['Sex'].replace('f', 'F')
df['Age'] = df['Rings'] + 1.5

x_full = df.drop(['Rings', 'Age'], axis=1)
y = df['Age']
X_train_full, X_test_full, y_train_full, y_test_full = train_test_split(x_full, y, test_size=0.25, random_state=42)

encoder = OneHotEncoder(drop='first', sparse_output=False)
encoded_sex = encoder.fit_transform(X_train_full[['Sex']])

encoded_sex_df = pd.DataFrame(encoded_sex, columns=encoder.get_feature_names_out(['Sex']), index=X_train_full.index)

X_train_full_encoded = X_train_full.drop('Sex', axis=1)
X_train_full_encoded = pd.concat([X_train_full_encoded, encoded_sex_df], axis=1)

encoded_sex_test = encoder.transform(X_test_full[['Sex']])
encoded_sex_test_df = pd.DataFrame(encoded_sex_test, columns=encoder.get_feature_names_out(['Sex']), index=X_test_full.index)

X_test_full_encoded = X_test_full.drop('Sex', axis=1)
X_test_full_encoded = pd.concat([X_test_full_encoded, encoded_sex_test_df], axis=1)

rf_reg = RandomForestRegressor(n_estimators=200, max_depth=10, min_samples_split=10)
rf_reg.fit(X_train_full_encoded, y_train_full)

explainer = RegressionExplainer(rf_reg, X_test_full_encoded, y_test_full)
db = ExplainerDashboard(explainer)
db.to_yaml("dashboard.yaml", explainerfile="explainer.joblib", dump_explainer=True)
