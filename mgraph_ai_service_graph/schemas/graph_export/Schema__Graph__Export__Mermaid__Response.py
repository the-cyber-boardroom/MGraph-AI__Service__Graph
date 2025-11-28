from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                   import Schema__Graph__Ref


class Schema__Graph__Export__Mermaid__Response(Type_Safe):                      # Response for Mermaid format export
    graph_ref : Schema__Graph__Ref      = None                                  # Resolved reference
    mermaid   : str                     = None                                  # todo: create a schema for mermaid code | Mermaid format content
    success   : bool                    = False                                 # Whether export succeeded