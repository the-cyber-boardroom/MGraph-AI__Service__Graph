from typing                                                                         import Dict
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now    import Timestamp_Now
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id     import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key    import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text



class Schema__Error__Response(Type_Safe):                                           # Consistent error response format
    error     : Safe_Str__Id                                                        # Machine-readable error type
    message   : Safe_Str__Text                                                      # Human-readable message
    details   : Dict[Safe_Str__Key, Safe_Str__Text]                                 # Optional context
    timestamp : Timestamp_Now                                                       # When error occurred