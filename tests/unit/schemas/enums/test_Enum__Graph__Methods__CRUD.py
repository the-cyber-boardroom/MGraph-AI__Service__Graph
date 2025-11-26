from unittest                                                                            import TestCase
from enum                                                                                import Enum
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Methods__CRUD                    import Enum__Graph__Methods__CRUD

class test_Enum__Graph__Methods__CRUD(TestCase):

    def test__all_methods(self):                                                         # Test all CRUD method enum values
        assert Enum__Graph__Methods__CRUD.CREATE_GRAPH == "create_graph"
        assert Enum__Graph__Methods__CRUD.GET_GRAPH    == "get_graph"
        assert Enum__Graph__Methods__CRUD.DELETE_GRAPH == "delete_graph"
        assert Enum__Graph__Methods__CRUD.LIST_GRAPHS  == "list_graphs"
        assert Enum__Graph__Methods__CRUD.GRAPH_EXISTS == "graph_exists"
        assert Enum__Graph__Methods__CRUD.GRAPH_STATS  == "graph_stats"

    def test__is_string_enum(self):                                                      # Test enum is string-based
        assert issubclass(Enum__Graph__Methods__CRUD, str)
        assert issubclass(Enum__Graph__Methods__CRUD, Enum)

    def test__enum_count(self):                                                          # Test expected method count
        methods = list(Enum__Graph__Methods__CRUD)
        assert len(methods) == 6


