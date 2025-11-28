from typing                                                                         import Any
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id     import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                   import Schema__Graph__Ref


class Schema__Graph__Export__Response(Type_Safe):                               # Base response for export operations
    graph_ref : Schema__Graph__Ref      = None                                  # Resolved reference
    format    : Safe_Str__Id            = None                                  # Export format (json, dot, mermaid)
    content   : Any                     = None                                  # todo: see what is the best schema to use here | Exported content as string
    success   : bool                    = False                                 # Whether export succeeded