import pytest
from src.linkedin_scraper import LinkedInScraper


def test_scrape_profiles(scraper):
    data = scraper.scrape_profiles("Digital Marketing Managers in USA")
    assert isinstance(data, dict)  # Adjusted based on expected response structure
