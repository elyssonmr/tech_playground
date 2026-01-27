from http import HTTPStatus

from playground_api.settings import Settings


def test_get_version_should_return_version(client):
    response = client.get('/version')

    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json == {'version': Settings().VERSION}
