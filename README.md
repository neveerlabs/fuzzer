# Fuzzer

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.13%2B-blue)

**Fuzzer** adalah alat _penetration testing_ untuk model bahasa besar (LLM) yang dirancang khusus untuk menguji ketahanan filter etika dan keamanan AI. Alat ini secara otomatis mengirimkan berbagai payload _jailbreak_ dan prompt injeksi ke model AI target (melalui API cloud) dan mencatat mana yang berhasil menembus batasan moral AI.

> **Disclaimer**: Proyek ini hanya untuk tujuan pendidikan, riset keamanan, dan pengujian sistem sendiri. Jangan digunakan untuk aktivitas ilegal atau merugikan pihak lain.

## Fitur Utama

- **Cloud‑Native** – Tidak perlu GPU atau spek tinggi. Semua beban komputasi dijalankan di server cloud (OpenRouter).
- **Multi‑Model** – Mendukung banyak model AI, termasuk model _uncensored_ seperti `Dolphin`, `Hermes`, atau `Llama‑3.1` dan lain lain.
- **Modular Payloads** – Koleksi payload _jailbreak_ (DAN, Developer Mode, Role Play, Obfuscation) dan dapat ditambahkan/update.
- **Output Berwarna** – Hasil `SUCCESS` (hijau), `FAILED` (merah), atau `UNKNOWN` (putih) langsung terlihat di terminal.
- **Laporan CSV** – Semua hasil pengujian otomatis tersimpan rapi untuk analisis lanjutan.

## Instalasi & Setup

### 1. Clone Repositori
```bash
git clone https://github.com/neveerlabs/fuzzer.git
cd fuzzer
```
### 2. Aktifkan environment
```bash
source venv/bin/activate    # Linux/Mac
.\venv\Scripts\activate     # (Windows)
```
### 3. Install dependen
```bash
pip install -r requirements.txt
```
### 4. Dapatkan API Key Gratis dari OpenRouter
* Daftar / login di https://openrouter.ai
* Masuk ke https://openrouter.ai/Keys
* Klik **Create Key**, beri nama (misal `Fuzzer`), lalu salin API Key yang muncul.
### 5. Konfigurasi **`config.yaml`**
Buka `config.yaml` dan tempelkan API key anda:
```yaml
# config.yaml
target:
  model: "rekaai/reka-edge" # Model dapat diubah

api:
  key: "sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Ganri dengan API Key milik anda
  url: "https://openrouter.ai/api/v1/chat/completions"
```
> **Tips memilih model**: Gunakan model dengan label `uncensored` atau `abliterated` agar lebih mudah di-*bypass*. Contoh: `cognitivecomputations/dolphin-mixtral` atau `nousresearch/hermes-2-pro-mistral`
### Cara Menggunakan
Jalankan perintah berikut dari terminal:
```bash
python3 fuzzer.py
```

---

Alat akan mulai mengombinasikan setiap payload dengan setiap pertanyaan berbahaya dan mengirimkannya ke model AI target. Progress akan ditampilkan di terminal dengan kode warna:

* 🟢 **SUCCESS** – AI memberikan jawaban teknis (filter etika jebol).
* 🔴 **FAILED** – AI menolak menjawab.
* ⚪ **UNKNOWN** – Respon tidak jelas (AI bingung), perlu dicek manual.

Setelah selesai (atau dihentikan paksa dengan cara `Ctrl+C`), semua hasil akan tersimpan di `fuzzing_results.csv`.

## Kustomisasi
* **Tambah Payload Baru**: Cukup tambahkan file `.txt` baru di folder `data/payloads/` (satu baris = satu payload).
* **Tambah Pertanyaan**: Edit `data/harmful_questions.txt`.
* **Ganti Model AI**: Ubah nilai `model` di `config.yaml` (lihat daftar model gratis di https://openrouter.ai/models).

## Lisensi
Proyek ini dilisensikan di bawah **`MIT License`**. Silakan gunakan, modifikasi, dan sebarkan secara bebas dengan tetap menyertakan atribusi.

---

## Dukung Proyek Ini
Jika alat ini bermanfaat, beri bintang ⭐ di GitHub dan bagikan ke teman-teman *red teamer* atau peneliti AI lainnya!
> *Dibuat dengan oleh para penghobi keamanan siber yang penasaran seberapa kuat pagar moral AI modern*.
