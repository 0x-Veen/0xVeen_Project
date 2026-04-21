#T ool  js_analyser.py
import os
import subprocess
import requests
from core.utils.logger import print_info, print_success, print_warn, print_error

def run(js_files_list, output_dir):
    print_info("🧠 Starting JavaScript Analysis...")

    secretfinder_path = "tools/SecretFinder/SecretFinder.py"  # adjust per your environment
    linkfinder_path = "tools/LinkFinder/linkfinder.py"      # adjust per your environment

    if not os.path.isfile(js_files_list):
        print_warn(f"⚠️ JS files list not found: {js_files_list}")
        return

    with open(js_files_list, "r", encoding="utf-8") as f:
        js_urls = [line.strip() for line in f if line.strip() and line.startswith("http")]

    if not js_urls:
        print_warn("⚠️ No JavaScript URLs found in the list.")
        return

    js_output_dir = os.path.join(output_dir, "js_analysis")
    os.makedirs(js_output_dir, exist_ok=True)

    secrets_output = os.path.join(js_output_dir, "js_secrets.txt")
    links_output = os.path.join(js_output_dir, "js_endpoints.txt")
    raw_js_output = os.path.join(output_dir, "scripts_raw.txt")

    analyzed = 0
    downloaded = 0

    with open(secrets_output, "w", encoding="utf-8") as s_out, open(links_output, "w", encoding="utf-8") as l_out, open(raw_js_output, "w", encoding="utf-8") as raw_out:
        for url in js_urls:
            print_info(f"🔎 Analyzing: {url}")
            analyzed += 1

            s_out.write(f"\n--- Secrets in {url} ---\n")
            try:
                subprocess.run(
                    ["python3", secretfinder_path, "-i", url, "-o", "cli"],
                    stdout=s_out, stderr=subprocess.DEVNULL, timeout=30
                )
            except subprocess.TimeoutExpired:
                print_warn(f"⏱️ SecretFinder timed out for: {url}")
                s_out.write("[!] SecretFinder timeout.\n")
            except Exception as e:
                print_error(f"❌ SecretFinder failed on {url}: {str(e)}")
                s_out.write(f"[!] SecretFinder error: {str(e)}\n")

            l_out.write(f"\n--- Endpoints in {url} ---\n")
            try:
                subprocess.run(
                    ["python3", linkfinder_path, "-i", url, "-o", "cli"],
                    stdout=l_out, stderr=subprocess.DEVNULL, timeout=30
                )
            except subprocess.TimeoutExpired:
                print_warn(f"⏱️ LinkFinder timed out for: {url}")
                l_out.write("[!] LinkFinder timeout.\n")
            except Exception as e:
                print_error(f"❌ LinkFinder failed on {url}: {str(e)}")
                l_out.write(f"[!] LinkFinder error: {str(e)}\n")

            try:
                resp = requests.get(url, timeout=15)
                if resp.status_code == 200 and resp.text.strip():
                    raw_out.write(f"\n--- Content from {url} ---\n")
                    raw_out.write(resp.text + "\n")
                    downloaded += 1
                else:
                    print_warn(f"⚠️ Empty or bad response from: {url}")
            except Exception as e:
                print_warn(f"⚠️ Failed to download {url}: {str(e)}")

    print_success(f"✅ Analyzed {analyzed} JS files.")
    print_success(f"📄 JS secrets saved to: {secrets_output}")
    print_success(f"📄 JS endpoints saved to: {links_output}")
    print_success(f"📄 Raw JS content saved to: {raw_js_output}")
    print_success(f"⬇️ Successfully downloaded {downloaded} JS files.")
