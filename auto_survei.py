import argparse
import os
import random
import re
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

URL_SURVEI = "https://star-survei3a.kemenimipas.go.id/ly/ASCG83Kb"
XPATH_CAPTCHA_IMAGE = (
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[31]/div/div/div/div/div/div/div[1]/div/img"
)
XPATH_CAPTCHA_INPUT = (
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[31]/div/div/div/div/div/div/div[2]/div/input"
)
XPATH_CAPTCHA_REFRESH = (
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[31]/div/div/div/div/div/div/div[2]/div/span"
)
XPATH_SUBMIT = "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[32]/div/div/button[1]"
XPATH_CONFIRM_YA = "/html/body/div[3]/div[2]/div/div[2]/button[2]"
XPATH_CAPTCHA_ERROR_OK = "/html/body/div[3]/div[2]/div/div[2]/button"

XPATH_PRODUK_LAYANAN_OPTION_9 = (
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[2]/div/div/div/div/dd/select/option[9]" #Layanan Kunjungan
)
XPATH_NAMA = (
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[4]/div/div/div/div/div[1]/div/input[2]" #Nama Lengkap
)
XPATH_HP = (
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[5]/div/div/div/div/div[1]/div/input[2]" #Nomor Handphone
)

XPATH_PEKERJAAN = [
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[6]/div/div/div/div/div[1]/div/label[1]", #PNS
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[6]/div/div/div/div/div[1]/div/label[4]", #SWASTA
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[6]/div/div/div/div/div[1]/div/label[5]", #WIRAUSAHA
]

XPATH_USIA = [
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[7]/div/div/div/div/div[1]/div/label[1]", #18-20 tahun
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[7]/div/div/div/div/div[1]/div/label[2]", #21-30 tahun
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[7]/div/div/div/div/div[1]/div/label[3]", #31-40 tahun
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[7]/div/div/div/div/div[1]/div/label[4]", #41-50 tahun
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[7]/div/div/div/div/div[1]/div/label[5]", #51-60 tahun
]

XPATH_GENDER_LAKI = (
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[8]/div/div/div/div/div[1]/div/label[1]" #laki-laki
)
XPATH_GENDER_PEREMPUAN = (
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[8]/div/div/div/div/div[1]/div/label[2]" #perempuan
)   

XPATH_PENDIDIKAN = [
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[9]/div/div/div/div/div[1]/div/label[1]", #SD
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[9]/div/div/div/div/div[1]/div/label[2]", #SMP
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[9]/div/div/div/div/div[1]/div/label[3]", #SMA
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[9]/div/div/div/div/div[1]/div/label[4]", #Diploma
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[9]/div/div/div/div/div[1]/div/label[5]", #S1
]

XPATH_SKM_SPKP = [
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[11]/div/div/div/div/div[1]/div/div/div/a[6]", #Informasi tentang jenis pelayanan tersedia melalui media elektronik maupun non elektronik (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[12]/div/div/div/div/div[1]/div/div/div/a[6]", #Persyaratan pelayanan yang harus Bapak/Ibu penuhi sesuai dengan persyaratan yang ditetapkan/diinfokan (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[13]/div/div/div/div/div[1]/div/div/div/a[6]", #Alur/prosedur pelayanan ini mudah diikuti/dilakukan (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[14]/div/div/div/div/div[1]/div/div/div/a[6]", #Alur/prosedur pelayanan ini mudah diikuti/dilakukan (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[15]/div/div/div/div/div[1]/div/div/div/a[6]", #Jangka waktu penyelesaian pelayanan yang Bapak/Ibu terima sesuai dengan ketentuan (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[16]/div/div/div/div/div[1]/div/div/div/a[6]", #Produk pelayanan yang tercantum dalam standar pelayanan (diinformasikan) sesuai dengan hasil yang Bapak/Ibu terima (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[17]/div/div/div/div/div[1]/div/div/div/a[6]", #Ada tidaknya tarif/biaya pelayanan yang Bapak/Ibu bayarkan sesuai dengan ketentuan (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[18]/div/div/div/div/div[1]/div/div/div/a[6]", #Ketersediaan dan kemudahan akses terhadap sarana prasarana pendukung pelayanan/sistem pelayanan online (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[19]/div/div/div/div/div[1]/div/div/div/a[6]", #Layanan konsultasi dan pengaduan yang ada mudah digunakan/diakses (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[20]/div/div/div/div/div[1]/div/div/div/a[6]", #Petugas pelayanan/sistem pelayanan online yang ada merespon keperluan Bapak/Ibu dengan cepat (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[21]/div/div/div/div/div[1]/div/div/div/a[6]", #Bagaimana pendapat Bapak/Ibu tentang pengetahuan, keahlian, keterampilan, dan pengalaman petugas dalam memberikan pelayanan? (bintang 6)
]

