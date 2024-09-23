import time
import sys
import requests
import json
import csv
from concurrent.futures import ThreadPoolExecutor

def show_intro():
    texts = [
        "SELAMAT DATANG DI TOOLS SUBSCAN",
        "Author Tools By : Najmi Khaeri Arrisa Putra",
        "Instagram : @najmikhaeri13",
        "Tiktok    : @najmikhaeri"
    ]
    
    for text in texts:
        print(text)
        time.sleep(0.5)
    time.sleep(1)

def get_subdomains_from_crtsh(domain):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            subdomains = {entry['common_name'] for entry in data if domain in entry['common_name']}
            return list(subdomains)
        else:
            print(f"Error: crt.sh responded with status code {response.status_code}")
            return []
    except Exception as e:
        print(f"Error getting subdomains from crt.sh: {e}")
        return []

def save_to_csv(subdomains, domain):
    filename = f"subdomains_{domain}.csv"
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Subdomain'])
            for subdomain in subdomains:
                writer.writerow([subdomain])
        print(f"Hasil disimpan di {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def save_to_json(subdomains, domain):
    filename = f"subdomains_{domain}.json"
    try:
        with open(filename, 'w') as file:
            json.dump({"subdomains": subdomains}, file, indent=4)
        print(f"Hasil disimpan di {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def save_to_txt(subdomains, domain):
    filename = f"subdomains_{domain}.txt"
    try:
        with open(filename, 'w') as file:
            for subdomain in subdomains:
                file.write(subdomain + '\n')
        print(f"Hasil disimpan di {filename}")
    except Exception as e:
        print(f"Error saving to TXT: {e}")

def gather_subdomains(domain):
    sources = [
        get_subdomains_from_crtsh,
    ]
    
    subdomains = set()
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_source = {executor.submit(source, domain): source for source in sources}
        for future in future_to_source:
            try:
                result = future.result()
                subdomains.update(result)
            except Exception as e:
                print(f"Error with {future_to_source[future]}: {e}")

    return sorted(subdomains)

def main():
    show_intro()

    domain = input("\nMasukkan domain (contoh: example.com): ")
    
    print("\nMengumpulkan subdomain...")
    subdomains = gather_subdomains(domain)

    if subdomains:
        print(f"\nSubdomain yang ditemukan untuk {domain}:")
        for subdomain in subdomains:
            print(f"- {subdomain}")
        
        save_format = input("\nIngin menyimpan hasil ke file? (csv/json/txt/tidak): ").lower()
        if save_format == 'csv':
            save_to_csv(subdomains, domain)
        elif save_format == 'json':
            save_to_json(subdomains, domain)
        elif save_format == 'txt':
            save_to_txt(subdomains, domain)
        else:
            print("Hasil tidak disimpan ke file.")
    else:
        print(f"Tidak ditemukan subdomain untuk {domain}.")

if __name__ == "__main__":
    main()