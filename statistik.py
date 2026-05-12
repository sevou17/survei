"""Hitung statistik persentase dari log_survei.txt.

Membaca file log dan menghasilkan persentase untuk:
- Jenis Kelamin
- Pekerjaan
- Usia
- Pendidikan
"""

from collections import Counter
from pathlib import Path

LOG_FILE = Path(__file__).parent / "log_survei.txt"


def baca_data(path: Path) -> list[dict]:
    """Baca log dan kembalikan list of dict per responden."""
    data: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return data

    header = [h.strip() for h in lines[0].split("|")]

    for line in lines[1:]:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != len(header):
            continue
        data.append(dict(zip(header, parts)))

    return data


def hitung_persentase(data: list[dict], kolom: str) -> list[tuple[str, int, float]]:
    """Hitung jumlah & persentase tiap nilai unik pada kolom tertentu."""
    counter = Counter(row[kolom] for row in data)
    total = sum(counter.values())
    hasil = [
        (nilai, jumlah, (jumlah / total) * 100)
        for nilai, jumlah in counter.most_common()
    ]
    return hasil


def urutan_usia(item: tuple[str, int, float]) -> tuple[int, int]:
    """Kunci urut untuk rentang usia '18-20 tahun', '21-30 tahun', dst."""
    teks = item[0].replace("tahun", "").strip()
    try:
        awal_str, akhir_str = teks.split("-")
        return (int(awal_str.strip()), int(akhir_str.strip()))
    except ValueError:
        return (999, 999)


def urutan_pendidikan(item: tuple[str, int, float]) -> int:
    urutan = {"SD": 1, "SMP": 2, "SMA": 3, "Diploma": 4, "S1": 5, "S2": 6, "S3": 7}
    return urutan.get(item[0], 99)


def cetak_tabel(judul: str, data: list[tuple[str, int, float]]) -> None:
    print()
    print(f"=== {judul} ===")
    lebar_kategori = max(len(nilai) for nilai, _, _ in data)
    lebar_kategori = max(lebar_kategori, len("Kategori"))

    print(f"{'Kategori'.ljust(lebar_kategori)} | {'Jumlah':>6} | Persentase")
    print(f"{'-' * lebar_kategori}-+-{'-' * 6}-+-----------")
    for nilai, jumlah, persen in data:
        print(f"{nilai.ljust(lebar_kategori)} | {jumlah:>6} | {persen:6.2f}%")


def main() -> None:
    data = baca_data(LOG_FILE)
    total = len(data)
    print(f"Total responden: {total}")

    jk = hitung_persentase(data, "Jenis kelamin")
    pekerjaan = hitung_persentase(data, "Pekerjaan")
    usia = sorted(hitung_persentase(data, "Usia"), key=urutan_usia)
    pendidikan = sorted(
        hitung_persentase(data, "Pendidikan"), key=urutan_pendidikan
    )

    cetak_tabel("Jenis Kelamin", jk)
    cetak_tabel("Pekerjaan", pekerjaan)
    cetak_tabel("Usia", usia)
    cetak_tabel("Pendidikan", pendidikan)


if __name__ == "__main__":
    main()
