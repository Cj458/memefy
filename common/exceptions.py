from enum import Enum


class CustomExceptionError(str, Enum):

    REQUEST_UNPROCESSABLE = 'Ошибка при обработке запроса. Убедитесь в корректности body'
    MEME_NOT_FOUND = 'Meme не найден!'

