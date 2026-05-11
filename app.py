import streamlit as st
import google.generativeai as genai
import requests

# Setup API
genai.configure(api_key="API_KEY_LO_DISINI")
model = genai.GenerativeModel("gemini-2.5-flash")

# Page config
st.set_page_config(
    page_title="TaniPintar",
    page_icon="🌾",
    layout="wide"
)

# CSS Premium Hijau Gelap + Gold
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
    
    * { font-family: 'Poppins', sans-serif !important; }
    
    .stApp {
        background: #0a1f0a !important;
    }
    
    section[data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #0d2b0d 0%, #1a4a1a 50%, #0d2b0d 100%);
        border: 1px solid #c9a84c;
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(201,168,76,0.08) 0%, transparent 60%);
    }
    .hero-badge {
        background: linear-gradient(135deg, #c9a84c, #f0d080);
        color: #0a1f0a;
        padding: 0.3rem 1.2rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .hero h1 {
        color: #f0d080 !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        text-shadow: 0 0 40px rgba(201,168,76,0.3);
        letter-spacing: -1px;
    }
    .hero p {
        color: #a8c5a8 !important;
        font-size: 1.1rem !important;
        margin: 0.5rem 0 0 0 !important;
    }

    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, #0d2b0d, #152e15);
        border: 1px solid rgba(201,168,76,0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s;
    }
    .feature-card:hover {
        border-color: #c9a84c;
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(201,168,76,0.15);
    }
    .feature-card h3 {
        color: #f0d080 !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        margin: 0.5rem 0 0.3rem 0 !important;
    }
    .feature-card p {
        color: #7a9e7a !important;
        font-size: 0.85rem !important;
        margin: 0 !important;
    }

    /* Section Title */
    .section-title {
        color: #f0d080 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin: 2rem 0 1rem 0 !important;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(201,168,76,0.3);
    }

    /* Form Container */
    .form-container {
        background: linear-gradient(135deg, #0d2b0d, #152e15);
        border: 1px solid rgba(201,168,76,0.2);
        border-radius: 20px;
        padding: 2rem;
    }

    /* Input Labels */
    .stSelectbox label, .stTextInput label, 
    .stTextArea label, .stNumberInput label,
    .stMultiSelect label {
        color: #c9a84c !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }

    /* Input Fields */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: #0a1f0a !important;
        border: 1px solid rgba(201,168,76,0.3) !important;
        color: #e8f5e8 !important;
        border-radius: 10px !important;
    }
    .stSelectbox > div > div:focus,
    .stTextInput > div > div > input:focus {
        border-color: #c9a84c !important;
        box-shadow: 0 0 0 2px rgba(201,168,76,0.2) !important;
    }

    /* Submit Button */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #c9a84c, #f0d080) !important;
        color: #0a1f0a !important;
        border: none !important;
        padding: 0.8rem 3rem !important;
        border-radius: 50px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(201,168,76,0.3) !important;
        transition: all 0.3s !important;
        letter-spacing: 0.5px !important;
    }
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(201,168,76,0.5) !important;
    }

    /* Weather Card */
    .weather-card {
        background: linear-gradient(135deg, #0d2b4a, #1a3d6b);
        border: 1px solid rgba(100,160,255,0.3);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        color: #a8d4ff;
        margin: 1.5rem 0;
        font-size: 0.95rem;
    }
    .weather-card b { color: #7ab8ff; }

    /* Result Card */
    .result-card {
        background: linear-gradient(135deg, #0d2b0d, #152e15);
        border: 1px solid rgba(201,168,76,0.4);
        border-radius: 20px;
        padding: 2rem;
        color: #c8e6c8;
        margin: 1.5rem 0;
        line-height: 1.8;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .result-card h1, .result-card h2, 
    .result-card h3, .result-card strong {
        color: #f0d080 !important;
    }

    /* Success/Warning */
    .stSuccess {
        background: rgba(201,168,76,0.1) !important;
        border: 1px solid rgba(201,168,76,0.3) !important;
        border-radius: 10px !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #4a7a4a;
        font-size: 0.8rem;
        border-top: 1px solid rgba(201,168,76,0.1);
        margin-top: 3rem;
    }
    .footer span { color: #c9a84c; }
</style>
""", unsafe_allow_html=True)

# Fungsi cuaca
def get_cuaca(kota):
    try:
        url = f"https://wttr.in/{kota}?format=j1"
        response = requests.get(url, timeout=5)
        data = response.json()
        cuaca = data['current_condition'][0]
        return {
            "suhu": cuaca['temp_C'],
            "kelembaban": cuaca['humidity'],
            "kondisi": cuaca['weatherDesc'][0]['value'],
            "angin": cuaca['windspeedKmph'],
            "curah_hujan": cuaca['precipMM']
        }
    except:
        return None

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI PERTANIAN INDONESIA ✦</div>
    <h1>🌾 TaniPintar</h1>
    <p>Asisten AI Pertanian Cerdas dengan Data Cuaca Realtime untuk Petani Indonesia</p>
</div>
""", unsafe_allow_html=True)

# Feature Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size:2rem">🌤️</div>
        <h3>Cuaca Realtime</h3>
        <p>Analisis berdasarkan cuaca terkini di lokasi Anda</p>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size:2rem">🤖</div>
        <h3>AI Canggih</h3>
        <p>Ditenagai Google Gemini AI terbaru</p>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size:2rem">⚡</div>
        <h3>Saran Langsung</h3>
        <p>Tindakan konkret yang bisa dilakukan hari ini</p>
    </div>""", unsafe_allow_html=True)

# Form
st.markdown('<p class="section-title">📝 Ceritakan Kondisi Tanaman Anda</p>', unsafe_allow_html=True)

with st.form("form_tani"):
    col1, col2 = st.columns(2)
    with col1:
        jenis_tanaman = st.selectbox("🌱 Jenis Tanaman", [
            "Padi", "Jagung", "Cabai", "Tomat", "Singkong",
            "Kedelai", "Bawang", "Sayuran lainnya"
        ])
        umur_tanaman = st.number_input("📅 Umur Tanaman (hari)", min_value=1, max_value=365, value=30)
        luas_lahan = st.selectbox("📐 Luas Lahan", [
            "Kurang dari 0.5 hektar", "0.5 - 1 hektar",
            "1 - 2 hektar", "Lebih dari 2 hektar"
        ])
    with col2:
        lokasi = st.text_input("📍 Kota/Kabupaten", placeholder="Contoh: Bogor")
        jenis_tanah = st.selectbox("🪨 Kondisi Tanah", [
            "Normal/subur", "Kering/tandus",
            "Terlalu basah/becek", "Berlumpur", "Berbatu"
        ])
        pupuk_terakhir = st.selectbox("🌿 Pemupukan Terakhir", [
            "Belum pernah", "Kurang dari 1 minggu",
            "1-2 minggu lalu", "Lebih dari 1 bulan lalu"
        ])

    kondisi = st.text_area(
        "💬 Ceritakan kondisi tanaman Anda:",
        placeholder="Contoh: Daun padi saya menguning sejak 3 hari lalu, ada bercak coklat...",
        height=120
    )
    masalah = st.multiselect("⚠️ Masalah yang dialami:", [
        "Daun menguning/layu", "Hama/serangga",
        "Cuaca tidak menentu", "Tanah terlalu kering",
        "Tanah terlalu basah/banjir", "Pertumbuhan lambat",
        "Penyakit tanaman", "Tidak ada masalah, minta saran rutin"
    ])
    submit = st.form_submit_button("🔍 Analisis Tanaman Saya Sekarang")

# Proses
if submit:
    if kondisi and lokasi:
        with st.spinner("🌤️ Mengambil data cuaca realtime..."):
            cuaca = get_cuaca(lokasi)

        if cuaca:
            st.markdown(f"""
            <div class="weather-card">
                🌤️ <b>Cuaca {lokasi} Sekarang:</b>
                {cuaca['kondisi']} &nbsp;|&nbsp; 🌡️ {cuaca['suhu']}°C &nbsp;|&nbsp;
                💧 Kelembaban {cuaca['kelembaban']}% &nbsp;|&nbsp;
                🌬️ Angin {cuaca['angin']} km/h &nbsp;|&nbsp;
                🌧️ Hujan {cuaca['curah_hujan']}mm
            </div>
            """, unsafe_allow_html=True)

        with st.spinner("🤖 AI sedang menganalisis..."):
            masalah_text = ", ".join(masalah) if masalah else "tidak disebutkan"
            cuaca_text = f"Suhu {cuaca['suhu']}°C, kelembaban {cuaca['kelembaban']}%, kondisi {cuaca['kondisi']}, curah hujan {cuaca['curah_hujan']}mm" if cuaca else "tidak tersedia"

            prompt = f"""
            Kamu adalah ahli pertanian Indonesia senior dengan pengalaman 20 tahun,
            berbicara dengan bahasa yang mudah dipahami petani desa Indonesia.

            DATA TANAMAN:
            - Jenis tanaman: {jenis_tanaman}
            - Umur tanaman: {umur_tanaman} hari
            - Lokasi: {lokasi}
            - Luas lahan: {luas_lahan}
            - Kondisi tanah: {jenis_tanah}
            - Pemupukan terakhir: {pupuk_terakhir}
            - Masalah: {masalah_text}
            - Cerita petani: {kondisi}

            DATA CUACA REALTIME {lokasi.upper()}: {cuaca_text}

            Berikan analisis SPESIFIK dalam format:

            🔍 DIAGNOSIS
            (penyebab spesifik berdasarkan umur tanaman, cuaca hari ini, kondisi tanah)

            ⚡ TINDAKAN HARI INI
            (apa yang HARUS dilakukan petani hari ini, spesifik dan detail)

            📅 RENCANA 2 MINGGU KE DEPAN
            (langkah konkret harian/mingguan)

            ⚠️ WASPADAI
            (risiko spesifik berdasarkan cuaca dan kondisi sekarang)

            💊 REKOMENDASI OBAT/PUPUK
            (nama produk spesifik yang mudah dicari di toko pertanian lokal)

            💡 TIPS PRO
            (tips dari pengalaman 20 tahun yang tidak semua orang tahu)

            Jawaban harus SPESIFIK. Jangan terlalu umum.
            """

            response = model.generate_content(prompt)

            st.markdown(f"""
            <div class="result-card">
                {response.text}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:rgba(201,168,76,0.1); border:1px solid rgba(201,168,76,0.3); 
            border-radius:12px; padding:1rem 1.5rem; margin-top:1rem; color:#c9a84c;">
                💬 <b>Ada pertanyaan lanjutan?</b> Isi form di atas lagi dengan detail lebih lengkap!
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Mohon isi lokasi dan kondisi tanaman Anda!")

# Footer
st.markdown("""
<div class="footer">
    🌾 <span>TaniPintar</span> — Teknologi AI untuk Petani Indonesia 🇮🇩<br>
    Dibuat dengan ❤️ untuk membantu petani Indonesia sejahtera
</div>
""", unsafe_allow_html=True)