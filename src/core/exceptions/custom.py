from http import HTTPStatus


class DomainException(Exception):
    """
    Classe para exceções específicas de domínio na aplicação.
    """

    status_code: int = HTTPStatus.BAD_REQUEST.value
    code: str = 'DOMAIN_ERROR'


class MultipleException(Exception):
    """
    Classe para representar múltiplas exceções ocorridas simultaneamente.
    """

    status_code: int = HTTPStatus.BAD_REQUEST
    code: str = 'MULTIPLE_ERRORS'


class RequestValidationErrorException(Exception):
    """Raised when request validation fails."""

    status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY.value
    code: str = 'VALIDATION_ERROR'
