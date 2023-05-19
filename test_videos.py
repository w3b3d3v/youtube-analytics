from unittest import mock
from videos import get_playlists, get_videos_by_playlist_id, process_playlists, process_videos
import api
import json
import traceback

def test_get_playlists():
    # Mock the YouTube object
    youtube_mock = mock.Mock()
    youtube_mock.playlists().list().execute.return_value = {
        "items": [
            {
                "id": "playlist_id1",
                "snippet": {
                    "title": "Playlist 1"
                }
            },
            {
                "id": "playlist_id2",
                "snippet": {
                    "title": "Playlist 2"
                }
            }
        ]
    }

    # Call the get_playlists function
    playlists = get_playlists(youtube_mock, "channel_id", max_results=10)

    # Assert the expected results
    assert len(playlists) == 2
    assert playlists[0]["id"] == "playlist_id1"
    assert playlists[0]["snippet"]["title"] == "Playlist 1"
    assert playlists[1]["id"] == "playlist_id2"
    assert playlists[1]["snippet"]["title"] == "Playlist 2"

def test_get_videos_by_playlist_id():
    # Mock the YouTube object
    youtube_mock = mock.Mock()
    youtube_mock.playlistItems().list().execute.return_value = {
        "items": [
            {
                "id": "video_id1",
                "snippet": {
                    "title": "Video 1"
                }
            },
            {
                "id": "video_id2",
                "snippet": {
                    "title": "Video 2"
                }
            }
        ]
    }

    # Call the get_videos_by_playlist_id function
    videos = get_videos_by_playlist_id("playlist_id", youtube_mock, max_results=10)

    # Assert the expected results
    assert len(videos) == 2
    assert videos[0]["id"] == "video_id1"
    assert videos[0]["snippet"]["title"] == "Video 1"
    assert videos[1]["id"] == "video_id2"
    assert videos[1]["snippet"]["title"] == "Video 2"

def test_process_playlists():
    # Mock the YouTube object
    youtube_mock = mock.Mock()
    
    # Mock the get_playlists function
    get_playlists_mock = mock.Mock(return_value=[
        {
            "id": "playlist_id1",
            "snippet": {
                "title": "Playlist 1",
                "publishedAt": "2023-05-19T12:00:00Z"
            }
        },
        {
            "id": "playlist_id2",
            "snippet": {
                "title": "Playlist 2",
                "publishedAt": "2023-05-18T12:00:00Z"
            }
        }
    ])
    
    # Set up the patch for the get_playlists function
    with mock.patch("videos.get_playlists", get_playlists_mock):
        # Create a mock object for the Playlist class
        playlist_mock = mock.Mock(spec=api.Playlist)
        api.Playlist = playlist_mock
        
        # Call the process_playlists function
        process_playlists(youtube_mock)
        
    # Assert that the get_playlists function was called with the correct arguments
    get_playlists_mock.assert_called_once_with(youtube=youtube_mock, channel_id="UCP8Qy0VXJUzE8MCJdqARrtA")
    
    # Assert that the insert method of Playlist class was called with the correct arguments
    expected_calls = [
        mock.call({
            "data": {
                "playlist_id": "playlist_id1",
                "playlist_name": "Playlist 1",
                "playlist_published_at": "2023-05-19"
            }
        }),
        mock.call({
            "data": {
                "playlist_id": "playlist_id2",
                "playlist_name": "Playlist 2",
                "playlist_published_at": "2023-05-18"
            }
        })
    ]
    playlist_mock().insert.assert_has_calls(expected_calls, any_order=True)

