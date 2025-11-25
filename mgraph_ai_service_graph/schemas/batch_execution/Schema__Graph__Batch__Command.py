from typing                                                                                     import Dict, Any
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Identifier import Safe_Str__Python__Identifier
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Area                                    import Enum__Graph__Area


class Schema__Graph__Batch__Command(Type_Safe):
    area    : Enum__Graph__Area                     # Functional area
    method  : Safe_Str__Python__Identifier          # Method name
    payload : Dict[str, Any]                        # Request data

