import model
from utils import call_api
import pyinputplus as pyip
from user import User
from graph import Graph
from typing import Optional


is_run = True
user: Optional[User] = None
graph: Optional[Graph] = None
model.load_user_data(file_path="./data/user.csv")
model.load_grap_data(file_path="./data/graph.csv")

# user lib instead
# def validate_user_input_int(message: str, valid_input: list):
#     while True:
#         try:
#             user_choice = input(message)
#             if int(user_choice) not in valid_input:
#                 raise Exception("Please type the correct option value")
#             return int(user_choice)
#         except TypeError as e:
#             print(f"Please type a numeric value only")
#         except Exception as e:
#             print(e)

# def validate_user_input_str(message: str, valid_input: list):
#     while True:
#         try:
#             user_choice = input(message)
#             if user_choice not in valid_input:
#                 raise Exception("Please type the correct option value")
#             return user_choice
#         except TypeError as e:
#             print(f"Please type a numeric value only")
#         except Exception as e:
#             print(e)

def create_new_user():
    global user
    user_name = pyip.inputStr(prompt="User name for this service:")
    token = pyip.inputStr(prompt="Token for this service:")
    agree_terms_of_service = pyip.inputChoice(
        prompt="Specify yes or no whether you agree to the terms of service.",
        choices= ["yes", "no"]
    )
    not_minor = pyip.inputChoice(
        prompt="Specify yes or no as to whether you are not a minor or if you are a minor and you have the parental consent of using this service.",
        choices= ["yes", "no"]
    )

    request_body = model.config["pixela_api"]["create_user"]["request_body"]
    request_body["username"] = user_name
    request_body["token"] = token
    request_body["agreeTermsOfService"] = agree_terms_of_service
    request_body["notMinor"] = not_minor

    response = call_api(
        method= model.config["pixela_api"]["create_user"]["method"],
        url= model.config["pixela_api"]["create_user"]["endpoint"],
        json = request_body
    )

    try:
        if response["isSuccess"]:
            model.insert_user(user_name= user_name, x_user_token= token)
            user = User(user_name, token)
            print(response["message"])
            print(f"Welcome {getattr(user,"user_name")}")
        else:
            print(response["message"])
    except KeyError as e:
        print(response["error"])

def login():
    global user
    user_name = pyip.inputStr(prompt="User name login:")
    token = pyip.inputStr(prompt="Token:")

    selection_user_data = model.user_data[
        (model.user_data["user_name"] == user_name)
            & (model.user_data["x_user_token"]== token)
    ]

    if not selection_user_data.empty:
        user = User(user_name, token)
        print(f"Welcome {getattr(user, "user_name")} comeback")
        choose_graph_for_task(getattr(user, "graphs"))
    else:
        print(f"Username or token isn't correct")

def create_graph():
    global graph
    if user is None:
        print(f"Please sign in first")
        return
    graph_id = pyip.inputStr(prompt="ID for identifying the pixelation graph:")
    graph_name = pyip.inputStr(prompt="The name of the pixelation graph:")
    graph_unit = pyip.inputStr(prompt="A unit of the quantity recorded in the pixelation graph:")
    graph_type = pyip.inputChoice(
        prompt="It is the type of quantity to be handled in the graph:",
        choices=["float","int"]
    )
    graph_color = pyip.inputChoice(
        prompt="The display color of the pixel in the pixelation graph:",
        choices=["shibafu","momiji","sora","ichou","ajisai","kuro"]
    )

    user.create_a_graph(graph_id, graph_name, graph_unit, graph_type, graph_color)
    model.insert_graph(getattr(user,"user_name"), getattr(user.current_graph,"graph_id"))

def choose_graph_for_task(user_graph: list[Graph])->None:
    global graph

    if not len(user_graph):
        print("Please create a graph before proceeding.")
        return
    description = ""
    choices = []

    for index, graph in enumerate(user_graph):
        description += f"Index {index}: {getattr(graph,"graph_id")} \n"
        choices.append(str(index))

    description = "Please enter the index to choose a graph for the task:" + "\n" + description
    user_graph_id = pyip.inputChoice(prompt=description, choices=choices)
    graph = user_graph[int(user_graph_id)]
    user.current_graph = graph
    print(f"Welcome {getattr(user, "user_name")} work in {getattr(graph, "graph_id")}")

def post_a_pixel()->None:

    if graph is None:
        print(f"Please sign in first")
        return

    date = pyip.inputDate(
        prompt="The date on which the quantity is to be recorded:",
        formats=["%d/%m/%y"]
    )

    quantity = pyip.inputFloat(
        prompt="Specify the quantity to be registered on the specified date:",
    )

    graph.post_a_pixel(date, quantity)

def update_a_pixel():
    if graph is None:
        print(f"Please sign in first")
        return

    date = pyip.inputDate(
        prompt="The date on which the quantity is to be updated:",
        formats=["%d/%m/%y"]
    )

    quantity = pyip.inputFloat(
        prompt="Specify the quantity to be updated on the specified date:",
    )

    graph.update_a_pixel(date, quantity)

def delete_a_pixel():
    if graph is None:
        print(f"Please sign in first")
        return

    date = pyip.inputDate(
        prompt="The date on which the quantity is to be updated:",
        formats=["%d/%m/%y"]
    )

    graph.delete_a_pixel(date)


while is_run:
    description = ""
    choice = []
    if user is None:
        description = """
Please choose one option below:
1. Sign in
2. Sign up
0. Sign out
"""
        choice = ["0","1","2"]
    else:
        description = """
Please choose one option below:
3. Create a graph
4. Post a pixel
5. Update a pixel
6. Switch to another graph
7. Delete a pixel
0. Sign out
        """
        choice = ["0", "3", "4","5","6","7"]

    user_choice = pyip.inputChoice(prompt=description,choices = choice)
    match user_choice:
        case "0":
            is_run = False
            model.save_user(file_path="./data/user.csv")
            model.save_graph_data(file_path="./data/graph.csv")
            user = None
            graph = None
            print("Good bye, see ya")
        case "2":
            create_new_user()
        case "1":
            login()
        case "3":
            create_graph()
        case "4":
            post_a_pixel()
        case "5":
            update_a_pixel()
        case "6":
            choose_graph_for_task(getattr(user,"graphs"))
        case "7":
            delete_a_pixel()

