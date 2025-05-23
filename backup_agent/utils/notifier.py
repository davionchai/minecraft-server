import requests
import logging

from requests.models import Response

logger: logging.Logger = logging.getLogger(__name__)


class DiscordApi:
    def __init__(self, webhook: str):
        self.base_url: str = webhook

    def call_api_endpoint(self, data: dict) -> Response:
        """Sends a POST request to the Discord webhook URL with the provided data.

        Args:
            data (dict): The data to be sent in the request body.

        Returns:
            Response: The response object from the POST request.
        """
        try:
            response: Response = requests.post(url=self.base_url, json=data)
            # success call will return status_code 204
        except Exception as error_unknown:
            logger.error(f"{error_unknown}")
        else:
            if not response.ok:
                logger.error(f"Response Headers - {response.headers}")
                logger.error(f"Status Code - {response.status_code}")
                logger.error(f"Response - {response.json()}")
            return response
