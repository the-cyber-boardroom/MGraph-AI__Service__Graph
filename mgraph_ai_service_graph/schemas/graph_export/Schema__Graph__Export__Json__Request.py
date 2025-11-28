from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Export__Json__Request(Type_Safe):                          # Request for JSON format export
    graph_ref   : Schema__Graph__Ref    = None                                  # Reference to graph to export
    compressed  : bool                  = False                                 # Use compressed JSON format
    pretty      : bool                  = True                                  # Pretty print JSON