from typing                                                                                 import List, Dict
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key


class Schema__Graph__Batch__Response(Type_Safe):
    results       : List[Dict[Safe_Str__Key, Safe_Str__Text]]                               # Command responses (type-safe) | todo: convert Dict to separate class (since Type_Safe__Dict, now supports it)
    total_commands: Safe_UInt                                                               # Total commands in batch
    stop_on_error : bool                                                                    # if stop_on_error was set
    success       : bool                                                                    # If all requests where executed ok
    successful    : Safe_UInt                                                               # Successfully executed count
    failed        : Safe_UInt                                                               # Failed count
    errors        : List[Safe_Str__Text]                                                    # Error messages for failed commands
