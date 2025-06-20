# -*- coding: utf-8 -*-
"""TASK 2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sjsPZGecX_57XvcCC6FHaD2A_10O-Q99
"""

from google.colab import files
uploaded = files.upload()
import pandas as pd

df = pd.read_csv('data.csv', encoding='ISO-8859-1')  # Make sure the file name matches exactly
df.head()
# Check for null values
print(df.isnull().sum())

# Drop rows with missing values
df.dropna(inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
import datetime

# Convert InvoiceDate to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Set snapshot date (max date in dataset)
snapshot_date = df['InvoiceDate'].max() + datetime.timedelta(days=1)

# Create RFM table
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',  # Frequency
    'TotalAmount': 'sum'  # Monetary
})

rfm.rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalAmount': 'Monetary'
}, inplace=True)

rfm.head()
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

inertia = []

for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(rfm_scaled)
    inertia.append(kmeans.inertia_)

plt.plot(range(1, 11), inertia, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()
kmeans = KMeans(n_clusters=4, random_state=0)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
rfm.head()
import seaborn as sns

# Recency vs Monetary
sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Cluster', palette='Set1')
plt.title("Customer Segmentation")
plt.show()
rfm.groupby('Cluster').mean()