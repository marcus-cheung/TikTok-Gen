"""Module providing a class for uploading to tiktok."""
# https://developers.tiktok.com/doc/content-posting-api-get-started/
# pylint: disable=missing-timeout, too-few-public-methods

import os
import json
import requests

from status import Status, DummyResponse

ACCOUNT_INFO_JSON = "Account_Info.json"

CREATOR_INFO_URL = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"
DIRECT_POST_URL = "https://open.tiktokapis.com/v2/post/publish/video/init/"
GET_VIDEO_STATUS_URL = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"


CHUNK_SIZE = 1048576  # 5MB

RESPONSE_OK = 200
RESPONSE_PARTIAL_CONTENT = 206
RESPONSE_CREATED = 201


def _direct_post_init_data(caption: str, video_size: int) -> dict:
    return {
        "post_info": {
            "title": caption,
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 0,
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,
            "chunk_size": CHUNK_SIZE,
            "total_chunk_count": max(video_size // CHUNK_SIZE, 1),
        },
    }


class UploadSession:
    """Allows for uploads onto tiktok page."""

    def __init__(self, username: str):
        self._login(username)
        self.auth_header = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        }
        self.max_video_post_duration_sec = 0

    def _login(self, username: str):
        with open(ACCOUNT_INFO_JSON, "r") as f:
            account_info = json.load(f)
            user_info = account_info[username]
            user_info[access]

    def _query_creator_info(self) -> Status:
        response = requests.post(url=CREATOR_INFO_URL, headers=self.auth_header)
        self.max_video_post_duration_sec = response.json()["data"][
            "max_video_post_duration_sec"
        ]
        return Status(response)

    def _direct_post_init(self, caption: str, video_size: int) -> Status:
        init_data = _direct_post_init_data(caption, video_size)

        response = requests.post(
            url=DIRECT_POST_URL, headers=self.auth_header, data=init_data
        )
        return Status(response)

    def _file_upload(self, upload_url: str, video_size: int, video_path: str) -> Status:
        response = DummyResponse()
        first_byte = 0
        while first_byte < video_size:
            end_byte = min(first_byte + CHUNK_SIZE - 1, video_size)
            header = {
                "Content-Range": f"bytes {first_byte}-{end_byte}/{video_size}",
                "Content-Type": "video/mp4",
            }
            status = requests.put(url=upload_url, headers=header, data=video_path)
            if status not in [
                RESPONSE_PARTIAL_CONTENT,
                RESPONSE_CREATED,
            ]:
                break
            first_byte = end_byte
        return Status(response)

    def _get_video_status(self, publish_id: str) -> Status:
        response = requests.post(
            url=GET_VIDEO_STATUS_URL,
            headers=self.auth_header,
            data={"publish_id": publish_id},
        )
        return Status(response)

    def direct_post(self, caption: str, video_path: str) -> Status:
        """Posts video with caption."""
        creator_info_status = self._query_creator_info()
        if creator_info_status != RESPONSE_OK:
            return creator_info_status
        video_size = os.path.getsize(video_path)
        init_status = self._direct_post_init(caption, video_size)
        if init_status != RESPONSE_OK:
            return init_status
        upload_url = init_status["data"]["upload_url"]
        file_upload_status = self._file_upload(upload_url, video_size, video_path)
        if file_upload_status != RESPONSE_CREATED:
            return file_upload_status
        publish_id = init_status["data"]["publish_id"]
        get_video_status = self._get_video_status(publish_id)
        return get_video_status


UploadSession("hi", "bny")
