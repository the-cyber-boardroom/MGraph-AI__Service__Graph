from unittest                                                                            import TestCase
from enum                                                                                import Enum
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Area                             import Enum__Graph__Area
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Methods__CRUD                    import Enum__Graph__Methods__CRUD
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Methods__Edit                    import Enum__Graph__Methods__Edit
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Methods__Query                   import Enum__Graph__Methods__Query
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Methods__Cache                   import Enum__Graph__Methods__Cache
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Methods__Export                  import Enum__Graph__Methods__Export


class test_Enum__Graph__Area(TestCase):

    def test__all_areas(self):                                                           # Test all area enum values exist
        assert Enum__Graph__Area.GRAPH_CRUD   == "graph_crud"
        assert Enum__Graph__Area.GRAPH_EDIT   == "graph_edit"
        assert Enum__Graph__Area.GRAPH_QUERY  == "graph_query"
        assert Enum__Graph__Area.GRAPH_CACHE  == "graph_cache"
        assert Enum__Graph__Area.GRAPH_EXPORT == "graph_export"

    def test__is_string_enum(self):                                                      # Test enum is string-based
        assert issubclass(Enum__Graph__Area, str)
        assert issubclass(Enum__Graph__Area, Enum)

        # String comparison works directly
        assert Enum__Graph__Area.GRAPH_CRUD == "graph_crud"
        assert str(Enum__Graph__Area.GRAPH_CRUD) == "graph_crud"

    def test__enum_count(self):                                                          # Test all expected areas
        areas = list(Enum__Graph__Area)
        assert len(areas) == 5

    def test__enum_iteration(self):                                                      # Test iteration
        area_values = [area.value for area in Enum__Graph__Area]
        assert "graph_crud"   in area_values
        assert "graph_edit"   in area_values
        assert "graph_query"  in area_values
        assert "graph_cache"  in area_values
        assert "graph_export" in area_values


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


class test_Enum__Graph__Methods__Cache(TestCase):

    def test__all_methods(self):                                                         # Test all Cache method enum values
        assert Enum__Graph__Methods__Cache.CACHE_STORE    == "cache_store"
        assert Enum__Graph__Methods__Cache.CACHE_RETRIEVE == "cache_retrieve"
        assert Enum__Graph__Methods__Cache.CACHE_DELETE   == "cache_delete"
        assert Enum__Graph__Methods__Cache.CACHE_EXISTS   == "cache_exists"
        assert Enum__Graph__Methods__Cache.CACHE_LIST     == "cache_list"

    def test__is_string_enum(self):                                                      # Test enum is string-based
        assert issubclass(Enum__Graph__Methods__Cache, str)
        assert issubclass(Enum__Graph__Methods__Cache, Enum)

    def test__enum_count(self):                                                          # Test expected method count
        methods = list(Enum__Graph__Methods__Cache)
        assert len(methods) == 5


class test_Enum__Graph__Methods__Export(TestCase):

    def test__all_methods(self):                                                         # Test all Export method enum values
        assert Enum__Graph__Methods__Export.EXPORT_JSON    == "export_json"
        assert Enum__Graph__Methods__Export.EXPORT_DOT     == "export_dot"
        assert Enum__Graph__Methods__Export.EXPORT_MERMAID == "export_mermaid"
        assert Enum__Graph__Methods__Export.IMPORT_JSON    == "import_json"
        assert Enum__Graph__Methods__Export.IMPORT_DOT     == "import_dot"
        assert Enum__Graph__Methods__Export.IMPORT_MERMAID == "import_mermaid"

    def test__is_string_enum(self):                                                      # Test enum is string-based
        assert issubclass(Enum__Graph__Methods__Export, str)
        assert issubclass(Enum__Graph__Methods__Export, Enum)

    def test__enum_count(self):                                                          # Test expected method count
        methods = list(Enum__Graph__Methods__Export)
        assert len(methods) == 6