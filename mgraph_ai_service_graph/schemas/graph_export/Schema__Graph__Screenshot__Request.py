from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Screenshot__Request(Type_Safe):                            # Request for screenshot/image generation
    graph_ref         : Schema__Graph__Ref  = None                              # Reference to graph to render
    width             : Safe_UInt           = None                              # Optional width in pixels
    height            : Safe_UInt           = None                              # Optional height in pixels
    include_node_ids  : bool                = False                             # Include node IDs in labels
    show_value_nodes  : bool                = True                              # Show value node contents