import pandas as pd
import math
df=pd.read_excel("Employee_Survey_Results.xlsx")
df.loc[:, 'Clicked Suspicious Link (Yes/No)'] = df['Clicked Suspicious Link (Yes/No)'].apply(lambda x: 1 if x == 'Yes' else 0)

df['Clicked Suspicious Link (Yes/No)']=df['Clicked Suspicious Link (Yes/No)'].astype(int)

train_fish=df['Training Hours (0-10)'].corr(df['Phishing Confidence (1-5)'])
train_passwd=df['Training Hours (0-10)'].corr(df['Strong Passwords (1-5)'])
print(train_fish)
print(train_passwd)

train_click=df['Training Hours (0-10)'].corr(df['Clicked Suspicious Link (Yes/No)'])
print(train_click)
