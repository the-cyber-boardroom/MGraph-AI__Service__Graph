from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from osbot_fast_api.api.schemas.safe_str.Safe_Str__Fast_API__Route__Tag                     import Safe_Str__Fast_API__Route__Tag
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Request          import Schema__Graph__Batch__Request
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Response         import Schema__Graph__Batch__Response
from mgraph_ai_service_graph.service.batch_execution.Graph__Batch__Executor                 import Graph__Batch__Executor

ROUTES_PATHS__GRAPH_BATCH = [ '/graph/batch/execute'         ]
TAG__ROUTES_GRAPH_BATCH   = 'graph/batch'

class Routes__Graph__Batch(Fast_API__Routes):                                       # Batch execution routes - multi-operation endpoints

    tag            : Safe_Str__Fast_API__Route__Tag =  TAG__ROUTES_GRAPH_BATCH      # FastAPI route tag
    batch_executor : Graph__Batch__Executor                                         # Batch command executor

    def execute(self,                                                               # Execute a batch of graph commands
                request: Schema__Graph__Batch__Request                              # Batch request with list of commands
               ) -> Schema__Graph__Batch__Response:                                 # Response with results for each command and error summary
        return self.batch_executor.execute(request)

    def setup_routes(self):                                                         # Register batch execution route
        self.add_route_post(self.execute)
        return self
