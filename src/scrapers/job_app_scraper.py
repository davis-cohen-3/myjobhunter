from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from typing import Dict, Any, List, Optional
import time
import json
import os
import re
import anthropic # type: ignore
import logging
import argparse
from dotenv import load_dotenv # type: ignore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()

class JobScraper:
    """Base class for job scrapers with common functionality"""
    
    def __init__(self, headless: bool = True):
        """Initialize the job scraper with webdriver setup"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            logger.warning("ANTHROPIC_API_KEY not found in environment variables!")
        self.client = anthropic.Anthropic(api_key=api_key) if api_key else None

    def get_page_text(self) -> str:
        """Extract all visible text from the page"""
        return self.driver.find_element(By.TAG_NAME, "body").text
    
    def process_with_llm(self, content: Dict[str, Any], platform: str) -> Dict[str, Any]:
        """Process job content with Claude to extract structured data"""
        if not self.client:
            logger.error("Anthropic API key not configured")
            return {"error": "LLM client not configured", "raw_data": content}
        
        prompt = f"""
        Extract structured information from this {platform} job posting.
        
        JOB POSTING CONTENT:
        {content.get('full_text', '')}
        
        Return a JSON object with these fields:
        - job_title: The exact title of the position
        - company_name: Name of the hiring company
        - location: Where the job is located (include if remote)
        - employment_type: Full-time, Part-time, Contract, etc.
        - department: Which department the role belongs to
        - application_deadline: The deadline to apply if specified
        - compensation: Salary range and compensation details
        - required_skills: List of required skills
        - experience_level: Junior, Mid, Senior, Lead, etc.
        - job_description: A 2-3 sentence summary of the role
        - responsibilities: List of key responsibilities
        - qualifications: List of required qualifications
        - benefits: List of benefits mentioned
        - good_fit_indicators: List of traits that make someone a good fit
        - poor_fit_indicators: List of traits that would make someone a poor fit
        - application_instructions: How to apply
        - source_url: {content.get('url', 'Not provided')}
        - platform: {platform}
        
        Only include fields where information is explicitly provided. Use null for missing information.
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=2000,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = response.content[0].text
            json_match = re.search(r'```json\n(.*?)\n```', result_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = result_text
            
            # Clean up and parse JSON
            json_str = json_str.strip()
            structured_data = json.loads(json_str)
            
            # Add source URL if not included
            if 'source_url' not in structured_data:
                structured_data['source_url'] = content.get('url')
            if 'platform' not in structured_data:
                structured_data['platform'] = platform
                
            return structured_data
            
        except Exception as e:
            logger.error(f"Error processing with LLM: {str(e)}")
            return {"error": str(e), "raw_data": content}
    
    def close(self):
        """Close the webdriver"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

class AshbyJobScraper(JobScraper):
    """Scraper specific to Ashby job postings"""
    
    def scrape_job(self, url: str) -> Dict[str, Any]:
        """Scrape an Ashby job posting and extract structured data"""
        logger.info(f"Scraping Ashby job: {url}")
        
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='ashby-job-posting-right-pane']"))
            )
            time.sleep(2)  
            
            job_title_element = self.driver.find_element(By.CSS_SELECTOR, "div[class*='_titles_']")
            job_title = job_title_element.text if job_title_element else "Not found"
            
            full_text = self.get_page_text()
            
            # Captured data
            job_data = {
                "url": url,
                "job_title": job_title,
                "full_text": full_text,
                "platform": "Ashby"
            }
            
            structured_data = self.process_with_llm(job_data, "Ashby")
            return structured_data
            
        except Exception as e:
            logger.error(f"Error scraping Ashby job: {str(e)}")
            return {"error": str(e), "url": url, "platform": "Ashby"}
        

class GreenhouseJobScraper(JobScraper):
    """Scraper specific to Greenhouse job postings"""
    
    def scrape_job(self, url: str) -> Dict[str, Any]:
        """Scrape an Greenhouse job posting and extract structured data"""
        logger.info(f"Scraping Greenhouse job: {url}")
        
        try:
            self.driver.get(url)
            
            job_title = self.driver.title.split(' | ')[0] if ' | ' in self.driver.title else "Not found"
            
            # Get all text from the body element
            full_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Captured data
            job_data = {
                "url": url,
                "job_title": job_title,
                "full_text": full_text,
                "platform": "Greenhouse"
            }
            
            structured_data = self.process_with_llm(job_data, "Greenhouse")
            return structured_data
            
        except Exception as e:
            logger.error(f"Error scraping Greenhouse job: {str(e)}")
            return {"error": str(e), "url": url, "platform": "Greenhouse"}
        
class LeverJobScraper(JobScraper):
    """Scraper specific to Lever job postings"""
    
    def scrape_job(self, url: str) -> Dict[str, Any]:
        """Scrape a Lever job posting and extract structured data"""
        logger.info(f"Scraping Lever job: {url}")
        
        try:
            self.driver.get(url)
            
            time.sleep(2)  # Allow dynamic content to load
            
            # Extract basic job information
            job_title_element = self.driver.find_element(By.CLASS_NAME, "posting-headline")
            job_title = job_title_element.find_element(By.TAG_NAME, "h2").text if job_title_element else "Not found"
            
            # Get full text content for LLM processing
            full_text = self.get_page_text()
            
            # Prepare data for LLM processing
            job_data = {
                "url": url,
                "job_title": job_title,
                "full_text": full_text,
                "platform": "Lever"
            }
            
            # Process with LLM
            structured_data = self.process_with_llm(job_data, "Lever")
            return structured_data
            
        except Exception as e:
            logger.error(f"Error scraping Lever job: {str(e)}")
            return {"error": str(e), "url": url, "platform": "Lever"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape job postings from various platforms')
    parser.add_argument('url', type=str, help='URL of the job posting to scrape')
    parser.add_argument('--headless', action='store_true', default=True, 
                        help='Run browser in headless mode (default: True)')
    parser.add_argument('--output', type=str, default='job_data.json',
                        help='Output file path (default: job_data.json)')
    args = parser.parse_args()
    
    url = args.url
    if 'ashbyhq.com' in url:
        scraper = AshbyJobScraper(headless=args.headless)
        scraper_name = 'Ashby'
    elif 'lever.co' in url:
        # When you implement the Lever scraper
        scraper = LeverJobScraper(headless=args.headless)  # Placeholder
        scraper_name = 'Lever'
    elif 'greenhouse.io' in url:
        scraper = GreenhouseJobScraper(headless=args.headless)  #
        scraper_name = 'Greenhouse'
    else:
        logger.error(f"Unsupported job platform for URL: {url}")
        print(f"Error: Unsupported job platform for URL: {url}")
        print("Supported platforms: Ashby (ashbyhq.com), Lever (lever.co), Greenhouse (greenhouse.io)")
        exit(1)
    
    try:
        logger.info(f"Scraping {scraper_name} job posting: {url}")
        job_data = scraper.scrape_job(url)
        
        with open(args.output, "w") as f:
            json.dump(job_data, indent=2, fp=f)
        logger.info(f"Job data saved to {args.output}")
        
        print(f"Successfully scraped {scraper_name} job posting")
        print(f"Data saved to {args.output}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}")
    finally:
        scraper.close()