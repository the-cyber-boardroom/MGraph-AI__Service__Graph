from typing                                                                                 import Dict
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                                      import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                                      import Node_Id
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key


class Schema__Graph__Edge__Data(Type_Safe):                                                 # Edge data structure for query results
    edge_id      : Edge_Id                                                                   # Edge identifier
    from_node_id : Node_Id                                                                   # Source node
    to_node_id   : Node_Id                                                                   # Target node
    edge_type    : Safe_Str__Id                                                             # Edge type/relationship
    edge_data    : Dict[Safe_Str__Key, str]                                                 # todo: find a better schema for edge_data | Edge attributes
