import pytest

from playground_api.schemas import EntrevistadoFlatResponse
from playground_api.services import ResponseService


@pytest.fixture
def service(session):
    return ResponseService(session)


async def test_query_entrevistados_should_return_list(service, entrevistado):
    entrevistados = await service.get_entrevistados(0, 5)

    assert len(entrevistados) == 1
    assert entrevistados[0].id == entrevistado.id
    assert entrevistados[0].nome == entrevistado.nome


async def test_query_pergunta_should_return_respostas(service, resposta):
    pergunta = await resposta.awaitable_attrs.pergunta

    respostas = await service.get_pergunta_respostas(0, 5, pergunta.id)

    assert len(respostas) == 1
    respostas[0].nota == resposta.nota
    respostas[0].pergunta == pergunta.pergunta


async def test_query_non_existing_pergunta_should_return_respostas(
    service, resposta
):
    non_exists_id = 99999

    respostas = await service.get_pergunta_respostas(0, 5, non_exists_id)

    assert len(respostas) == 0


async def test_query_company_should_return_responses(service, entrevistado):
    location = entrevistado.localidade
    entrevistados = await service.get_by_location(0, 5, location)

    assert len(entrevistados) == 1
    assert entrevistados[0].id == entrevistado.id
    assert entrevistados[0].nome == entrevistado.nome
    assert entrevistados[0].localidade == location


async def test_query_entrevistados_should_return_flat_list(
    service, entrevistado
):
    entrevistados = await service.get_entrevistados_flat_list(0, 5)

    assert len(entrevistados) == 1
    assert isinstance(entrevistados[0], EntrevistadoFlatResponse)
