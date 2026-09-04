# Chatbot Jaringan Komputer 🤖🌐

Proyek ini adalah sistem Chatbot berbasis *Retrieval-Augmented Generation (RAG)* yang dirancang untuk menjawab pertanyaan terkait jaringan komputer, komunikasi nirkabel, dan materi terkait lainnya. Chatbot ini dibangun dengan **FastAPI** di sisi backend dan **React + Vite** di sisi frontend, serta menggunakan **ChromaDB** sebagai basis data vektor untuk penyimpanan dokumen.

## 🚀 Fitur Utama

- **Tanya Jawab Pintar**: Chatbot dapat memberikan jawaban spesifik berdasarkan modul/dokumen (PDF, PPTX) seputar Jaringan Komputer.
- **RAG Architecture**: Menggabungkan kemampuan pencarian (*retrieval*) dari dokumen dan pembuatan teks (*generation*) menggunakan *Large Language Model* (LLM) melalui **Groq API**.
- **Modern UI/UX**: Tampilan chat interaktif, bersih, dan responsif menggunakan React dan Vite.
- **Pemrosesan Dokumen Otomatis**: Skrip *ingest* yang otomatis mengubah dokumen-dokumen materi menjadi vektor (*embedding*) di ChromaDB.

---

## 🛠️ Tech Stack (Teknologi yang Digunakan)

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: Uvicorn
- **AI / LLM Orchestration**: [LangChain](https://python.langchain.com/)
- **LLM Provider**: Groq (Via `langchain-groq`)
- **Embeddings**: HuggingFace (`intfloat/multilingual-e5-small`)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **Konfigurasi**: Pydantic Settings

### Frontend
- **Framework**: [React 19](https://react.dev/) + [Vite](https://vitejs.dev/)
- **Bahasa**: TypeScript
- **Styling**: CSS Vanilla (Responsive & Modern)
- **Icons**: Lucide React
- **Markdown Parsing**: React-Markdown

---

## 📁 Struktur Proyek

```text
chatbot-jaringan/
│
├── backend/                  # Kode Backend (Python)
│   ├── app/                  # Logika Utama FastAPI & LangChain
│   ├── data/
│   │   ├── chroma/           # Direktori penyimpanan vektor ChromaDB
│   │   └── documents/        # Kumpulan file sumber (PDF/PPTX) untuk Chatbot
│   ├── scripts/
│   │   └── ingest.py         # Skrip untuk memasukkan dokumen ke ChromaDB
│   ├── .env                  # File variabel lingkungan backend (TIDAK di-commit)
│   └── requirements.txt      # Daftar dependensi Python
│
├── frontend/                 # Kode Frontend (Node.js/React)
│   ├── src/                  # Kode komponen UI React & TypeScript
│   ├── public/               # File aset statis
│   ├── package.json          # Daftar dependensi & script Node
│   └── vite.config.ts        # Konfigurasi Vite
│
├── .gitignore                # File ignore Git
├── DESIGNKU.md               # Dokumen rancangan desain sistem
├── PRD.md                    # Product Requirements Document
└── README.md                 # Dokumentasi ini
```

---

## ⚙️ Persyaratan Sistem (Prerequisites)

Pastikan Anda sudah menginstal aplikasi berikut di komputer Anda:
1. **Python** (Versi 3.8 atau lebih baru)
2. **Node.js** (Versi 18 atau lebih baru) & **npm**
3. **Git**
4. Kunci API (*API Key*) dari [Groq](https://console.groq.com/).

---

## 🚀 Cara Mulai & Menjalankan Proyek

Ikuti langkah-langkah di bawah ini secara berurutan untuk menjalankan aplikasi di lingkungan lokal Anda.

### 1. Konfigurasi Backend (FastAPI)

Buka terminal dan arahkan ke folder `backend`:
```bash
cd backend
```

**a. Buat Virtual Environment dan Aktifkan:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**b. Instal Dependensi:**
```bash
pip install -r requirements.txt
```

**c. Konfigurasi Variabel Lingkungan (`.env`):**
Buat file bernama `.env` di dalam folder `backend/` dan isi dengan konfigurasi berikut. Pastikan Anda memasukkan Groq API Key Anda.

```env
# Konfigurasi LLM
GROQ_API_KEY="masukkan_api_key_groq_anda_disini"

# (Opsional) Sesuaikan jika Anda mengganti model default di config.py
# LLM_MODEL="llama3-70b-8192" 
```

**d. Proses Dokumen ke dalam Database Vektor (Ingestion):**
Sebelum menjalankan server, jalankan skrip ini agar Chatbot memiliki "pengetahuan" dari dokumen PDF/PPTX yang ada di folder `data/documents/`:
```bash
python scripts/ingest.py
```
*(Tunggu hingga proses ekstraksi teks dan pembuatan embedding selesai)*.

**e. Jalankan Server Backend:**
```bash
uvicorn app.main:app --reload
```
Backend sekarang berjalan di: **http://localhost:8000**
*(Anda dapat melihat dokumentasi API interaktif di http://localhost:8000/docs)*

---

### 2. Konfigurasi Frontend (React + Vite)

Buka tab terminal baru dan arahkan ke folder `frontend`:
```bash
cd frontend
```

**a. Instal Dependensi NPM:**
```bash
npm install
```

**b. Jalankan Server Development Frontend:**
```bash
npm run dev
```
Frontend sekarang berjalan di: **http://localhost:5173**

---

## 📝 Catatan Penting
- **Cross-Origin Resource Sharing (CORS)**: Frontend dan Backend diatur agar dapat berkomunikasi di `localhost`. Jika Anda menjalankan frontend di port yang berbeda, pastikan untuk memperbarui variabel `frontend_url` di `backend/app/core/config.py`.
- **Database ChromaDB**: Data dari hasil _ingestion_ akan tersimpan secara lokal di folder `backend/data/chroma`. Folder ini diabaikan oleh `.gitignore` untuk mencegah repo menjadi bengkak. Apabila ada penambahan dokumen baru, pastikan menjalankan skrip `ingest.py` kembali.

---
Dibuat dengan ❤️ untuk pembelajaran Jaringan Komputer.
