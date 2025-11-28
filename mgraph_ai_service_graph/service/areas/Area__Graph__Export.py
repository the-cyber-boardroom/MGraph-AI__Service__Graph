import json
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
            json_data = mgraph.json__compress()
        else:
            json_data = mgraph.json()
            # json_data    = mgraph.json()
            # if request.pretty:
            #     json_content = json.dumps(json_data, indent=2, default=str)
            # else:
            #     json_content = json.dumps(json_data, default=str)

        return Schema__Graph__Export__Json__Response(graph_ref = resolved_ref,
                                                     json_data = json_data   ,
                                                     success   = True        )

    # ═══════════════════════════════════════════════════════════════════════════════
    # DOT Export
    # ═══════════════════════════════════════════════════════════════════════════════

    def export_dot(self,                                                        # Export graph to DOT format (Graphviz)
                   request: Schema__Graph__Export__Dot__Request
              ) -> Schema__Graph__Export__Dot__Response:

        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)

        export     = mgraph.export()
        dot_config = export.export_dot().config                                 # Get DOT config for customization

        if request.rankdir:
            dot_config.graph_attrs['rankdir'] = request.rankdir                 # todo: fix because graph_attrs

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

        screenshot = mgraph.screenshot()

        if request.rankdir:
            screenshot.set_rankdir(request.rankdir)

        output_format = request.format or 'png'
        content_type  = self._get_content_type(output_format)

        if output_format == 'png':
            image_bytes = screenshot.png()
        elif output_format == 'svg':
            image_bytes = screenshot.svg()
        elif output_format == 'pdf':
            image_bytes = screenshot.pdf()
        else:
            image_bytes = screenshot.png()                                      # Default to PNG
            content_type = 'image/png'

        import base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8') if image_bytes else None

        return Schema__Graph__Screenshot__Response(graph_ref    = resolved_ref ,
                                                   format       = output_format,
                                                   image_base64 = image_base64 ,
                                                   content_type = content_type ,
                                                   success      = image_base64 is not None)

    def _get_content_type(self, format: str) -> str:                            # Map format to MIME type
        content_types = { 'png' : 'image/png'        ,
                          'svg' : 'image/svg+xml'    ,
                          'pdf' : 'application/pdf'  ,
                          'jpg' : 'image/jpeg'       ,
                          'jpeg': 'image/jpeg'       }
        return content_types.get(format, 'image/png')