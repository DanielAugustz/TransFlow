import asyncio
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from src.models.corrida_model import Corrida
from src.producer import broker, publicar_corrida_finalizada
from src.consumer import app_faststream
from src.database.mongo_client import corridas_collection
from src.database.redis_client import redis_client

# Lifespan: Gerencia o ciclo de vida (Startup/Shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica de Retry (Insistência) para conectar ao RabbitMQ
    max_retries = 15
    wait_seconds = 5
    
    for attempt in range(max_retries):
        try:
            print(f"Tentando conectar ao RabbitMQ (Tentativa {attempt + 1}/{max_retries})...")
            await broker.start()
            print("Broker RabbitMQ Conectado com Sucesso!")
            break  # Conectou? Sai do loop!
        except Exception as e:
            # Se for a última tentativa, mostra o erro real
            if attempt == max_retries - 1:
                print(f"Erro fatal: Não foi possível conectar ao RabbitMQ após {max_retries} tentativas.")
                raise e
            # Se não, espera um pouco e tenta de novo
            print(f"Falha na conexão. Retentando em {wait_seconds} segundos...")
            await asyncio.sleep(wait_seconds)
            
    yield
    # Desliga a conexão quando o app fechar
    await broker.close()

app = FastAPI(title="TransFlow API", lifespan=lifespan)

# --- Endpoints ---

@app.post("/corridas", status_code=202)
async def cadastrar_corrida(corrida: Corrida):
    """
    Recebe a corrida e envia para processamento assíncrono (RabbitMQ)
    """
    try:
        # Publica no broker
        await publicar_corrida_finalizada(corrida.dict())
        return {"message": "Corrida recebida e enviada para processamento", "id": corrida.id_corrida}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/corridas")
async def listar_corridas():
    """
    Lista todas as corridas salvas no MongoDB
    """
    corridas = await corridas_collection.find().to_list(100)
    for c in corridas:
        c.pop("_id", None) 
    return corridas

@app.get("/corridas/{forma_pagamento}")
async def filtrar_corridas(forma_pagamento: str):
    """
    Filtra corridas pelo tipo de pagamento
    """
    query = {"forma_pagamento": forma_pagamento}
    corridas = await corridas_collection.find(query).to_list(100)
    for c in corridas:
        c.pop("_id", None)
    return corridas

@app.get("/saldo/{motorista}")
async def consultar_saldo(motorista: str):
    """
    Busca o saldo no Redis
    """
    chave = f"saldo:{motorista.lower()}"
    saldo = await redis_client.get(chave)
    
    if saldo is None:
        return {"motorista": motorista, "saldo": 0.0}
    
    return {"motorista": motorista, "saldo": float(saldo)}