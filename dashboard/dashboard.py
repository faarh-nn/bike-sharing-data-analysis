import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='dark')

def get_total_count_by_hour_df(hour_df):
  hour_count_df =  hour_df.groupby(by="hr").agg({"cnt": ["sum"]})
  return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (hour_df):
    sum_order_items_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season (day_df): 
    season_df = day_df.groupby(by="season").cnt.sum().reset_index() 
    return season_df

days_df = pd.read_csv("day_df_final.csv")
hours_df = pd.read_csv("hour_df_final.csv")

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with st.sidebar:
    st.image("logo.png", width=150)

    # Mengambil start_date & end_date dari date_input
    date_input = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

# Menangani error jika hanya satu tanggal yang dipilih
if isinstance(date_input, tuple) and len(date_input) == 2:
    start_date, end_date = date_input
else:
    start_date, end_date = min_date_days, max_date_days
  
main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & 
                       (days_df["dteday"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & 
                        (hours_df["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)

# memulai konvigurasi visualisasi data
st.header('🚲📊 Bike Sharing Analytics Dashboard')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.cnt.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Pola Penggunaan Sepeda Berdasarkan Hari Kerja dan Akhir Pekan")

# Menggunakan data yang sudah difilter berdasarkan rentang tanggal yang diinput
weekday_avg = main_df_days.groupby('weekday')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(data=weekday_avg, x='weekday', y='cnt', marker='o', color='blue', ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu')
ax.grid()
st.pyplot(fig)  # Menampilkan visualisasi di Streamlit

st.subheader("Pengaruh Cuaca dan Musim Terhadap Penyewaan Sepeda")

# Membuat tab untuk tiga visualisasi
tab1, tab2, tab3 = st.tabs(["Penyewaan Sepeda Berdasarkan Musim", "Penyewaan Sepeda Berdasarkan Kondisi Cuaca", "Hubungan Suhu & Penyewaan Sepeda"])

# Tab 1: Rata-rata penyewaan sepeda berdasarkan musim
with tab1:
    fig, ax = plt.subplots(figsize=(8, 5))
    sorted_season = main_df_days.groupby('season')['cnt'].mean().sort_values(ascending=False).index
    sns.barplot(ax=ax, x='season', y='cnt', data=main_df_days, estimator='mean', errorbar=None, order=sorted_season)
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Musim')
    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig)

# Tab 2: Rata-rata penyewaan sepeda berdasarkan kondisi cuaca
with tab2:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(ax=ax, x='weathersit', y='cnt', data=main_df_days, estimator='mean', errorbar=None)
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig)

# Tab 3: Scatter plot hubungan suhu dengan jumlah penyewaan sepeda
with tab3:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(ax=ax, x='temp', y='cnt', data=main_df_days, alpha=0.5, color='green')
    ax.set_title('Hubungan Suhu (Celcius) dengan Jumlah Penyewaan Sepeda')
    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig)  

st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Jam")

# Gunakan main_df_hour untuk data yang sudah difilter
hourly_avg = main_df_hour.groupby('hr')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=hourly_avg, x='hr', y='cnt', marker='o', color='purple', ax=ax)
ax.set_xticks(range(24))
ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Jam')
ax.set_xlabel("")
ax.set_ylabel("")
st.pyplot(fig)

st.subheader("Analisis RFM - Rental Sepeda 🚴‍♂️ (Berdasarkan Rentang Waktu yang Dipilih)")

# Filter data berdasarkan input user
filtered_df = days_df[(days_df["dteday"] >= str(start_date)) & 
                      (days_df["dteday"] <= str(end_date))]

# Hitung Recency
recency = (max_date_days - filtered_df["dteday"].max()).days

# Hitung Frequency
frequency = filtered_df["dteday"].nunique()

# Hitung Monetary
monetary = filtered_df["cnt"].sum()

# Menampilkan hasilnya di Streamlit
st.write(f"**Recency:** {recency} hari sejak transaksi terakhir")
st.write(f"**Frequency:** {frequency} hari dengan transaksi")
st.write(f"**Monetary:** {monetary:,} total penyewaan")