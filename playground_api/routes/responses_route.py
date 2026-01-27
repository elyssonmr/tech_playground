from http import HTTPStatus

from fastapi import APIRouter

from playground_api.custom_types import T_Database, T_Pagination
from playground_api.schemas import (
    ListEntrevistadoFlatResponse,
    ListEntrevistadosResponse,
    ListRespostaResponse,
)
from playground_api.services import ResponseService

router = APIRouter(prefix='/responses', tags=['Responses'])


@router.get(
    '/interviewed',
    response_model=ListEntrevistadosResponse,
    status_code=HTTPStatus.OK,
)
async def list_by_interviewed(pagination: T_Pagination, session: T_Database):
    offset = pagination.page * pagination.limit
    service = ResponseService(session)

    entrevistados = await service.get_entrevistados(offset, pagination.limit)

    return ListEntrevistadosResponse(
        page=pagination.page,
        limit=pagination.limit,
        entrevistados=entrevistados,
    )


@router.get('/question/{question_id}', response_model=ListRespostaResponse)
async def list_by_question(
    question_id: int, pagination: T_Pagination, session: T_Database
):
    offset = pagination.page * pagination.limit
    service = ResponseService(session)
    respostas = await service.get_pergunta_respostas(
        offset, pagination.limit, question_id
    )

    return ListRespostaResponse(respostas=respostas)


@router.get('/company/{location}', response_model=ListEntrevistadosResponse)
async def list_by_company_location(
    location: str, pagination: T_Pagination, session: T_Database
):
    offset = pagination.page * pagination.limit
    service = ResponseService(session)
    entrevistados = await service.get_by_location(
        offset, pagination.limit, location
    )

    return ListEntrevistadosResponse(
        page=pagination.page,
        limit=pagination.limit,
        entrevistados=entrevistados,
    )


@router.get('/flat_list')
async def list_flat(pagination: T_Pagination, session: T_Database):
    offset = pagination.page * pagination.limit
    service = ResponseService(session)
    entrevistados = await service.get_entrevistados_flat_list(
        offset, pagination.limit
    )

    return ListEntrevistadoFlatResponse(
        page=pagination.page,
        limit=pagination.limit,
        entrevistados=entrevistados,
    )
