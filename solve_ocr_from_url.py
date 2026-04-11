import argparse
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import ddddocr
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


DEFAULT_PAGE_URL = "https://star-survei3a.kemenimipas.go.id/ly/ASCG83Kb"
DEFAULT_XPATH = (
    "/html/body/div[1]/div[1]/div/form/div[1]/div/div/div/div[31]/div/div/div/"
    "div/div/div/div[1]/div/img"
)


def get_brave_binary_path(custom_path: str | None) -> Path:
    """Get Brave browser binary path on Windows."""
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
        "Brave tidak ditemukan. Gunakan --brave-path atau set BRAVE_PATH."
    )


def fetch_captcha_url_from_page(
    page_url: str, xpath: str, brave_path: str | None, headless: bool
) -> str:
    """Open page in Brave incognito, read captcha image URL from XPath."""
    brave_binary = get_brave_binary_path(brave_path)

    options = Options()
    options.binary_location = str(brave_binary)
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-notifications")
    if headless:
        options.add_argument("--headless=new")

    # Let Selenium Manager resolve a compatible driver automatically.
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(page_url)
        wait = WebDriverWait(driver, 20)
        image = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        src = image.get_attribute("src")
        if not src:
            raise RuntimeError("Elemen gambar ditemukan, tapi atribut src kosong.")
        return urljoin(page_url, src)
    finally:
        driver.quit()


def download_image(url: str, referer: str) -> bytes:
    """Download image bytes from URL."""
    req = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": referer,
        },
    )
    with urlopen(req, timeout=20) as response:
        return response.read()


def solve_captcha_from_bytes(ocr: ddddocr.DdddOcr, image_bytes: bytes) -> str:
    """Run OCR and normalize result to uppercase."""
    result = ocr.classification(image_bytes)
    return result.strip().upper()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Open Brave incognito, grab captcha URL by XPath, then OCR"
    )
    parser.add_argument(
        "--page-url",
        default=DEFAULT_PAGE_URL,
        help="URL halaman yang berisi captcha",
    )
    parser.add_argument(
        "--xpath",
        default=DEFAULT_XPATH,
        help="Full XPath elemen gambar captcha",
    )
    parser.add_argument(
        "--save",
        default="captcha_downloaded.jpg",
        help="Simpan file hasil download ke path ini (default: captcha_downloaded.jpg)",
    )
    parser.add_argument(
        "--brave-path",
        help="Opsional: path brave.exe",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Jalankan browser tanpa tampilan UI",
    )
    args = parser.parse_args()

    try:
        image_url = fetch_captcha_url_from_page(
            page_url=args.page_url,
            xpath=args.xpath,
            brave_path=args.brave_path,
            headless=args.headless,
        )
    except FileNotFoundError as err:
        print(str(err))
        return
    except TimeoutException:
        print("Timeout: elemen captcha tidak ditemukan pada XPath yang diberikan.")
        return
    except WebDriverException as err:
        print(f"Gagal menjalankan Selenium/Brave: {err}")
        return

    try:
        image_bytes = download_image(image_url, referer=args.page_url)
    except HTTPError as err:
        print(f"Gagal download captcha (HTTP {err.code}): {image_url}")
        return
    except URLError as err:
        print(f"Gagal download URL: {err.reason}")
        return

    save_path = Path(args.save)
    save_path.write_bytes(image_bytes)

    ocr = ddddocr.DdddOcr(show_ad=False)
    text = solve_captcha_from_bytes(ocr, image_bytes)
    print(f"Halaman: {args.page_url}")
    print(f"Captcha URL: {image_url}")
    print(f"File: {save_path}")
    print(f"Hasil OCR: {text}")


if __name__ == "__main__":
    main()
