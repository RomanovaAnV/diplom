import os

from checkphoto import Faces_Recognition

def search_child_photos(photo_of_child_dir, photo_social_dir):
    """ 
    Input: путь к папке с фотографиями ребенка, путь к папке с фотографиями из соцсетей
    Output: путь к архиву архива
    """

    fr = Faces_Recognition(photo_of_child_dir, photo_social_dir)
    name_archive = fr.check_photo_social()

    for filename in os.listdir(photo_of_child_dir):
        os.remove(f'{photo_of_child_dir}/{filename}')

    return name_archive
