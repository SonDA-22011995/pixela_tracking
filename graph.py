from datetime import datetime
from utils import call_api
import model

class Graph:
    def __init__(self, user_name, graph_id):
        self.user_name = user_name
        self.graph_id = graph_id
        self.post_pixel = model.config["pixela_api"]["post_pixel"]

    def get_request_header(self)->str:
        request_header = self.post_pixel["request_header"]
        request_header["X-USER-TOKEN"] = model.get_user_token(self.user_name)
        return request_header

    def get_request_body(self, date: datetime, quantity: float)->str:
        request_body = self.post_pixel["request_body"]
        request_body["date"] = date.strftime("%Y%m%d")
        request_body["quantity"] = str(quantity)
        return request_body

    def get_end_point(self) -> str:
        end_point =self.post_pixel["endpoint"]
        end_point = end_point.replace("<username>", self.user_name)
        end_point = end_point.replace("<graphID>", self.graph_id)
        return end_point

    def post_a_pixel(self,date: datetime, quantity: float):
        request_header = self.get_request_header()
        request_body = self.get_request_body(date, quantity)
        end_point = self.get_end_point()

        response = call_api(
            method= self.post_pixel["method"],
            url=end_point,
            json=request_body,
            headers=request_header
        )

        try:
            if response["isSuccess"]:
                print(response["message"])
            else:
                print(response["message"])
        except KeyError as e:
            print(response["error"])