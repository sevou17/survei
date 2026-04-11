import argparse
from pathlib import Path

import ddddocr


def solve_captcha(ocr: ddddocr.DdddOcr, image_path: Path) -> str:
    """Read captcha image and return predicted text."""
    if not image_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {image_path}")

    image_bytes = image_path.read_bytes()
    result = ocr.classification(image_bytes)
    return result.strip().upper()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="OCR captcha image(s) -> text menggunakan ddddocr"
    )
    parser.add_argument(
        "images",
        nargs="*",
        help="Path gambar captcha. Jika kosong, proses semua *.jpg di folder ini.",
    )
    args = parser.parse_args()

    if args.images:
        image_paths = [Path(image) for image in args.images]
    else:
        image_paths = sorted(Path(".").glob("*.jpg"))

    if not image_paths:
        print("Tidak ada file .jpg yang ditemukan.")
        return

    ocr = ddddocr.DdddOcr(show_ad=False)
    for image_path in image_paths:
        text = solve_captcha(ocr, image_path)
        print(f"{image_path.name}: {text}")


if __name__ == "__main__":
    main()
