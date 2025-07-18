import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def scrape_jobs(keyword="intern"):
    url = "https://remoteok.com/remote-python-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("tr", class_="job")

    job_list = []

    for job in jobs:
        title_tag = job.find("h2")
        company_tag = job.find("h3")
        location_tag = job.find("div", class_="location")
        link_tag = job.find("a", class_="preventLink")

        if title_tag and company_tag:
            title = title_tag.get_text(strip=True)
            if keyword.lower() in title.lower():  # 🔍 Keyword filtering
                job_data = {
                    "title": title,
                    "company": company_tag.get_text(strip=True),
                    "location": location_tag.get_text(strip=True) if location_tag else "Remote",
                    "link": f"https://remoteok.com{link_tag['href']}" if link_tag else "N/A"
                }
                job_list.append(job_data)

    return job_list

def save_results(job_list, csv_file, json_file):
    df = pd.DataFrame(job_list)
    df.to_csv(csv_file, index=False)
    print(f"[✔] Saved {len(df)} jobs to {csv_file}")

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(job_list, f, indent=4, ensure_ascii=False)
    print(f"[✔] Saved {len(job_list)} jobs to {json_file}")

if __name__ == "__main__":
    keyword = "developer"  
    jobs = scrape_jobs(keyword)
    
    if jobs:
        save_results(jobs, "developer.csv", "developer.json")
    else:
        print("[!] No jobs found matching the keyword.")
