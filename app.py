import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Cancer EDA", layout="wide")

# --- Sidebar menu ---
page = st.sidebar.selectbox("Navigasi Halaman", ["🏠 Beranda", "🧬 EDA Pasien", "📄 Tentang Saya", "📬 Kontak"])

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("data/cancer_patients.csv")

df = load_data()

# ============================
# 🏠 HALAMAN BERANDA
# ============================
if page == "🏠 Beranda":
    st.title("🏠 Selamat Datang di Dashboard Analisis Pasien Kanker")
    st.markdown("""
    Aplikasi ini menyajikan **analisis interaktif** terhadap data 50.000 pasien kanker dari berbagai negara.

    Silakan pilih halaman di sidebar untuk melihat:
    - **EDA Pasien** (analisis data)
    - **Tentang Saya**
    - **Kontak**
    """)

# ============================
# 🧬 HALAMAN EDA
# ============================
elif page == "🧬 EDA Pasien":
    st.header("🧬 Exploratory Data Analysis - Pasien Kanker")

    # Filter
    st.sidebar.header("🔍 Filter Data")
    selected_country = st.sidebar.multiselect("Pilih Negara", df['Country_Region'].unique(), default=df['Country_Region'].unique())
    selected_gender = st.sidebar.multiselect("Pilih Gender", df['Gender'].unique(), default=df['Gender'].unique())
    selected_type = st.sidebar.multiselect("Pilih Jenis Kanker", df['Cancer_Type'].unique(), default=df['Cancer_Type'].unique())
    selected_age = st.sidebar.slider("Batasan Usia", int(df['Age'].min()), int(df['Age'].max()), (20, 80))

    filtered_df = df[
        (df['Country_Region'].isin(selected_country)) &
        (df['Gender'].isin(selected_gender)) &
        (df['Cancer_Type'].isin(selected_type)) &
        (df['Age'].between(selected_age[0], selected_age[1]))
    ]

    # Metrics
    st.subheader("📊 Ringkasan Data")
    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Pasien", f"{filtered_df.shape[0]}")
    col2.metric("Rata-rata Usia", f"{filtered_df['Age'].mean():.0f} thn")
    col3.metric("Rata-rata Biaya (USD)", f"${filtered_df['Treatment_Cost_USD'].mean():,.2f}")

    with st.expander("📁 Lihat Dataframe"):
        st.dataframe(filtered_df.head(20), use_container_width=True)

    if st.toggle("Tampilkan Grafik Jumlah Pasien per Tahun"):
        year_counts = filtered_df['Year'].value_counts().sort_index()
        fig = px.line(x=year_counts.index, y=year_counts.values, labels={'x': 'Tahun', 'y': 'Jumlah Pasien'}, title='Jumlah Pasien per Tahun')
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🧬 Distribusi Jenis Kanker")
    fig_bar = px.histogram(filtered_df, x="Cancer_Type", color="Gender", barmode="group")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("🔗 Korelasi Antar Faktor Risiko")
    corr_cols = ['Genetic_Risk', 'Air_Pollution', 'Alcohol_Use', 'Smoking', 'Obesity_Level', 'Survival_Years', 'Treatment_Cost_USD', 'Target_Severity_Score']
    fig_corr, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(filtered_df[corr_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig_corr)

    with st.expander("📌 Insight Menarik"):
        st.markdown(f"- Usia tertinggi pasien: **{filtered_df['Age'].max()} tahun**")
        st.markdown(f"- Negara dengan pasien terbanyak: **{filtered_df['Country_Region'].value_counts().idxmax()}**")
        st.markdown(f"- Jenis kanker paling umum: **{filtered_df['Cancer_Type'].value_counts().idxmax()}**")

# ============================
# 📄 HALAMAN TENTANG SAYA
# ============================
elif page == "📄 Tentang Saya":
    st.title("📄 Tentang Saya")
    st.markdown("""
    Halo! Saya **Syifa**, seorang data enthusiast yang tertarik dalam analisis data kesehatan.  
    Fokus utama saya adalah eksplorasi data, visualisasi, dan storytelling menggunakan Python.

    - 💼 Pernah magang di DJPb & KPPN Banda Aceh
    - 🧠 Familiar: Python, SQL, Power BI, Tableau
    - 🔍 Topik favorit: EDA, Customer Analysis, Segmentasi
    """)

# ============================
# 📬 HALAMAN KONTAK
# ============================
elif page == "📬 Kontak":
    st.title("📬 Kontak")
    st.markdown("""
    Terima kasih sudah mengunjungi dashboard saya!

    📧 Email: syifamujiburrahman@gmail.com  
    🔗 LinkedIn: [linkedin.com/in/syifa](https://www.linkedin.com/in/syifa01)  
    💻 GitHub: [github.com/syifa](https://github.com/syifa2202)
    """)
