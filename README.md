# myjobhunter
building this platform to automate and enhance my job-hunting tasks


CONDA VENV INSTRUCTIONS:
    To activate this environment
        $ conda activate jobhuntingenv

    To deactivate an active environment, use
        $ conda deactivate


IDEAS for pulling jobs + companies:

    APIfy
        - wellfound job scraper
        - linkedin job / post scraper
        - greenhouse job scraper

# AI-Powered Job Platform

A modern job application platform for developers that uses AI to automate and enhance the job search process. This platform intelligently scrapes job listings, extracts structured data, and prepares personalized insights to streamline the technical hiring process.

## Project Overview

This platform aims to reduce friction in the technical hiring process by automating repetitive tasks and providing AI-powered insights. The core focus is on helping developers find relevant opportunities while minimizing the time spent on manual filtering and application preparation.

## Current Features

### 1. Job Scraping Engine

- **Multi-Platform Support**: Currently supports scraping from:
  - Ashby (ashbyhq.com)
  - Greenhouse (greenhouse.io)
  - Lever (lever.co)
  - startups.gallery/jobs

- **Intelligent Data Extraction**: Uses Claude API to transform unstructured job listings into comprehensive, structured data including:
  - Job title and company details
  - Location and employment type
  - Required skills and experience level
  - Compensation information
  - Detailed responsibilities and qualifications
  - Application instructions

### 2. Technical Implementation

- **Web Scraping**: Selenium-based scraping with polite crawling protocols
- **AI Integration**: Claude API for intelligent content processing
- **Modular Architecture**: Extensible design for adding new job sources and features

## Planned Features

- Resume parsing and profile building
- AI-powered job matching and recommendations
- Application tracking and management
- Skill gap analysis and development recommendations
- Automated job search agent
- Interview preparation workflows

## Installation & Setup

### Prerequisites

- Python 3.10+
- Chrome browser (for Selenium WebDriver)
- Anthropic API key

### Environment Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/ai-job-platform.git
   cd ai-job-platform
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API credentials:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

## Usage

### Job Scraping

```bash
# Scrape a job posting from Ashby, Lever, or Greenhouse
python job_scraper.py https://example.ashbyhq.com/jobs/12345 --output job_data.json

# Additional options
python job_scraper.py https://example.lever.co/12345 --headless --output my_job.json
```

## Project Structure

```
ai-job-platform/
├── job_scraper.py        # Main script for job scraping
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables (not tracked in git)
├── data/                 # Directory for storing scraped job data
└── docs/                 # Documentation files
```

## Technology Stack

- **Python**: Core programming language
- **Selenium**: Web scraping and automation
- **Claude AI**: Natural language processing and data extraction
- **MongoDB**: Planned for persistent data storage
- **FastAPI**: Planned for API development

## Contribution

This project is currently in development. Contributions, suggestions, and feedback are welcome.

## License

[MIT License](LICENSE)