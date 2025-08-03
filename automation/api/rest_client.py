import requests


class RestClient:
    """
    RestClient is a generic API client for making HTTP requests using the requests library.

    Features:
    - Supports GET, POST, PUT HTTP methods.
    - Centralized request method for all HTTP verbs.
    - Allows passing request hooks for custom request/response handling.
    - Automatically builds endpoint URLs from a base URL.

    Args:
        base_url (str): The base URL for the API endpoints.
        hooks (dict, optional): Dictionary of request hooks for requests library (e.g., {'response': hook_fn}).

    Example usage:
        client = RestClient('https://api.example.com', hooks={'response': my_hook})
        response = client.get('users', params={'id': 1})
    """

    def __init__(self, base_url: str, hooks: dict | None = None) -> None:
        """
        Initialize the RestClient.

        Args:
            base_url (str): The base URL for the API endpoints.
            hooks (dict, optional): Dictionary of request hooks for requests library (e.g., {'response': hook_fn}).
        """
        self.base_url = base_url
        self.hooks = hooks or {}
    
    def request(self, method: str, endpoint: str = '', **kwargs) -> requests.Response:
        """
        Send an HTTP request using the specified method and endpoint.

        Args:
            method (str): HTTP method (e.g., 'get', 'post', 'put', 'delete').
            endpoint (str): API endpoint to append to the base URL.
            **kwargs: Additional arguments for requests.request (e.g., params, json, headers).

        Returns:
            requests.Response: The response object from the 'requests' library.
        """
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        kwargs.setdefault('hooks', self.hooks)
        response = requests.request(method, url, **kwargs)

        return response

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Send a GET request.

        Args:
            endpoint (str): API endpoint to append to the base URL.
            **kwargs: Additional arguments for requests.request.

        Returns:
            requests.Response: The response object.
        """
        response = self.request('get', endpoint, **kwargs)
        return response
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Send a POST request.

        Args:
            endpoint (str): API endpoint to append to the base URL.
            **kwargs: Additional arguments for requests.request.

        Returns:
            requests.Response: The response object.
        """
        response = self.request('post', endpoint,**kwargs)
        return response

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Send a PUT request.

        Args:
            endpoint (str): API endpoint to append to the base URL.
            **kwargs: Additional arguments for requests.request.

        Returns:
            dict: The JSON-decoded response.
        """
        response = self.request('put', endpoint,  **kwargs)
        return response
