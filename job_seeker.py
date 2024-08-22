import time
import random
from selenium import webdriver
from bs4 import BeautifulSoup
import csv

# Set up Selenium WebDriver
driver_path = "/usr/local/bin/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument(
    "--headless"
)  # Run in headless mode to avoid opening a browser window
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Random User-Agent to mimic different browsers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
]

options.add_argument(f"user-agent={random.choice(user_agents)}")

driver = webdriver.Chrome(executable_path=driver_path, options=options)

# LinkedIn Job Search URL
url = "https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=Tunisia"

driver.get(url)

# Sleep to allow the page to load
time.sleep(random.uniform(5, 10))

# Get the page content
soup = BeautifulSoup(driver.page_source, "html.parser")

# Close the WebDriver
driver.quit()

# Find all job listings (this will vary based on the website's structure)
jobs = soup.find_all("div", class_="result-card__contents job-result-card__contents")

# Open a CSV file to save the job listings
with open("linkedin_job_listings.csv", mode="w") as file:
    writer = csv.writer(file)
    writer.writerow(["Job Title", "Company", "Location", "Date Posted", "Link"])

    # Loop through the job listings and extract details
    for job in jobs:
        title = job.find("h3", class_="result-card__title").text.strip()
        company = job.find("h4", class_="result-card__subtitle").text.strip()
        location = job.find("span", class_="job-result-card__location").text.strip()
        date_posted = job.find("time")["datetime"]
        link = job.find("a", class_="result-card__full-card-link")["href"]

        # Write the job details to the CSV file
        writer.writerow([title, company, location, date_posted, link])

print("Job listings have been saved to linkedin_job_listings.csv")

# Set up a list of proxies
proxies = [
    "http://proxy1.com:port",
    "http://proxy2.com:port",
    # Add more proxies
]

# Choose a random proxy for each request
proxy = random.choice(proxies)
options.add_argument(f"--proxy-server={proxy}")
