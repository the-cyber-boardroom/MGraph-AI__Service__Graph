from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Get__Request(Type_Safe):
    graph_ref : Schema__Graph__Ref       = None                                  # Reference to graph to retrieve | todo: figure why when we don't do "= None" here we get an error (which crashes the creation of openapi.json in lambda), with an error similar to:  PydanticJsonSchemaWarning: Default value <mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref.Schema__Graph__Ref object at 0x1056a2ad0> is not JSON serializable;