XPATH_SPAK = [
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[23]/div/div/div/div/div[1]/div/div/div/a[6]", #Tidak ada diskriminasi yang dilakukan pegawai (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[24]/div/div/div/div/div[1]/div/div/div/a[6]", #Tidak ada kecurangan/pelayanan di luar prosedur yang dilakukan pegawai (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[25]/div/div/div/div/div[1]/div/div/div/a[6]", #Tidak ada pegawai yang meminta imbalan uang/barang/fasilitas diluar ketentuan (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[26]/div/div/div/div/div[1]/div/div/div/a[6]", #Tidak ada pungutan liar (pungli) oleh pegawai (bintang 6)
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[27]/div/div/div/div/div[1]/div/div/div/a[6]", #Tidak ada calo untuk layanan ini (bintang 6)
]

XPATH_EVALUASI_1 = (
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[29]/div/div/div/div/div[1]/div/label[1]" #Sebelum menjawab survei ini, apakah ada pegawai/pejabat pada unit layanan ini yang mengarahkan Bapak/Ibu/Saudara untuk memberikan jawaban yang bagus-bagus/baik-baik saja? (tidak)
)
XPATH_EVALUASI_2 = (
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[30]/div/div/div/div/div[1]/div/label[9]" #Perlu/tidak perlu perbaikan (sesuai pilihan berikut) (tidak ada yang perlu diperbaiki)
)

# Label untuk log (selaras dengan urutan XPath di atas)
PRODUK_LAYANAN_LOG = "Layanan Kunjungan (opsi ke-9 / index 8)"

LABEL_PEKERJAAN = ("PNS", "SWASTA", "WIRAUSAHA")

LABEL_USIA = (
    "18-20 tahun",
    "21-30 tahun",
    "31-40 tahun",
    "41-50 tahun",
    "51-60 tahun",
)

LABEL_PENDIDIKAN = ("SD", "SMP", "SMA", "Diploma", "S1")

LABEL_SKM_SPKP = (
    "Informasi jenis pelayanan tersedia (media elektronik & non elektronik) — bintang 6",
    "Persyaratan pelayanan dipenuhi sesuai ketentuan — bintang 6",
    "Alur/prosedur pelayanan mudah diikuti — bintang 6",
    "Alur/prosedur pelayanan mudah diikuti — bintang 6 (pertanyaan ganda di form)",
    "Jangka waktu penyelesaian sesuai ketentuan — bintang 6",
    "Produk pelayanan sesuai standar & hasil yang diterima — bintang 6",
    "Tarif/biaya sesuai ketentuan — bintang 6",
    "Sarana prasarana / sistem online — bintang 6",
    "Layanan konsultasi & pengaduan mudah diakses — bintang 6",
    "Petugas/sistem merespon cepat — bintang 6",
    "Pengetahuan, keahlian, keterampilan petugas — bintang 6",
)

LABEL_SPAK = (
    "Tidak ada diskriminasi oleh pegawai — bintang 6",
    "Tidak ada kecurangan di luar prosedur — bintang 6",
    "Tidak ada permintaan imbalan di luar ketentuan — bintang 6",
    "Tidak ada pungli — bintang 6",
    "Tidak ada calo — bintang 6",
)

LABEL_EVALUASI_1 = (
    "Sebelum survei, ada pegawai yang mengarahkan jawaban 'bagus-bagus'? — Tidak"
)
LABEL_EVALUASI_2 = "Perbaikan layanan — Tidak ada yang perlu diperbaiki"


