import streamlit as st
import joblib
import pandas as pd
import numpy as np
from preprocess_pipeline import SingleInstancePreprocessor
from get_real_home_listing import get_home_listings
from home_listing_display import display_home_listings

model = joblib.load('random_forest.joblib')
preprocessor = SingleInstancePreprocessor()


temp = {}
st.set_page_config(
    page_title="🏠 Ev Fiyatı Tahmin ve Öneri aracı",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    :root {
        --primary: #2A3950;
        --secondary: #00C0A3;
        --background: #1A1A1A;
        --surface: #2D2D2D;
        --text-primary: #FFFFFF;
    }
    
    body {
        font-family: 'Arial', sans-serif;
        background-color: var(--background);
        color: var(--text-primary);
    }

    .stApp {
        background: var(--background);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    
    .header-container {
        background: var(--surface);
        padding: 3rem;
        border-radius: 15px;
        margin-bottom: 2.5rem;
        box-shadow: 0 6px 25px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .input-card {
        background: var(--surface);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.2rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }

    .input-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }
    
    .stSelectbox, .stNumberInput, .stTextInput {
        background: var(--primary) !important;
        border-radius: 10px !important;
        border: none !important;
        color: var(--text-primary) !important;
        padding: 0.75rem !important;
    }
    
    .stButton>button {
        background: var(--secondary) !important;
        color: var(--text-primary) !important;
        border: none;
        padding: 16px 36px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(0,192,163,0.4);
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,192,163,0.5);
    }
    
    .prediction-card {
        background: linear-gradient(135deg, var(--primary) 0%, #1B2838 100%);
        border-radius: 15px;
        padding: 2.5rem;
        text-align: center;
        margin: 2.5rem 0;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--secondary);
        margin: 1.8rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255,255,255,0.7);
        font-size: 0.95rem;
        margin-top: 3.5rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }

    /* Ek olarak, mobil uyumluluk için medya sorguları ekleyebilirsiniz */
    @media (max-width: 768px) {
        .header-container {
            padding: 2rem;
            margin-bottom: 2rem;
        }
        .section-title {
            font-size: 1.2rem;
            margin: 1.5rem 0;
        }
    }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("""
        <div class="header-container">
            <h1 style="margin:0;font-size:2.5rem">🏠 Ev Tahmin</h1>
            <p style="color:rgba(255,255,255,0.8);margin-top:0.5rem">Ev Fiyatı Tahmin Ve Öneri Aracı</p>
        </div>
    """, unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown('<div class="section-title">📍 Lokasyon Bilgileri</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:rgba(255,255,255,0.8);margin-bottom:1rem">Ev fiyatı tahmini yapmak için lütfen aşağıdaki bilgileri doldurun.</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            il_listesi = list(preprocessor.location_map.keys())
            selected_il = st.selectbox('İl', options=il_listesi)
            ilceler = list(preprocessor.location_map.get(selected_il, {}).keys())
            selected_ilce = st.selectbox('İlçe', options=ilceler)
            mahalleler = preprocessor.location_map.get(selected_il, {}).get(selected_ilce, [])
            selected_mahalle = st.selectbox('Mahalle', options=mahalleler)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-title">📐 Temel Özellikler</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            tipi = st.selectbox('Konut Tipi', options=['Daire', 'Residence', 'Villa', 'Müstakil Ev', 'Yazlık'])
            brut_metrekare = st.number_input('Brüt Metrekare (m²)', min_value=30, max_value=500, value=100)
            binanin_yasi = st.number_input('Bina Yaşı', min_value=0, max_value=100, value=5)
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">📊 Detaylı Özellikler</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            cols = st.columns(2)
            with cols[0]:
                oda_sayisi = st.selectbox('Oda', options=['1+1', '2+1', '3+1', '4+1', '5+1'])
                banyo_sayisi = st.number_input('Banyo', min_value=1, max_value=5, value=1)
                isitma_tipi = st.selectbox('Isıtma Tipi', options=['Doğalgaz', 'Merkezi Sistem', 'Elektrikli', 'Soba'])
            with cols[1]:
                bulundugu_kat = 3  # Ortalama veya tipik bir değer
                binanin_kat_sayisi = 10  # Ortalama veya tipik bir değer
                esya_durumu = st.selectbox('Eşya Durumu', options=['Eşyalı', 'Eşyasız'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-title">⚙️ Diğer Ayarlar</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            cols = st.columns(2)
            with cols[0]:
                site_icerisinde = st.selectbox('Site İçinde', options=['Evet', 'Hayır'])
            with cols[1]:
                kullanim_durumu = st.selectbox('Kullanım Durumu', options=['Konut', 'İş Yeri', 'Diğer'])
            st.markdown('</div>', unsafe_allow_html=True)

if st.button('💵 Tahmin Yap', use_container_width=True):
    input_data = {
        'Oda Sayısı': oda_sayisi,
        'Bulunduğu Kat': bulundugu_kat,
        'Isıtma Tipi': isitma_tipi,
        'Eşya Durumu': esya_durumu,
        'Site İçerisinde': site_icerisinde,
        'Tipi': tipi,
        'Brüt Metrekare': brut_metrekare,
        'Binanın Yaşı': binanin_yasi,
        'Binanın Kat Sayısı': binanin_kat_sayisi,
        'Kullanım Durumu': kullanim_durumu,
        'Banyo Sayısı': banyo_sayisi,
        'İl': selected_il,
        'İlçe': selected_ilce,
        'Mahalle': selected_mahalle
    }
    
        
    with st.spinner('AI analiz yapıyor...'):
        input_array = preprocessor.transform(input_data)
        
        tahmin = model.predict(input_array)
        
    st.markdown(f'''
        <div class="prediction-card">
            <h3 style="margin:0 0 1rem 0;color:rgba(255,255,255,0.9)">TAHMİN EDİLEN DEĞER</h3>
            <div style="font-size:2.8rem;font-weight:700;color:var(--secondary);margin:1rem 0">{tahmin[0]:,.0f} TL</div>
            <p style="color:rgba(255,255,255,0.7);margin:0">*Gerçek değerler piyasa koşullarına göre değişiklik gösterebilir</p>
        </div>
    ''', unsafe_allow_html=True)

    predicted_price = tahmin[0]
    with st.spinner("Seçim ile benzer özelliğe sahip ilanlar getiriliyor..."):
        home_listings = get_home_listings(selected_il, predicted_price)
        display_home_listings(home_listings)

st.markdown('''
    <div class="footer">
        <div>     @yusufenes || Konut Fiyatı Tahmin ve Konut Öneri Sistemi || Tüm veriler İnternet Üzerinden Alınmıştır Ticari Kullanım Hakkı Yoktur.</div>
        <div style="margin-top:0.5rem;font-size:0.8rem">
            <span style="opacity:0.7">Geliştirici: Yusuf Enes</span> • 
            <span style="opacity:0.7">🧑‍💻 <a href="https://github.com/yusuffenes">Github</a> </span>
        </div>
    </div>
''', unsafe_allow_html=True)

