# 🚲📊 Bike Sharing Analytics Dashboard"

## Deskripsi

Proyek ini bertujuan untuk melakukan analisis mendalam terhadap **Bike Sharing Dataset** guna mengungkap pola, tren, dan faktor-faktor yang memengaruhi penggunaan sepeda. Hasil analisis ini diharapkan dapat memberikan wawasan berharga serta informasi yang dapat digunakan untuk pengambilan keputusan yang lebih efektif.

## Struktur Direktori

- **/data**: Direktori ini menyimpan dataset yang digunakan dalam proyek, disimpan dalam format .csv, dan berfungsi sebagai sumber utama untuk analisis data.
- **/dashboard**: Direktori ini berisi data serta file utama, yaitu dashboard.py, yang digunakan untuk membangun dan menampilkan dashboard hasil analisis secara interaktif.
- **notebook.ipynb**: File ini digunakan sebagai wadah utama untuk melakukan eksplorasi data, analisis statistik, dan visualisasi guna mendapatkan wawasan yang lebih mendalam dari dataset.
## Cara Menjalankan Dashboard

## Setup Environment - Anaconda
```
conda create --name bike-sharing-ds python=3.13.2
conda activate bike-sharing-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir bike_sharing_data_analysis
cd bike_sharing_data_analysis
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```
