from typing                                                                     import Dict, List, Any
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text    import Safe_Str__Text


class Schema__Graph__Batch__Response(Type_Safe):
    results       : List[Dict[str, Any]]            # Responses
    total_commands: Safe_UInt                       # Total executed
    successful    : Safe_UInt                       # Success count
    failed        : Safe_UInt                       # Failure count
    errors        : List[Safe_Str__Text]            # Error messages