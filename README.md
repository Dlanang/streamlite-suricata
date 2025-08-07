# Suricata Anomaly Detection System

Sistem ini dirancang untuk mendeteksi anomali pada log Suricata menggunakan pendekatan Machine Learning berbasis `Isolation Forest`, dengan visualisasi via Streamlit dan endpoint backend melalui FastAPI.

---

## 📁 Struktur Direktori

```text
suricata-anomaly/
├── app/                    # Frontend Streamlit
│   ├── pages/
│   ├── static/
│   └── utils/
├── backend/                # Backend FastAPI
│   ├── api/
│   ├── core/
│   └── models/
├── data/
│   ├── input/              # CSV dari log Suricata
│   └── output/             # Hasil deteksi
├── deployment/
│   ├── nginx/
│   ├── certbot/
│   └── scripts/
├── logs/                   # Log aplikasi
├── notebooks/              # Exploratory Jupyter Notebooks
├── venv/                   # Virtual environment
├── .env                    # Variabel lingkungan
├── requirements.txt        # Dependensi Python
├── main.py                 # Entry point Streamlit
├── api_main.py             # Entry point FastAPI
└── detect.py               # Engine deteksi anomali
```

---

## 🚀 Instalasi & Setup

### 1. Clone Repo
```bash
git clone https://github.com/dlanang/streamlite-suricata.git
cd suricata-anomaly
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalasi Requirements

```bash
pip install -r requirements.txt
```

### 4. Buat File `.env`

```env

sequenceDiagram
    User->>Streamlit: Buka /home
    Streamlit->>FastAPI: GET /anomalies/json
    FastAPI->>Database: Query data
    Database-->>FastAPI: Return data
    FastAPI-->>Streamlit: JSON response
    Streamlit->>User: Render dataframe

## 💻 Menjalankan Aplikasi

### Jalankan Streamlit (Frontend)

```bash
streamlit run main.py
```

### Jalankan FastAPI (Backend)

```bash
uvicorn api_main:app --reload --port 8000
```

## 🧠 Machine Learning Model

Model deteksi anomali menggunakan `IsolationForest`. Data numerik dari log Suricata dibaca dan dilabeli dengan prediksi anomali (-1 = anomali, 1 = normal).

```python
from sklearn.ensemble import IsolationForest
clf = IsolationForest(contamination=0.01)
```


## 📈 Visualisasi di Streamlit

* Upload file log Suricata (`.csv`)
* Jalankan deteksi anomali
* Tampilkan hasil visualisasi
* Ekspor hasil ke JSON & CSV (`data/output/`)

---

## 📡 Dokumentasi API (FastAPI)

### 🔐 Auth Header

Gunakan basic auth (bawaan FastAPI HTTPBasic).

```
Authorization: Basic base64(admin:bekik_cantik123)
```

### **GET /**

**Cek status server**

```http
GET / HTTP/1.1
```

**Response:**

```json
{"status": "API is running"}
```

### **POST /detect**

**Jalankan deteksi anomali**

```http
POST /detect HTTP/1.1
Content-Type: multipart/form-data
Authorization: Basic ...

file: [suricata_logs.csv]
```

**Response:**

```json
{
  "status": "ok",
  "anomalies_detected": 14,
  "output_file": "data/output/anomaly_results.csv"
}
```


### **GET /results/json**

**Ambil hasil deteksi dalam format JSON**

```http
GET /results/json HTTP/1.1
```

**Response:**

```json
[
  {"src_ip": "...", "dest_ip": "...", ..., "anomaly": -1},
  ...
]
```


### **GET /results/csv**

**Ambil hasil deteksi dalam format CSV**

```http
GET /results/csv HTTP/1.1
```

**Response:** File `anomaly_results.csv` sebagai attachment.


## 📊 Output Hasil

Setiap baris dari file `anomaly_results.csv` akan memiliki kolom tambahan `anomaly`:

* `-1` = Anomali
* `1`  = Normal

Contoh:

```csv
timestamp,src_ip,dest_ip,bytes,flags,anomaly
2025-08-07 10:01:22,192.168.1.10,10.10.10.5,5432,S,1
2025-08-07 10:01:24,192.168.1.20,10.10.10.8,12000,PA,-1
```

## 🔐 Keamanan

* Akses API menggunakan HTTP Basic Auth
* Simpan kredensial di `.env` file
* Validasi input dengan `Pydantic`
* Logging ke folder `logs/`


## 💪 Testing

```bash
pytest tests/
```

---

## 📌 TODO

* [ ] Integrasi ke Grafana/Loki
* [ ] Penjadwalan deteksi otomatis via Cron/Task
* [ ] Fitur input manual dari Streamlit
* [ ] Penyimpanan hasil ke database (SQLite / PostgreSQL)


## 📄 Lisensi

MIT License.
