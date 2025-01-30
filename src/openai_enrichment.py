import openai
import logging
import time
import random

logger = logging.getLogger(__name__)


class OpenAIEnricher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.initialize_openai()

    def initialize_openai(self):
        openai.api_key = self.api_key

    def _call_with_retry(self, func, *args, **kwargs):
        max_retries = 5
        base_delay = 2  # seconds
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except openai.error.RateLimitError as e:
                logger.warning(
                    f"Rate limit exceeded. Attempt {attempt + 1} of {max_retries}. Error: {e}"
                )
                delay = base_delay * (2**attempt) + random.uniform(
                    0, 1
                )  # Exponential backoff with jitter
                time.sleep(delay)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise
        logger.error("Max retries reached. Failed to complete request.")
        raise Exception("Failed to generate response due to rate limiting.")

    def summarize_profile(self, profile_data):
        prompt = f"Summarize the following LinkedIn profile data: {profile_data}"
        try:
            response = self._call_with_retry(
                openai.ChatCompletion.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=100,
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return ""

    def generate_outreach_message(self, profile_data):
        prompt = f"Generate a personalized outreach message for the following candidate: {profile_data}"
        try:
            response = self._call_with_retry(
                openai.ChatCompletion.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=100,
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            logger.error(f"Error generating outreach message: {e}")
            return ""
