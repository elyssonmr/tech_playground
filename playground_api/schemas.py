from datetime import date

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(0, ge=0)
    limit: int = Field(25, gt=0, le=100)


class EntrevistadoResponse(BaseModel):
    id: int
    nome: str
    email: str
    email_corporativo: str
    genero: str
    geracao: str
    area: str
    cargo: str
    funcao: str
    localidade: str
    tempo_empresa: str
    n0_empresa: str
    n1_diretoria: str
    n2_gerencia: str
    n3_coordenacao: str
    n4_area: str
    respostas: list['RespostaResponse'] | None


class ListEntrevistadosResponse(PaginationParams):
    entrevistados: list[EntrevistadoResponse]


class RespostaResponse(BaseModel):
    pergunta: str
    nota: int
    comentario: str


class ListRespostaResponse(PaginationParams):
    respostas: list[RespostaResponse]


class EntrevistadoFlatResponse(BaseModel):
    nome: str
    email: str
    email_corporativo: str
    area: str
    cargo: str
    localidade: str
    tempo_empresa: str
    genero: str
    n0_empresa: str
    n1_diretoria: str
    n2_gerencia: str
    n3_coordenacao: str
    n4_area: str
    data_resposta: date
    interesse_cargo: int
    comentario_interesse_cargo: str
    contribuicao: int
    comentario_contribuicao: str
    aprendizado_desenvolvimento: int
    comentario_aprendizado_desenvolvimento: str
    feedback: int
    comentario_feedback: str
    interacao_gestor: int
    comentario_interacao_gestor: str
    clareza_carreira: int
    comentario_clareza_carreira: str
    expectativa_permanencia: int
    comentario_expectativa_permanencia: str
    enps: int
    comentario_enps: str


class ListEntrevistadoFlatResponse(PaginationParams):
    entrevistados: list[EntrevistadoFlatResponse]


class NPSResponse(BaseModel):
    nps: float


class MedianResponse(BaseModel):
    pergunta: str
    median: int


class ListMediansResponse(BaseModel):
    medians: list[MedianResponse]


class CountResponse(BaseModel):
    count: int
