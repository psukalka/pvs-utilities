import grpc 

import recommendation_pb2
import recommendation_pb2_grpc

class RecommendationClient():
    def __init__(self, host: str='localhost', port: int=50051) -> None:
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = recommendation_pb2_grpc.ShowRecommendationStub(self.channel)

    def get_recommendations(self, user_id, show_id):
        try:
            request = recommendation_pb2.RecommendationRequest(
                user_id = user_id,
                show_id = show_id
            )
            response = self.stub.GetRecommendations(request)
            print(f"Server response: {response.show_ids}")
            return response.show_ids
        except:
            print(f"Request failed")
            return []
        
    def close(self):
        self.channel.close()

def main():
    client = RecommendationClient()
    try:
        user_id = 1
        show_id = 10
        recommendations = client.get_recommendations(user_id, show_id)
    finally:
        client.close()

if __name__ == "__main__":
    main()
