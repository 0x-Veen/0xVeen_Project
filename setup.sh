#!/usr/bin/env bash
set -e

echo "[*] Updating packages..."
sudo apt update

echo "[*] Installing base dependencies..."
sudo apt install -y python3 python3-venv python3-pip golang-go curl wget unzip

echo "[*] Ensuring Go bin is in PATH..."
if ! grep -q 'export PATH=$PATH:$HOME/go/bin' "$HOME/.bashrc"; then
  echo 'export PATH=$PATH:$HOME/go/bin' >> "$HOME/.bashrc"
fi
export PATH="$PATH:$HOME/go/bin"

echo "[*] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[*] Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[*] Installing Go-based tools..."
go install github.com/ffuf/ffuf/v2@latest
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/tomnomnom/assetfinder@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

echo "[*] Installing Amass..."
# جرّب من apt أولًا، ولو عندك طريقة تانية ثابتة في بيئتك استخدمها
if command -v amass >/dev/null 2>&1; then
  echo "[+] amass already installed"
else
  sudo apt install -y amass || true
fi

echo "[*] Installing Findomain binary..."
TMP_DIR="$(mktemp -d)"
cd "$TMP_DIR"

# هات آخر إصدار لينكس x86_64 لو جهازك المعتاد كده
wget -O findomain-linux.zip https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux.zip
unzip findomain-linux.zip
chmod +x findomain
sudo mv findomain /usr/local/bin/findomain

cd -
rm -rf "$TMP_DIR"

echo "[*] Verifying installations..."
for tool in ffuf subfinder assetfinder katana httpx findomain; do
  if command -v "$tool" >/dev/null 2>&1; then
    echo "[+] $tool installed"
  else
    echo "[-] $tool NOT found"
  fi
done

if command -v amass >/dev/null 2>&1; then
  echo "[+] amass installed"
else
  echo "[-] amass NOT found"
fi

echo
echo "[*] Done. Activate env with:"
echo "source venv/bin/activate"
