# SIC SATRIA DATA 2026 - Analisis Transisi Energi & Kendaraan Listrik (EV) di Indonesia 🇮🇩⚡

## 📌 Deskripsi Proyek
Laporan Proyek dan *Source Code* ini merupakan submission untuk **Statistics Infographic Competition (SIC) SATRIA DATA 2026** dengan sub-tema: *Transisi Energi dan Tantangan Industri Nasional*. 

Proyek ini bertujuan untuk memvisualisasikan adopsi, demografi geografis, dan tren penetrasi Kendaraan Listrik (EV) di Indonesia guna mengevaluasi ketimpangan pemerataan infrastruktur pengisian daya serta efektivitas subsidi pemerintah dalam mencapai *Net Zero Emission*.

## 🛠️ Output Tugas
Sesuai dengan panduan rubrik kompetisi, proyek ini memuat dua jenis output utama:
1. **Dashboard Interaktif (Web-Based)**: Dibangun menggunakan Python (Streamlit & Plotly) untuk menyajikan eksplorasi data secara dinamis dan *storytelling* interaktif. Berkas: `app.py`
2. **Infografis Statis (Poster A4)**: Poster visual yang merangkum keseluruhan data deskriptif menuju kesimpulan yang solid. Berkas: `infografis.html`

## 📊 Metodologi & Sumber Data
Mengingat keterbatasan *raw data* agregat individu EV di Indonesia bagi publik, dataset yang dilampirkan (`ev_indonesia_data.csv`) merupakan data **sintetis/simulasi representatif** (berisi 20.000 baris sampel). 

Dataset ini di-*generate* secara proporsional dan divalidasi silang berdasarkan statistik faktual yang dirilis oleh:
- Laporan Perkembangan KBLBB Kementerian ESDM RI (2025/2026).
- Data Sertifikat Registrasi Uji Tipe (SRUT) Kementerian Perhubungan RI.
- Laporan *wholesales* manufaktur kendaraan listrik nasional.

## 💡 Analisis & Rekomendasi Kebijakan
Dari visualisasi yang dibangun, ditarik kesimpulan bahwa tantangan terbesar transisi energi industri Indonesia adalah **Ketimpangan Infrastruktur (Jawa-Sentris)** dan **Penetrasi Pasar Roda 4 yang Tertahan Harga (Daya Beli)**. Solusi aplikatif yang direkomendasikan:
1. **Pemerataan Terarah:** Ekspansi infrastruktur SPKLU pada jalur logistik darat utama di luar Jawa-Bali.
2. **Fokus Armada Komersial:** Keringanan pajak/subsidi korporat (*fleet*) untuk mendongkrak penciptaan *Green Jobs*.
3. **Hilirisasi Penuh:** Percepatan Giga-Factory perakitan sel baterai utuh guna menekan *Base MSRP* tanpa ketergantungan subsidi APBN jangka panjang.

---

## 💻 Cara Menjalankan Kode (Bagi Dosen/Penguji)
Jika Dosen Penilai ingin menjalankan dan membedah *source code* secara lokal di mesin mereka, berikut adalah langkahnya:

1. Pastikan **Python 3.9+** telah terinstal.
2. Lakukan *Clone repository* GitHub ini ke perangkat Anda.
3. Instal semua paket pustaka (dependensi) yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan server lokal antarmuka web Streamlit:
   ```bash
   streamlit run app.py
   ```
5. Akses hasil *render* melalui `http://localhost:8501`.
