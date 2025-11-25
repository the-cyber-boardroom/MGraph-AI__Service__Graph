from osbot_fast_api.api.routes.Fast_API__Routes import Fast_API__Routes


class Routes__Graph__Batch(Fast_API__Routes):
    tag: str = 'graph-batch'

    batch_executor: Graph__Batch__Executor         # Batch engine

    def execute(self, request: Schema__Graph__Batch__Request
               ) -> Schema__Graph__Batch__Response:
        return self.batch_executor.execute(request)

    def setup_routes(self):
        self.add_route_post(self.execute)
        return self