from osbot_fast_api.api.routes.Routes__Set_Cookie                                           import Routes__Set_Cookie
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API                                import Serverless__Fast_API
from osbot_fast_api_serverless.fast_api.routes.Routes__Info                                 import Routes__Info
from mgraph_ai_service_graph.config                                                         import FAST_API__TITLE
from mgraph_ai_service_graph.utils.Version                                                  import version__mgraph_ai_service_graph
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__CRUD                            import Routes__Graph__CRUD
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Edit                            import Routes__Graph__Edit
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Query                           import Routes__Graph__Query
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Batch                           import Routes__Graph__Batch


class Graph_Service__Fast_API(Serverless__Fast_API):                                        # FastAPI application for Graph Service

    def setup(self):                                                                        # Configure FastAPI application settings
        with self.config as _:
            _.title   = FAST_API__TITLE
            _.version = version__mgraph_ai_service_graph
        return super().setup()

    def setup_routes(self):                                                                 # Register all route handlers
        self.add_routes(Routes__Info         )                                              # Health/info endpoints
        self.add_routes(Routes__Set_Cookie   )                                              # Cookie management
        self.add_routes(Routes__Graph__CRUD  )                                              # Graph CRUD operations
        self.add_routes(Routes__Graph__Edit  )                                              # Graph edit operations
        self.add_routes(Routes__Graph__Query )                                              # Graph query operations
        self.add_routes(Routes__Graph__Batch )                                              # Batch execution
