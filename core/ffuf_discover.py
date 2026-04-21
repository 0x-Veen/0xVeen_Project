import os
import subprocess
import json
from datetime import datetime
from core.utils.logger import print_info, print_success, print_error

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def run(live_domains_file, output_dir, wordlist=""):
    print(f"\n{YELLOW}{'═' * 60}")
    print(f"{CYAN}🚀 Starting FFUF Fuzzing Phase...{RESET}")
    print(f"{YELLOW}{'═' * 60}{RESET}\n")

    default_wordlist = os.path.join("wordlists", "common.txt")
    wordlist_paths = [wl.strip() for wl in wordlist.split(",") if wl.strip()] if wordlist.strip() else [default_wordlist]

    output_ffuf_dir = os.path.join(output_dir, "ffuf_results")
    os.makedirs(output_ffuf_dir, exist_ok=True)

    log_file = os.path.join(output_ffuf_dir, "all_ffuf_results.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        pass

    if not os.path.exists(live_domains_file):
        print_error(f"❌ live domains input not found: {live_domains_file}")
        return

    with open(live_domains_file, "r", encoding="utf-8") as f:
        targets = [line.strip().replace("https://", "").replace("http://", "") for line in f if line.strip()]

    for domain in targets:
        domain = domain.replace("https://", "").replace("http://", "").strip("/")

        for wl in wordlist_paths:
            wl_name = os.path.basename(wl)
            url = f"https://{domain}/FUZZ"
            domain_output = os.path.join(output_ffuf_dir, f"{domain}__{wl_name}.json")

            command = [
                "ffuf",
                "-u", url,
                "-w", wl,
                "-t", "50",
                "-mc", "200,204",
                "-o", domain_output,
                "-of", "json",
                "-timeout", "10"
            ]

            try:
                print_info(f"🚀 Fuzzing {domain} with wordlist: {wl_name} ...")
                subprocess.run(command, capture_output=True, text=True)

                if os.path.exists(domain_output) and os.path.getsize(domain_output) > 0:
                    with open(domain_output, "r", encoding="utf-8") as jf:
                        data = json.load(jf)
                        results = data.get("results", [])
                        if results:
                            print(f"\n{CYAN}{'═' * 60}\n📍 Results for {domain} ({wl_name}):{RESET}")
                            with open(log_file, "a", encoding="utf-8") as log:
                                log.write("\n" + "═" * 60 + f"\n📍 Results for {domain} ({wl_name}):\n" + "═" * 60 + "\n")
                                for r in results:
                                    status = r.get("status")
                                    path = r.get("input", {}).get("FUZZ")
                                    full_url = url.replace("FUZZ", path)
                                    redirect = r.get("redirectlocation")
                                    arrow = f" (➡ {redirect})" if redirect else ""

                                    color = GREEN if str(status).startswith("2") else YELLOW if str(status).startswith("3") else RED

                                    print(f"  {color}[{status}]{RESET} /{path} → {full_url}{arrow}")
                                    log.write(f"  [{status}] /{path} → {full_url}{arrow}\n")
                else:
                    print_info(f"🔸 No results for {domain} with {wl_name}")

            except Exception as e:
                with open(log_file, "a", encoding="utf-8") as log:
                    log.write(f"[!] Error for {domain} with {wl_name}: {str(e)}\n")
                print_error(f"❌ Error with {domain} & {wl_name}: {str(e)}")
