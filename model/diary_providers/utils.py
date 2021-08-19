from exceptions.providers import NoSuchDairyProvider
from model import MesDiary, FakeDiaryProvider
from model.diary_providers.base_diary_provider import BaseDiaryProvider

# List of Diary Providers. If you create ones, you should add it here
PROVIDERS = [
    MesDiary,
    FakeDiaryProvider
]


def get_provider_by_unique_name(unique_name: str) -> BaseDiaryProvider:
    """
    This method returns DiaryProvider by it's unique name
    :param unique_name: Unique name of provider, passed in headers
    :return: DiaryProvider class
    :raises NoSuchDiaryProvider if this provider doesn't exists
    """
    for provider in PROVIDERS:
        if provider.unique_name == unique_name:
            return provider
    raise NoSuchDairyProvider
