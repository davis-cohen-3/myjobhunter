from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
import time
import pandas as pd # type: ignore
from typing import List, Tuple, Dict, Any
import argparse


class StartupJobScraper:
    def __init__(self):
        """Initialize the job scraper with an empty job dictionary"""
        self.organized_jobs = {}
        self.setup_driver()
        
    def setup_driver(self):
        """Set up the Selenium webdriver"""
        options = webdriver.ChromeOptions()
        service = Service(ChromeDriverManager().install())
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(service=service, options=options)
        
    def load_more_jobs(self, num_clicks: int) -> None:
        """
        Click 'Load More' button specified number of times, scraping jobs after each click
        
        Args:
            num_clicks: Number of times to click the 'Load More' button
        """
        try:
        # Navigate to the initial page
            self.driver.get("https://startups.gallery/jobs/")
            time.sleep(3)  # Initial page load wait
            
            for i in range(num_clicks):
                try:
                    load_more_button = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Load More')]")
                    load_more_button.click()
                    time.sleep(5)

                    positions, company_info, job_app_links = self.pull_data()
                    self.organize_data(positions, company_info, job_app_links)
                
                except Exception as e:
                    print(f"Error clicking 'Load More' button on iteration {i+1}: {e}")
                    break
            

        except Exception as e:
            print(f"Error loading initial page: {e}")
            raise
    
    def pull_data(self) -> Tuple[List[str], List[str], List[str]]:
        """
        Extract job information from the current page
        
        Returns:
            Tuple containing lists of job titles, company info, and application links
        """
        try:
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[class*='framer-1fxtycr'][class*='framer-1s7tguz']")
            
            if not job_elements:
                print("No job elements found")
                return [], [], []

            parent_container = job_elements[0].find_element(By.XPATH, "./ancestor::div[contains(@class, 'framer-')]")
            company_divs = parent_container.find_elements(By.CSS_SELECTOR, "div[data-framer-name='Company Name']")
            company_texts = [div.text for div in company_divs]
            job_app_links = []

            print(f'Length of company_texts: {len(company_texts)}')
            print(f'Company_texts: {company_texts}')
            
            for link in job_elements:
                job_url = link.get_attribute("href")
                job_app_links.append(job_url)
            
            positions, company_info = [], []
            
            for i, data in enumerate(company_texts):
                if i % 2 == 0:
                    positions.append(data)
                else:
                    company_info.append(data)
            
            return positions, company_info, job_app_links
        
        except Exception as e:
            print(f"Error extracting job data: {e}")
            return [], [], []
        
    def organize_data(self, jobs: List[str], company_info: List[str], job_app_links: List[str]) -> None:
        """
        Organize scraped job data and add to the main dictionary if not already present
        
        Args:
            jobs: List of job roles
            company_info: List of company names/descriptions
            job_app_links: List of job application URLs
        """
        assert len(jobs) == len(company_info) == len(job_app_links), "Lists must have equal length"

        for i in range(len(jobs)):
            if job_app_links[i] not in self.organized_jobs:
                url_key = job_app_links[i]
                self.organized_jobs[url_key] = {
                    "title": jobs[i],
                    "company_info": company_info[i]
                }

    def save_to_csv(self, filename: str = "startup_jobs.csv") -> None:
        """
        Save job data to CSV file
        
        Args:
            filename: Name of output CSV file
        """
        # Create a list of dictionaries with URL included as a column
        rows = []
        for url, data in self.organized_jobs.items():
            row = {"url": url}
            row.update(data)
            rows.append(row)
        
        df = pd.DataFrame(rows)
        
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    
    def cleanup(self):
        """Close the webdriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    """Main function to run the job scraping workflow"""
    parser = argparse.ArgumentParser(description="Scrape startup jobs from startups.gallery")
    parser.add_argument('-n', '--num_clicks', type=int, default=1,
                        help='Number of times to click "Load More" button (default: 1)')
    args = parser.parse_args()
    
    print(f"Starting job scraping with {args.num_clicks} Load More clicks...")
    
    scraper = StartupJobScraper()
    
    try:
        scraper.load_more_jobs(args.num_clicks)
        scraper.save_to_csv()
        
        print(f"Scraped {len(scraper.organized_jobs)} jobs successfully!")
    finally:
        scraper.cleanup()


if __name__ == "__main__":
    main()