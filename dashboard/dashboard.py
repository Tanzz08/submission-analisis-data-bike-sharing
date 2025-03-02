import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_data
def load_data():
    day_df = pd.read_csv("day_df.csv")  
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    day_df['year'] = day_df['dteday'].dt.year
    day_df['month'] = day_df['dteday'].dt.strftime('%b')
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    day_df['month'] = pd.Categorical(day_df['month'], categories=month_order, ordered=True)
    return day_df

day_df = load_data()

st.sidebar.header("Dashboard Bike Rentals")
selected_years = st.sidebar.multiselect("Pilih Tahun", options=day_df['year'].unique(), default=day_df['year'].unique())

filtered_df = day_df[day_df['year'].isin(selected_years)]


st.subheader("Tren Peminjaman Sepeda per Bulan berdasarkan tahunnya")
monthly_trend = filtered_df.groupby(['year', 'month']).agg({'cnt': 'sum'}).reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=monthly_trend, x='month', y='cnt', hue='year', marker='o', palette="tab10", ax=ax)
ax.set_title("Monthly Bike Rentals Trends per Year", fontsize=14)
ax.set_xlabel("Month")
ax.set_ylabel("Total Rentals")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.legend(title="Year")
ax.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig)

st.write("Grafik menunjukkan adanya peningkatan jumlah peminjaman sepeda pada tahun 2012 dibandingkan tahun 2011, terutama pada bulan-bulan musim panas seperti Juni hingga September.")

st.subheader("Perbandingan Peminjaman Sepeda pada Hari Kerja dan Hari Libur")
workingday_cnt = filtered_df.groupby('workingday')['cnt'].sum()
holiday_cnt = filtered_df.groupby('holiday')['cnt'].sum()
comparison_df = pd.DataFrame({
    'Type': ['Non-Working Day', 'Working Day', 'Holiday', 'Non-Holiday'],
    'Total Rentals': [workingday_cnt[0], workingday_cnt[1], holiday_cnt[1], holiday_cnt[0]]
})
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=comparison_df, x="Type", y="Total Rentals", palette=["#a6c8ff", "#003f8a", "#cce0ff", "#002b5e"], ax=ax)
ax.set_title("Comparison of Bike Rentals: Working Days vs Holidays", fontsize=14)
ax.set_ylabel("Total Rentals")
ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
st.pyplot(fig)

st.write("Dari grafik, terlihat bahwa peminjaman sepeda pada hari kerja lebih tinggi dibandingkan hari libur. Ini menunjukkan bahwa mayoritas pengguna memanfaatkan sepeda untuk keperluan sehari-hari seperti pergi ke kantor atau sekolah.")
