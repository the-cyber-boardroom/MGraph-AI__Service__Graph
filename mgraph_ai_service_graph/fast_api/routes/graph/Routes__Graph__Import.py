from osbot_fast_api.api.routes.Fast_API__Routes                                     import Fast_API__Routes
from osbot_fast_api.api.schemas.safe_str.Safe_Str__Fast_API__Route__Tag             import Safe_Str__Fast_API__Route__Tag
from mgraph_ai_service_graph.schemas.graph_import.Schema__Graph__Import             import (Schema__Graph__Import__Request,
                                                                                            Schema__Graph__Import__Compressed__Request,
                                                                                            Schema__Graph__Import__Response)
from mgraph_ai_service_graph.service.areas.Area__Graph__Import                      import Area__Graph__Import


TAG__ROUTES_GRAPH_IMPORT   = 'graph-import'
ROUTES_PATHS__GRAPH_IMPORT = [ '/graph-import/import-graph' ,
                               '/graph-import/compressed'   ]


class Routes__Graph__Import(Fast_API__Routes):                                  # Graph import routes - accept full graph submissions
    tag         : Safe_Str__Fast_API__Route__Tag = TAG__ROUTES_GRAPH_IMPORT     # FastAPI route tag
    area_import : Area__Graph__Import                                           # Import operations area

    # ═══════════════════════════════════════════════════════════════════════════════
    # Import Standard JSON Format
    # ═══════════════════════════════════════════════════════════════════════════════

    def import_graph(self,                                                              # Import graph from standard JSON format
             request: Schema__Graph__Import__Request
            ) -> Schema__Graph__Import__Response:
        return self.area_import.import_graph(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Import Compressed JSON Format
    # ═══════════════════════════════════════════════════════════════════════════════

    def compressed(self,                                                        # Import graph from compressed JSON format
                   request: Schema__Graph__Import__Compressed__Request
                  ) -> Schema__Graph__Import__Response:
        return self.area_import.import_graph_compressed(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Route Setup
    # ═══════════════════════════════════════════════════════════════════════════════

    def setup_routes(self):
        self.add_route_post(self.import_graph)
        self.add_route_post(self.compressed  )
        return self
