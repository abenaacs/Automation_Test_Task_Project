import argparse
from src.linkedin_scraper import LinkedInScraper
from src.google_sheets import GoogleSheetsClient
from src.openai_enrichment import OpenAIEnricher
from src.utils import log_info, log_error
from src.config import (
    PHANTOMBUSTER_API_KEY,
    SERVICE_ACCOUNT_FILE,
    GOOGLE_SHEET_ID,
    OPENAI_API_KEY,
)


def scrape_and_organize_data(query, api_key, sheet_id, service_account_file):
    scraper = LinkedInScraper(api_key)
    google_sheets_client = GoogleSheetsClient(sheet_id, service_account_file)
    log_info(f"Scraping LinkedIn profiles for query: {query}")
    profiles = scraper.scrape_profiles(query)
    if not profiles:
        log_error("No profiles found.")
        return []

    log_info("Organizing data in Google Sheets")
    sheet_data = []
    header = ["Name", "Job Title", "Company Name", "Location", "LinkedIn Profile URL"]
    sheet_data.append(header)

    for profile in profiles:
        row = [
            profile.get("companyName"),
            profile.get("tagLine"),
            profile.get("industry"),
            profile.get("location"),
            profile.get("companyUrl"),
        ]
        sheet_data.append(row)

    rows_updated = google_sheets_client.append_data("Sheet1!A1:E1", sheet_data)
    log_info(f"Updated {rows_updated} rows in Google Sheets")
    return profiles


def enrich_data_with_ai(profiles, openai_key, sheet_id, service_account_file):
    openai_enricher = OpenAIEnricher(openai_key)
    google_sheets_client = GoogleSheetsClient(sheet_id, service_account_file)
    log_info("Enriching data with OpenAI")

    enriched_data = []
    header = ["Summary", "Outreach Message"]
    enriched_data.append(header)

    for profile in profiles:
        profile_summary = openai_enricher.summarize_profile(str(profile))
        outreach_message = openai_enricher.generate_outreach_message(str(profile))
        enriched_row = [profile_summary, outreach_message]
        enriched_data.append(enriched_row)

    rows_updated = google_sheets_client.append_data("Sheet1!F1:G1", enriched_data)
    log_info(f"Updated {rows_updated} rows in Google Sheets with enriched data")


def main(query):
    profiles = scrape_and_organize_data(
        query, PHANTOMBUSTER_API_KEY, GOOGLE_SHEET_ID, SERVICE_ACCOUNT_FILE
    )
    if profiles:
        enrich_data_with_ai(
            profiles, OPENAI_API_KEY, GOOGLE_SHEET_ID, SERVICE_ACCOUNT_FILE
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automate LinkedIn data collection, organize in Google Sheets, and enrich with AI"
    )
    parser.add_argument("--query", type=str, help="Search query for LinkedIn profiles")
    args = parser.parse_args()
    if not args.query:
        log_error("Please provide a search query using --query option")
        exit(1)
    main(args.query)
