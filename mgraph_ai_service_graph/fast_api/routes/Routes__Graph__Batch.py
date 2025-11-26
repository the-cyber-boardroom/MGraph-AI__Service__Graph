from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes

from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Request          import Schema__Graph__Batch__Request
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Response         import Schema__Graph__Batch__Response

from mgraph_ai_service_graph.service.batch_execution.Graph__Batch__Executor                 import Graph__Batch__Executor


class Routes__Graph__Batch(Fast_API__Routes):                           # Batch execution routes - multi-operation endpoints
                                                                        # Provides batch operation capability for executing multiple graph
                                                                        # operations in a single API call. This is the core innovation of
                                                                        # the service.
                                                                        #
                                                                        # Benefits:
                                                                        #     - Reduced network overhead (1 request vs many)
                                                                        #     - Atomic operation support (stop_on_error)
                                                                        #     - Efficient for complex workflows

    tag            : str                     = 'graph-batch'            # FastAPI route tag
    batch_executor : Graph__Batch__Executor                             # Batch command executor

    def execute(self,                                                   # Execute a batch of graph commands
                request: Schema__Graph__Batch__Request                  # Batch request with list of commands
               ) -> Schema__Graph__Batch__Response:                     # Response with results for each command and error summary
        return self.batch_executor.execute(request)

    def setup_routes(self):                                             # Register batch execution route
        self.add_route_post(self.execute)
        return self
