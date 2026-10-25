# CafeRate API

REST API sederhana untuk mengelola data kafe dan ulasan pengunjung. Proyek menggunakan FastAPI, Pydantic v2, struktur modular, API key sederhana, dan pytest TestClient.

## Fitur
- Menambahkan dan melihat katalog kafe.
- Mencari kafe berdasarkan area.
- Menambahkan dan melihat ulasan kafe.
- Menghitung rata-rata rating serta jumlah ulasan.
- Validasi request dan response menggunakan Pydantic.
- Proteksi endpoint data menggunakan header `X-API-Key`.
- Automated test suite.

> Penyimpanan saat ini menggunakan memori (in-memory), sehingga data akan kembali kosong saat server dimulai ulang. Ini cocok untuk sprint/prototipe; database bisa ditambahkan kemudian.

## Persyaratan
Python 3.9 atau lebih baru (sudah diuji di Python 3.9).

## Menjalankan di macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Buka `http://127.0.0.1:8000/docs` untuk mencoba API melalui Swagger UI.

## API key
Untuk endpoint `/api/v1/...`, kirim header:

```text
X-API-Key: caferate-dev-key
```

Ini adalah API key contoh untuk tugas, bukan mekanisme keamanan produksi. Jangan menggunakan key contoh untuk aplikasi nyata.

## Endpoint

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/` | Informasi layanan, tanpa API key |
| POST | `/api/v1/cafes` | Menambahkan kafe |
| GET | `/api/v1/cafes` | Daftar kafe; mendukung `?area=Makassar` |
| GET | `/api/v1/cafes/{cafe_id}` | Detail kafe dan ringkasan rating |
| GET | `/api/v1/cafes/{cafe_id}/rating-card` | Kartu ringkasan rating khas CafeRate |
| POST | `/api/v1/cafes/{cafe_id}/reviews` | Menambahkan ulasan ke kafe |
| GET | `/api/v1/cafes/{cafe_id}/reviews` | Daftar ulasan untuk kafe |
| GET | `/api/v1/reviews/{review_id}` | Detail satu ulasan |
| DELETE | `/api/v1/reviews/{review_id}` | Menghapus ulasan |

## Contoh request

Tambahkan kafe:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/cafes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: caferate-dev-key" \
  -d '{"name":"Kopi Sudut","area":"Samata","address":"Jl. H.M. Yasin Limpo","category":"Coffee Shop"}'
```

Tambahkan ulasan:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/cafes/1/reviews \
  -H "Content-Type: application/json" \
  -H "X-API-Key: caferate-dev-key" \
  -d '{"visitor_alias":"PengunjungA","service_rating":5,"taste_rating":4,"ambience_rating":5,"comment":"Pelayanan ramah dan tempat nyaman."}'
```

## Menjalankan tes

```bash
pytest -v
```

Tes dibuat menggunakan `pytest` dan FastAPI `TestClient`. Data penyimpanan di-reset sebelum setiap tes agar hasil tes tidak saling memengaruhi.

## Struktur folder

```text
CafeRate/
├── main.py
├── requirements.txt
├── README.md
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── errors.py
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── memory.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── cafes.py
│   │   └── reviews.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── cafe.py
│   │   └── review.py
│   └── services/
│       ├── __init__.py
│       └── rating.py
└── tests/
    ├── conftest.py
    └── test_api.py
```
