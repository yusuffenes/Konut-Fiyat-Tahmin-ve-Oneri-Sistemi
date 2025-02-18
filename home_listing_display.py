import streamlit as st

def display_home_listings(listings):
    st.markdown("""
        <style>
        .listing-card {
            background: #2D2D2D;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s;
        }
        .listing-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .price-tag {
            color: #00C0A3;
            font-size: 1.4rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }
        .property-info {
            color: rgba(255,255,255,0.8);
            font-size: 0.9rem;
            margin: 0.3rem 0;
        }
        .listing-link {
            display: inline-block;
            background: #2A3950;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            margin-top: 0.5rem;
            transition: background 0.2s;
        }
        .listing-link:hover {
            background: #374863;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### 🏠 Benzer Fiyatlı İlanlar", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    for idx, listing in enumerate(listings):
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"""
                <div class="listing-card">
                    <img src="{listing['resim_url']}" style="width: 100%; height: 200px; object-fit: cover; object-position: center; border-radius: 5px; margin-bottom: 0.5rem;">
                    <div style="font-size:1.2rem; font-weight:bold">{listing['title']}</div>
                    <div class="price-tag">{listing['price']:,} TL</div>
                    <div class="property-info">📏 {listing['Brüt Metrekare']}</div>
                    <div class="property-info">🏘️ {listing.get('Oda Sayısı', 'Belirtilmemiş')}</div>
                    <div class="property-info">♨️ {listing.get('Isıtma Tipi', 'Belirtilmemiş')}</div>
                    <a href="{listing['url']}" target="_blank" class="listing-link">İlanı Görüntüle →</a>
                </div>
            """, unsafe_allow_html=True)
