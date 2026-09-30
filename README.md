# Auto Survei STAR (Kemenimipas)

Skrip Python untuk mengisi otomatis formulir survei **STAR** (contoh tautan: `star-survei3a.kemenimipas.go.id`) lewat **Selenium** dengan browser **Brave** (mode penyamaran). Captcha dibaca dengan **ddddocr**.

## Prasyarat

- Python 3.10+ (disarankan)
- [Brave Browser](https://brave.com/) terpasang, atau set path manual (lihat di bawah)
- [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) yang cocok dengan versi Chromium Brave Anda (Selenium 4 biasanya mengelola driver otomatis jika sudah dikonfigurasi)

## Instalasi

```bash
pip install selenium ddddocr
```

## File penting

| File | Fungsi |
|------|--------|
| `auto_survei.py` | Alur utama: buka form, isi data acak, OCR captcha, kirim |
| `nama lk.txt` / `nama pr.txt` | Daftar nama; nama yang terpakai dihapus dari file |
| `solve_ocr_from_url.py` | Utilitas uji OCR captcha dari halaman (opsional) |

## Menjalankan

```bash
python auto_survei.py
```

Opsi berguna:

- `--url` — URL form (default sudah di kode)
- `--male-file` / `--female-file` — path file nama
- `--brave-path` — path `brave.exe` jika tidak terdeteksi (atau set env `BRAVE_PATH`)
- `--headless` — tanpa jendela browser
- `--repeat N` — jumlah pengisian berturut-turut
- `--keep-open-seconds N` — biarkan browser terbuka N detik per iterasi

## Catatan

- XPath dan struktur form **bisa berubah** kapan saja; jika situs diperbarui, skrip mungkin perlu disesuaikan.
- Penggunaan otomatis bisa melanggar ketentuan situs. Pastikan Anda punya izin dan gunakan secara bertanggung jawab.
