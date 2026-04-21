#!/usr/bin/env python3
import os
import argparse
from core.utils.banner import print_banner
from core.utils.logger import print_info, print_success, print_error

# import modules
from core import subdomain_enum, httpx_check, ffuf_discover, crawler, js_analyzer, secrets_finder

def create_output_dir(domain, base_dir="output"):
    path = os.path.join(base_dir, domain)
    os.makedirs(path, exist_ok=True)
    return path

def safe_run(name, func, *args):
    print_info(f"➡️ Running: {name}")
    try:
        return func(*args)
    except Exception as e:
        print_error(f"❌ Error in {name}: {e}")
        return None

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="0xVeen — Mini Recon Framework (student project)")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g. example.com)")
    parser.add_argument("--start", help="Start stage (subdomain,httpx,ffuf,crawl,js,secrets)")
    parser.add_argument("--only", help="Run only one specific stage")
    parser.add_argument("--stop", help="Stop after a certain stage")
    parser.add_argument("-o", "--output", default="output", help="Output base directory")
    args = parser.parse_args()

    domain = args.domain
    output_dir = create_output_dir(domain, base_dir=args.output)
    print_info(f"🎯 Target: {domain}")
    print_info(f"📁 Output: {output_dir}")

    stages = [
        ("subdomain", subdomain_enum.run, (domain, output_dir)),
        ("httpx", httpx_check.run, (os.path.join(output_dir, "subdomains.txt"), output_dir)),
        ("ffuf", ffuf_discover.run, (os.path.join(output_dir, "live.txt"), output_dir, "")),
        ("crawl", crawler.run, (output_dir,)),
        ("js", js_analyzer.run, (os.path.join(output_dir, "katana", "js_files.txt"), output_dir)),
        ("secrets", secrets_finder.run, (output_dir,))
    ]

    # Only one stage requested
    if args.only:
        target = args.only.lower()
        for name, func, params in stages:
            if name == target:
                print_info(f"⚙️ Running only stage: {name}")
                safe_run(name, func, *params)
                print_success(f"✅ Stage {name} completed.")
                return
        print_error(f"❌ Unknown stage: {args.only}")
        return

    # compute start/stop indices
    start_idx = 0
    stop_idx = len(stages)
    if args.start:
        for i, (name, _, _) in enumerate(stages):
            if name == args.start.lower():
                start_idx = i
                break
    if args.stop:
        for i, (name, _, _) in enumerate(stages):
            if name == args.stop.lower():
                stop_idx = i + 1
                break

    # run stages in order
    for name, func, params in stages[start_idx:stop_idx]:
        print_info("\n" + "="*60)
        print_info(f"🧩 Stage: {name}")
        print_info("="*60)
        safe_run(name, func, *params)
        print_success(f"✅ Completed stage: {name}")

    print_success("\n🎉 Recon completed successfully!")

if __name__ == '__main__':
    main()
