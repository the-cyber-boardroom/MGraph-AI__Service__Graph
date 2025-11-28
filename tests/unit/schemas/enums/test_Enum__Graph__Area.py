from unittest                                                                            import TestCase
from enum                                                                                import Enum
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Area                             import Enum__Graph__Area


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
        assert str(Enum__Graph__Area.GRAPH_CRUD) == "Enum__Graph__Area.GRAPH_CRUD"

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