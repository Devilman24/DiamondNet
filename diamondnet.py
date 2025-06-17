import argparse
import asyncio
import httpx
import time

def print_banner():
    banner = r"""
 _________________________________________________________
|\=========================================================\
||                                                         |
||        _        __        ___        __        _        |
||       ; `-.__.-'. `-.__.-'. .`-.__.-' .`-.__.-' :       |
||     _.'. . . . . . . . .,,,,,,,. . . . . . . . .`._     |
||   .'. . . . . . . . ,a@@@@@@@@@@@a, . . . . . . . .`.   |
||   `. . . . ,a@@@@@a@@@a@@@@@@@@@a@@@a@@@@@a, . . . ,'   |
||     ) . . a@@@@@@a@@@@@a@@@@@@@a@@@@@a@@@@@@a . . (     |
||   ,' . . .@@@%%%a@@@@@@@@@@@@@@@@@@@@@a%%%@@@  . . `.   |
||   `.. . . @@@%%a@@@@@@""@@@@@@@""@@@@@@a%%@@@ . . .,'   |
||     ). . . "@@a@@@@@@@@@SSSSSSS@@@@@@@@@a@@" . . .(     |
||   ,'. . . . . `@@@@@@@@SSS, ,SSS@@@@@@@@' . . . . .`.   |
||   `. . . . . . `@@@@@@@`SSS:SSS'@@@@@@@' . . . . . ,'   |
||     ) . . . . . `@@@@@@@sssssss@@@@@@@' . . . . . (     |
||   ,' . . . . . ,a@@a@@@@@@@@@@@@@@@a@@a, . . . . . `.   |
||   `.. . . . .a@@@a@@@@@a@@@a@@@a@@@@@a@@@a. . . . .,'   |
||     ). . . .a@@@@@a@@@@@@@@@@@@@@@@@a@@@@@a. . . .(     |
||   ,'. . . . @@@@@@a@@@@'   "   `@@@@a@@@@@@ . . . .`.   |
||   `. . . . .@@@@@@@aaaa,       ,aaaa@@@@@@@  . . . ,'   |
||     ) . . . `@@@@@@@@@@@@a, ,a@@@@@@@@@@@@' . . . (     |
||   ,' . . . . .`@@@@@@@@@@a@a@a@@@@@@@@@@'. . . . . `.   |
||   `;;;;;;;;;;;;aaaaaaaaaa@@@@@aaaaaaaaaa;;;;;;;;;;;;'   |
||     );;;;;;;,mMMMMMMMm@@@@@@@@@@@mMMMMMMMm,;;;;;;;(     |
||   ,;;;;;;;;a@%#%%#%%#%Mm@@@@@@@mM%#%%#%%#%@a;;;;;;;;,   |
||   `;;;;;;;;@@%%%%%%%%%%M@@";"@@M%%%%%%%%%%@@;;;;;;;;'   |
||     );;;;;;`@a%%%%%%%%mM";;;;;"Mm%%%%%%%%a@';;;;;;(     |
||   ,;;;;;;;;;;"@@@@@@@@";;;;;;;;;"@@@@@@@@";;;;;;;;;;,   |
||   `;;;;;;;;;;;;"""""";;;;;;;;;;;;;"""""";;;;;;;;;;;;'   |
||     );;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;Devilman24(     |
||     `:;;;:-~~~-:;;:-~~~-:;;;;;:-~~~-:;;:,-~~~-:;;;:'    |
||       ~~~       ~~        ~~~        ~~        ~~~      |
||                     .=============.                     |
||                     |   Mr. Bill  :                     |
||                     `-------------'                     |
\|_________________________________________________________|
"""
    print(banner)

async def check_path(session, directory, base_url, timeout, codes_to_check, progress, semaphore):
    url = f"{base_url.rstrip('/')}/{directory.lstrip('/')}"
    async with semaphore:
        try:
            start = time.time()
            response = await session.get(url, timeout=timeout)
            elapsed = time.time() - start
            status = response.status_code
            if status in codes_to_check:
                result = f"[FOUND {status}]"
            else:
                result = f"[IGNORED {status}]"
        except httpx.RequestError:
            elapsed = 0
            result = "[ERROR]"

        await print_progress(progress, result, url, elapsed)

