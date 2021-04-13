from api_wrappers import vk_api_wrapper, tg_api_wrapper, APIWrapper
from typing import Type


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
