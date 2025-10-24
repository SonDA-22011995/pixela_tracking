from pandas import DataFrame


class User:
    def __init__(self, user_name, x_user_token):
        self.user_name = user_name
        self.x_user_token = x_user_token

    def get_graph_id(self, graph_data: DataFrame) ->list:
        graph_data_by_user = graph_data[graph_data["user_name"] == self.user_name]
        return graph_data_by_user.to_dict('records')

