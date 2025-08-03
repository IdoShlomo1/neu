import pytest


@pytest.mark.parametrize("text, description", [
    ("hello world", "Basic test with two words"),
    ("   leading and trailing spaces   ", "Test with leading/trailing spaces"),
    ("multiple   spaces", "Test with multiple spaces"),
    ("שלום עולם", "Test with Hebrew characters"),
    ("hello, world! 123", "Test with special characters and punctuation"),
    (' '.join([f"word-{i}" for i in range(1000)]), "Test with a very long string"),
    ("hello", "Test with a single word"),
])
def test_reverse_string(api_client, text: str, description: str):
    """
    Test the reverse endpoint returns the reversed text.
    """
    print(f"Testing reverse with text: {text} - {description}")
    reverse_response = api_client.reverse(text)
    assert reverse_response.status_code == 200
    response_data = reverse_response.json()
    print(f"Reversed result: {response_data['result']}")
    print(f"Original text: {text}")
    assert "result" in response_data
    expected_result = ' '.join(reversed(text.strip().split()))
    assert response_data["result"] == expected_result


def test_restore(api_client):
    """
    Test the restore endpoint returns the last reversed result.
    """
    input_text = "restore test"
    api_client.reverse(input_text)
    restore_response = api_client.restore()

    assert restore_response.status_code == 200
    response_data = restore_response.json()
    assert "result" in response_data
    expected_result = ' '.join(reversed(input_text.strip().split()))
    assert response_data["result"] == expected_result, f"Expected '{expected_result}', got '{response_data['result']}'"


def test_reverse_empty_string(api_client):
    """
    Test the reverse endpoint with an empty string returns an empty result.
    """
    text = ""
    response = api_client.reverse(text)
    assert response.status_code == 400
    assert response.json() == {"error": "Missing 'text' query parameter"}


def test_restore_after_multiple_reverses(api_client):
    """
    Test that restore returns the most recent reversed result after multiple reverses.
    """
    first_response = api_client.reverse("one two three")
    print(f"First reverse result: {first_response.json()['result']}")
    second_response = api_client.reverse("alpha beta gamma")

    print(f"Second reverse result: {second_response.json()['result']}")
    restore_response = api_client.restore()
    assert restore_response.status_code == 200
    response_data = restore_response.json()

    expected_result = "gamma beta alpha"
    assert response_data["result"] == expected_result, f"Expected '{expected_result}', got '{response_data['result']}'"


def test_content_type_is_json(api_client):
    """
    Test that all responses have application/json content-type.
    """
    reverse_response = api_client.reverse("json test")
    assert reverse_response.headers["Content-Type"].startswith("application/json")
    restore_response = api_client.restore()
    assert restore_response.headers["Content-Type"].startswith("application/json")
