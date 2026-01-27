from datetime import date

import pytest
from factory import Factory, Sequence, SubFactory
from factory.fuzzy import FuzzyDate, FuzzyInteger, FuzzyText
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from playground_api.app import app
from playground_api.database import get_session
from playground_api.models import (
    Entrevistado,
    Pergunta,
    Resposta,
    table_registry,
)

QUESTIONS = [
    'Interesse no Cargo',
    'Contribuição',
    'Aprendizado e Desenvolvimento',
    'Feedback',
    'Interação com Gestor',
    'Clareza sobre Possibilidades de Carreira',
    'Expectativa de Permanência',
    'eNPS',
]


@pytest.fixture(scope='session')
async def engine():
    with PostgresContainer('postgres:18-alpine', driver='psycopg') as postgres:
        engine = create_async_engine(postgres.get_connection_url())
        yield engine


@pytest.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


class PerguntaFactory(Factory):
    class Meta:
        model = Pergunta

    pergunta = Sequence(lambda n: QUESTIONS[n % len(QUESTIONS)])


class EntrevistadoFactory(Factory):
    class Meta:
        model = Entrevistado

    nome = FuzzyText()
    email = FuzzyText()
    email_corporativo = FuzzyText()
    genero = FuzzyText()
    geracao = FuzzyText()
    area = FuzzyText()
    cargo = FuzzyText()
    funcao = FuzzyText()
    localidade = FuzzyText()
    tempo_empresa = FuzzyText()
    n0_empresa = FuzzyText()
    n1_diretoria = FuzzyText()
    n2_gerencia = FuzzyText()
    n3_coordenacao = FuzzyText()
    n4_area = FuzzyText()


class RespostaFactory(Factory):
    class Meta:
        model = Resposta

    data = FuzzyDate(date.today())
    nota = FuzzyInteger(low=1, high=10)
    comentario = FuzzyText()
    pergunta = SubFactory(PerguntaFactory)
    entrevistado = SubFactory(EntrevistadoFactory)


@pytest.fixture
async def entrevistado(session):
    obj = EntrevistadoFactory()
    RespostaFactory.build_batch(8, entrevistado=obj)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)

    return obj


@pytest.fixture
async def resposta(session):
    obj = RespostaFactory()
    session.add(obj)
    await session.commit()
    await session.refresh(obj)

    return obj
