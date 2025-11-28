from unittest                                                                            import TestCase
from enum                                                                                import Enum
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Methods__Export                  import Enum__Graph__Methods__Export

class test_Enum__Graph__Methods__Export(TestCase):

    def test__all_methods(self):                                                         # Test all Export method enum values
        assert Enum__Graph__Methods__Export.EXPORT_JSON    == "export_json"
        assert Enum__Graph__Methods__Export.EXPORT_DOT     == "export_dot"
        assert Enum__Graph__Methods__Export.EXPORT_MERMAID == "export_mermaid"
        assert Enum__Graph__Methods__Export.SCREENSHOT     == "screenshot"

    def test__is_string_enum(self):                                                      # Test enum is string-based
        assert issubclass(Enum__Graph__Methods__Export, str)
        assert issubclass(Enum__Graph__Methods__Export, Enum)

    def test__enum_count(self):                                                          # Test expected method count
        methods = list(Enum__Graph__Methods__Export)
        assert len(methods) == 4