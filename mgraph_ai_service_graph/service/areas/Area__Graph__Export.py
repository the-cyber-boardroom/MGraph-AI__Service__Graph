from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Json__Request      import Schema__Graph__Export__Json__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Json__Response     import Schema__Graph__Export__Json__Response
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Dot__Request       import Schema__Graph__Export__Dot__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Dot__Response      import Schema__Graph__Export__Dot__Response
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Mermaid__Request   import Schema__Graph__Export__Mermaid__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Mermaid__Response  import Schema__Graph__Export__Mermaid__Response
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Screenshot__Request        import Schema__Graph__Screenshot__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Screenshot__Response       import Schema__Graph__Screenshot__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service
from osbot_utils.utils.Env                                                                  import env_var_set
from osbot_utils.utils.Misc                                                                 import bytes_to_base64


ENV_VAR_URL__MGRAPH_DB_SERVERLESS = "URL__MGRAPH_DB_SERVERLESS"

class Area__Graph__Export(Type_Safe):                                           # Graph export operations area

    graph_service: Graph__Service

    # ═══════════════════════════════════════════════════════════════════════════════
    # JSON Export
    # ═══════════════════════════════════════════════════════════════════════════════

    def export_json(self,                                                       # Export graph to JSON format
                    request: Schema__Graph__Export__Json__Request
               ) -> Schema__Graph__Export__Json__Response:

        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)

        if request.compressed:
            graph_json = mgraph.json__compress()
        else:
            graph_json = mgraph.json()
            # json_data    = mgraph.json()
            # if request.pretty:
            #     json_content = json.dumps(json_data, indent=2, default=str)
            # else:
            #     json_content = json.dumps(json_data, default=str)

        return Schema__Graph__Export__Json__Response(graph_ref  = resolved_ref,
                                                     graph_json = graph_json   ,
                                                     success    = True        )

    # ═══════════════════════════════════════════════════════════════════════════════
    # DOT Export
    # ═══════════════════════════════════════════════════════════════════════════════

    def export_dot(self,                                                        # Export graph to DOT format (Graphviz)
                   request: Schema__Graph__Export__Dot__Request
              ) -> Schema__Graph__Export__Dot__Response:

        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)

        export     = mgraph.export()
        # todo: see if we shouldn't expose the MGraph__Export__Dot__Config schema to the caller, since that already has tons of options
        #dot_config = export.export_dot().config                                 # Get DOT config for customization

        dot_content = export.to__dot()

        return Schema__Graph__Export__Dot__Response(graph_ref = resolved_ref,
                                                    dot       = dot_content ,
                                                    success   = True        )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Mermaid Export
    # ═══════════════════════════════════════════════════════════════════════════════

    def export_mermaid(self,                                                    # Export graph to Mermaid format
                       request: Schema__Graph__Export__Mermaid__Request
                  ) -> Schema__Graph__Export__Mermaid__Response:

        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)

        export          = mgraph.export()
        mermaid_content = export.to__mermaid()

        return Schema__Graph__Export__Mermaid__Response(graph_ref = resolved_ref  ,
                                                        mermaid   = mermaid_content,
                                                        success   = True          )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Screenshot (Image) Export
    # ═══════════════════════════════════════════════════════════════════════════════

    def screenshot(self,                                                        # Generate graph image/screenshot
                   request: Schema__Graph__Screenshot__Request
              ) -> Schema__Graph__Screenshot__Response:
        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)
        #return Schema__Graph__Screenshot__Response(graph_ref=resolved_ref)

        if env_var_set(ENV_VAR_URL__MGRAPH_DB_SERVERLESS):
            screenshot  = mgraph.screenshot()
            image_bytes = screenshot.dot()
            if image_bytes:
                image_base64 = bytes_to_base64(image_bytes) if image_bytes else None
                content_type = 'image/png'
                return Schema__Graph__Screenshot__Response(graph_ref    = resolved_ref ,
                                                           image_base64 = image_base64 ,
                                                           content_type = content_type ,
                                                           success      = True         )

        return Schema__Graph__Screenshot__Response(graph_ref = resolved_ref ,
                                                   success   = False        )

    # def _get_content_type(self, format: str) -> str:                            # Map format to MIME type
    #     content_types = { 'png' : 'image/png'        ,
    #                       'svg' : 'image/svg+xml'    ,
    #                       'pdf' : 'application/pdf'  ,
    #                       'jpg' : 'image/jpeg'       ,
    #                       'jpeg': 'image/jpeg'       }
    #     return content_types.get(format, 'image/png')