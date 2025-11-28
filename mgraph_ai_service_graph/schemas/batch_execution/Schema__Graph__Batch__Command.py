from typing                                                                                         import Dict
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Identifier     import Safe_Str__Python__Identifier
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key                    import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                        import Safe_Str__Text
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Area                                        import Enum__Graph__Area


class Schema__Graph__Batch__Command(Type_Safe):
    area    : Enum__Graph__Area                                                             # Functional area (CRUD, Edit, Query, etc)
    method  : Safe_Str__Python__Identifier          = None                                  # Method name to call  | todo: find out why we get this error in FastPI docs page rendering: Default value _ is not JSON serializable; excluding default from JSON schema [non-serializable-default
    payload : Dict[Safe_Str__Key, Safe_Str__Text]                                           # Request data as type-safe dict
