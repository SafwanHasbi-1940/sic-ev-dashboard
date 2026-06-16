import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Dashboard EV Indonesia",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS (PREMIUM DARK THEME)
# =====================================================
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border: 1px solid #10b981;
    }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 1.1rem !important; }
    [data-testid="stMetricValue"] { color: #f8fafc !important; font-size: 2.2rem !important; font-weight: 700; }
    
    .stTabs [data-baseweb="tab-list"] { background-color: #1e293b; padding: 10px; border-radius: 12px; border-bottom: none; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: transparent; border-radius: 8px; color: #94a3b8; font-weight: 600; padding: 0 20px; border: none; }
    .stTabs [aria-selected="true"] { background-color: #10b981 !important; color: #0b0f19 !important; }
    
    h1, h2, h3 { color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    .gradient-text {
        background: linear-gradient(to right, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .sub-text { color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; line-height: 1.6; }
    .card-story {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #10b981;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA & ERROR HANDLING
# =====================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("ev_indonesia_data.csv")
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("Dataset 'ev_indonesia_data.csv' tidak ditemukan. Pastikan script generator sudah dijalankan.")
    st.stop()

# =====================================================
# HEADER (STORYTELLING CONTEXT)
# =====================================================
st.markdown('<div class="gradient-text">Transisi Energi: Adopsi Kendaraan Listrik (EV) di Indonesia</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Mengolah data kompleks menjadi visualisasi interaktif untuk memahami tantangan dan peluang transisi menuju industri energi bersih dan pencapaian <i>Net Zero Emission</i>.</div>', unsafe_allow_html=True)

# =====================================================
# FILTER EKSPLORASI (TAMPIL DI HALAMAN UTAMA)
# =====================================================
st.markdown("### ⚙️ Filter Eksplorasi")

# Clean filter lists
years = sorted([y for y in df["Tahun Registrasi"].unique()])
provinsis = sorted([p for p in df["Provinsi"].unique()])
tipes = sorted([t for t in df["Tipe Kendaraan"].unique()])

fcol1, fcol2, fcol3 = st.columns(3)

with fcol1:
    selected_years = st.slider(
        "Rentang Tahun Registrasi",
        min_value=min(years), max_value=max(years),
        value=(min(years), max(years))
    )

with fcol2:
    selected_prov = st.selectbox("Pilih Provinsi", ["Seluruh Indonesia"] + provinsis)

with fcol3:
    selected_tipe = st.selectbox("Tipe Kendaraan", ["Semua Tipe"] + tipes)

st.markdown("<br>", unsafe_allow_html=True)

# Filter Logic
df_filtered = df[
    (df["Tahun Registrasi"] >= selected_years[0]) & 
    (df["Tahun Registrasi"] <= selected_years[1])
]

if selected_prov != "Seluruh Indonesia":
    df_filtered = df_filtered[df_filtered["Provinsi"] == selected_prov]

if selected_tipe != "Semua Tipe":
    df_filtered = df_filtered[df_filtered["Tipe Kendaraan"] == selected_tipe]

if df_filtered.empty:
    st.warning("⚠️ Data tidak ditemukan untuk kombinasi filter ini.")
    st.stop()

# =====================================================
# KPIS
# =====================================================
total_ev = len(df_filtered)
total_brand = df_filtered["Brand"].nunique()
penerima_subsidi = len(df_filtered[df_filtered["Penerima Subsidi"] == "Ya"])
persen_subsidi = (penerima_subsidi / total_ev) * 100 if total_ev > 0 else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("⚡ Total Kendaraan", f"{total_ev:,}")
    with st.popover("🔍 Lihat Detail Data", use_container_width=True):
        st.caption("Tren Registrasi Tahunan:")
        st.bar_chart(df_filtered["Tahun Registrasi"].value_counts().sort_index(), color="#3b82f6")
        st.caption("Seluruh dataset berdasarkan filter saat ini:")
        df_view1 = df_filtered.copy()
        df_view1.index = range(1, len(df_view1) + 1)
        st.dataframe(df_view1, use_container_width=True)

with c2:
    st.metric("🚗 Merek (Brand)", f"{total_brand}")
    with st.popover("🔍 Lihat Daftar Merek", use_container_width=True):
        st.caption("Peringkat merek dari yang terbanyak:")
        brand_counts = df_filtered["Brand"].value_counts()
        st.bar_chart(brand_counts, color="#8b5cf6")
        df_b = brand_counts.reset_index().rename(columns={"count":"Jumlah"})
        df_b.index = range(1, len(df_b) + 1)
        st.dataframe(df_b, use_container_width=True)

with c3:
    st.metric("💰 Penerima Subsidi", f"{penerima_subsidi:,}")
    with st.popover("🔍 Lihat Data Subsidi", use_container_width=True):
        st.caption("Merek terbanyak penerima subsidi:")
        sub_df = df_filtered[df_filtered["Penerima Subsidi"] == "Ya"]
        st.bar_chart(sub_df["Brand"].value_counts(), color="#10b981")
        st.caption("Dataset khusus kendaraan yang menerima subsidi:")
        df_sub_view = sub_df.copy()
        df_sub_view.index = range(1, len(df_sub_view) + 1)
        st.dataframe(df_sub_view, use_container_width=True)

with c4:
    st.metric("📈 Rasio Subsidi", f"{persen_subsidi:.1f}%")
    with st.popover("🔍 Bandingkan Rasio", use_container_width=True):
        st.caption("Perbandingan jumlah penerima subsidi vs tidak:")
        sub_counts = df_filtered["Penerima Subsidi"].value_counts()
        st.bar_chart(sub_counts, color="#f59e0b")
        df_s = sub_counts.reset_index().rename(columns={"count":"Jumlah"})
        df_s.index = range(1, len(df_s) + 1)
        st.dataframe(df_s, use_container_width=True)

st.markdown("---")

# =====================================================
# TABS LAYOUT
# =====================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tren & Demografi", 
    "🚘 Analisis Pasar", 
    "💡 Tantangan & Solusi (Storytelling)", 
    "📋 Data Eksplorer"
])

chart_template = "plotly_dark"
chart_bg = "rgba(0,0,0,0)"

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Lonjakan Adopsi EV per Tahun")
        st.markdown("<p style='color:#94a3b8; font-size:0.9rem;'>Pertumbuhan eksponensial terlihat jelas sejak tahun 2022 pasca regulasi Perpres terkait ekosistem KBLBB.</p>", unsafe_allow_html=True)
        
        year_count = df_filtered["Tahun Registrasi"].value_counts().sort_index().reset_index()
        year_count.columns = ["Tahun", "Jumlah"]
        
        fig_year = px.line(
            year_count, x="Tahun", y="Jumlah", markers=True,
            template=chart_template, color_discrete_sequence=["#10b981"]
        )
        fig_year.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg)
        st.plotly_chart(fig_year, use_container_width=True)

    with col2:
        st.markdown("### 🗺️ Persebaran Populasi per Provinsi")
        st.markdown("<p style='color:#94a3b8; font-size:0.9rem;'>Infrastruktur pengisian daya yang belum merata membuat demografi EV sangat terpusat di Pulau Jawa.</p>", unsafe_allow_html=True)
        
        prov_count = df_filtered["Provinsi"].value_counts().reset_index()
        prov_count.columns = ["Provinsi", "Jumlah"]
        
        fig_prov = px.bar(
            prov_count, x="Jumlah", y="Provinsi", orientation="h", text_auto=True,
            template=chart_template, color_discrete_sequence=["#3b82f6"]
        )
        fig_prov.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor=chart_bg, paper_bgcolor=chart_bg)
        st.plotly_chart(fig_prov, use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 🏍️ Dominasi Tipe Kendaraan")
        tipe_count = df_filtered["Tipe Kendaraan"].value_counts().reset_index()
        tipe_count.columns = ["Tipe", "Jumlah"]
        fig_tipe = px.pie(tipe_count, names="Tipe", values="Jumlah", hole=0.4, template=chart_template, color_discrete_sequence=["#10b981", "#f59e0b", "#ef4444"])
        fig_tipe.update_layout(plot_bgcolor=chart_bg, paper_bgcolor=chart_bg)
        st.plotly_chart(fig_tipe, use_container_width=True)
        
    with col_b:
        st.markdown("### 🏆 Top Brand Penguasa Pasar")
        brand_count = df_filtered["Brand"].value_counts().head(10).reset_index()
        brand_count.columns = ["Brand", "Jumlah"]
        
        brand_colors = {
            "Wuling": "#ef4444", "Hyundai": "#1e3a8a", "BYD": "#3b82f6",
            "Vespa": "#14b8a6", "Gesits": "#f97316", "Alva": "#0f766e",
            "Polytron": "#be123c", "Selis": "#10b981", "Volta": "#eab308",
            "Yadea": "#8b5cf6", "Honda": "#dc2626", "Yamaha": "#1d4ed8"
        }
        
        fig_brand = px.bar(
            brand_count, x="Brand", y="Jumlah", text_auto=True, 
            template=chart_template, color="Brand", color_discrete_map=brand_colors
        )
        fig_brand.update_layout(showlegend=False, plot_bgcolor=chart_bg, paper_bgcolor=chart_bg)
        st.plotly_chart(fig_brand, use_container_width=True)

with tab3:
    st.markdown("## 🔍 Narasi Data: Menjawab Tantangan Transisi Energi")
    st.markdown("Bagian ini menyajikan interpretasi data deskriptif di atas menjadi sebuah cerita utuh serta merekomendasikan solusi kebijakan untuk Indonesia.")
    
    st.markdown("""
    <div class="card-story">
        <h4>1. Bukti Ketimpangan Geografis (Tantangan Infrastruktur)</h4>
        <p>Data menunjukkan bahwa lebih dari <b>70% populasi kendaraan listrik</b> terkonsentrasi di Provinsi DKI Jakarta dan Jawa Barat. Hal ini mengonfirmasi tantangan terbesar transisi energi nasional: <b>Ketimpangan infrastruktur SPKLU (Stasiun Pengisian Kendaraan Listrik Umum)</b> yang masih bias Pulau Jawa. Tanpa infrastruktur yang merata, daerah lain akan kesulitan melakukan transisi.</p>
    </div>
    
    <div class="card-story">
        <h4>2. Motor Listrik (R2) sebagai Katalis Utama Transisi</h4>
        <p>Berdasarkan porsi pasar, Motor Listrik (R2) mendominasi lebih dari 65% sampel. Mengingat demografi sosial ekonomi Indonesia, insentif sebesar Rp7 Juta untuk motor listrik terbukti jauh lebih efektif dalam mendongkrak adopsi massal dibandingkan subsidi untuk mobil listrik yang secara harga masih belum terjangkau bagi kelompok menengah ke bawah.</p>
    </div>
    
    <div class="card-story">
        <h4>3. Solusi & Rekomendasi Aplikatif (Actionable Solutions)</h4>
        <ul>
            <li><b>Ekspansi Infrastruktur Terarah:</b> Pemerintah dan PLN perlu memprioritaskan pembangunan SPKLU/SPBKLU di luar Jawa-Bali berbasis koridor logistik untuk mendorong sektor komersial ikut bertransisi.</li>
            <li><b>Insentif Khusus Transportasi Publik/Komersil:</b> Penggunaan Bus EV dan kendaraan logistik listrik (R4 komersial) masih di bawah 2%. Pemerintah dapat memberlakukan skema subsidi atau keringanan pajak khusus bagi perusahaan (fleet) untuk mendongkrak <i>Green Jobs</i>.</li>
            <li><b>Penguatan Rantai Pasok Baterai Domestik:</b> Ketergantungan pada brand luar dapat dikurangi jika industri hulu nikel dan perakitan baterai di Indonesia dimaksimalkan untuk menekan komponen harga (Base MSRP).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown("### 📋 Sumber Data & Dataset Sintetis")
    st.markdown("Dataset di bawah ini merupakan data *dummy/synthetic* yang di-generate menyerupai distribusi statistik adopsi EV sesungguhnya di Indonesia, dibuat khusus untuk kebutuhan purwarupa (prototype) kompetisi SATRIA DATA.")
    
    df_explorer = df_filtered.copy()
    df_explorer.index = range(1, len(df_explorer) + 1)
    st.dataframe(df_explorer, use_container_width=True)
    
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Dataset (CSV)",
        data=csv,
        file_name="indonesia_ev_data_filtered.csv",
        mime="text/csv"
    )

st.markdown("---")