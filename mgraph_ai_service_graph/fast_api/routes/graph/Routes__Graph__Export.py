from fastapi                                                                                import Response, HTTPException
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
from osbot_utils.utils.Misc import base64_to_bytes

TAG__ROUTES_GRAPH_EXPORT   = 'graph-export'
ROUTES_PATHS__GRAPH_EXPORT = [ '/graph-export/to-json'       ,
                               '/graph-export/dot'           ,
                               '/graph-export/mermaid'       ,
                               '/graph-export/screenshot'    ,
                               '/graph-export/screenshot/png']


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
        return self.area_export.screenshot(request).json()                      # todo: see why we need to convert this to .json(), or we get this pydantic error: 1 validation error for Schema__Graph__Screenshot__Response__BaseModel\nformat\n  Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]\n

    def screenshot__png(self,                                                        # Generate graph screenshot/image
                       request: Schema__Graph__Screenshot__Request
                  ) -> Schema__Graph__Screenshot__Response:
        screenshot_response = self.area_export.screenshot(request)
        if screenshot_response.success:
            png_bytes = base64_to_bytes(screenshot_response.image_base64)
            return Response(content=png_bytes,
                            media_type=screenshot_response.content_type,
        )
        else:
            raise HTTPException(status_code=500, detail="Could not create screenshot")





    def setup_routes(self):
        self.add_route_post(self.to_json      )
        self.add_route_post(self.dot       )
        self.add_route_post(self.mermaid   )
        self.add_route_post(self.screenshot)
        self.add_route_post(self.screenshot__png)
        return self