from fastapi import APIRouter

from playground_api.custom_types import T_Database
from playground_api.schemas import (
    ListMediansResponse,
    MedianResponse,
    NPSResponse,
)
from playground_api.services import CalculationService

router = APIRouter(prefix='/calculations', tags=['Calculations'])


@router.get('/nps', response_model=NPSResponse)
async def calculate_nps(session: T_Database):
    service = CalculationService(session)

    result = await service.calculate_nps()

    return NPSResponse(nps=result)


@router.get('/medians', response_model=ListMediansResponse)
async def calculate_medians(session: T_Database):
    service = CalculationService(session)

    medians = await service.calculate_medians()
    medians_response = []
    for pergunta in medians:
        median = medians[pergunta]
        medians_response.append(
            MedianResponse(pergunta=pergunta, median=median)
        )

    return ListMediansResponse(medians=medians_response)


@router.get('/answers_location/{location_name}')
async def count_answers_by_location(location_name: str, session: T_Database):
    service = CalculationService(session)

    answers_by_location = await service.interviewed_by_location(location_name)

    return answers_by_location
