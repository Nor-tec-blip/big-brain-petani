
import streamlit as st
import google.generativeai as genai
import requests

# Setup API
genai.configure(api_key="AIzaSyBGXWHL606XMInt28YNPe0PHVMW38FCSCY")
model = genai.GenerativeModel("gemini-2.5-flash")

# Custom CSS
st.markdown("""
<style>
    /* Background utama */
    .stApp {
        background: linear-gradient(135deg, #f0fff4 0%, #e8f5e9 50%, #f1f8e9 100%);
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #2e7d32, #66bb6a);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(46,125,50,0.3);
    }
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .main-header p {
        color: #c8e6c9;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Card cuaca */
    .weather-card {
        background: linear-gradient(135deg, #0288d1, #4fc3f7);
        padding: 1rem 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(2,136,209,0.3);
        font-size: 1rem;
    }
    
    /* Card hasil analisis */
    .result-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        border-left: 6px solid #43a047;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
    
    /* Form styling */
    .stSelectbox label, .stTextInput label, .stTextArea label, .stNumberInput label {
        font-weight: 600 !important;
        color: #2e7d32 !important;
        font-size: 0.95rem !important;
    }
    
    /* Tombol */
    .stFormSubmitButton button {
        background: linear-gradient(135deg, #43a047, #66bb6a) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 3rem !important;
        border-radius: 50px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(67,160,71,0.4) !important;
        transition: all 0.3s !important;
    }
    .stFormSubmitButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(67,160,71,0.5) !important;
    }

    /* Tips box */
    .tips-box {
        background: linear-gradient(135deg, #fff8e1, #fff3cd);
        border: 2px solid #ffc107;
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.85rem;
    }

    /* Sembunyiin header bawaan streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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

# Header
st.markdown("""
<div class="main-header">
    <h1>🌾 TaniPintar</h1>
    <p>Asisten AI Pertanian Cerdas untuk Petani Indonesia 🇮🇩</p>
</div>
""", unsafe_allow_html=True)

# Info singkat
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 🌤️ Cuaca Realtime\nAnalisis berdasarkan cuaca terkini di lokasi Anda")
with col2:
    st.markdown("### 🤖 AI Canggih\nDitenagai teknologi AI terbaru dari Google")
with col3:
    st.markdown("### ⚡ Saran Langsung\nTindakan konkret yang bisa dilakukan hari ini")

st.markdown("---")
st.markdown("### 📝 Ceritakan Kondisi Tanaman Anda")

# Form
with st.form("form_tani"):
    col1, col2 = st.columns(2)

    with col1:
        jenis_tanaman = st.selectbox("🌱 Jenis Tanaman", [
            "Padi", "Jagung", "Cabai", "Tomat", "Singkong",
            "Kedelai", "Bawang", "Sayuran lainnya"
        ])
        umur_tanaman = st.number_input("📅 Umur Tanaman (hari)", min_value=1, max_value=365, value=30)
        luas_lahan = st.selectbox("📐 Luas Lahan", [
            "Kurang dari 0.5 hektar",
            "0.5 - 1 hektar",
            "1 - 2 hektar",
            "Lebih dari 2 hektar"
        ])

    with col2:
        lokasi = st.text_input("📍 Kota/Kabupaten", placeholder="Contoh: Bogor")
        jenis_tanah = st.selectbox("🪨 Kondisi Tanah", [
            "Normal/subur",
            "Kering/tandus",
            "Terlalu basah/becek",
            "Berlumpur",
            "Berbatu"
        ])
        pupuk_terakhir = st.selectbox("🌿 Pemupukan Terakhir", [
            "Belum pernah",
            "Kurang dari 1 minggu",
            "1-2 minggu lalu",
            "Lebih dari 1 bulan lalu"
        ])

    kondisi = st.text_area(
        "💬 Ceritakan kondisi tanaman Anda:",
        placeholder="Contoh: Daun padi saya menguning sejak 3 hari lalu, ada bercak coklat di beberapa helai daun...",
        height=120
    )

    masalah = st.multiselect("⚠️ Masalah yang dialami:", [
        "Daun menguning/layu",
        "Hama/serangga",
        "Cuaca tidak menentu",
        "Tanah terlalu kering",
        "Tanah terlalu basah/banjir",
        "Pertumbuhan lambat",
        "Penyakit tanaman",
        "Tidak ada masalah, minta saran rutin"
    ])

    submit = st.form_submit_button("🔍 Analisis Tanaman Saya Sekarang!")

# Proses
if submit:
    if kondisi and lokasi:
        with st.spinner("🌤️ Mengambil data cuaca realtime..."):
            cuaca = get_cuaca(lokasi)

        if cuaca:
            st.markdown(f"""
            <div class="weather-card">
                🌤️ <b>Cuaca {lokasi} Sekarang:</b> 
                {cuaca['kondisi']} | 🌡️ {cuaca['suhu']}°C | 
                💧 Kelembaban {cuaca['kelembaban']}% | 
                🌬️ Angin {cuaca['angin']} km/h | 
                🌧️ Hujan {cuaca['curah_hujan']}mm
            </div>
            """, unsafe_allow_html=True)

        with st.spinner("🤖 AI sedang menganalisis kondisi tanaman Anda..."):
            masalah_text = ", ".join(masalah) if masalah else "tidak disebutkan"
            cuaca_text = f"Suhu {cuaca['suhu']}°C, kelembaban {cuaca['kelembaban']}%, kondisi {cuaca['kondisi']}, curah hujan {cuaca['curah_hujan']}mm" if cuaca else "data cuaca tidak tersedia"

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

            DATA CUACA REALTIME {lokasi.upper()}:
            {cuaca_text}

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
            <div class="tips-box">
                💬 <b>Ada pertanyaan lanjutan?</b> Isi form di atas lagi dengan detail lebih lengkap!
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Mohon isi lokasi dan kondisi tanaman Anda!")

# Footer
st.markdown("""
<div class="footer">
    🌾 TaniPintar — Teknologi AI untuk Petani Indonesia 🇮🇩<br>
    Dibuat dengan ❤️ untuk membantu petani Indonesia
</div>
""", unsafe_allow_html=True)