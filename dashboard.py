import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv('df_day_analisis.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['year'].replace({0: 2011, 1: 2012})

# Sidebar - filters
st.sidebar.header("Filter Data")
year_selected = st.sidebar.multiselect("Pilih Tahun", df['year'].unique(), default=df['year'].unique())
month_selected = st.sidebar.multiselect("Pilih Bulan", df['month'].unique(), default=df['month'].unique())
workday_filter = st.sidebar.radio("Pilih Hari Kerja atau Libur", ['Semua', 'Hari Kerja', 'Hari Libur'])

# Filter data
df_filtered = df[(df['year'].isin(year_selected)) & (df['month'].isin(month_selected))]

# Filter for working day or weekend
if workday_filter == 'Hari Kerja':
    df_filtered = df_filtered[df_filtered['workingday'] == 1]
elif workday_filter == 'Hari Libur':
    df_filtered = df_filtered[df_filtered['workingday'] == 0]

# Dashboard title
st.title("Dashboard Analisis Penyewaan Sepeda")

# Total usage by day (line plot)
st.subheader("Total Penggunaan Sepeda per Hari")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='date', y='total', data=df_filtered, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Usage by weather condition (bar plot)
st.subheader("Penggunaan Sepeda Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='weather_situation', y='total', data=df_filtered, estimator='mean', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Working day vs weekend (box plot)
st.subheader("Penggunaan Sepeda Hari Kerja vs Akhir Pekan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x='workingday', y='total', data=df_filtered)
ax.set_xticklabels(['Akhir Pekan', 'Hari Kerja'])
st.pyplot(fig)

# Usage by season (bar plot)
st.subheader("Penggunaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='season', y='total', data=df_filtered, estimator='mean', ax=ax)
st.pyplot(fig)

# Monthly trend in bike usage (line plot)
st.subheader("Tren Penggunaan Sepeda Berdasarkan Bulan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='month', y='total', data=df_filtered, marker='o', ax=ax)
st.pyplot(fig)

# Usage statistics (descriptive statistics)
st.subheader("Statistik Penggunaan Sepeda")
st.write(df_filtered[['casual', 'registered', 'total']].describe())

# Pie chart: Casual vs Registered usage
st.subheader("Proporsi Penggunaan Kasual vs Terdaftar")
casual_vs_registered = df_filtered[['casual', 'registered']].sum()
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(casual_vs_registered, labels=['Kasual', 'Terdaftar'], autopct='%1.1f%%', colors=['lightblue', 'orange'], startangle=90)
ax.axis('equal')
st.pyplot(fig)

# Yearly trends (line plot)
st.subheader("Penggunaan Sepeda Berdasarkan Tahun")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='year', y='total', data=df_filtered, marker='o', ax=ax)
st.pyplot(fig)

# Additional insights and conclusions
st.subheader("Kesimpulan")
st.write("""
    - **Pengaruh Cuaca**: Penggunaan sepeda cenderung lebih tinggi pada cuaca cerah atau berawan sebagian.
    - **Musim**: Penggunaan sepeda meningkat selama musim panas dan menurun selama musim dingin.
    - **Hari Kerja vs Akhir Pekan**: Pengguna terdaftar lebih banyak menggunakan sepeda pada hari kerja, sedangkan pengguna kasual lebih banyak bersepeda di akhir pekan.
    - **Tren Bulanan**: Bulan-bulan musim panas seperti Juni hingga September menunjukkan penggunaan sepeda yang lebih tinggi.
""")
