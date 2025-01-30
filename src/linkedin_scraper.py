import requests
import time
import logging
from io import StringIO
import csv
from src.utils import log_info, log_error

logger = logging.getLogger(__name__)


class LinkedInScraper:
    def __init__(self, api_key):
        self.api_key = api_key

    def scrape_profiles(self, query):
        # Step 1: Launch the agent
        launch_url = "https://api.phantombuster.com/api/v2/agents/launch"
        headers = {
            "Content-Type": "application/json",
            "x-phantombuster-key": self.api_key,
        }
        payload = {
            "id": "8777897519511673",  # Replace with your actual phantomId
            "args": {"query": query},
        }
        try:
            # Launch the agent
            response = requests.post(launch_url, headers=headers, json=payload)
            response.raise_for_status()
            container_id = response.json().get("containerId")
            if not container_id:
                log_error("Failed to launch agent: No containerId returned.")
                return []

            logger.info(
                f"Agent launched successfully with container ID: {container_id}"
            )

            # Step 2: Wait for the agent to complete
            fetch_url = "https://api.phantombuster.com/api/v2/containers/fetch"
            while True:
                time.sleep(10)  # Wait 10 seconds before checking status
                fetch_response = requests.get(
                    fetch_url,
                    headers=headers,
                    params={"id": container_id},
                )
                fetch_response.raise_for_status()
                status = fetch_response.json().get("status")
                logger.info(f"Current status: {status}")

                if status == "finished":
                    break  # Agent completed successfully
                elif status in ["error", "failed"]:
                    log_error(f"Agent failed with status: {status}")
                    return []
                # Else, continue waiting

            # Step 3: Fetch the output
            output_url = "https://api.phantombuster.com/api/v2/containers/fetch-output"
            output_response = requests.get(
                output_url,
                headers=headers,
                params={"id": container_id},
            )
            output_response.raise_for_status()
            output_data = output_response.json()

            # Debug: Print the raw output data
            logger.debug(f"Raw output data: {output_data}")

            # Step 4: Extract file URLs from the output
            if "output" not in output_data:
                log_error("No output data found.")
                return []

            # Parse the output to extract file URLs
            output_text = output_data["output"]
            csv_url = None
            json_url = None
            for line in output_text.split("\n"):
                if "CSV saved at" in line:
                    csv_url = line.split("CSV saved at ")[1].strip()
                elif "JSON saved at" in line:
                    json_url = line.split("JSON saved at ")[1].strip()

            if not csv_url and not json_url:
                log_error("No CSV or JSON file URLs found in the output.")
                return []

            # Step 5: Download the CSV or JSON file
            if csv_url:
                file_response = requests.get(csv_url)
                file_response.raise_for_status()
                data = file_response.text  # CSV data as text
                # Parse CSV data into a list of dictionaries
                f = StringIO(data)
                reader = csv.DictReader(f)
                profiles = [row for row in reader]
            elif json_url:
                file_response = requests.get(json_url)
                file_response.raise_for_status()
                profiles = file_response.json()  # JSON data as a Python object

            logger.info(f"Data retrieved: {profiles}")
            return profiles
        except requests.exceptions.HTTPError as http_err:
            log_error(f"HTTP error occurred: {http_err}")
            if response.status_code == 401:
                log_error("Unauthorized: Check your API key and permissions.")
            return []
        except requests.exceptions.RequestException as e:
            log_error(f"Error fetching LinkedIn data: {e}")
            return []


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape LinkedIn profiles")
    parser.add_argument("--query", type=str, help="Search query for LinkedIn profiles")
    parser.add_argument("--api_key", type=str, help="PhantomBuster API Key")
    args = parser.parse_args()
    scraper = LinkedInScraper(args.api_key)
    profiles = scraper.scrape_profiles(args.query)
    print(profiles)