def get_brave_binary_path(custom_path: str | None) -> Path:
    candidates = []
    if custom_path:
        candidates.append(Path(custom_path))
    env_path = os.environ.get("BRAVE_PATH")
    if env_path:
        candidates.append(Path(env_path))
    candidates.extend(
        [
            Path(
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            ),
            Path(
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
            ),
        ]
    )
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Brave tidak ditemukan. Pakai --brave-path atau set environment BRAVE_PATH."
    )


def load_names(path: str) -> list[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    names = [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not names:
        raise ValueError(f"File kosong: {path}")
    return names


def pop_random_name_and_persist(names: list[str], source_path: str) -> str:
    if not names:
        raise RuntimeError(f"Nama pada file habis: {source_path}")

    selected_name = random.choice(names)
    names.remove(selected_name)

    # Simpan ulang file agar nama yang sudah dipakai tidak terpakai lagi.
    content = "\n".join(names)
    if content:
        content += "\n"
    Path(source_path).write_text(content, encoding="utf-8")
    return selected_name


def random_phone() -> str:
    prefixes = ["0811", "0812", "0813", "0821", "0822", "0823", "0851", "0852", "0853", "0814", "0815", "0816", "0855", "0856", "0857", "0858", "0817", "0818", "0819", "0859", "0877", "0878", "0895", "0896", "0897", "0898", "0899", "0881", "0882", "0883", "0884", "0885", "0886", "0887", "0888", "0889", "0831", "0832", "0833", "0838"]
    prefix = random.choice(prefixes)
    total_len = random.choice([11, 12])
    remaining = total_len - len(prefix)
    return prefix + "".join(random.choices("0123456789", k=remaining))


def setup_driver(brave_path: str | None, headless: bool) -> webdriver.Chrome:
    brave_binary = get_brave_binary_path(brave_path)
    options = Options()
    options.binary_location = str(brave_binary)
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-notifications")
    if headless:
        options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)


def click_xpath(driver: webdriver.Chrome, wait: WebDriverWait, xpath: str) -> None:
    el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    except Exception:
        driver.execute_script("arguments[0].click();", el)
    time.sleep(0.15)


def fill_input_xpath(driver: webdriver.Chrome, wait: WebDriverWait, xpath: str, value: str) -> None:
    el = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    el.clear()
    el.send_keys(value)


def wait_page_fully_loaded(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    # Pastikan komponen penting form sudah siap sebelum autofill dimulai.
    wait.until(EC.visibility_of_element_located((By.XPATH, XPATH_NAMA)))
    wait.until(EC.visibility_of_element_located((By.XPATH, XPATH_HP)))
    wait.until(EC.visibility_of_element_located((By.XPATH, XPATH_CAPTCHA_IMAGE)))
    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_EVALUASI_1)))


def select_produk_layanan(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    option = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_PRODUK_LAYANAN_OPTION_9)))
    select_el = option.find_element(By.XPATH, "./ancestor::select[1]")
    Select(select_el).select_by_index(8)


def solve_captcha_text(image_bytes: bytes) -> str:
    try:
        import ddddocr  # type: ignore[reportMissingImports]
    except ImportError as err:
        raise RuntimeError("Library ddddocr belum terpasang. Install dulu: pip install ddddocr") from err

    ocr = ddddocr.DdddOcr(show_ad=False)
    ocr_text = ocr.classification(image_bytes)
    ocr_text = re.sub(r"[^A-Za-z0-9]", "", ocr_text).strip().upper()
    if not ocr_text:
        raise RuntimeError("OCR captcha gagal: hasil kosong.")
    return ocr_text


def solve_and_fill_captcha(driver: webdriver.Chrome, wait: WebDriverWait) -> str:

    img_el = wait.until(EC.visibility_of_element_located((By.XPATH, XPATH_CAPTCHA_IMAGE)))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img_el)

    # Simpan captcha dari elemen image (langsung dari browser) ke file lokal.
    image_bytes = img_el.screenshot_as_png
    captcha_path = Path("captcha_downloaded.jpg")
    captcha_path.write_bytes(image_bytes)
    ocr_text = solve_captcha_text(image_bytes)

    fill_input_xpath(driver, wait, XPATH_CAPTCHA_INPUT, ocr_text)
    return ocr_text


