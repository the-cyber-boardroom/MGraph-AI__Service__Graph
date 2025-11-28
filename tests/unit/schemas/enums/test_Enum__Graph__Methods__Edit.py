from unittest                                                                            import TestCase
from enum                                                                                import Enum
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Methods__Edit                    import Enum__Graph__Methods__Edit

class test_Enum__Graph__Methods__Edit(TestCase):

    def test__all_methods(self):                                                         # Test all Edit method enum values
        assert Enum__Graph__Methods__Edit.ADD_NODE       == "add_node"
        assert Enum__Graph__Methods__Edit.ADD_EDGE       == "add_edge"
        assert Enum__Graph__Methods__Edit.DELETE_NODE    == "delete_node"
        assert Enum__Graph__Methods__Edit.DELETE_EDGE    == "delete_edge"
        assert Enum__Graph__Methods__Edit.UPDATE_NODE    == "update_node"
        assert Enum__Graph__Methods__Edit.UPDATE_EDGE    == "update_edge"
        assert Enum__Graph__Methods__Edit.ADD_VALUE_NODE == "add_value_node"
        assert Enum__Graph__Methods__Edit.ADD_PREDICATE  == "add_predicate"

    def test__is_string_enum(self):                                                      # Test enum is string-based
        assert issubclass(Enum__Graph__Methods__Edit, str)
        assert issubclass(Enum__Graph__Methods__Edit, Enum)

    def test__enum_count(self):                                                          # Test expected method count
        methods = list(Enum__Graph__Methods__Edit)
        assert len(methods) == 8


