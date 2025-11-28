from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Export__Mermaid__Request(Type_Safe):                       # Request for Mermaid format export
    graph_ref        : Schema__Graph__Ref   = None                              # Reference to graph to export
    include_node_ids : bool                 = False                             # Include node IDs in labels
    direction        : str                  = 'TD'                              # Graph direction: TD, TB, BT, LR, RL