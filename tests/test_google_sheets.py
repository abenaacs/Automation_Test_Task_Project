from unittest.mock import MagicMock, patch
import pytest
from src.google_sheets import GoogleSheetsClient
from src.config import SERVICE_ACCOUNT_FILE  # Import the service account file path


def test_append_and_read_data(mocker):
    # Create mock service and values objects
    mock_service = MagicMock()
    mock_values = MagicMock()

    # Set up the chain of calls for the append method
    mock_values.append.return_value.execute.return_value = {
        "updates": {"updatedRows": 1}
    }
    # Assign the mock_values to the spreadsheets().values() call
    mock_service.spreadsheets().values.return_value = mock_values

    # Patch the _initialize_service method to return the mock_service
    mocker.patch(
        "src.google_sheets.GoogleSheetsClient._initialize_service",
        return_value=mock_service,
    )

    # Initialize GoogleSheetsClient with both sheet_id and service_account_file
    client = GoogleSheetsClient("test_sheet_id", SERVICE_ACCOUNT_FILE)

    sample_data = [["Name", "Job Title", "Company Name", "Location", "LinkedIn URL"]]
    rows_updated = client.append_data("Sheet1!A1:E1", sample_data)
    assert rows_updated == 1

    # Similarly, set up the get method
    mock_values.get.return_value.execute.return_value = {"values": sample_data}
    fetched_data = client.read_data("Sheet1!A1:E1")
    assert fetched_data == sample_data
