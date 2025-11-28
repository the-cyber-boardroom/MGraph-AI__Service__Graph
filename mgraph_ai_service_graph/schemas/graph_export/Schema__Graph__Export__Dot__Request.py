from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Export__Dot__Request(Type_Safe):                           # Request for DOT format export with options
    graph_ref         : Schema__Graph__Ref  = None                              # Reference to graph to export
    include_node_ids  : bool                = False                             # Include node IDs in labels
    include_edge_ids  : bool                = False                             # Include edge IDs in labels
    show_value_nodes  : bool                = True                              # Show value node contents
    rankdir           : str                 = 'TB'                              # Graph direction: TB, BT, LR, RL