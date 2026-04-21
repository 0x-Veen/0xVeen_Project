# Tool crawler.py
import os
import subprocess
import shutil
from core.utils.logger import print_info, print_success, print_error

def run(output_dir):
    print_info("🔍 Starting web crawling using Katana...")

    input_file = os.path.join(output_dir, "live_hosts_only.txt")
    katana_dir = os.path.join(output_dir, "katana")
    os.makedirs(katana_dir, exist_ok=True)

    katana_output_file = os.path.join(katana_dir, "katana_urls.txt")
    js_links_file = os.path.join(katana_dir, "js_files.txt")
    sensitive_files_file = os.path.join(katana_dir, "sensitive_files.txt")

    # تعريف المجموعات قبل أي شيء
    all_urls = set()
    js_links = set()
    sensitive_links = set()

    if not os.path.isfile(input_file):
        print_error("❌ live.txt not found. Please run httpx first.")
        return

    if not shutil.which("katana"):
        print_error("❌ Katana is not installed or not in PATH.")
        return

    sensitive_exts = [".js", ".env", ".log", ".json", ".conf", ".xml",
                      ".zip", ".tar.gz", ".rar", ".bak", ".old", ".sql"]

    with open(input_file, "r") as infile:
        live_domains = [line.strip() for line in infile if line.strip()]

    for domain in live_domains:
        print_info(f"🌐 Crawling: {domain}")
        try:
            result = subprocess.run(
                ["katana", "-u", domain, "-silent"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )
            output = result.stdout.strip()
            if not output:
                print_info(f"⚠️ No results from Katana for: {domain}")
                continue

            for url in output.splitlines():
                url = url.strip().lower()
                all_urls.add(url)
                for ext in sensitive_exts:
                    if url.endswith(ext):
                        if ext == ".js":
                            js_links.add(url)
                        else:
                            sensitive_links.add(url)

        except subprocess.TimeoutExpired:
            print_error(f"⏱️ Timeout while crawling {domain}")
        except Exception as e:
            print_error(f"❌ Error running Katana on {domain}: {str(e)}")

    # Write results if any
    def save(path, data, label):
        if data:
            with open(path, "w") as f:
                f.write("\n".join(sorted(data)) + "\n")
            print_success(f"✅ {label} saved to: {path}")
        else:
            print_info(f"ℹ️ No {label} found.")

    save(katana_output_file, all_urls, "All URLs")
    save(js_links_file, js_links, "JS files")
    save(sensitive_files_file, sensitive_links, "Sensitive files")

    print_success("🎯 Katana crawling completed.")
