from unittest                                                                            import TestCase
from enum                                                                                import Enum
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Methods__Cache                   import Enum__Graph__Methods__Cache

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


