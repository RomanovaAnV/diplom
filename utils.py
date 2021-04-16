import random
import threading
from datetime import datetime

from api_wrappers import vk_api_wrapper, tg_api_wrapper, APIWrapper
from typing import Type
import face_recognition
import requests
import shutil
import os
import config
import dlib


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
        open(f"{dir_path}/{i}.jpg", 'wb').write(r.content)


def download_album_photos(album_link: str, request_dir: str) -> str:
    print("defining album resource type")
    album_resource_type = define_album_resource(album_link)
    print("getting wrapper for album type")
    api_wrapper = get_api_wrapper(album_resource_type)()
    print("getting photo link list")
    link_list = api_wrapper.get_photo_list(album_link)
    print(len(link_list), "links gotten")

    print("downloading photos from album")
    album_dir = f"{request_dir}{config.album_subdir}"
    make_dir(album_dir)
    download_photos_to_dir(link_list, album_dir)

    return album_dir


# def find_face_in_album(album_link: str, request_dir: str) -> str:
#     """
#     Находит совпадения и отдает путь к архиву
#     :param album_link:
#     :param request_dir:
#     :return:
#     """
#     print("FACE SEARCHER STARTED")
#     download_album_photos(album_link, request_dir)
#     album_dir = f"{request_dir}/{config.album_subdir}"
#     required_face_dir = f"{request_dir}/{config.searching_faces_subdir}"
#     matches_dir = f"{request_dir}/matches/"
#
#     print("getting face encodings")
#     target_face_encodings = []
#     for img_path in os.listdir(required_face_dir):
#         img_path = f"{required_face_dir}/{img_path}"
#         target_face_img = face_recognition.load_image_file(img_path)
#         target_face_encodings.extend(face_recognition.face_encodings(target_face_img))
#
#     print("matching faces from album")
#     for img_path in os.listdir(album_dir):
#         img_path = f"{album_dir}/{img_path}"
#         photo = face_recognition.load_image_file(img_path)
#         photo_faces_encodings = face_recognition.face_encodings(photo)
#         print(f"PHOTO {img_path} has {len(photo_faces_encodings)} faces")
#
#         if len(target_face_encodings) == 0:
#             print("NO FACES ON TARGET IMAGE")
#             return "no faces found"
#         face_matches = face_recognition.compare_faces(photo_faces_encodings, target_face_encodings[0])
#         if True in face_matches:
#             print("MATCH FOUND")
#             make_dir(matches_dir)
#             shutil.copy(img_path, matches_dir)
#     print("DONE")
#     return zip_request_matches(request_dir)


def find_face_and_make_archive(album_link: str, request_id: int, thread_storage: dict, ) -> str:
    start_dt = datetime.now()

    thread_storage['statuses'][int(request_id)] = "start"

    print("CUDA STATUS", dlib.DLIB_USE_CUDA)
    model = "cnn" if dlib.DLIB_USE_CUDA else "hog"
    print("USING MODEL", model)
    print("FACE SEARCHER STARTED")
    request_dir = define_request_dir(request_id)

    thread_storage['statuses'][int(request_id)] = "Скачивание альбома..."

    download_album_photos(album_link, request_dir)
    album_dir = f"{request_dir}/{config.album_subdir}"
    required_face_dir = f"{request_dir}{config.searching_faces_subdir}"
    matches_dir = f"{request_dir}/matches/"

    album_downloading_time = datetime.now() - start_dt
    print("На счкчивание альбома затрачено", album_downloading_time.seconds, "секунд")

    thread_storage['statuses'][int(request_id)] = "Сбор данных с ваших фотографий..."
    print("getting face encodings")
    target_face_encodings = []
    for img_path in os.listdir(required_face_dir):
        img_path = f"{required_face_dir}/{img_path}"
        target_face_img = face_recognition.load_image_file(img_path)
        target_face_locations = face_recognition.face_locations(target_face_img, model=model)
        target_face_encodings.extend(face_recognition.face_encodings(target_face_img, target_face_locations))

    print("matching faces from album")
    thread_storage['statuses'][int(request_id)] = "Поиск лица в альбоме..."
    for img_path in os.listdir(album_dir):
        img_path = f"{album_dir}/{img_path}"
        unknown_photo = face_recognition.load_image_file(img_path)
        unknown_face_locations = face_recognition.face_locations(unknown_photo, model=model)
        unknown_faces_encodings = face_recognition.face_encodings(unknown_photo, unknown_face_locations)
        print(f"PHOTO {img_path} has {len(unknown_faces_encodings)} faces")

        if len(target_face_encodings) == 0:
            print("NO FACES ON TARGET IMAGE")
            return "no faces found"
        face_matches = []
        for target_face in target_face_encodings:
            face_recognition.compare_faces(unknown_faces_encodings, target_face)
            results = face_recognition.compare_faces(unknown_faces_encodings, target_face, tolerance=0.55)
            face_matches.extend(results)

        if True in face_matches:
            print("MATCH FOUND")
            make_dir(matches_dir)
            shutil.copy(img_path, matches_dir)
    print("DONE")
    thread_storage['statuses'][int(request_id)] = "done"
    return zip_request_matches(request_dir)


def generate_request_id() -> int:
    request_id = random.randint(0, 1_000_000_000)
    while os.path.exists(config.upload_dir+"/"+str(request_id)):
        request_id = random.randint(0, 1000000)
    return request_id


def zip_request_matches(request_dir: str) -> str:
    print("making archive")
    zip_archive_path = request_dir+"/"+config.result_archive_name
    shutil.make_archive(zip_archive_path, "zip", request_dir+"/"+config.matched_photos_subdir)
    return zip_archive_path+".zip"


def check_file_exists(file_path: str) -> bool:
    exists = os.path.exists(file_path)
    is_file = os.path.isfile(file_path)
    return exists and is_file


def define_request_dir(request_id) -> str:
    request_dir_path = config.upload_dir + "/" + str(request_id)
    return request_dir_path

# class FaceSearchingThread(threading.Thread):
#     def __init__(self, **kwargs):
#         self.status = ""
#         super().__init__(**kwargs)
#
#     def run(self):
#         print("123")
#         self.status = random.randint(5, 23234)
#         return

