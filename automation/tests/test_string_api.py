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
    response = api_client.reverse(text)
    assert response.status_code == 200
    data = response.json()
    print(f"Reversed result: {data['result']}")
    print(f"Original text: {text}")
    assert "result" in data
    assert data["result"] == ' '.join(reversed(text.strip().split()))


def test_restore(api_client):
    """
    Test the restore endpoint returns the last reversed result.
    """
    text = "restore test"
    api_client.reverse(text)
    response = api_client.restore()

    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    res = ' '.join(reversed(text.strip().split()))
    assert data["result"] == res, f"Expected '{text}', got '{data['result']}'"


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
    res = api_client.reverse("one two three")
    print(f"First reverse result: {res.json()['result']}")
    res2 = api_client.reverse("alpha beta gamma")

    print(f"Second reverse result: {res2.json()['result']}")
    response = api_client.restore()
    assert response.status_code == 200
    data = response.json()

    assert data["result"] == "gamma beta alpha", f"{data}"


def test_content_type_is_json(api_client):
    """
    Test that all responses have application/json content-type.
    """
    response = api_client.reverse("json test")
    assert response.headers["Content-Type"].startswith("application/json")
    response = api_client.restore()
    assert response.headers["Content-Type"].startswith("application/json")
