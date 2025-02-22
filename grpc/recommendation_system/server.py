from concurrent import futures
import grpc
import recommendation_pb2
import recommendation_pb2_grpc

class ShowRecommendationServicer(recommendation_pb2_grpc.ShowRecommendationServicer):
    def GetRecommendations(self, request, context):
        user_id = request.user_id
        show_id = request.show_id
        print(f"User: {user_id}, show: {show_id}")
        recommended_shows = [1,2,3]
        return recommendation_pb2.RecommendationResponse(
            show_ids=recommended_shows
        )

def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_send_message_length', 10 * 1024 * 1024),
            ('grpc.max_receive_message_length', 10 * 1024 * 1024)
        ]
    )

    recommendation_pb2_grpc.add_ShowRecommendationServicer_to_server(
        ShowRecommendationServicer(), server
    )

    port = 50051
    server.add_insecure_port(f'[::]:{port}')
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        print(f"Stopped server")

if __name__ == "__main__":
    serve()