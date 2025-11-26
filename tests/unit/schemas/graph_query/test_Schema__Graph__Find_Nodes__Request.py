from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                    import Type_Safe__List
from osbot_utils.type_safe.primitives.core.Safe_UInt                                     import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                    import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id          import Safe_Str__Id
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request      import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response     import Schema__Graph__Find_Nodes__Response


class test_Schema__Graph__Find_Nodes__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Find_Nodes__Request() as _:
            assert type(_)            is Schema__Graph__Find_Nodes__Request
            assert base_classes(_)    == [Type_Safe, object]
            assert type(_.graph_id)   is Random_Guid
            assert type(_.node_type)  is Safe_Str__Id
            assert type(_.limit)      is Safe_UInt
            assert type(_.offset)     is Safe_UInt
            assert _.limit            == 100                                             # Default value
            assert _.offset           == 0                                               # Default value

            assert _.obj() == __(graph_id  = _.graph_id  ,
                                 node_type = _.node_type ,
                                 limit     = 100         ,
                                 offset    = 0           )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id  = Random_Guid()
        node_type = Safe_Str__Id("Person")

        with Schema__Graph__Find_Nodes__Request(graph_id  = graph_id  ,
                                                node_type = node_type ,
                                                limit     = 50        ,
                                                offset    = 10        ) as _:
            assert _.graph_id  == graph_id
            assert _.node_type == node_type
            assert _.limit     == 50
            assert _.offset    == 10

    def test__pagination_defaults(self):                                                 # Test default pagination values
        with Schema__Graph__Find_Nodes__Request() as _:
            assert _.limit  == 100                                                       # Default limit
            assert _.offset == 0                                                         # Default offset

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        with Schema__Graph__Find_Nodes__Request(node_type = "Entity" ,
                                                limit     = 25       ,
                                                offset    = 5        ) as original:
            json_data = original.json()

            with Schema__Graph__Find_Nodes__Request.from_json(json_data) as restored:
                assert type(restored.graph_id)  is Random_Guid
                assert type(restored.node_type) is Safe_Str__Id
                assert type(restored.limit)     is Safe_UInt
                assert type(restored.offset)    is Safe_UInt
                assert restored.limit           == 25
                assert restored.offset          == 5


class test_Schema__Graph__Find_Nodes__Response(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Find_Nodes__Response() as _:
            assert type(_)             is Schema__Graph__Find_Nodes__Response
            assert base_classes(_)     == [Type_Safe, object]
            assert type(_.graph_id)    is Random_Guid
            assert type(_.node_ids)    is Type_Safe__List                                # Type_Safe__List not raw list
            assert type(_.total_found) is Safe_UInt
            assert type(_.has_more)    is bool
            assert _.has_more          is False

            assert _.obj() == __(graph_id    = _.graph_id ,
                                 node_ids    = []         ,
                                 total_found = 0          ,
                                 has_more    = False      )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id  = Random_Guid()
        node_ids  = [Obj_Id(), Obj_Id(), Obj_Id()]

        with Schema__Graph__Find_Nodes__Response(graph_id    = graph_id  ,
                                                 node_ids    = node_ids  ,
                                                 total_found = 100       ,
                                                 has_more    = True      ) as _:
            assert _.graph_id    == graph_id
            assert len(_.node_ids) == 3
            assert _.total_found == 100
            assert _.has_more    is True

    def test__empty_results(self):                                                       # Test with no results
        with Schema__Graph__Find_Nodes__Response(node_ids    = []   ,
                                                 total_found = 0    ,
                                                 has_more    = False) as _:
            assert len(_.node_ids) == 0
            assert _.total_found   == 0
            assert _.has_more      is False

    def test__pagination_scenario(self):                                                 # Test pagination with more results
        node_ids = [Obj_Id() for _ in range(10)]

        with Schema__Graph__Find_Nodes__Response(node_ids    = node_ids ,
                                                 total_found = 50       ,
                                                 has_more    = True     ) as _:
            assert len(_.node_ids) == 10
            assert _.total_found   == 50
            assert _.has_more      is True                                               # More results available

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        node_ids = [Obj_Id(), Obj_Id()]
        with Schema__Graph__Find_Nodes__Response(node_ids    = node_ids ,
                                                 total_found = 25       ,
                                                 has_more    = True     ) as original:
            json_data = original.json()

            with Schema__Graph__Find_Nodes__Response.from_json(json_data) as restored:
                assert type(restored.graph_id)    is Random_Guid
                assert type(restored.total_found) is Safe_UInt
                assert restored.total_found       == 25
                assert restored.has_more          is True