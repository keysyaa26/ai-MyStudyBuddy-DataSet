# MyStudyBuddy — Proses Pengolahan Data untuk Fitur Summarize

Deskripsi singkat tentang alur pengolahan data yang dipakai untuk membuat model AI fitur _summarize_ pada aplikasi MyStudyBuddy.

## Tujuan

Menyusun sebuah dataset yang bersih dan terstandarisasi untuk melatih model ringkasan (summarization). Hasil akhir berupa file CSV/Parquet dengan tiga kolom: `text`, `summary`, dan `source`.

## Sumber Data

- Dataset publik dari Kaggle (berbagai dataset teks yang relevan).
- Dataset publik dari Hugging Face (corpora, news, dan dataset ringkasan tersedia).
- Pengambilan data sendiri dari Wikipedia (artikel yang dipilih dan diproses).

Link dataset:
- Kaggle: https://www.kaggle.com/datasets/linkgish/indosum
- Hugging Face: https://huggingface.co/datasets/csebuetnlp/xlsum

## Overview Proses

1. Pengumpulan (collection)
   - Unduh dataset relevan dari Kaggle dan Hugging Face.
   - Crawl atau ekspor artikel Wikipedia yang diperlukan.

2. Preprocessing (`Preprocessing_Data.ipynb`)
   - Membersihkan dan melakukan standardisasi data mentah.
   - Menghasilkan dataset yang siap untuk pelatihan model.

#### **Tahapan Preprocessing**

Proses pembersihan teks meliputi beberapa langkah:

| Langkah | Aksi | Contoh |
|---------|------|--------|
| **Hapus HTML Tags** | Menghilangkan tag HTML dan markup lainnya | `<b>teks</b>` → `teks` |
| **Hapus URL** | Menghilangkan link internet | `https://example.com` → ` ` |
| **Hapus Separator** | Menghilangkan karakter pemisah (----) | `Title ---- Content` → `Content` |
| **Hapus Escape Characters** | Menghilangkan `\t`, `\r`, `\n` | Teks dengan newline dihapus |
| **Hapus Simbol Berulang** | Menghilangkan underscore, dash, tilde berulang | `___text___` → `text` |
| **Hapus Titik Berulang** | Ubah titik berulang ke titik tunggal | `...` → `. ` |
| **Hapus Karakter Khusus** | Hanya pertahankan huruf, angka, dan tanda baca dasar | Hapus emoji, karakter aneh lainnya |
| **Normalisasi Spasi** | Menghilangkan spasi ganda/triple | `word  word` → `word word` |


Penghapusan Duplikat dan Data Kosong
- **Hapus Duplikat**: Menghilangkan baris dengan teks yang identik
- **Hapus Data Kosong**: Menghilangkan baris dengan teks kosong atau whitespace-only

Data yang sudah dibersihkan disimpan ke file: 
```
file_summarize_clean.csv
```

Struktur output:
| Kolom | Deskripsi |
|-------|-----------|
| `text` | Teks artikel yang sudah dibersihkan |
| `summary` | Ringkasan artikel yang sudah dibersihkan |

### 🎯 Output

**File**: `file_summarize_clean.csv`
