from abc import ABC, abstractmethod


class APIWrapper(ABC):
    """
    Abstract API Wrapper
    """

    @abstractmethod
    def get_photo_list(self, link: str) -> list:  # должен возвращать список фото или директория со скачанными фото
        raise NotImplemented(f"get_photo_list not implemented for {self.__class__}")
