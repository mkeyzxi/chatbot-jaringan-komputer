# Chatbot Jaringan Komputer

Chatbot Jaringan Komputer adalah aplikasi berbasis Retrieval-Augmented Generation (RAG) untuk menjawab pertanyaan seputar materi jaringan komputer dengan pendekatan kontekstual. Aplikasi ini menggunakan FastAPI di backend, React + Vite di frontend, dan ChromaDB untuk penyimpanan vektor dokumen.

## Fitur utama

- Chat interaktif berbasis web
- RAG menggunakan dokumen pembelajaran sebagai konteks utama
- Pencarian semantik dengan ChromaDB
- Integrasi LLM dengan provider Gemini dan Groq
- Frontend responsif menggunakan React + Vite
- Dokumentasi API otomatis via Swagger / OpenAPI

## Tech stack

### Backend
- Python 3.11+
- FastAPI
- Uvicorn
- LangChain
- LangChain Google GenAI
- LangChain OpenAI-compatible client
- ChromaDB
- Hugging Face Embeddings
- Pydantic + Pydantic Settings

### Frontend
- React 19
- Vite
- TypeScript
- CSS custom
- Lucide React
- React Markdown + GFM

## Struktur proyek

```text
chatbot-jaringan/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── generation/
│   │   ├── retrieval/
│   │   └── schemas/
│   ├── data/
│   │   ├── chroma/
│   │   └── documents/
│   ├── scripts/
│   │   └── ingest.py
│   ├── .env
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── .env
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.*
├── DESIGNKU.md
├── PRD.md
├── README.md
└── .gitignore
```

## Persyaratan sistem

Sebelum mulai, pastikan sudah terinstal:

- Windows 10/11
- Git
- Python 3.11 atau 3.12
- Node.js 18+ dan npm
- Anaconda / Miniconda (opsional, tapi direkomendasikan)
- API key dari Google Gemini dan/atau Groq

## Persiapan environment

### Opsi 1: Menggunakan Conda

Buka Anaconda Prompt atau PowerShell lalu jalankan:

```powershell
conda create -n chatbot-jaringan python=3.11 -y
conda activate chatbot-jaringan
```

### Opsi 2: Menggunakan venv biasa di Windows

```powershell
cd C:\belajarku\Belajar Flask\chatbot-jaringan\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Jika PowerShell memblokir script activation, jalankan:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\venv\Scripts\Activate.ps1
```

## Instalasi backend

Masuk ke folder backend:

```powershell
cd C:\belajarku\Belajar Flask\chatbot-jaringan\backend
```

### Install dependency Python

```powershell
pip install -r requirements.txt
```

Jika ingin install satu per satu, gunakan:

```powershell
pip install fastapi uvicorn langchain langchain-community langchain-google-genai langchain-openai pypdf sentence-transformers chromadb python-dotenv pydantic pydantic-settings
```

## Konfigurasi environment backend

Buat file `.env` di dalam folder `backend` seperti berikut:

```env
APP_NAME=chatbot-jaringan-komputer
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000

FRONTEND_URL=http://localhost:5173

EMBEDDING_MODEL=intfloat/multilingual-e5-small
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

VECTOR_DB=chroma
CHROMA_PERSIST_DIRECTORY=./data/chroma
CHROMA_COLLECTION=jaringan-komputer
RETRIEVAL_K=5

DEFAULT_LLM_MODE=berpikir
LLM_PROVIDER=gemini
LLM_MODEL=gemini-3.8-flash
FAST_LLM_PROVIDER=groq
FAST_LLM_MODEL=openai/gpt-oss-120b
THINKING_LLM_PROVIDER=gemini
THINKING_LLM_MODEL=gemini-3.8-flash
LLM_TEMPERATURE=0.1
LLM_TOP_P=0.9

GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
GEMINI_API_KEY=YOUR_GOOGLE_API_KEY
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

Catatan:
- Untuk mode `berpikir`, gunakan model yang tersedia di provider Google sesuai akun Anda.
- Jangan pernah commit file `.env` ke repository publik.
- Jika Anda memakai environment Conda, pastikan `conda activate chatbot-jaringan` sudah aktif sebelum menjalankan perintah Python.

## Ingest dokumen ke ChromaDB

Sebelum chatbot bisa menjawab, dokumen harus di-ingest terlebih dahulu.

```powershell
cd C:\belajarku\Belajar Flask\chatbot-jaringan\backend
python scripts\ingest.py
```

Atau jika memakai module environment:

```powershell
python -m scripts.ingest
```

Dokumen sumber biasanya berada di:

```text
backend\data\documents\
```

## Menjalankan backend

### Menggunakan PowerShell / CMD biasa

```powershell
cd C:\belajarku\Belajar Flask\chatbot-jaringan\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Menggunakan Conda

