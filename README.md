# 0xVeen — Recon Framework

## Overview

0xVeen is a recon framework for gathering information on a domain. It uses multiple tools integrated via `0xveen.py`.

---

## ⚙️ Setup & Installation

Follow these steps to run the tool properly:

```bash
# 1) Clone the repository
git clone https://github.com/0x-Veen/0xVeen_Project.git

# 2) Move into the project folder
cd 0xVeen_Project

# 3) Create virtual environment
python3 -m venv venv

# 4) Activate virtual environment
source venv/bin/activate

# 5) Install Python requirements
pip install -r requirements.txt

# 6) Give permission & run setup script
chmod +x setup.sh
./setup.sh
```

---

## 🧰 Included Tools

* **Subdomain Enumeration** (`subdomain_enum.py`) — collects subdomains.
* **HTTPX Check** (`httpx_check.py`) — checks live hosts.
* **FFUF** (`ffuf_discover.py`) — fuzzing for hidden paths.
* **Crawler** (`crawler.py`) — collects URLs and JS files.
* **JS Analyzer** (`js_analyzer.py`) — analyzes JS with SecretFinder and LinkFinder.
* **Secrets Finder** (`secrets_finder.py`) — searches for keys, tokens, passwords.

---

## 📦 Requirements

### 🐍 Python

* Python 3.8+

### 🔧 External Tools

* subfinder
* assetfinder
* amass
* findomain
* httpx
* ffuf
* katana
* SecretFinder
* LinkFinder

### 📚 Python Libraries

* requests

---

## 🚀 Usage

```bash
python3 0xveen.py -d example.com                # Run all stages
python3 0xveen.py -d example.com --only ffuf    # Run only FFUF stage
python3 0xveen.py -d example.com --start httpx  # Start from HTTPX
python3 0xveen.py -d example.com --stop ffuf    # Stop at FFUF
python3 0xveen.py -d example.com -o ./output    # Custom output folder
```

---

## 📂 Output

* `subdomains.txt` — found subdomains
* `live.txt` — live URLs
* `ffuf_results/` — FFUF JSON results
* `katana/js_files.txt` — JS files
* `found_secrets.txt` — discovered secrets

---

## ⚠️ Disclaimer

Use only on domains you own or have permission to test.

---

## ⭐ Project

# 0xVeen_Project
