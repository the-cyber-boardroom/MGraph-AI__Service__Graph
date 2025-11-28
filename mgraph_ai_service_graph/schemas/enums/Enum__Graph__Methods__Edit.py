from enum import Enum


class Enum__Graph__Methods__Edit(str, Enum):
    ADD_NODE        = "add_node"
    ADD_EDGE        = "add_edge"
    DELETE_NODE     = "delete_node"
    DELETE_EDGE     = "delete_edge"
    UPDATE_NODE     = "update_node"
    UPDATE_EDGE     = "update_edge"
    ADD_VALUE_NODE  = "add_value_node"      # MGraph value node
    ADD_PREDICATE   = "add_predicate"       # Semantic edge