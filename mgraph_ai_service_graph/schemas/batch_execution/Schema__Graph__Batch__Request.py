from typing                                                                             import List
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id         import Safe_Str__Id
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Command      import Schema__Graph__Batch__Command

class Schema__Graph__Batch__Request(Type_Safe):
    commands      : List[Schema__Graph__Batch__Command]             # Commands to execute
    stop_on_error : bool                = False                     # Transaction mode
    namespace     : Safe_Str__Id = "default"                        # Cache namespace


