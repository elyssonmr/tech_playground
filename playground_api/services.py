import statistics

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from playground_api.models import Entrevistado, Pergunta, Resposta
from playground_api.schemas import (
    EntrevistadoFlatResponse,
    EntrevistadoResponse,
    RespostaResponse,
)


class ResponseService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def _extract_respostas(self, respostas_db):
        respostas = []
        for resposta in respostas_db:
            pergunta = await resposta.awaitable_attrs.pergunta
            respostas.append(
                RespostaResponse(
                    pergunta=pergunta.pergunta,
                    nota=resposta.nota,
                    comentario=resposta.comentario,
                )
            )

        return respostas

    async def _extract_entrevistado(self, entrevistado):
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
            respostas=await self._extract_respostas(respostas),
        )

        return entrevistado_response

    async def _extract_resposta(self, resposta_db: Resposta):
        pergunta = await resposta_db.awaitable_attrs.pergunta
        return RespostaResponse(
            pergunta=pergunta.pergunta,
            nota=resposta_db.nota,
            comentario=resposta_db.comentario,
        )

    async def _get_response_date(self, entrevistado_db: Entrevistado):
        respostas = await entrevistado_db.awaitable_attrs.respostas

        return respostas[0].data

    async def _process_answered_questions(self, entrevistado_db: Entrevistado):
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

    async def _extract_flat_entrevistado(self, entrevistado_db: Entrevistado):
        response_date = await self._get_response_date(entrevistado_db)
        answered_questions = await self._process_answered_questions(
            entrevistado_db
        )
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
            comentario_interesse_cargo=answered_questions[
                'comentario_interesse_cargo'
            ],
            contribuicao=answered_questions['contribuicao'],
            comentario_contribuicao=answered_questions[
                'comentario_contribuicao'
            ],
            aprendizado_desenvolvimento=answered_questions[
                'aprendizado_desenvolvimento'
            ],
            comentario_aprendizado_desenvolvimento=answered_questions[
                'comentario_aprendizado_desenvolvimento'
            ],
            feedback=answered_questions['feedback'],
            comentario_feedback=answered_questions['comentario_feedback'],
            interacao_gestor=answered_questions['interacao_gestor'],
            comentario_interacao_gestor=answered_questions[
                'comentario_interacao_gestor'
            ],
            clareza_carreira=answered_questions['clareza_carreira'],
            comentario_clareza_carreira=answered_questions[
                'comentario_clareza_carreira'
            ],
            expectativa_permanencia=answered_questions[
                'expectativa_permanencia'
            ],
            comentario_expectativa_permanencia=answered_questions[
                'comentario_expectativa_permanencia'
            ],
            enps=answered_questions['enps'],
            comentario_enps=answered_questions['comentario_enps'],
        )

    async def _query_entrevistados(self, offset: int, limit: int):
        query = select(Entrevistado).options(
            joinedload(Entrevistado.respostas).joinedload(Resposta.pergunta)
        )
        query = query.offset(offset).limit(limit)

        return (await self._session.scalars(query)).unique().all()

    async def get_entrevistados(self, offset: int, limit: int):
        entrevistados = await self._query_entrevistados(offset, limit)

        entrevistados_response = []
        for entrevistado in entrevistados:
            entrevistados_response.append(
                await self._extract_entrevistado(entrevistado)
            )

        return entrevistados_response

    async def get_pergunta_respostas(
        self, offset: int, limit: int, question_id: int
    ):
        query = select(Resposta).options(joinedload(Resposta.pergunta))
        query = query.offset(offset).limit(limit)
        query = query.filter(Resposta.pergunta_fk == question_id)

        respostas = (await self._session.scalars(query)).unique().all()

        respostas_response = []
        for resposta in respostas:
            respostas_response.append(await self._extract_resposta(resposta))

        return respostas_response

    async def get_by_location(self, offset: int, limit: int, location: str):
        query = select(Entrevistado).options(
            joinedload(Entrevistado.respostas).joinedload(Resposta.pergunta)
        )
        query = query.offset(offset).limit(limit)
        query = query.filter(Entrevistado.localidade == location)

        entrevistados = (await self._session.scalars(query)).unique().all()

        entrevistados_response = []
        for entrevistado in entrevistados:
            entrevistados_response.append(
                await self._extract_entrevistado(entrevistado)
            )

        return entrevistados_response

    async def get_entrevistados_flat_list(self, offset: int, limit: int):
        entrevistados_db = await self._query_entrevistados(offset, limit)
        entrevistados = []
        for entrevistado in entrevistados_db:
            entrevistados.append(
                await self._extract_flat_entrevistado(entrevistado)
            )

        return entrevistados


class CalculationService:
    def __init__(self, session):
        self._session = session

    async def calculate_nps(self):
        # Performing Database Calculation
        min_promoters = 9
        max_detractors = 6
        promoter_calc = case((Resposta.nota >= min_promoters, 1))
        detractor_calc = case((Resposta.nota <= max_detractors, 1))

        query = select(
            func.count(Resposta.id).label('total'),
            func.count(promoter_calc).label('promoters'),
            func.count(detractor_calc).label('detractors'),
        ).filter(Pergunta.pergunta == 'eNPS')

        result = (await self._session.execute(query)).one()

        if result.total == 0:
            return 0

        nps = (
            (result.promoters / result.total)
            - (result.detractors / result.total)
        ) * 100
        return round(nps, 2)

    async def calculate_medians(self):
        query = select(Pergunta).options(joinedload(Pergunta.respostas))
        query = query.filter(Pergunta.pergunta != 'eNPS')

        perguntas = (await self._session.scalars(query)).unique().all()

        medians = {}

        for pergunta in perguntas:
            respostas = await pergunta.awaitable_attrs.respostas
            medians[pergunta.pergunta] = statistics.median([
                r.nota for r in respostas
            ])

        return medians

    async def interviewed_by_location(self, location):
        # Performing Database Calculation
        query = (
            select(
                Entrevistado.localidade,
                func.count(Entrevistado.localidade).label('count'),
            )
            .group_by(Entrevistado.localidade)
            .order_by(func.count(Entrevistado.localidade).desc())
        ).filter(Entrevistado.localidade == location)

        result = (await self._session.execute(query)).all()

        return dict(result)
