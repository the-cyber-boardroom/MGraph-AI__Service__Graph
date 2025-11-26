from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id          import Safe_Str__Id
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request              import Schema__Graph__Get__Request


class test_Schema__Graph__Get__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Get__Request() as _:
            assert type(_)            is Schema__Graph__Get__Request
            assert base_classes(_)    == [Type_Safe, object]
            assert type(_.graph_id)   is Obj_Id
            assert type(_.namespace)  is Safe_Str__Id
            assert _.namespace        == "default"                                       # Default value

            assert _.obj() == __(graph_id  = _.graph_id ,                                # Auto-generated
                                 namespace = "default"  )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id  = Obj_Id()
        namespace = Safe_Str__Id("test-namespace")

        with Schema__Graph__Get__Request(graph_id=graph_id, namespace=namespace) as _:
            assert _.graph_id  == graph_id
            assert _.namespace == namespace

            assert _.obj() == __(graph_id  = graph_id       ,
                                 namespace = "test-namespace")

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        with Schema__Graph__Get__Request(namespace="my-namespace") as original:
            json_data = original.json()

            with Schema__Graph__Get__Request.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.graph_id)  is Obj_Id
                assert type(restored.namespace) is Safe_Str__Id


