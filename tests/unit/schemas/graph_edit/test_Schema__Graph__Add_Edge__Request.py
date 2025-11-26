from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                    import Type_Safe__Dict
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id          import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key         import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text             import Safe_Str__Text
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Request         import Schema__Graph__Add_Edge__Request


class test_Schema__Graph__Add_Edge__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Add_Edge__Request() as _:
            assert type(_)              is Schema__Graph__Add_Edge__Request
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.graph_id)     is Obj_Id
            assert type(_.from_node_id) is Obj_Id
            assert type(_.to_node_id)   is Obj_Id
            assert type(_.edge_type)    is Safe_Str__Id
            assert type(_.edge_data)    is Type_Safe__Dict
            assert _.auto_cache         is True

            assert _.obj() == __(graph_id     = _.graph_id     ,
                                 from_node_id = _.from_node_id ,
                                 to_node_id   = _.to_node_id   ,
                                 edge_type    = _.edge_type    ,
                                 edge_data    = __()           ,
                                 auto_cache   = True           )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id     = Obj_Id()
        from_node_id = Obj_Id()
        to_node_id   = Obj_Id()
        edge_type    = Safe_Str__Id("KNOWS")
        edge_data    = {Safe_Str__Key("since"): Safe_Str__Text("2024")}

        with Schema__Graph__Add_Edge__Request(graph_id     = graph_id     ,
                                              from_node_id = from_node_id ,
                                              to_node_id   = to_node_id   ,
                                              edge_type    = edge_type    ,
                                              edge_data    = edge_data    ,
                                              auto_cache   = False        ) as _:
            assert _.graph_id     == graph_id
            assert _.from_node_id == from_node_id
            assert _.to_node_id   == to_node_id
            assert _.edge_type    == edge_type
            assert _.auto_cache   is False

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        edge_data = {Safe_Str__Key("weight"): Safe_Str__Text("1.5")}
        with Schema__Graph__Add_Edge__Request(edge_type  = "CONTAINS" ,
                                              edge_data  = edge_data  ,
                                              auto_cache = True       ) as original:
            json_data = original.json()

            with Schema__Graph__Add_Edge__Request.from_json(json_data) as restored:
                assert type(restored.graph_id)     is Obj_Id
                assert type(restored.from_node_id) is Obj_Id
                assert type(restored.to_node_id)   is Obj_Id
                assert type(restored.edge_type)    is Safe_Str__Id

                assert restored.obj () == original.obj ()
                assert restored.json() == original.json()


