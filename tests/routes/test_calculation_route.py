from http import HTTPStatus


def test_get_nps_should_calculate_nps(client, entrevistado):
    response = client.get('/calculations/nps')

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert isinstance(response_data['nps'], float)


def test_get_medians_should_calculate_questions_medians(client, entrevistado):
    question_size = 7
    response = client.get('/calculations/medians')

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    # Values are random, we cant check values
    assert len(response_data['medians']) == question_size


def test_get_count_by_area_should_return_answers_from_location(
    client, entrevistado
):
    response = client.get(
        f'/calculations/answers_location/{entrevistado.localidade}'
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data[entrevistado.localidade] == 1
