import requests

from .rest_client import RestClient


class ApiClient(RestClient):
    def reverse(self, text: str) -> requests.Response:
        """
        Reverse the words in the input text.

        Args:
            text (str): The input text to reverse.

        Returns:
            dict: A dictionary containing the reversed result.
        """
        response = self.get('/reverse', params={'text': text})
        return response
    
    def restore(self) -> requests.Response:
        """
        Restore the last reversed result.

        Returns:
            dict: A dictionary containing the restored result.
        """
        response = self.get('/restore')
        return response