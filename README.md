# Assistente de Relacionamentos - API

Uma API FastAPI que funciona como um assistente de relacionamentos para homens, utilizando a API do Google Gemini para fornecer conselhos, sugestões de mensagens e análises de conversas de forma respeitosa e genuína.

## Funcionalidades

- **Chat Geral**: Conversas sobre relacionamentos e comunicação
- **Análise de Conversas**: Análise detalhada de mensagens trocadas
- **Sugestões de Mensagens**: Sugestões personalizadas para diferentes situações
- **Conselhos de Relacionamento**: Conselhos específicos e práticos

## Configuração

1. **Instalação das dependências:**
```bash
pip install -r requirements.txt
```

2. **Configuração das variáveis de ambiente:**
```bash
cp .env.example .env
```

3. **Configure sua chave da API do Gemini no arquivo `.env`:**
```
GEMINI_API_KEY=sua_chave_aqui
```

## Execução

```bash
python main.py
```

Ou usando uvicorn diretamente:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

### GET /
Endpoint raiz para verificar se a API está online.

### GET /health
Verificação de saúde da aplicação.

### POST /chat
Chat geral com o assistente.

**Body:**
```json
{
  "message": "Como iniciar uma conversa interessante?",
  "context": "Contexto opcional",
  "message_type": "general"
}
```

### POST /analyze-conversation
Análise de conversas existentes.

**Body:**
```json
{
  "messages": [
    "Oi, como você está?",
    "Oi! Estou bem, obrigada. E você?"
  ],
  "context": "Primeiro encontro"
}
```

### POST /suggest-message
Sugestões de mensagens para situações específicas.

**Body:**
```json
{
  "situation": "Quero convidar ela para um café",
  "relationship_stage": "conhecidos",
  "tone": "casual"
}
```

### POST /relationship-advice
Conselhos detalhados sobre relacionamentos.

**Body:**
```json
{
  "message": "Como demonstrar interesse sem ser invasivo?",
  "context": "Contexto da situação"
}
```

## Princípios Éticos

Este assistente foi desenvolvido com foco em:
- **Respeito**: Todas as sugestões promovem respeito mútuo
- **Consentimento**: Enfatiza a importância do consentimento
- **Autenticidade**: Encoraja comunicação genuína
- **Crescimento pessoal**: Foca no desenvolvimento de habilidades sociais saudáveis

## Estrutura do Projeto

```
/
├── main.py              # Aplicação principal FastAPI
├── models.py            # Modelos Pydantic
├── gemini_service.py    # Serviço de integração com Gemini
├── config.py            # Configurações da aplicação
├── exceptions.py        # Tratamento de exceções
├── requirements.txt     # Dependências
├── .env.example        # Exemplo de variáveis de ambiente
└── README.md           # Documentação
```