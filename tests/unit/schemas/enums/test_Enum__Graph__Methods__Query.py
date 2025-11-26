from unittest                                                                            import TestCase
from enum                                                                                import Enum
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Methods__Query                   import Enum__Graph__Methods__Query

class test_Enum__Graph__Methods__Query(TestCase):

    def test__all_methods(self):                                                         # Test all Query method enum values
        assert Enum__Graph__Methods__Query.FIND_NODE          == "find_node"
        assert Enum__Graph__Methods__Query.FIND_NODES_BY_TYPE == "find_nodes_by_type"
        assert Enum__Graph__Methods__Query.FIND_EDGES_BY_TYPE == "find_edges_by_type"
        assert Enum__Graph__Methods__Query.GET_NEIGHBORS      == "get_neighbors"
        assert Enum__Graph__Methods__Query.GET_NODE_PATH      == "get_node_path"
        assert Enum__Graph__Methods__Query.QUERY_BY_PREDICATE == "query_by_predicate"
        assert Enum__Graph__Methods__Query.SEARCH_VALUE_NODES == "search_value_nodes"

    def test__is_string_enum(self):                                                      # Test enum is string-based
        assert issubclass(Enum__Graph__Methods__Query, str)
        assert issubclass(Enum__Graph__Methods__Query, Enum)

    def test__enum_count(self):                                                          # Test expected method count
        methods = list(Enum__Graph__Methods__Query)
        assert len(methods) == 7


