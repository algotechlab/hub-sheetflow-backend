from src.core.exceptions.custom import NotFoundException


class GroupNotFoundException(NotFoundException):
    code = 'GROUP_NOT_FOUND_ERROR'


__all__ = [
    'GroupNotFoundException',
    'NotFoundException',
]
