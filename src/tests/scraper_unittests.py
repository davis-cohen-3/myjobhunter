"""
Unit tests for the startups.gallery scraper.
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from bs4 import BeautifulSoup

from src.scrapers.startups_gallery import StartupsGalleryScraper


class TestStartupsGalleryScraper(unittest.TestCase):
    """Test cases for the StartupsGalleryScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create scraper with Selenium disabled for testing
        self.scraper = StartupsGalleryScraper(use_selenium=False)
        
        # Load sample HTML files for testing
        self.sample_listing_html = self._load_sample_html('sample_listing_page.html')
        self.sample_detail_html = self._load_sample_html('sample_job_detail.html')
    
    def _load_sample_html(self, filename):
        """Load sample HTML from test fixtures."""
        # Check if the test fixtures directory exists
        fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        filepath = os.path.join(fixtures_dir, filename)
        
        # If the file doesn't exist, return a minimal HTML template
        if not os.path.exists(filepath):
            if 'listing' in filename:
                return """
                <html>
                <body>
                    <div class="job-listing-item">
                        <h3 class="job-title">Python Developer</h3>
                        <span class="company-name">Test Company</span>
                        <div class="job-location">Remote</div>
                        <a class="apply-link" href="https://example.com/apply">Apply</a>
                        <a class="company-website" href="https://example.com">Website</a>
                        <a class="linkedin-profile" href="https://linkedin.com/company/example">LinkedIn</a>
                        <div class="job-description">This is a test job description.</div>
                    </div>
                    <span class="total-pages">3</span>
                </body>
                </html>
                """
            else:
                return """
                <html>
                <body>
                    <h1 class="job-title">Senior Python Developer</h1>
                    <div class="company-name">Detailed Company</div>
                    <div class="job-location">San Francisco, CA</div>
                    <div class="job-description">Detailed job description goes here.</div>
                </body>
                </html>
                """
        
        # Load the actual file if it exists
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    @patch('requests.Session')
    def test_get_page_content(self, mock_session):
        """Test fetching page content."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.text = self.sample_listing_html
        mock_response.raise_for_status = MagicMock()
        
        # Set up the mock session
        mock_session_instance = mock_session.return_value
        mock_session_instance.get.return_value = mock_response
        
        # Call the method with a test URL
        content = self.scraper._get_page_content("https://test.com")
        
        # Assertions
        self.assertEqual(content, self.sample_listing_html)
        mock_session_instance.get.assert_called_once()
    
    def test_get_total_pages(self):
        """Test extracting total page count."""
        soup = BeautifulSoup(self.sample_listing_html, 'html.parser')
        total_pages = self.scraper._get_total_pages(soup)
        self.assertEqual(total_pages, 3)
    
    def test_parse_job_listing(self):
        """Test parsing a job listing element."""
        soup = BeautifulSoup(self.sample_listing_html, 'html.parser')
        job_element = soup.select_one("div.job-listing-item")
        
        job_data = self.scraper._parse_job_listing(job_element)
        
        # Assertions
        self.assertEqual(job_data['title'], "Python Developer")
        self.assertEqual(job_data['company'], "Test Company")
        self.assertEqual(job_data['location'], "Remote")
        self.assertEqual(job_data['apply_link'], "https://example.com/apply")
        self.assertEqual(job_data['company_website'], "https://example.com")
        self.assertEqual(job_data['linkedin'], "https://linkedin.com/company/example")
    
    def test_extract_jobs_from_page(self):
        """Test extracting multiple job listings from a page."""
        jobs = self.scraper._extract_jobs_from_page(self.sample_listing_html)
        
        # Should find at least one job
        self.assertGreaterEqual(len(jobs), 1)
        
        # First job should have expected fields
        first_job = jobs[0]
        self.assertIn('title', first_job)
        self.assertIn('company', first_job)
        self.assertIn('location', first_job)
    
    @patch.object(StartupsGalleryScraper, '_get_page_content')
    @patch.object(StartupsGalleryScraper, '_get_total_pages')
    @patch.object(StartupsGalleryScraper, '_extract_jobs_from_page')
    def test_scrape_jobs(self, mock_extract, mock_get_pages, mock_get_content):
        """Test the main scraping function."""
        # Set up mocks
        mock_get_content.return_value = self.sample_listing_html
        mock_get_pages.return_value = 2
        mock_extract.return_value = [
            {
                'title': 'Job 1',
                'company': 'Company 1',
                'location': 'Location 1'
            },
            {
                'title': 'Job 2',
                'company': 'Company 2',
                'location': 'Location 2'
            }
        ]
        
        # Call the method
        jobs = self.scraper.scrape_jobs(max_pages=2)
        
        # Assertions
        self.assertEqual(len(jobs), 4)  # 2 pages with 2 jobs each
        mock_get_content.assert_called()
        mock_get_pages.assert_called_once()
        self.assertEqual(mock_extract.call_count, 2)
    
    def test_context_manager(self):
        """Test using the scraper as a context manager."""
        with patch.object(StartupsGalleryScraper, '__exit__') as mock_exit:
            with StartupsGalleryScraper(use_selenium=True) as scraper:
                # Just ensure it works as a context manager
                pass
            
            # Verify __exit__ was called
            mock_exit.assert_called_once()


if __name__ == '__main__':
    unittest.main()