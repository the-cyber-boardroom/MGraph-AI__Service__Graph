from typing                                                                                 import Dict, Type

from mgraph_ai_service_graph.fast_api.routes.server.Routes__Graph__Cache import Routes__Graph__Cache
from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from osbot_fast_api.api.routes.Routes__Set_Cookie                                           import Routes__Set_Cookie
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API                                import Serverless__Fast_API
from osbot_fast_api_serverless.fast_api.routes.Routes__Info                                 import Routes__Info
from fastapi                                                                                import Request
from fastapi.responses                                                                      import JSONResponse
from mgraph_ai_service_graph.exceptions.Graph__Service__Error                               import Graph__Service__Error
from mgraph_ai_service_graph.schemas.error.Schema__Error__Response                          import Schema__Error__Response
from mgraph_ai_service_graph.config                                                         import FAST_API__TITLE
from mgraph_ai_service_graph.utils.Version                                                  import version__mgraph_ai_service_graph
from mgraph_ai_service_graph.fast_api.routes.server.Routes__Graph__Server                   import Routes__Graph__Server
from mgraph_ai_service_graph.fast_api.routes.graph.Routes__Graph__Export                    import Routes__Graph__Export
from mgraph_ai_service_graph.fast_api.routes.graph.Routes__Graph__CRUD                      import Routes__Graph__CRUD
from mgraph_ai_service_graph.fast_api.routes.graph.Routes__Graph__Edit                      import Routes__Graph__Edit
from mgraph_ai_service_graph.fast_api.routes.graph.Routes__Graph__Query                     import Routes__Graph__Query
from mgraph_ai_service_graph.fast_api.routes.graph.Routes__Graph__Batch                     import Routes__Graph__Batch


class Graph_Service__Fast_API(Serverless__Fast_API):                                        # FastAPI application for Graph Service
    routes_classes : Dict[Type[Fast_API__Routes], Fast_API__Routes]

    def setup(self):                                                                        # Configure FastAPI application settings
        with self.config as _:
            _.title   = FAST_API__TITLE
            _.version = version__mgraph_ai_service_graph
        self.setup_exception_handlers()
        return super().setup()

    def setup_routes(self):                                                                 # Register all route handlers
        self.add_routes(Routes__Info         )                                              # Health/info endpoints
        self.add_routes(Routes__Set_Cookie   )                                              # Cookie management
        self.add_routes(Routes__Graph__CRUD  )                                              # Graph CRUD operations
        self.add_routes(Routes__Graph__Edit  )                                              # Graph edit operations
        self.add_routes(Routes__Graph__Query )                                              # Graph query operations
        self.add_routes(Routes__Graph__Batch )                                              # Batch execution
        self.add_routes(Routes__Graph__Export)                                              # Graph export
        self.add_routes(Routes__Graph__Cache )
        self.add_routes(Routes__Graph__Server)                                              # Server details and stats

    def setup_exception_handlers(self):                                             # Register global exception handlers
        app = self.app()

        @app.exception_handler(Graph__Service__Error)
        def handle_graph_service_error(request: Request,                            # Note: sync function, not async
                                       exc    : Graph__Service__Error
                                      ) -> JSONResponse:
            error_response = Schema__Error__Response(error   = exc.error_type,
                                                     message = exc.message   ,
                                                     details = exc.details or {})
            return JSONResponse(status_code = exc.status_code      ,
                                content     = error_response.json())


    # todo: add these changes to the main Fast_API project (since these are quite useful)
    def add_routes(self, class_routes):
        class_routes_instance = class_routes(app=self.app()).setup()                        # capture the instance created
        self.routes_classes[class_routes] = class_routes_instance                           # stored it on the routes_classes object
        return self

    def routes_instance(self, routes_class: Type[Fast_API__Routes]) -> Fast_API__Routes:
            return self.routes_classes.get(routes_class)
