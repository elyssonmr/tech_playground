from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from playground_api.database import get_session
from playground_api.models import Entrevistado, Resposta
from playground_api.schemas import (
    EntrevistadoResponse,
    ListEntrevistadosResponse,
    PaginationParams,
    RespostaResponse,
)

T_database = Annotated[AsyncSession, Depends(get_session)]
T_Pagination = Annotated[PaginationParams, Query()]

router = APIRouter(prefix='/responses', tags=['Responses'])


async def extract_perguntas_info(perguntas):
    pass


async def extract_respostas_info(respostas_db: list[Resposta]):
    respostas = []
    for resposta in respostas_db:
        pergunta = await resposta.awaitable_attrs.pergunta
        respostas.append(
            RespostaResponse(
                pergunta=pergunta.pergunta,
                nota=resposta.nota,
                comentario=resposta.comentario
            )
        )

    return respostas


async def extract_entrevistado_info(entrevistado: Entrevistado):
    respostas = await entrevistado.awaitable_attrs.respostas

    entrevistado_response = EntrevistadoResponse(
        id=entrevistado.id,
        nome=entrevistado.nome,
        email=entrevistado.email,
        email_corporativo=entrevistado.email_corporativo,
        genero=entrevistado.genero,
        geracao=entrevistado.geracao,
        area=entrevistado.area,
        cargo=entrevistado.cargo,
        funcao=entrevistado.funcao,
        localidade=entrevistado.localidade,
        tempo_empresa=entrevistado.tempo_empresa,
        n0_empresa=entrevistado.n0_empresa,
        n1_diretoria=entrevistado.n1_diretoria,
        n2_gerencia=entrevistado.n2_gerencia,
        n3_coordenacao=entrevistado.n3_coordenacao,
        n4_area=entrevistado.n4_area,
        respostas=await extract_respostas_info(respostas)
    )

    return entrevistado_response


@router.get(
    '',
    response_model=ListEntrevistadosResponse,
    status_code=HTTPStatus.OK
)
async def list_interviewed(pagination: T_Pagination, session: T_database):
    offset = pagination.page * pagination.limit
    query = select(Entrevistado).options(
        joinedload(
            Entrevistado.respostas
        ).joinedload(Resposta.pergunta)
    )
    query = query.offset(offset).limit(pagination.limit)

    entrevistados = (await session.scalars(query)).unique().all()
    entrevistados_response = []
    for entrevistado in entrevistados:
        entrevistados_response.append(
            await extract_entrevistado_info(entrevistado)
        )

    return ListEntrevistadosResponse(
        page=pagination.page,
        limit=pagination.limit,
        entrevistados=entrevistados_response
    )
