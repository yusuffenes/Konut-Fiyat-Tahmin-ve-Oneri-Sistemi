import numpy as np
import re
import json
import pandas as pd 

class SingleInstancePreprocessor:
    def __init__(self, location_map_path='location_map.json'):
        self.isitma_mapping = {
            "Doğalgaz": 5,  
            "Merkezi Sistem": 6,
            "Elektrikli": 3,
            "Soba": 1,
            "Isıtma Yok": 0,
            "Other": 4,
            "Klimalı": 3,
            "Doğalgaz Sobalı": 4,
            "Merkezi (Pay Ölçer)": 6,
            "Merkezi Doğalgaz": 6,
            "Güneş Enerjisi": 9,
            "Yerden Isıtma": 7,
            "Merkezi Kömür": 8,
            "Şömine": 2,
            "Jeotermal": 10,
            "Kat Kaloriferi": 11,
            "Isı Pompası": 12
        }
        self.esya_mapping = {
            "Eşyalı": 1,
            "Eşyasız": 0,
            "Belirtilmemiş": 2,
            "Boşluk": 2 
        }
        self.tipi_mapping = {
            "Daire": 3,
            "Residence": 5,
            "Villa": 8,
            "Müstakil Ev": 6,
            "Yazlık": 4,
            "Bina": 3,
            "Köy Evi": 1,
            "Çiftlik Evi": 2,
            "Devremülk": 5,
            "Yalı Dairesi": 7,
            "Köşk": 9,
            "Prefabrik": 1,
            "Yalı": 12,
            "Dağ Evi": 4,
            "Kooperatif": 3
        }
        self.kullanim_mapping = {
            "Konut": 0,
            "İş Yeri": 1,
            "Diğer": 2,
            "Boş": 3,
            "Boşluk2": 3 
        }
        self.yatirim_mapping = {
            'Yatırıma Uygun':'10',
            'Yatırıma Uygun Değil':'0',
            'Bilinmiyor':'1',
            'Belirtilmemiş':'1'
        }
        
        self.oturma_mapping = {
            'Kendisi' : 0,
            'Kiracı': 1,
        }

        try:
            with open(location_map_path, 'r', encoding='utf-8') as f:
                self.location_map = json.load(f)
        except FileNotFoundError:
            print(f"Hata: {location_map_path} dosyası bulunamadı.")
            self.location_map = {}

    def transform(self, input_data):
        """
        Tek bir örnek için girdi verilerini dönüştürür.
        """
        input_series = pd.Series(input_data)

        oda = input_series.get("Oda Sayısı")
        if isinstance(oda, str):
            oda = oda.strip()
            if "Stüdyo" in oda:
                oda_val = 0.0
            elif "+" in oda:
                try:
                    parts = oda.split("+")
                    oda_val = float(parts[0]) + float(parts[1])
                except Exception:
                    oda_val = float(oda.replace("Oda", "").strip())
            else:
                oda_val = float(oda.replace("Oda", "").strip())
        else:
            oda_val = float(oda)

        kat = input_series.get("Bulunduğu Kat")
        if isinstance(kat, str):
            kat_val = int(re.sub(r'\D', '', kat))
        else:
            kat_val = int(kat)

        isitma = input_series.get("Isıtma Tipi")
        isitma_val = self.isitma_mapping.get(isitma, 4)

        esya = input_series.get("Eşya Durumu")
        esya_val = self.esya_mapping.get(esya, 2)

        site = input_series.get("Site İçerisinde", "Hayır")
        site_val = 1 if site == "Evet" else 0

        tipi = input_series.get("Tipi")
        tipi_val = self.tipi_mapping.get(tipi, 3) 

        metrekare = input_series.get("Brüt Metrekare")
        if isinstance(metrekare, str):
            metrekare_val = float(re.sub(r'[^0-9]', '', metrekare))
        else:
            metrekare_val = float(metrekare)

        yas = input_series.get("Binanın Yaşı")
        if isinstance(yas, str):
            yas_val = int(re.sub(r'\D', '', yas))
        else:
            yas_val = int(yas)

        bina_kat = input_series.get("Binanın Kat Sayısı")
        bina_kat_val = int(bina_kat)

        kullanim = input_series.get("Kullanım Durumu")
        kullanim_val = self.kullanim_mapping.get(kullanim, 0)  
        
        yatirim = input_series.get("Yatırıma Uygunluk")
        yatirim_val = self.yatirim_mapping.get(yatirim, 1)  

        banyo = input_series.get("Banyo Sayısı")
        banyo_val = int(banyo)

        il = input_series.get("İl")
        ilce = input_series.get("İlçe")
        mahalle = input_series.get("Mahalle")

        il_val = 0  
        ilce_val = 0 
        mahalle_val = 0  

        if il in self.location_map:
            il_val = list(self.location_map.keys()).index(il)
            if ilce in self.location_map[il]:
                ilce_val = list(self.location_map[il].keys()).index(ilce)
                if mahalle in self.location_map[il][ilce]:
                    mahalle_val = self.location_map[il][ilce].index(mahalle)
                    
        oturma_durumu = input_series.get('oturma_durumu')
        oturma_val = self.oturma_mapping.get(oturma_durumu,0)
        

        features = [oda_val, kat_val, isitma_val, esya_val, site_val, tipi_val,
                    metrekare_val, yas_val, bina_kat_val, kullanim_val, yatirim_val, banyo_val,
                    il_val, ilce_val, mahalle_val,oturma_val]

        X = np.array(features).reshape(1, -1)
        return X
