import pandas as pd 
# import mysql.connector
from sqlalchemy import create_engine



df = pd.read_csv(r'C:\Users\ASUS\Data_analysis_Project\customer_shopping_behavior.csv')
# cheching for any null values in our dataset 
# print(df.isnull().sum())

# we have to change the null values into 0 for the better data analysis
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x:x.fillna(x.median()))

# now we have to change the Columns name into camel case 

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ", '_')

#here we are renaming the  purchase_amount_(usd)
df = df.rename(columns={"purchase_amount_(usd)": "purchase_amount"})
# creating column age-group to understand the customer behaviour
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age-group'] = pd.qcut(df['age'], q=4, labels=labels)

# create a column purchase_frequency_days

frequency_mapping = {
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Month':90
}
df['purchase_frequency_days']= df['frequency_of_purchases'].map(frequency_mapping)
# checking if this two colums have the same value
# print(df['discount_applied'] == df['promo_code_used'].all().sum())

df = df.drop('promo_code_used',axis=1)

# Create a connection
engine = create_engine("mysql+pymysql://root:123456@localhost/amazon_data")

# insert the data into mysql
df.to_sql('sales_table',con=engine,if_exists='replace',index=False)
print("✅ Data loaded successfully into MySQL!")


# Read SQL table into pandas DataFrame

df = pd.read_sql("SELECT * FROM sales_table", con=engine)

# print(df.head())

# print(df.columns)