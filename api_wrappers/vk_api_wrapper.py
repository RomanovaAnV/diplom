from api_wrappers import APIWrapper
import config

import requests


class VkAPIWrapper(APIWrapper):
    def __init__(self):
        pass

    @staticmethod
    def vk_api_req(method: str, **kwargs):
        service_token = config.vk_api_service_key
        version = "5.130"
        params = ""
        for k, v in kwargs.items():
            params += f"{k}={v}&"
        req = requests.post(f"https://api.vk.com/method/{method}?{params}v={version}&access_token={service_token}")
        print(req.json())
        return req.json()

    def get_photo_list(self, link: str) -> list:
        owner_id, album_id = link.split("album")[1].split("_")
        if album_id == "0":
            album_id = "profile"

        # сначала нужно узнать сколько всего фото в альбоме
        print(album_id, owner_id)

        photos_count = self.vk_api_req("photos.get", owner_id=owner_id,
                                       album_id=album_id, count=0).get('response').get('count')
        # if photos_count is None:
        #     return None

        photo_links = []
        part_length = 20
        for offset in range(0, photos_count, part_length):
            photos_api_resp = self.vk_api_req("photos.get", owner_id=owner_id,
                                              album_id=album_id, count=part_length, offset=offset)
            photo_items = photos_api_resp.get('response').get('items')
            for photo in photo_items:
                photo_links.append(photo.get('sizes')[-1].get('url'))

        return photo_links



