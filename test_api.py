import pytest
from unittest.mock import patch
from api import Playlist, HEADERS, POST_HEADERS

@pytest.fixture
def mock_playlist_requests():
    with patch("api.requests") as mock_requests:
        yield mock_requests

def test_get_all_playlists(mock_playlist_requests):
    # Set up the mock response
    mock_response = mock_playlist_requests.get.return_value
    mock_response.text = "Mocked response"

    # Create an instance of the Playlist class
    playlist = Playlist()

    # Call the get_all method
    result = playlist.get_all()

    # Assert the result
    assert result == "Mocked response"
    mock_playlist_requests.get.assert_called_once_with(url="https://strapi.w3d.community/playlists?populate=*", headers=HEADERS)

def test_get_playlist_by_id(mock_playlist_requests):
    # Set up the mock response
    mock_response = mock_playlist_requests.get.return_value
    mock_response.text = "Mocked response"

    # Create an instance of the Playlist class
    playlist = Playlist()

    # Call the get_by_id method
    result = playlist.get_by_id("123")

    # Assert the result
    assert result == '"Mocked response"'
    mock_playlist_requests.get.assert_called_once_with(url="https://strapi.w3d.community/playlists/123?populate=*", headers=HEADERS)

def test_insert_playlist(mock_playlist_requests):
    # Set up the mock response
    mock_response = mock_playlist_requests.post.return_value
    mock_response.text = "Mocked response"

    # Create an instance of the Playlist class
    playlist = Playlist()

    # Call the insert method
    playlist_data = {"name": "Test Playlist"}
    result = playlist.insert(playlist_data)

    # Assert the result
    assert result == "Mocked response"
    
    expected_url = "https://strapi.w3d.community/playlists/createOrUpdate"
    expected_headers = POST_HEADERS
    expected_data = '{"name": "Test Playlist"}'
    
    assert mock_playlist_requests.post.call_count == 1
    actual_call_args = mock_playlist_requests.post.call_args
    actual_url, actual_kwargs = actual_call_args[0][0], actual_call_args[1]
    assert actual_url == expected_url
    assert actual_kwargs["headers"] == expected_headers
    assert actual_kwargs["data"] == expected_data