async def check_subdomain(session, subdomain, base_domain, protocol, timeout, codes_to_check, progress, semaphore):
    url = f"{protocol}://{subdomain}.{base_domain}"
    async with semaphore:
        try:
            start = time.time()
            response = await session.get(url, timeout=timeout)
            elapsed = time.time() - start
            status = response.status_code
            if status in codes_to_check:
                result = f"[FOUND {status}]"
            else:
                result = f"[IGNORED {status}]"
        except httpx.RequestError:
            elapsed = 0
            result = "[ERROR]"

        await print_progress(progress, result, url, elapsed)

async def print_progress(progress, result, url, elapsed):
    async with progress["lock"]:
        progress["count"] += 1
        progress["total_time"] += elapsed
        completed = progress["count"]
        total = progress["total"]
        avg_time = progress["total_time"] / completed if completed > 0 else 0
        percent = (completed / total) * 100
        remaining_time = avg_time * (total - completed)

        line = (f"{result} {url} | Progress: {completed}/{total} "
                f"({percent:.1f}%) | Avg: {avg_time:.2f}s | "
                f"Est. remaining: {remaining_time:.2f}s")

        print("\r" + " " * (len(progress.get("last_line", "")) + 5), end="\r")
        print(line, end="")
        progress["last_line"] = line

        if completed == total:
            print()  # final newline

async def main():
    parser = argparse.ArgumentParser(description="Bruteforce paths or subdomains.")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., http://example.com/ or domain.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Wordlist file containing paths or subdomains.")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent tasks (default: 10).")
    parser.add_argument("-to", "--timeout", type=float, default=5.0, help="Request timeout in seconds (default: 5).")
    parser.add_argument("-c", "--codes", type=str, default="200", help="HTTP status codes to show (e.g., '200,301,403').")
    parser.add_argument("-m", "--mode", choices=["paths", "subdomains"], default="paths",
                        help="Scan mode: 'paths' for path bruteforce, 'subdomains' for subdomain bruteforce.")
    parser.add_argument("-p", "--protocol", choices=["http", "https"], default="https",
                        help="Protocol to use for subdomains mode (default: https).")
    args = parser.parse_args()

    print_banner()  # Affiche le dessin au lancement

    max_threads = args.threads
    timeout = args.timeout
    codes_to_check = set(map(int, args.codes.split(',')))
    mode = args.mode
    protocol = args.protocol

    # Load wordlist
    try:
        with open(args.wordlist, "r", encoding="latin-1") as file:
            entries = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] Wordlist file '{args.wordlist}' not found.")
        return
    except UnicodeDecodeError as e:
        print(f"[ERROR] Unable to read wordlist file '{args.wordlist}': {e}")
        return

    if mode == "paths":
        base_url = args.url
        print(f"[*] Mode: Path bruteforce on {base_url}")
    else:
        base_domain = args.url.lower()
        if base_domain.startswith("http://"):
            base_domain = base_domain[len("http://"):]
        elif base_domain.startswith("https://"):
            base_domain = base_domain[len("https://"):]
        if base_domain.startswith("www."):
            base_domain = base_domain[len("www."):]
        print(f"[*] Mode: Subdomain bruteforce on {base_domain} (protocol {protocol})")

    print(f"[*] Wordlist: {args.wordlist}")
    print(f"[*] Threads: {max_threads}")
    print(f"[*] HTTP codes to check: {codes_to_check}")
    print(f"[*] Number of entries to test: {len(entries)}")
    print("[*] Starting scan...\n")

    progress = {
        "count": 0,
        "total": len(entries),
        "total_time": 0.0,
        "lock": asyncio.Lock(),
        "last_line": ""
    }

    semaphore = asyncio.Semaphore(max_threads)

    async with httpx.AsyncClient() as client:
        tasks = []
        for entry in entries:
            if mode == "paths":
                tasks.append(check_path(client, entry, base_url, timeout, codes_to_check, progress, semaphore))
            else:
                tasks.append(check_subdomain(client, entry, base_domain, protocol, timeout, codes_to_check, progress, semaphore))

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
