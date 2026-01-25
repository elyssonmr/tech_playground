from datetime import date, datetime

from sqlalchemy import Date, ForeignKey, SmallInteger, String, Text, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class BaseModel(AsyncAttrs):
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


@table_registry.mapped_as_dataclass
class Entrevistado(BaseModel):
    __tablename__ = 'entrevistados'

    nome: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150))
    email_corporativo: Mapped[str] = mapped_column(String(150))
    genero: Mapped[str] = mapped_column(String(15))
    geracao: Mapped[str] = mapped_column(String(15))
    area: Mapped[str] = mapped_column(String(50))
    cargo: Mapped[str] = mapped_column(String(50))
    funcao: Mapped[str] = mapped_column(String(50))
    localidade: Mapped[str] = mapped_column(String(50))
    tempo_empresa: Mapped[str] = mapped_column(String(50))
    n0_empresa: Mapped[str] = mapped_column(String(50))
    n1_diretoria: Mapped[str] = mapped_column(String(50))
    n2_gerencia: Mapped[str] = mapped_column(String(50))
    n3_coordenacao: Mapped[str] = mapped_column(String(50))
    n4_area: Mapped[str] = mapped_column(String(50))

    respostas: Mapped[list['Resposta']] = relationship(
        init=False
    )


@table_registry.mapped_as_dataclass
class Pergunta(BaseModel):
    __tablename__ = 'perguntas'

    pergunta: Mapped[str] = mapped_column(String(100))
    respostas: Mapped[list['Resposta']] = relationship(
        init=False, back_populates='pergunta'
    )


@table_registry.mapped_as_dataclass
class Resposta(BaseModel):
    __tablename__ = 'respostas'

    data: Mapped[date] = mapped_column(Date(), index=True)
    nota: Mapped[int] = mapped_column(SmallInteger())
    comentario: Mapped[str] = mapped_column(Text(), nullable=True)
    pergunta_fk: Mapped[int] = mapped_column(ForeignKey('perguntas.id'))
    pergunta: Mapped[Pergunta] = relationship(
        init=False,
    )
    entrevistado_fk: Mapped[int] = mapped_column(
        ForeignKey('entrevistados.id'), index=True
    )
    entrevistado: Mapped[Entrevistado] = relationship(
        init=False, back_populates='respostas'
    )
