import os
from unittest import mock
import pytest
from auth import youtube_authenticate

@pytest.fixture
def mock_build():
    with mock.patch("auth.build") as mock_build:
        yield mock_build


def test_youtube_authenticate(mock_build):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    os.environ["YOUTUBE_API_KEY"] = "my_api_key"

    result = youtube_authenticate()
    mock_build.assert_called_once_with("youtube", "v3", developerKey="my_api_key")

    assert isinstance(result, mock.Mock)
