import pandas as pd


# load a subset of the dataset
df = pd.read_csv("metadata.csv", nrows=100)

# Data preview
print(df.head(2), '\n')

# Exploring the Data
# Check dimensions (rows, columns) because we only loaded the first 100 rows, I expect that rows=100
print("Shape:", df.shape, "\n")

# Data types of each column
print("Data types:\n", df.dtypes, "\n")

# Missing values per column
print("Missing values:\n", df.isnull().sum(), "\n")

# Basic statistics for numerical columns
print("Statistical summary:\n", df.describe(), "\n")
