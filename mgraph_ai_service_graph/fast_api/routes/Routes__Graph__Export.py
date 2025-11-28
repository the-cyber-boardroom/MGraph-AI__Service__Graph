from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Json__Request      import Schema__Graph__Export__Json__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Json__Response     import Schema__Graph__Export__Json__Response
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Dot__Request       import Schema__Graph__Export__Dot__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Dot__Response      import Schema__Graph__Export__Dot__Response
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Mermaid__Request   import Schema__Graph__Export__Mermaid__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Mermaid__Response  import Schema__Graph__Export__Mermaid__Response
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Screenshot__Request        import Schema__Graph__Screenshot__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Screenshot__Response       import Schema__Graph__Screenshot__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__Export                              import Area__Graph__Export


TAG__ROUTES_GRAPH_EXPORT   = 'graph-export'
ROUTES_PATHS__GRAPH_EXPORT = [ '/graph-export/to-json'   ,
                               '/graph-export/dot'       ,
                               '/graph-export/mermaid'   ,
                               '/graph-export/screenshot']


class Routes__Graph__Export(Fast_API__Routes):                                  # Graph export routes
    tag         : str                = TAG__ROUTES_GRAPH_EXPORT
    area_export : Area__Graph__Export

    # todo: see what is the best naming to use here (so that it is consistent) , we can't use .json() since that is already part of the Type_Safe class
    def to_json(self,                                                              # Export graph to JSON format
                request: Schema__Graph__Export__Json__Request
           ) -> Schema__Graph__Export__Json__Response:
        return self.area_export.export_json(request)

    def dot(self,                                                               # Export graph to DOT format
            request: Schema__Graph__Export__Dot__Request
           ) -> Schema__Graph__Export__Dot__Response:
        return self.area_export.export_dot(request)

    def mermaid(self,                                                           # Export graph to Mermaid format
                request: Schema__Graph__Export__Mermaid__Request
               ) -> Schema__Graph__Export__Mermaid__Response:
        return self.area_export.export_mermaid(request)

    def screenshot(self,                                                        # Generate graph screenshot/image
                   request: Schema__Graph__Screenshot__Request
                  ) -> Schema__Graph__Screenshot__Response:
        return self.area_export.screenshot(request)

    def setup_routes(self):
        self.add_route_post(self.to_json      )
        self.add_route_post(self.dot       )
        self.add_route_post(self.mermaid   )
        self.add_route_post(self.screenshot)
        return self