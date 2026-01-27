from http import HTTPStatus

DEFAULT_PAGE = 0
DEFAULT_LIMIT = 25


def test_get_entrevistados_should_return_interviewed(client, entrevistado):
    response = client.get('/responses/interviewed')

    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert len(response_json['entrevistados']) == 1
    assert response_json['page'] == DEFAULT_PAGE
    assert response_json['limit'] == DEFAULT_LIMIT
    assert response_json['entrevistados'][0]['nome'] == entrevistado.nome


def test_get_entrevistados_should_return_empty_list(client):
    response = client.get('/responses/interviewed')

    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert len(response_json['entrevistados']) == 0
    assert response_json['page'] == DEFAULT_PAGE
    assert response_json['limit'] == DEFAULT_LIMIT


async def test_get_pergunta_respostas_should_return_responses(
    client, resposta
):
    question = await resposta.awaitable_attrs.pergunta
    response = client.get(f'/responses/question/{question.id}')

    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert len(response_json['respostas']) == 1
    assert response_json['page'] == DEFAULT_PAGE
    assert response_json['limit'] == DEFAULT_LIMIT
    assert response_json['respostas'][0]['nota'] == resposta.nota


def test_get_response_location_should_return_responses(client, entrevistado):
    response = client.get(f'/responses/company/{entrevistado.localidade}')

    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert len(response_json['entrevistados']) == 1
    assert response_json['page'] == DEFAULT_PAGE
    assert response_json['limit'] == DEFAULT_LIMIT
    assert response_json['entrevistados'][0]['nome'] == entrevistado.nome


def test_get_flat_list_should_return_entrevistados_flat_list(
    client, entrevistado
):
    response = client.get('/responses/flat_list')

    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert len(response_json['entrevistados']) == 1
    assert response_json['page'] == DEFAULT_PAGE
    assert response_json['limit'] == DEFAULT_LIMIT
    assert response_json['entrevistados'][0]['nome'] == entrevistado.nome
    assert 'enps' in response_json['entrevistados'][0].keys()
