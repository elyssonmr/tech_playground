import pytest

from playground_api.services import CalculationService


@pytest.fixture
def service(session):
    return CalculationService(session)


async def test_calculate_nps_should_return_nps_data(service, entrevistado):
    nps_data = await service.calculate_nps()

    # Data is random, so we can't really compare values
    assert isinstance(nps_data, float)


async def test_calculate_no_data_nps_should_return_zero_nps_data(service):
    nps_data = await service.calculate_nps()

    assert nps_data == 0


async def test_calculate_means_should_return_means_per_question(
    service, entrevistado
):
    means_questions = 7

    means_data = await service.calculate_medians()

    assert isinstance(means_data, dict)
    # Data is random, so we can't really compare values
    assert len(means_data.keys()) == means_questions


async def test_calculate_no_data_means_should_return_empty_dict(service):
    means_data = await service.calculate_medians()

    assert isinstance(means_data, dict)
    # Data is random, so we can't really compare values
    assert len(means_data.keys()) == 0


async def test_count_locations_should_return_count_by_location(
    service, entrevistado
):
    location_count_data = await service.interviewed_by_location()

    assert isinstance(location_count_data, dict)
    # Data is random, so we can't really compare key values
    for key in location_count_data:
        assert location_count_data[key] == 1
