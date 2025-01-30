from unittest.mock import patch, MagicMock
from src.linkedin_scraper import LinkedInScraper


@patch("src.linkedin_scraper.requests.post")
def test_scrape_linkedin_profiles(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"name": "John Doe"}]}
    mock_post.return_value = mock_response

    scraper = LinkedInScraper("dummy_key")
    profiles = scraper.scrape_profiles("Digital Marketing Managers in the USA")
    assert isinstance(profiles, list)
    assert len(profiles) > 0
