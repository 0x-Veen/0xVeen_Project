#!/usr/bin/env python3
import os
import re
import shutil
import subprocess

def tool_exists(name):
    return shutil.which(name) is not None

def run_cmd(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
    except:
        return ""

def clean_subdomain(line, domain):
    line = line.strip().lower()
    line = re.sub(r'^https?://', '', line)  # remove protocol
    line = line.split('/')[0]                # remove path
    line = line.split(':')[0]                # remove port
    if line.startswith('*.'):
        line = line[2:]
    if line.endswith('.'):
        line = line[:-1]
    if line == domain or line.endswith('.' + domain):
        return line
    return None

def run(domain, output_dir):
    print(f"[+] Starting subdomain enumeration for {domain}...")
    os.makedirs(output_dir, exist_ok=True)
    results = set()

    # Run each tool if installed
    if tool_exists("subfinder"):
        print("[+] Running subfinder...")
        out = run_cmd(f"subfinder -d {domain} -silent")
        for line in out.splitlines():
            sub = clean_subdomain(line, domain)
            if sub:
                results.add(sub)

    if tool_exists("assetfinder"):
        print("[+] Running assetfinder...")
        out = run_cmd(f"assetfinder --subs-only {domain}")
        for line in out.splitlines():
            sub = clean_subdomain(line, domain)
            if sub:
                results.add(sub)

    if tool_exists("amass"):
        print("[+] Running amass...")
        out = run_cmd(f"amass enum -passive -norecursive -d {domain}")
        for line in out.splitlines():
            sub = clean_subdomain(line, domain)
            if sub:
                results.add(sub)

    if tool_exists("findomain"):
        print("[+] Running findomain...")
        out = run_cmd(f"findomain -t {domain} -q")
        for line in out.splitlines():
            sub = clean_subdomain(line, domain)
            if sub:
                results.add(sub)

    # crt.sh (if curl + jq available)
    if tool_exists("curl") and tool_exists("jq"):
        print("[+] Fetching crt.sh subdomains...")
        out = run_cmd(f'curl -s https://crt.sh/?q=%25.{domain}&output=json | jq -r ".[].name_value"')
        for line in out.splitlines():
            for subline in line.split('\n'):
                sub = clean_subdomain(subline, domain)
                if sub:
                    results.add(sub)

    # Write final sorted results
    sub_file = os.path.join(output_dir, "subdomains.txt")
    if results:
        with open(sub_file, "w") as f:
            for sub in sorted(results):
                f.write(sub + "\n")
        print(f"[✓] Found {len(results)} unique subdomains. Saved to {sub_file}")
    else:
        print("[-] No subdomains found.")
