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
    ListRespostaResponse,
    PaginationParams,
    RespostaResponse,
    EntrevistadoFlatResponse,
    ListEntrevistadoFlatResponse
)

T_Database = Annotated[AsyncSession, Depends(get_session)]
T_Pagination = Annotated[PaginationParams, Query()]

router = APIRouter(prefix='/responses', tags=['Responses'])


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


async def extract_resposta_info(resposta_db: Resposta):
    pergunta = await resposta_db.awaitable_attrs.pergunta
    return RespostaResponse(
        pergunta=pergunta.pergunta,
        nota=resposta_db.nota,
        comentario=resposta_db.comentario
    )


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

async def get_response_date(entrevistado_db: Entrevistado):
    respostas = await entrevistado_db.awaitable_attrs.respostas

    return respostas[0].data

async def process_answered_questions(entrevistado_db: Entrevistado):
    answered_keys = {
        'Interesse no Cargo': 'interesse_cargo',
        'Contribuição': 'contribuicao',
        'Aprendizado e Desenvolvimento': 'aprendizado_desenvolvimento',
        'Feedback': 'feedback',
        'Interação com Gestor': 'interacao_gestor',
        'Clareza sobre Possibilidades de Carreira': 'clareza_carreira',
        'Expectativa de Permanência': 'expectativa_permanencia',
        'eNPS': 'enps',
    }
    respostas = await entrevistado_db.awaitable_attrs.respostas

    answered_questions_map = {}
    for resposta in respostas:
        pergunta = await resposta.awaitable_attrs.pergunta
        key = answered_keys.get(pergunta.pergunta)
        answered_questions_map[key] = resposta.nota
        answered_questions_map[f'comentario_{key}'] = resposta.comentario

    return answered_questions_map


async def extract_flat_entrevistado_info(entrevistado_db: Entrevistado):
    response_date = await get_response_date(entrevistado_db)
    answered_questions = await process_answered_questions(entrevistado_db)
    return EntrevistadoFlatResponse(
        id=entrevistado_db.id,
        nome=entrevistado_db.nome,
        email=entrevistado_db.email,
        email_corporativo=entrevistado_db.email_corporativo,
        genero=entrevistado_db.genero,
        geracao=entrevistado_db.geracao,
        area=entrevistado_db.area,
        cargo=entrevistado_db.cargo,
        funcao=entrevistado_db.funcao,
        localidade=entrevistado_db.localidade,
        tempo_empresa=entrevistado_db.tempo_empresa,
        n0_empresa=entrevistado_db.n0_empresa,
        n1_diretoria=entrevistado_db.n1_diretoria,
        n2_gerencia=entrevistado_db.n2_gerencia,
        n3_coordenacao=entrevistado_db.n3_coordenacao,
        n4_area=entrevistado_db.n4_area,
        data_resposta=response_date,
        interesse_cargo=answered_questions['interesse_cargo'],
        comentario_interesse_cargo=answered_questions['comentario_interesse_cargo'],
        contribuicao=answered_questions['contribuicao'],
        comentario_contribuicao=answered_questions['comentario_contribuicao'],
        aprendizado_desenvolvimento=answered_questions['aprendizado_desenvolvimento'],
        comentario_aprendizado_desenvolvimento=answered_questions['comentario_aprendizado_desenvolvimento'],
        feedback=answered_questions['feedback'],
        comentario_feedback=answered_questions['comentario_feedback'],
        interacao_gestor=answered_questions['interacao_gestor'],
        comentario_interacao_gestor=answered_questions['comentario_interacao_gestor'],
        clareza_carreira=answered_questions['clareza_carreira'],
        comentario_clareza_carreira=answered_questions['comentario_clareza_carreira'],
        expectativa_permanencia=answered_questions['expectativa_permanencia'],
        comentario_expectativa_permanencia=answered_questions['comentario_expectativa_permanencia'],
        enps=answered_questions['enps'],
        comentario_enps=answered_questions['comentario_enps'],
    )


@router.get(
    '/interviewed',
    response_model=ListEntrevistadosResponse,
    status_code=HTTPStatus.OK
)
async def list_by_interviewed(pagination: T_Pagination, session: T_Database):
    offset = pagination.page * pagination.limit
    query = select(Entrevistado).options(
        joinedload(Entrevistado.respostas).joinedload(Resposta.pergunta)
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


@router.get('/question/{question_id}', response_model=ListRespostaResponse)
async def list_by_question(
    question_id: int, pagination: T_Pagination, session: T_Database
):
    offset = pagination.page * pagination.limit

    query = select(Resposta).options(joinedload(Resposta.pergunta))
    query = query.offset(offset).limit(pagination.limit)
    query = query.filter(Resposta.pergunta_fk == question_id)

    respostas_db = (await session.scalars(query)).unique().all()

    respostas = []
    for resposta in respostas_db:
        respostas.append(
            await extract_resposta_info(resposta)
        )

    return ListRespostaResponse(
        respostas=respostas
    )


@router.get('/company/{location}', response_model=ListEntrevistadosResponse)
async def list_by_company_location(
    location: str, pagination: T_Pagination, session: T_Database
):
    offset = pagination.page * pagination.limit

    query = select(Entrevistado).options(
        joinedload(Entrevistado.respostas).joinedload(Resposta.pergunta)
    )
    query = query.offset(offset).limit(pagination.limit)
    query = query.filter(Entrevistado.localidade == location)

    entrevistados_db = (await session.scalars(query)).unique().all()

    entrevistados = []
    for entrevistado in entrevistados_db:
        entrevistados.append(
            await extract_entrevistado_info(entrevistado)
        )

    return ListEntrevistadosResponse(
        page=pagination.page,
        limit=pagination.limit,
        entrevistados=entrevistados
    )

@router.get('/flat_list')
async def list_flat(
    pagination: T_Pagination, session: T_Database
):
    offset = pagination.page * pagination.limit
    query = select(Entrevistado).options(
        joinedload(Entrevistado.respostas).joinedload(Resposta.pergunta)
    )
    query = query.offset(offset).limit(pagination.limit)
    entrevistados_db = (await session.scalars(query)).unique().all()
    entrevistados = []
    for entrevistado in entrevistados_db:
        entrevistados.append(
            await extract_flat_entrevistado_info(entrevistado)
        )

    return ListEntrevistadoFlatResponse(
        page=pagination.page,
        limit=pagination.limit,
        entrevistados=entrevistados
    )
