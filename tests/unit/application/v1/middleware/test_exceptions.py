import json

import pytest
from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.application.api.v1.middlewares.exceptions import custom_exception_handler
from src.core.exceptions.custom import (
    DomainException,
    InfrastructureException,
    MultipleException,
)


class DummyRequest(Request):
    def __init__(self):
        scope = {'type': 'http'}
        super().__init__(scope)


@pytest.mark.asyncio
async def test_handle_domain_exception():
    exc = DomainException('Erro de domínio')
    response: JSONResponse = await custom_exception_handler(DummyRequest(), exc)

    assert response.status_code == exc.status_code

    body = json.loads(response.body)
    assert body == {
        'code': exc.code,
        'message': 'Erro de domínio',
    }


@pytest.mark.asyncio
async def test_handle_infrastructure_exception():
    exc = InfrastructureException('Falha de infraestrutura')
    response: JSONResponse = await custom_exception_handler(DummyRequest(), exc)

    assert response.status_code == exc.status_code
    assert json.loads(response.body) == {
        'code': exc.code,
        'message': 'Falha de infraestrutura',
    }


@pytest.mark.asyncio
async def test_handle_generic_exception():
    exc = Exception('Erro genérico')
    response: JSONResponse = await custom_exception_handler(DummyRequest(), exc)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert json.loads(response.body) == {
        'code': 'HTTP_ERROR',
        'message': 'Erro genérico',
    }


@pytest.mark.asyncio
async def test_handle_multiple_exception():
    class FakeErr1(Exception):
        code = 'ERR_1'

    class FakeErr2(Exception):
        code = 'ERR_2'

    status = 422
    err1 = FakeErr1('msg1', 'field1')
    err2 = FakeErr2('msg2', 'field2')

    exc = MultipleException(err1, err2)
    exc.status_code = status

    response: JSONResponse = await custom_exception_handler(DummyRequest(), exc)

    assert response.status_code == status
    assert json.loads(response.body) == [
        {
            'field': 'field1',
            'code': 'ERR_1',
            'message': 'msg1',
        },
        {
            'field': 'field2',
            'code': 'ERR_2',
            'message': 'msg2',
        },
    ]
