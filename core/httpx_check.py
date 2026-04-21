import os
import subprocess
from core.utils.logger import print_info, print_success, print_error

def run(subdomains_file, output_dir):
    print_info("🌐 Probing for live hosts using httpx...")

    live_hosts_file = os.path.join(output_dir, "live_hosts.txt")
    live_hosts_only_file = os.path.join(output_dir, "live_hosts_only.txt")
    live_txt = os.path.join(output_dir, "live.txt")

    if not os.path.exists(subdomains_file):
        print_error(f"❌ Subdomains file not found: {subdomains_file}")
        return

    try:
        cmd = [
            "httpx",
            "-l", subdomains_file,
            "-silent",
            "-status-code",
            "-title",
            "-tech-detect",
            "-ip",
            "-no-color",
            "-timeout", "10",
            "-threads", "50"
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        output = result.stdout

        if not output:
            print_error("❌ No live hosts found.")
            return

        urls = []
        urls_200 = []

        for line in output.splitlines():
            if line.startswith("http://") or line.startswith("https://"):
                parts = line.split()
                url = parts[0]
                urls.append(url)

                if any("[200" in part for part in parts):
                    urls_200.append(url)

        # Remove duplicates and sort
        urls_200 = sorted(set(urls_200))
        urls = sorted(set(urls))

        # Save URLs with status 200
        with open(live_hosts_only_file, "w") as f:
            for url in urls_200:
                f.write(url + "\n")

        # Save all live URLs
        with open(live_txt, "w") as f:
            for url in urls:
                f.write(url + "\n")

        # Save full output
        with open(live_hosts_file, "w") as f:
            f.write(output)

        print_success(f"✅ Full live host info saved to: {live_hosts_file}")
        print_success(f"✅ Live URLs for FFUF saved to: {live_hosts_only_file} (only 200s)")
        print_success(f"✅ live.txt saved for other modules: {live_txt}")

    except Exception as e:
        print_error(f"❌ Error running httpx: {e}")
