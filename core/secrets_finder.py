# Tool secrets_finder.py
import os
import re
from core.utils.logger import print_info, print_success, print_warn

def run(output_dir):
    print_info("🔍 Starting secrets finding...")

    input_files = [
        os.path.join(output_dir, "katana", "katana_urls.txt"),
        os.path.join(output_dir, "js_analysis", "js_endpoints.txt"),
        os.path.join(output_dir, "js_analysis", "js_secrets.txt"),
        os.path.join(output_dir, "scripts_raw.txt"),
    ]


    # Clean, well-formed regex patterns dictionary
    regex_patterns = {
        "AWS Access Key": r"AKIA[0-9A-Z]{16}",
        "AWS Secret Key": r"(?i)aws(.{0,20})?(secret|key)['\"=:\s]{1,5}[0-9a-zA-Z/+=]{40}",
        "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
        "Generic API Key": r"(?i)(api_key|apikey|api-key)['\"=:\s]{1,5}[0-9A-Za-z]{16,45}",
        "Bearer Token": r"(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*",
        "Authorization": r"(?i)(authorization)['\"=:\s]{1,5}[A-Za-z0-9\-._~+/]+=*",
        "Email": r"[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-.]+",
        "Password": r"(?i)(pass|password)['\"=:\s]{1,5}[^\s]{4,50}",
        "Private Key": r"-----BEGIN (RSA|DSA|EC|PGP) PRIVATE KEY-----",
        "JWT": r"eyJ[A-Za-z0-9\-_=]+?\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_.+/=]*"
    }

    findings = []

    for full_path in input_files:
        if not os.path.isfile(full_path):
            print_warn(f"⚠️ {full_path} not found, skipping...")
            continue

        with open(full_path, "r", errors="ignore", encoding="utf-8") as f:
            content = f.read()

        for label, pattern in regex_patterns.items():
            matches = re.findall(pattern, content)
            for match in matches:
                # if regex has groups, match may be a tuple; normalize it
                if isinstance(match, tuple):
                    match_str = "".join([m for m in match if m])
                else:
                    match_str = str(match)
                findings.append((label, match_str.strip(), full_path))

    if not findings:
        print_warn("❌ No secrets found.")
    else:
        output_file = os.path.join(output_dir, "found_secrets.txt")
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(f"🗂️ Total secrets found: {len(findings)}\n\n")
            for label, secret, source in sorted(findings):
                out.write(f"[{label}] {secret}  (from {source})\n")
        print_success(f"✅ Found {len(findings)} secrets.")
        print_success(f"📄 Secrets saved to: {output_file}")
