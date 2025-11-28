from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Exists__Response(Type_Safe):
    graph_ref : Schema__Graph__Ref          = None                              # Reference that was checked
    exists    : bool                        = False                             # Whether graph exists