from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Get__Response(Type_Safe):
    graph_ref : Schema__Graph__Ref          = None                              # Resolved reference
    #mgraph    : MGraph                      = None                              # Retrieved graph
    mgraph    : dict                        = None                              # todo: review Pydantic error that happens when we do this, which looks like caused by Schema__MGraph__Graph use of ForwardRef graph_type   : Type['Schema__MGraph__Graph'] (this could also be an issue in the Type_Safe to BaseModel workflow)
    success   : bool                        = False                             # Whether retrieval succeeded