def _captcha_invalid_detected(driver: webdriver.Chrome, wait: WebDriverWait) -> bool:
    # Kalau captcha input sudah tidak ada/ tidak terlihat (biasanya setelah submit sukses pindah halaman),
    # anggap tidak invalid supaya loop retry berhenti.
    try:
        input_el = driver.find_element(By.XPATH, XPATH_CAPTCHA_INPUT)
        if not input_el.is_displayed():
            return False
    except Exception:
        return False

    # Heuristik: kalau situs menandai input captcha invalid lewat aria/class atau menampilkan teks error.
    try:
        aria_invalid = (input_el.get_attribute("aria-invalid") or "").strip().lower()
        class_attr = (input_el.get_attribute("class") or "").lower()
        if aria_invalid == "true":
            return True
        if any(token in class_attr for token in ["invalid", "is-invalid", "error", "has-error"]):
            return True
    except Exception:
        # Kalau input tidak bisa dicek, lanjut cek teks error.
        pass

    # Cek teks error di sekitar widget captcha saja (bukan seluruh halaman),
    # supaya tidak false-positive karena teks lain di halaman mengandung "captcha".
    err_xpath = (
        ".//*[contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'captcha') and "
        "(contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'salah') or "
        "contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'tidak') or "
        "contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'invalid'))]"
    )
    try:
        container = input_el.find_element(By.XPATH, "./ancestor::div[contains(@class,'form') or contains(@class,'field') or contains(@class,'col')][1]")
        return len(container.find_elements(By.XPATH, err_xpath)) > 0
    except Exception:
        return False


def _wait_captcha_img_fully_decoded(driver: webdriver.Chrome, img_el) -> bool:
    """True jika <img> sudah selesai fetch/decode (bukan placeholder loading)."""
    try:
        return bool(
            driver.execute_script(
                "var e=arguments[0]; return !!(e && e.complete && e.naturalWidth > 0 "
                "&& e.naturalHeight > 0);",
                img_el,
            )
        )
    except Exception:
        return False


def _refresh_captcha(driver: webdriver.Chrome, wait: WebDriverWait, prev_png: bytes | None) -> None:
    click_xpath(driver, wait, XPATH_CAPTCHA_REFRESH)

    # Tunggu captcha baru: DOM selesai load + bitmap berbeda dari sebelum refresh.
    # Hanya membandingkan PNG bisa salah (frame transisi/spinner sudah beda bytes).
    def _fresh_captcha_ready(d):
        try:
            img_el = d.find_element(By.XPATH, XPATH_CAPTCHA_IMAGE)
            if not img_el.is_displayed():
                return False
            if not _wait_captcha_img_fully_decoded(d, img_el):
                return False
            if prev_png is None:
                return True
            return img_el.screenshot_as_png != prev_png
        except Exception:
            return False

    try:
        WebDriverWait(driver, 20).until(_fresh_captcha_ready)
    except TimeoutException:
        pass

    # Pastikan tidak ada flicker: dua screenshot berurutan identik = gambar stabil.
    stable_deadline = time.time() + 5
    while time.time() < stable_deadline:
        try:
            img_el = driver.find_element(By.XPATH, XPATH_CAPTCHA_IMAGE)
            if not _wait_captcha_img_fully_decoded(driver, img_el):
                time.sleep(0.12)
                continue
            a = img_el.screenshot_as_png
            time.sleep(0.18)
            b = driver.find_element(By.XPATH, XPATH_CAPTCHA_IMAGE).screenshot_as_png
            if a == b:
                return
        except Exception:
            pass
        time.sleep(0.12)

    # Fallback: buffer singkat agar decode selesai walau stabilitas tidak tercapai.
    time.sleep(0.35)


