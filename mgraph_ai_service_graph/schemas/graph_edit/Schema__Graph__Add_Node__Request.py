from typing                                                                     import Dict, Any
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid           import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id


class Schema__Graph__Add_Node__Request(Type_Safe):
    graph_id   : Random_Guid                        # Target graph
    node_type  : Safe_Str__Id                       # Node type name
    node_data  : Dict[str, Any]                     # Node data (flexible)
    auto_cache : bool               = True          # Update cache

