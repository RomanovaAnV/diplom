from api_wrappers import vk_api_wrapper


def test_vk_api_wrapper():
    album_link = "https://vk.com/album-406973_0"
    # album_link = "https://vk.com/album-406973_281392572"
    vk_w = vk_api_wrapper.VkAPIWrapper()

    photos = vk_w.get_photo_list(album_link)
    print(photos)


if __name__ == "__main__":
    test_vk_api_wrapper()