```powershell
conda activate chatbot-jaringan
cd C:\belajarku\Belajar Flask\chatbot-jaringan\backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Setelah server berjalan, cek:

- Swagger UI: http://localhost:8000/docs
- API root: http://localhost:8000/api
- Health check: http://localhost:8000/api/health

## Instalasi frontend

Buka terminal baru, lalu jalankan:

```powershell
cd C:\belajarku\Belajar Flask\chatbot-jaringan\frontend
npm install
```

## Menjalankan frontend

### PowerShell

```powershell
cd C:\belajarku\Belajar Flask\chatbot-jaringan\frontend
npm run dev
```

### Jika Vite default port 5173 tidak terbuka

Cek apakah port sudah dipakai:

```powershell
netstat -ano | findstr :5173
```

Jika port sudah dipakai, bisa jalankan Vite di port lain:

```powershell
npm run dev -- --host 0.0.0.0 --port 4173
```

Akses frontend via:

```text
http://localhost:5173
```

## Konfigurasi frontend `.env`

Buat file `.env` di folder `frontend` dengan isi:

```env
VITE_API_URL=http://localhost:8000/api
```

Jika frontend dan backend berjalan di local machine, konfigurasi ini sudah cukup.

## Menjalankan seluruh aplikasi

1. Aktifkan environment Python backend
2. Jalankan backend di folder `backend`
3. Jalankan frontend di folder `frontend`
4. Buka browser ke `http://localhost:5173`

## API endpoint yang umum dipakai

- `POST /api/chat` → kirim pertanyaan ke chatbot
- `GET /api/health` → cek status server
- `GET /docs` → dokumentasi Swagger UI

Contoh request dengan curl di PowerShell:

```powershell
curl -X POST "http://localhost:8000/api/chat" `
  -H "Content-Type: application/json" `
  -d '{"question":"Apa itu subnetting?","mode":"berpikir"}'
```

## Troubleshooting umum

### 1. `No module named uvicorn`

Pastikan environment sudah aktif dan dependency terinstal:

```powershell
python -m pip install -r requirements.txt
```

### 2. `Failed to fetch` atau CORS error

Pastikan backend berjalan di `http://localhost:8000` dan frontend memanggil `http://localhost:8000/api`.

Cek juga file backend `app/main.py` dan `.env` supaya `FRONTEND_URL` benar.

### 3. `404` saat membuka `/health`

Root endpoint bukan `/health`, tetapi `/api/health` karena router backend diprefix dengan `/api`.

### 4. Model LLM lama atau tidak responsif

Pastikan model yang dipakai valid untuk provider yang Anda pilih. Untuk provider Gemini, cek model yang tersedia di akun Anda. Mode `berpikir` biasanya lebih lama dibanding mode `cepat` karena model lebih berat.

### 5. ChromaDB tidak menemukan dokumen

Jalankan ulang ingest:

```powershell
python scripts\ingest.py
```

Pastikan folder dokumen berisi file yang valid dan siap diproses.

## Catatan penting

- File `.env` tidak boleh di-push ke Git
- Simpan API key di environment yang aman
- Jika ada pembaruan struktur dokumen atau penambahan materi baru, jalankan ulang ingest
- Untuk deployment lebih lanjut, gunakan environment variable di server production bukan file `.env` lokal

## Sumber referensi proyek

- [PRD.md](PRD.md)
- [DESIGNKU.md](DESIGNKU.md)

## Penutup

Proyek ini siap digunakan untuk prototyping chatbot pembelajaran jaringan komputer berbasis RAG di lingkungan lokal. Jika ingin dikembangkan lebih lanjut, langkah berikutnya bisa berupa:

- menambahkan streaming response ke frontend
- menambah model mode cepat dan mode berpikir lebih jelas
- menambah autentikasi sederhana
- menambah upload dokumen dari UI

Dibuat untuk kebutuhan pembelajaran dan eksperimen chatbot AI di bidang jaringan komputer.
