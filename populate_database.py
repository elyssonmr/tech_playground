import asyncio
from csv import DictReader
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from playground_api.database import async_engine
from playground_api.models import Entrevistado, Pergunta, Resposta


class DataCSVPopulator:
    def __init__(self):
        self._data = []
        self._empresa = None
        self._perguntas = []
        self._load_questions()

    def _read_csv_data(self):
        self._data = []
        with open('data.csv', encoding='utf-8') as csv_file:
            for row in DictReader(csv_file, delimiter=';'):
                self._data.append(row)

    def _extract_interviewed(self, answer_data):
        interviewed = Entrevistado(
            nome=answer_data['nome'],
            email=answer_data['email'],
            email_corporativo=answer_data['email_corporativo'],
            genero=answer_data['genero'],
            geracao=answer_data['geracao'],
            area=answer_data['area'],
            cargo=answer_data['cargo'],
            funcao=answer_data['funcao'],
            localidade=answer_data['localidade'],
            tempo_empresa=answer_data['tempo_de_empresa'],
            n0_empresa=answer_data['n0_empresa'],
            n1_diretoria=answer_data['n1_diretoria'],
            n2_gerencia=answer_data['n2_gerencia'],
            n3_coordenacao=answer_data['n3_coordenacao'],
            n4_area=answer_data['n4_area'],
        )

        return interviewed

    def _load_questions(self):
        self._perguntas.append(Pergunta('Interesse no Cargo'))
        self._perguntas.append(Pergunta('Contribuição'))
        self._perguntas.append(Pergunta('Aprendizado e Desenvolvimento'))
        self._perguntas.append(Pergunta('Feedback'))
        self._perguntas.append(Pergunta('Interação com Gestor'))
        self._perguntas.append(
            Pergunta('Clareza sobre Possibilidades de Carreira')
        )
        self._perguntas.append(Pergunta('Expectativa de Permanência'))
        self._perguntas.append(Pergunta('eNPS'))

    def _get_pergunta(self, question):
        for pergunta in self._perguntas:
            if pergunta.pergunta == question:
                return pergunta

        return None

    def _extract_answers(self, answer_data, interviewed):
        answer_keys = [
            ('Interesse no Cargo', 'Comentários - Interesse no Cargo'),
            ('Contribuição', 'Comentários - Contribuição'),
            (
                'Aprendizado e Desenvolvimento',
                'Comentários - Aprendizado e Desenvolvimento',
            ),
            ('Feedback', 'Comentários - Feedback'),
            ('Interação com Gestor', 'Comentários - Interação com Gestor'),
            (
                'Clareza sobre Possibilidades de Carreira',
                'Comentários - Clareza sobre Possibilidades de Carreira',
            ),
            (
                'Expectativa de Permanência',
                'Comentários - Expectativa de Permanência',
            ),
            ('eNPS', '[Aberta] eNPS'),
        ]

        responses = []
        for question_key, comment_key in answer_keys:
            response_date = datetime.strptime(
                answer_data['Data da Resposta'], '%d/%m/%Y'
            ).date()
            question = self._get_pergunta(question_key)
            response_value = int(answer_data[question_key])
            response_comment = answer_data[comment_key]
            response = Resposta(
                data=response_date,
                nota=response_value,
                comentario=response_comment,
                pergunta=question,
                entrevistado=interviewed
            )
            responses.append(response)

        return responses

    async def process(self):
        print('Reading CSV data')
        self._read_csv_data()
        total = len(self._data)
        print(f'Read {total} answers')
        print('Importing CSV Data to the database')
        print()
        for count, answer_data in enumerate(self._data, start=1):
            interviewed = self._extract_interviewed(answer_data)
            answers = self._extract_answers(answer_data, interviewed)

            async with AsyncSession(
                async_engine, expire_on_commit=False
            ) as session:
                session.add(interviewed)
                session.add_all(answers)
                await session.commit()

            print(f'Imported {count:03d} of {total}', end='\r', flush=True)

        print()
        print()
        print('Importing Finished!!')


async def main():
    populator = DataCSVPopulator()
    await populator.process()


if __name__ == '__main__':
    asyncio.run(main())