def submit_form(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    click_xpath(driver, wait, XPATH_SUBMIT)
    click_xpath(driver, wait, XPATH_CONFIRM_YA)


def _handle_captcha_error_popup(driver: webdriver.Chrome) -> bool:
    popup_text_xpath = (
        "//*[contains(normalize-space(.), 'Kode Verifikasi Captcha Tidak Sesuai')]"
    )
    short_wait = WebDriverWait(driver, 3)
    try:
        short_wait.until(EC.visibility_of_element_located((By.XPATH, popup_text_xpath)))
        ok_btn = short_wait.until(
            EC.element_to_be_clickable((By.XPATH, XPATH_CAPTCHA_ERROR_OK))
        )
        try:
            ok_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", ok_btn)
        time.sleep(0.2)
        return True
    except Exception:
        return False


def submit_form_with_captcha_retry(
    driver: webdriver.Chrome,
    wait: WebDriverWait,
    max_captcha_attempts: int = 5,
) -> tuple[str, int]:
    last_captcha_value = ""
    prev_png: bytes | None = None

    for attempt in range(1, max_captcha_attempts + 1):
        img_el = wait.until(EC.visibility_of_element_located((By.XPATH, XPATH_CAPTCHA_IMAGE)))
        prev_png = img_el.screenshot_as_png
        last_captcha_value = solve_and_fill_captcha(driver, wait)
        print(
            f"  [captcha] percobaan {attempt}/{max_captcha_attempts} | "
            f"OCR → isian: {last_captcha_value}"
        )

        submit_form(driver, wait)

        # Jika popup captcha gagal muncul, klik OK lalu ulang captcha.
        if not _handle_captcha_error_popup(driver):
            return last_captcha_value, attempt

        print("  [captcha] kode tidak sesuai — refresh gambar, coba lagi…")
        _refresh_captcha(driver, wait, prev_png)

    raise RuntimeError("Captcha/OCR tidak valid setelah beberapa percobaan refresh.")


def print_isian_survei_lengkap(
    *,
    nama: str,
    hp: str,
    gender_tampilan: str,
    pekerjaan: str,
    usia: str,
    pendidikan: str,
    captcha_value: str,
    captcha_percobaan_ke: int,
    max_captcha: int,
) -> None:
    print("")
    print("========== Ringkasan isian survei ==========")
    print(f"  Produk layanan: {PRODUK_LAYANAN_LOG}")
    print(f"  Nama lengkap: {nama}")
    print(f"  Nomor handphone: {hp}")
    print(f"  Jenis kelamin: {gender_tampilan}")
    print(f"  Pekerjaan: {pekerjaan}")
    print(f"  Usia: {usia}")
    print(f"  Pendidikan: {pendidikan}")
    print("  --- Penilaian SKM/SPKP (semua dipilih bintang 6) ---")
    for i, teks in enumerate(LABEL_SKM_SPKP, start=1):
        print(f"    {i:2}. {teks}")
    print("  --- Penilaian SPAK (semua dipilih bintang 6) ---")
    for i, teks in enumerate(LABEL_SPAK, start=1):
        print(f"    {i}. {teks}")
    print(f"  Evaluasi 1: {LABEL_EVALUASI_1}")
    print(f"  Evaluasi 2: {LABEL_EVALUASI_2}")
    print("  --- Verifikasi ---")
    print(f"  Captcha (OCR): {captcha_value}")
    print(
        f"  Submit captcha: berhasil pada percobaan ke-{captcha_percobaan_ke} "
        f"(maks {max_captcha})"
    )
    print("==========================================")
    print("")


def run_once(
    driver: webdriver.Chrome,
    wait: WebDriverWait,
    url: str,
    male_names: list[str],
    female_names: list[str],
    male_file_path: str,
    female_file_path: str,
) -> tuple[str, str, str, str]:
    driver.get(url)
    wait_page_fully_loaded(driver, wait)

    gender = random.choice(["laki", "perempuan"])
    if gender == "laki":
        nama = pop_random_name_and_persist(male_names, male_file_path)
        gender_xpath = XPATH_GENDER_LAKI
        gender_tampilan = "Laki-laki"
    else:
        nama = pop_random_name_and_persist(female_names, female_file_path)
        gender_xpath = XPATH_GENDER_PEREMPUAN
        gender_tampilan = "Perempuan"
    hp = random_phone()

    idx_pekerjaan = random.randrange(len(XPATH_PEKERJAAN))
    idx_usia = random.randrange(len(XPATH_USIA))
    idx_pendidikan = random.randrange(len(XPATH_PENDIDIKAN))

    select_produk_layanan(driver, wait)
    fill_input_xpath(driver, wait, XPATH_NAMA, nama)
    fill_input_xpath(driver, wait, XPATH_HP, hp)
    click_xpath(driver, wait, XPATH_PEKERJAAN[idx_pekerjaan])
    click_xpath(driver, wait, XPATH_USIA[idx_usia])
    click_xpath(driver, wait, gender_xpath)
    click_xpath(driver, wait, XPATH_PENDIDIKAN[idx_pendidikan])

    for xpath in XPATH_SKM_SPKP:
        click_xpath(driver, wait, xpath)
    for xpath in XPATH_SPAK:
        click_xpath(driver, wait, xpath)

    click_xpath(driver, wait, XPATH_EVALUASI_1)
    click_xpath(driver, wait, XPATH_EVALUASI_2)

    max_captcha = 5
    captcha_value, captcha_percobaan_ke = submit_form_with_captcha_retry(
        driver, wait, max_captcha_attempts=max_captcha
    )

    print_isian_survei_lengkap(
        nama=nama,
        hp=hp,
        gender_tampilan=gender_tampilan,
        pekerjaan=LABEL_PEKERJAAN[idx_pekerjaan],
        usia=LABEL_USIA[idx_usia],
        pendidikan=LABEL_PENDIDIKAN[idx_pendidikan],
        captcha_value=captcha_value,
        captcha_percobaan_ke=captcha_percobaan_ke,
        max_captcha=max_captcha,
    )

    return gender, nama, hp, captcha_value


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Auto isi survei di Brave mode penyamaran"
    )
    parser.add_argument("--url", default=URL_SURVEI, help="URL form survei")
    parser.add_argument("--male-file", default="nama lk.txt", help="Path file nama laki-laki")
    parser.add_argument(
        "--female-file", default="nama pr.txt", help="Path file nama perempuan"
    )
    parser.add_argument("--brave-path", help="Opsional path brave.exe")
    parser.add_argument("--headless", action="store_true", help="Jalankan tanpa UI")
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Jumlah pengisian. Default 1",
    )
    parser.add_argument(
        "--keep-open-seconds",
        type=int,
        default=0,
        help="Berapa detik browser dibiarkan terbuka per iterasi (default 0)",
    )
    parser.add_argument(
        "--max-attempts-per-repeat",
        type=int,
        default=3,
        help="Maksimal percobaan per iterasi jika gagal (default 3)",
    )
    args = parser.parse_args()

    male_names = load_names(args.male_file)
    female_names = load_names(args.female_file)

    try:
        for i in range(args.repeat):
            success = False
            for attempt in range(1, args.max_attempts_per_repeat + 1):
                driver = None
                try:
                    driver = setup_driver(args.brave_path, args.headless)
                    wait = WebDriverWait(driver, 30)
                    gender, nama, hp, captcha_value = run_once(
                        driver=driver,
                        wait=wait,
                        url=args.url,
                        male_names=male_names,
                        female_names=female_names,
                        male_file_path=args.male_file,
                        female_file_path=args.female_file,
                    )
                    print(
                        f"[{i + 1}] iterasi selesai (attempt {attempt}) | "
                        f"nama={nama} | hp={hp} | captcha={captcha_value}"
                    )
                    success = True
                finally:
                    if driver:
                        if args.keep_open_seconds > 0:
                            time.sleep(args.keep_open_seconds)
                        driver.quit()
                if success:
                    break
                print(
                    f"[{i + 1}] attempt {attempt} gagal, ulangi dengan browser baru..."
                )
            if not success:
                raise RuntimeError(
                    f"Iterasi ke-{i + 1} gagal setelah {args.max_attempts_per_repeat} percobaan."
                )
    except FileNotFoundError as err:
        print(str(err))
    except TimeoutException:
        print("Timeout saat menunggu elemen form. Cek koneksi atau XPath.")
    except RuntimeError as err:
        print(str(err))
    except WebDriverException as err:
        print(f"Gagal menjalankan Selenium/Brave: {err}")


if __name__ == "__main__":
    main()

