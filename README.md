# myjobhunter

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

### Job Scraping Engine

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

## Planned Features

- Resume parsing and profile building
- AI-powered job matching and recommendations
- Application tracking and management
- Skill gap analysis and development recommendations
- Automated job search agent
- Interview preparation workflows

### Environment Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   
3. Create a `.env` file with your API credentials:
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

## Technology Stack

- **Python**: Core programming language
- **Selenium**: Web scraping and automation
- **Claude AI**: Natural language processing and data extraction

## Contribution

This project is currently in development. Contributions, suggestions, and feedback are welcome.
