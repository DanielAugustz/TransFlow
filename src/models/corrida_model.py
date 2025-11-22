from pydantic import BaseModel, Field
from typing import Optional

class Passageiro(BaseModel):
    nome: str
    telefone: str

class Motorista(BaseModel):
    nome: str
    nota: float

class Corrida(BaseModel):
    id_corrida: str
    passageiro: Passageiro
    motorista: Motorista
    origem: str
    destino: str
    valor_corrida: float
    forma_pagamento: str

    class Config:
        json_schema_extra = {
            "example": {
                "id_corrida": "abc123",
                "passageiro": {"nome": "João", "telefone": "99999-1111"},
                "motorista": {"nome": "Carla", "nota": 4.8},
                "origem": "Centro",
                "destino": "Inoã",
                "valor_corrida": 35.50,
                "forma_pagamento": "DigitalCoin"
            }
        }