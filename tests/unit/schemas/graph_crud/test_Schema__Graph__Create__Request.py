from unittest                                                                            import TestCase
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request           import Schema__Graph__Create__Request


class test_Schema__Graph__Create__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Create__Request() as _:
            assert type(_)         is Schema__Graph__Create__Request
            assert base_classes(_) == [Type_Safe, object]
            assert _.graph_name    is None
            assert _.auto_cache    is True                                               # Default value
            assert _.namespace     == 'graph-service'                                          # Default value

    def test__with_values(self):                                                         # Test with explicit values
        with Schema__Graph__Create__Request(graph_name = "my-graph"  ,
                                            auto_cache = False       ,
                                            namespace  = "custom-ns" ) as _:
            assert _.graph_name == "my-graph"
            assert _.auto_cache is False
            assert _.namespace  == "custom-ns"


