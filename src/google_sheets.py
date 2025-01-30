from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging

logger = logging.getLogger(__name__)


class GoogleSheetsClient:
    def __init__(self, sheet_id, service_account_file):
        self.sheet_id = sheet_id
        self.service_account_file = service_account_file
        self.service = self._initialize_service()

    def _initialize_service(self):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file,
                scopes=["https://www.googleapis.com/auth/spreadsheets"],
            )
            return build("sheets", "v4", credentials=credentials)
        except Exception as e:
            logger.error(f"Error initializing Google Sheets service: {e}")
            raise

    def append_data(self, range_name, values):
        body = {"values": values}
        try:
            result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=self.sheet_id,
                    range=range_name,
                    valueInputOption="RAW",
                    insertDataOption="INSERT_ROWS",
                    body=body,
                )
                .execute()
            )
            return result.get("updates").get("updatedRows")
        except Exception as e:
            logger.error(f"Error appending data to Google Sheets: {e}")
            raise

    def read_data(self, range_name):
        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(spreadsheetId=self.sheet_id, range=range_name)
                .execute()
            )
            return result.get("values", [])
        except Exception as e:
            logger.error(f"Error reading data from Google Sheets: {e}")
            raise
