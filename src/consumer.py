from faststream import FastStream
from src.producer import broker
from src.models.corrida_model import Corrida
from src.database.redis_client import redis_client
from src.database.mongo_client import corridas_collection
import asyncio

app_faststream = FastStream(broker)

@broker.subscriber("corridas_queue")
async def processar_corrida(corrida_data: dict):
    print(f"[Consumer] Recebido: Corrida {corrida_data.get('id_corrida')}")

    try:
        corrida = Corrida(**corrida_data)
    except Exception as e:
        print(f"Erro de validação: {e}")
        return


    chave_saldo = f"saldo:{corrida.motorista.nome.lower()}"
    novo_saldo = await redis_client.incrbyfloat(chave_saldo, corrida.valor_corrida)
    print(f"[Redis] Saldo de {corrida.motorista.nome} atualizado para R$ {novo_saldo:.2f}")

    existente = await corridas_collection.find_one({"id_corrida": corrida.id_corrida})
    if not existente:
        await corridas_collection.insert_one(corrida.dict())
        print(f"[Mongo] Corrida {corrida.id_corrida} salva com sucesso!")
    else:
        print(f"[Mongo] Corrida {corrida.id_corrida} já existe.")