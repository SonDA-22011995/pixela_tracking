from pandas import DataFrame


class User:
    def __init__(self, user_name, x_user_token):
        self.user_name = user_name
        self.x_user_token = x_user_token

    def get_graph_id(self, graph_data: DataFrame) ->list[dict]:
        user_graph = graph_data[graph_data["user_name"] == self.user_name]
        return user_graph.to_dict('records')

