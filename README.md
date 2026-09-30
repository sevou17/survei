# Auto Survei STAR (Kemenimipas)

A Python automation script for automatically filling out **STAR survey forms** from the Indonesian Ministry of Immigration and Corrections (**Kemenimipas**) using **Selenium** and the **Brave Browser** in private/incognito mode.

The script can generate survey data, solve CAPTCHA challenges using **ddddocr**, and submit the form automatically.

> **Example website:** `star-survei3a.kemenimipas.go.id`

## ✨ Features

* 🌐 Automated form filling using Selenium
* 🦁 Supports Brave Browser
* 🕵️ Runs in private/incognito mode
* 🔤 CAPTCHA recognition using `ddddocr`
* 👤 Automatically selects names from male/female name lists
* 🗑️ Removes used names from the source file
* 🔁 Supports multiple consecutive submissions
* 👻 Optional headless browser mode
* ⏱️ Configurable browser open duration after each submission
* ⚙️ Configurable survey URL and file paths through command-line arguments

## 📋 Requirements

* **Python 3.10+** (recommended)
* **Brave Browser** installed
* A compatible **ChromeDriver** for the Chromium version used by Brave
* Internet connection

> Selenium 4 can automatically manage the appropriate driver in many configurations. If automatic driver management does not work, install a compatible ChromeDriver manually.

## 📦 Installation

Install the required Python packages:

```bash
pip install selenium ddddocr
```

## 📁 Project Structure

| File                    | Description                                                                                       |
| ----------------------- | ------------------------------------------------------------------------------------------------- |
| `auto_survei.py`        | Main automation script: opens the survey, fills in data, solves the CAPTCHA, and submits the form |
| `nama lk.txt`           | List of male names                                                                                |
| `nama pr.txt`           | List of female names                                                                              |
| `solve_ocr_from_url.py` | Optional utility for testing CAPTCHA OCR directly from the survey page                            |

## 🚀 Usage

Run the main script:

```bash
python auto_survei.py
```

### Command-Line Options

| Option                  | Description                                                |
| ----------------------- | ---------------------------------------------------------- |
| `--url`                 | Survey form URL                                            |
| `--male-file`           | Path to the male name list                                 |
| `--female-file`         | Path to the female name list                               |
| `--brave-path`          | Path to `brave.exe` if it is not detected automatically    |
| `--headless`            | Run the browser without displaying a window                |
| `--repeat N`            | Number of consecutive submissions                          |
| `--keep-open-seconds N` | Keep the browser open for `N` seconds after each iteration |

### Example

```bash
python auto_survei.py --repeat 5
```

Run in headless mode:

```bash
python auto_survei.py --headless --repeat 10
```

Specify a custom Brave executable:

```bash
python auto_survei.py --brave-path "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
```

You can also set the Brave executable path using the `BRAVE_PATH` environment variable.

## 🔧 Configuration

If Brave is not detected automatically, provide its executable path manually:

```bash
python auto_survei.py --brave-path "C:\Path\To\brave.exe"
```

Alternatively, set the environment variable:

```cmd
set BRAVE_PATH=C:\Path\To\brave.exe
```

## 🧩 How It Works

The general workflow is:

```text
Start
  │
  ▼
Open Survey Form
  │
  ▼
Generate / Select Survey Data
  │
  ▼
Fill Form
  │
  ▼
Capture CAPTCHA
  │
  ▼
OCR with ddddocr
  │
  ▼
Submit Form
  │
  ▼
Repeat (optional)
  │
  ▼
End
```

## ⚠️ Important Notes

* The survey website's **XPath selectors and HTML structure may change at any time**. If the website is updated, the automation script may need to be modified.
* CAPTCHA recognition using OCR is not guaranteed to work for every CAPTCHA variation.
* Make sure you have the necessary **authorization to automate submissions** to the target website.
* Automated submissions may violate the website's terms of service or survey policies.
* Use this project responsibly and avoid submitting false, misleading, or unauthorized survey responses.

## 🔐 Responsible Use

This project is intended for **authorized automation, testing, and educational purposes**.

Do not use it to:

* Submit fraudulent or misleading survey responses
* Flood or overload the survey service
* Circumvent access restrictions
* Automate submissions without permission

Always respect the website's terms of service and applicable policies.

## 🛠️ Technologies

* **Python**
* **Selenium**
* **Brave Browser**
* **ddddocr**
* **ChromeDriver / Chromium WebDriver**

## 📄 License

Add your preferred license here, for example:

```text
MIT License
```

If you intend to publish this project publicly on GitHub, choose a license that matches how you want others to use, modify, and distribute the code.
