import os
import shutil

import face_recognition
import cv2


class Faces_Recognition():

    def __init__(self, photo_of_child_dir, photo_social_dir):
        self.error_mean = 0.5
        self.model = 'hog'  # можно было бы использовать CUDA, но нужен графический процессор от nvidia (модель cnn, быстрее и лучше)
        self.photo_of_child_dir = photo_of_child_dir
        self.child_faces = self.faces_of_child()
        self.photo_social_dir = photo_social_dir

    def enconding_photo(self, photo_path):
        """ Создание дескриптора фото """
        photo = face_recognition.load_image_file(photo_path)

        ph_locations = face_recognition.face_locations(photo, model=self.model)

        ph_encodings = face_recognition.face_encodings(photo, ph_locations)

        return ph_encodings

    def faces_of_child(self):
        """ Создание дескрипторов для фото ребенка """
        child_faces = []

        for filename in os.listdir(self.photo_of_child_dir):
            child_faces.append(self.enconding_photo(f'{self.photo_of_child_dir}/{filename}')[0])            

        return child_faces

    def check_photo_social(self):
        """ Модель для нахождения и сравнения лиц """
        for filename in os.listdir(self.photo_social_dir):
            mark = False

            encodings = self.enconding_photo(f'{self.photo_social_dir}/{filename}')

            for face_encoding in encodings:

                # Сравниваем лицо ребенка и лица на фотографии
                results = face_recognition.compare_faces(self.child_faces, face_encoding, self.error_mean)

                # Если нет совпадений на фотографиях, то удаляем это фото
                if True in results:
                    mark = True
                    break

            if not mark:
                os.remove(f'{self.photo_social_dir}/{filename}')
        
        return self.photos_to_archive()

    def photos_to_archive(self):
        """ Создание архива из всех подходящих фотографий """
        return shutil.make_archive(self.photo_social_dir, 'zip', self.photo_social_dir)

