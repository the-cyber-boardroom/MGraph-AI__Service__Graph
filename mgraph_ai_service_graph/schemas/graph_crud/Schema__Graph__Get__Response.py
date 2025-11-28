from mgraph_db.mgraph.MGraph                                                    import MGraph
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Get__Response(Type_Safe):
    graph_ref : Schema__Graph__Ref          = None                              # Resolved reference
    mgraph    : MGraph                      = None                              # Retrieved graph
    success   : bool                        = False                             # Whether retrieval succeeded