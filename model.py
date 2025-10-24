from pathlib import Path
import pandas as pd
from utils import  load_data, save_data, load_config

user_data = pd.DataFrame(columns=['user_name', 'x_user_token'])
user_data = user_data.astype({'user_name': 'string', 'x_user_token': 'string'})
graph_data = pd.DataFrame(columns=['user_name', 'graph_id'])
graph_data = graph_data.astype({'user_name': 'string', 'graph_id': 'string'})

config = load_config(file_path="./config.json")

def load_user_data(file_path: str):
    global user_data
    if Path(file_path).exists():
        user_data = load_data(file_path)
        user_data = user_data.astype({'user_name': 'string', 'x_user_token': 'string'})

def load_grap_data(file_path: str):
    global graph_data
    if Path(file_path).exists():
        graph_data = load_data(file_path)
        graph_data = graph_data.astype({'user_name': 'string', 'graph_id': 'string'})

def save_user(file_path: str):
    save_data(file_path, user_data)

def save_graph_data(file_path: str):
    save_data(file_path, graph_data)

def insert_user(user_name, x_user_token):
    user_data.loc[len(user_data)] = [user_name, x_user_token]

def insert_graph(user_name, graph_id):
    graph_data.loc[len(graph_data)] = [user_name, graph_id]

def get_user_token(user_name:str)->str:
    data = user_data.loc[user_data["user_name"] == user_name, "x_user_token"]
    return data.iloc[0] if not data.empty else ""