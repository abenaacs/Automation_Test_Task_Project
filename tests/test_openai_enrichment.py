from unittest.mock import patch
from src.openai_enrichment import OpenAIEnricher


@patch("src.openai_enrichment.openai.Completion.create")
def test_summarize_and_generate_message(mock_create):
    mock_create.return_value = type(
        "obj", (object,), {"choices": [type("obj", (object,), {"text": "Summary"})]}
    )

    enricher = OpenAIEnricher("dummy_key")
    summary = enricher.summarize_profile(
        "John Doe, Digital Marketing Manager at XYZ Company, Location: New York"
    )
    message = enricher.generate_outreach_message(
        "John Doe, Digital Marketing Manager at XYZ Company, Location: New York"
    )
    assert len(summary) > 0
    assert len(message) > 0
