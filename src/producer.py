import os
from faststream.rabbit import RabbitBroker
from dotenv import load_dotenv

load_dotenv()

broker = RabbitBroker(os.getenv("RABBITMQ_URL"))

async def publicar_corrida_finalizada(dados_corrida: dict):
    """
    Publica o evento na fila 'corridas_queue'
    """
    await broker.publish(
        dados_corrida,
        queue="corridas_queue"
    )