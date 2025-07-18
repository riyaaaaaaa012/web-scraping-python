import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the job board
url = "https://remoteok.com/remote-python-jobs"

# Send HTTP request
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find job listings
jobs = soup.find_all("tr", class_="job")

job_list = []

for job in jobs:
    title_tag = job.find("h2")
    company_tag = job.find("h3")
    location_tag = job.find("div", class_="location")
    link_tag = job.find("a", class_="preventLink")

    if title_tag and company_tag:
        job_data = {
            "title": title_tag.get_text(strip=True),
            "company": company_tag.get_text(strip=True),
            "location": location_tag.get_text(strip=True) if location_tag else "Remote",
            "link": f"https://remoteok.com{link_tag['href']}" if link_tag else "N/A"
        }
        job_list.append(job_data)

# Convert to DataFrame
df = pd.DataFrame(job_list)

# Save to CSV
df.to_csv("remote_python_jobs.csv", index=False)

print("Scraped", len(df), "jobs. Saved to remote_python_jobs.csv.")
