TransFlow - Sistema de Corridas Assíncronas

O TransFlow é um protótipo de backend para gerenciamento de corridas urbanas desenvolvido para a disciplina de Sistemas Distribuídos. O projeto simula um cenário de alta concorrência onde a recepção da corrida é desacoplada do seu processamento financeiro e armazenamento, garantindo resiliência e escalabilidade.

Visão Geral da Arquitetura

O sistema é composto por microsserviços containerizados via Docker:

App (API Gateway + Consumer): Desenvolvido em Python (FastAPI)
Broker (RabbitMQ): Gerencia a fila `corridas_queue` para comunicação assíncrona.
Database (MongoDB):Banco NoSQL orientado a documentos para persistência do histórico de corridas.
Cache (Redis):Banco em memória para gestão de saldo dos motoristas em tempo real (operações atômicas).

---

1 Variáveis de Ambiente

O arquivo `.env` na raiz do projeto deve conter as seguintes configurações (já pré-configuradas para o ambiente Docker):

```ini
# Conexão com MongoDB Container: transflow-mongo
MONGO_URI=mongodb://mongo:27017

# Conexão com Redis Container: transflow-redis
REDIS_HOST=redis
REDIS_PORT=6379

# Conexão com RabbitMQ Container: transflow-rabbitmq
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/


2 Passos de Instalação
Pré-requisitos
Docker e Docker Compose instalados.

Execução
Clone este repositório:

Bash

git clone https://github.com/DanielAugustz/TransFlow.git
cd transflow
Suba o ambiente completo com um único comando:

Bash

docker-compose up --build
O sistema iniciará os contêineres do Mongo, Redis e RabbitMQ. A aplicação Python aguardará via script de resiliência até que todos os serviços estejam operacionais.

Acesse a documentação interativa Swagger UI:

http://localhost:8000/docs

3. Instruções de Uso e Testes
Utilize o Swagger UI /docs para realizar os testes abaixo:

Passo 1: Solicitar Corrida Processamento Assincrono
Simula um passageiro finalizando uma corrida. A API retorna 202 Accepted imediatamente e processa a transação em segundo plano.

Rota: POST /corridas

Payload de Exemplo:

JSON

{
  "destino": "São José",
  "forma_pagamento": "Forma de Pagamento",
  "id_corrida": "xxxx",
  "motorista": {
    "nome": "Daniel",
    "nota": 5.0
  },
  "origem": "Centro",
  "passageiro": {
    "nome": "Fabricio",
    "telefone": "99999-1111"
  },
  "valor_corrida": 42.3
}
Verificação: Observe os logs no terminal. Você verá mensagens coloridas indicando:

Recebimento do evento pelo Consumer.

Atualização de saldo no Redis.

Persistência no MongoDB.

Passo 2: Consultar Saldo Redis
Verifique se o valor da corrida foi creditado corretamente ao motorista.

Rota: GET /saldo/Carla

Resultado Esperado:
    Recebido: Corrida xxxx 
    Saldo de Daniel atualizado para R$ 126.90 
    Corrida xxxx salva com sucesso!


Passo 3: Listar Histórico MongoDB
Confira os dados persistidos no banco de dados.

Rota: GET /corridas

4. Captura de Tela do Sistema

![alt text](image.png)

