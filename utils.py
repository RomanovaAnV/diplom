from api_wrappers import vk_api_wrapper, tg_api_wrapper, APIWrapper
from typing import Type
import face_recognition
import requests
import shutil
import os


def get_api_wrapper(resource_name: str) -> Type[APIWrapper]:
    """
    Возвращает нужный api wrapper по названию ресурса
    :param resource_name:
    :return: APIWrapper
    """
    api_wrappers_dict = {
        "VK": vk_api_wrapper.VkAPIWrapper,
        "TG": tg_api_wrapper.TgAPIWrapper,
    }

    if resource_name in api_wrappers_dict.keys():
        return api_wrappers_dict[resource_name]
    else:
        raise ValueError(f"No API wrapper for resource {resource_name}")


def make_dir(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def define_album_resource(album_link: str) -> str:
    # эту функцию надо улучшить
    if "vk" in album_link:
        return "VK"


def download_photos_to_dir(links: list, dir_path: str):
    for i, link in enumerate(links):
        r = requests.get(link, allow_redirects=True)
        open(f"{dir_path}/{i}", 'wb').write(r.content)


def find_face_in_album(album_link: str, request_dir: str):
    print("FACE SEARCHER STARTED")
    print("defining album resource type")
    album_resource_type = define_album_resource(album_link)
    print("getting wrapper for album type")
    api_wrapper = get_api_wrapper(album_resource_type)()
    print("getting photo link list")
    link_list = api_wrapper.get_photo_list(album_link)
    print(len(link_list), "links gotten")

    print("downloading photos from album")
    make_dir(f"{request_dir}/album")
    download_photos_to_dir(link_list, f"{request_dir}/album")
    print("getting face encodings")
    target_face_encodings = []
    for img_path in os.listdir(f"{request_dir}/required_face"):
        img_path = f"{request_dir}/required_face/{img_path}"
        target_face_img = face_recognition.load_image_file(img_path)
        target_face_encodings.append(face_recognition.face_encodings(target_face_img)[0])

    print("matching faces from album")
    for img_path in os.listdir(f"{request_dir}/album"):
        img_path = f"{request_dir}/album/{img_path}"
        photo = face_recognition.load_image_file(img_path)
        photo_faces_encodings = face_recognition.face_encodings(photo)
        print(f"PHOTO {img_path} has {len(photo_faces_encodings)} faces")

        face_matches = face_recognition.compare_faces(photo_faces_encodings, target_face_encodings[0])
        if True in face_matches:
            print("MATCH FOUND")
            make_dir(f"{request_dir}/matches/")
            shutil.copy(img_path, f"{request_dir}/matches/")
    print("DONE")


