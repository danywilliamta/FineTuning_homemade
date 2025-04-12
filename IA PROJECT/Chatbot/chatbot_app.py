import os
import requests
import redis

from model_llm import OrderTool, DevisTool, StockTool
from flask import Flask, request
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_redis import RedisChatMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

openai_api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)

if not openai_api_key:
    raise ValueError("La clé API OpenAI est manquante ! Vérifiez votre fichier .env.")

REDIS_URL = os.getenv("REDIS_URL")
BASE_URL = os.getenv("BASE_URL")

redis_client = redis.Redis(host="redis", port=6379)

llm = ChatOpenAI(model="gpt-4", temperature=0)

system_message = SystemMessage(
    content="""Tu es un assistant intelligent spécialisé en gestion commerciale (devis, factures, commandes, stock).  
Analyse chaque demande et utilise un outil si nécessaire, même si un autre a été utilisé avant. 
Pour le modèle Product :
    - name : Le nom du produit (ex: "Disque de frein").
    - reference : La référence alphanumérique du produit (ex: "BG425Z", "90503").
    - quantite : La quantité du produit.
    - marque : La marque du produit.
Si l'information est insuffisante, demande des précisions.  
Traite chaque requête indépendamment de l'historique.  
Ne devine jamais de réponse ni d'information non fournie. Si tu ne sais pas, dis-le ou demande plus de détails.  
Réponds de manière concise, fluide et engageante (max. 2 phrases).
"""
)


@tool
def create_devis_tool(data: DevisTool) -> str:
    """Créer un devis pour un client."""
    return call_orm_function("/sale_order/create", data.model_dump())


@tool
def create_order_tool(data: OrderTool) -> str:
    """Créer une commande d'achat pour un fournisseur."""
    return call_orm_function("/purchase_order/create", data.model_dump())


@tool
def check_stock_tool(data: StockTool) -> str:
    """Vérifier le stock d'un produit."""
    return call_orm_function("/stock_quant/check", data.model_dump())


@tool
def edit_devis_tool(data: DevisTool, name_devis: str) -> str:
    """Modifier un devis."""
    payload = {"products": data.model_dump()['produits'], "client": data.client, "name": name_devis}
    return call_orm_function("/sale_order/edit", payload)


@tool
def edit_order_tool(data: OrderTool, name_order: str) -> str:
    """Modifier une commande."""
    payload = {"products": data.model_dump()['produits'], "fournisseur": data.fournisseur, "name": name_order}
    return call_orm_function("/purchase_order/edit", payload)


def call_orm_function(route, data):
    headers = {'Content-Type': 'application/json'}
    url = f"{BASE_URL}{route}"
    response = requests.post(url, json=data, headers=headers)
    return response.json().get('result').get('message')


tools = [create_devis_tool, create_order_tool, edit_devis_tool, check_stock_tool, edit_order_tool]
graph = create_react_agent(llm, tools=tools)


def get_memory(user_id: str):
    """Initialise la mémoire conversationnelle avec Redis pour un utilisateur."""
    chat_history = RedisChatMessageHistory(session_id=user_id, url="redis://redis:6379")
    return ConversationBufferMemory(chat_memory=chat_history, return_messages=True)


def get_user():
    url = f"{BASE_URL}/res_users/get_user"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json={}, headers=headers)
    user_id = response.json().get("result").get("user")
    return user_id


@app.route('/chatbot', methods=['POST'])
def chatbot():
    prompt_template = ChatPromptTemplate.from_messages(
        [
            system_message,
            MessagesPlaceholder(variable_name="history"),
            ("user", "{user_message}"),
        ]
    )

    if request.is_json:
        data = request.get_json()
        user_message = data["message"]
        user_id = get_user()
        memory = get_memory(user_id=str(user_id))

        memory.chat_memory.add_message(HumanMessage(content=user_message))

        inputs = {
            "messages": prompt_template.format(
                user_message=user_message, history=memory.load_memory_variables({})["history"]
            )
        }

        for s in graph.stream(inputs, stream_mode="values"):
            message = s["messages"][-1]
        memory.chat_memory.add_message(AIMessage(content=message.content))
        return {"response": message.content}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
