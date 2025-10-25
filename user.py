from pandas import DataFrame
from graph import Graph
from utils import call_api
import model


class User:
    def __init__(self, user_name, x_user_token):
        self.user_name = user_name
        self.x_user_token = x_user_token
        self.create_graph = model.config["pixela_api"]["create_graph"]
        self.request_header = model.config["pixela_api"]["request_header"]
        self.graphs = self.get_graph()
        self.current_graph = None

    def get_graph_id(self) ->list[dict]:
        graph_data: DataFrame = model.graph_data
        user_graph = graph_data[graph_data["user_name"] == self.user_name]
        return user_graph.to_dict('records')

    def get_graph(self):
        graph_list = []
        user_graph = self.get_graph_id()
        if len(user_graph):
            for graph in user_graph:
                graph_user = Graph(graph.get("user_name"), graph.get("graph_id"))
                graph_list.append(graph_user)
        return graph_list

    def get_request_header(self) -> str:
        request_header = self.request_header
        request_header["X-USER-TOKEN"] = model.get_user_token(self.user_name)
        return request_header

    def get_request_body_create_graph(self, graph_id, graph_name
            , graph_unit, graph_type, graph_color) -> str:
        request_body = self.create_graph["request_body"]
        request_body["id"] = graph_id
        request_body["name"] = graph_name
        request_body["unit"] = graph_unit
        request_body["type"] = graph_type
        request_body["color"] = graph_color
        return request_body

    def get_end_point_create_graph(self) -> str:
        end_point = self.create_graph["endpoint"]
        end_point = end_point.replace("<username>", self.user_name)
        return end_point

    def create_a_graph(self, graph_id, graph_name, graph_unit, graph_type, graph_color):
        request_header = self.get_request_header()
        request_body = self.get_request_body_create_graph(graph_id, graph_name
            , graph_unit, graph_type, graph_color)
        end_point = self.get_end_point_create_graph()

        response = call_api(
            method=self.create_graph["method"],
            url=end_point,
            json=request_body,
            headers=request_header
        )

        try:
            if response["isSuccess"]:
                self.current_graph = Graph(self.user_name, graph_id)
                self.graphs.append(self.current_graph)
                print(response["message"])
                print(f"The current graph is {getattr(self.current_graph,"graph_id")}")
            else:
                print(response["message"])
        except KeyError as e:
            print(response["error"])