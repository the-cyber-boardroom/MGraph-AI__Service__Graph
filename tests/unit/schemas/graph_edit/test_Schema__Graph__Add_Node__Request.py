from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                    import Type_Safe__Dict
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                    import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                         import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id          import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key         import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text             import Safe_Str__Text
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Request         import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Response        import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Request         import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Response        import Schema__Graph__Add_Edge__Response


class test_Schema__Graph__Add_Node__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Add_Node__Request() as _:
            assert type(_)            is Schema__Graph__Add_Node__Request
            assert base_classes(_)    == [Type_Safe, object]
            assert type(_.graph_id)   is Random_Guid
            assert type(_.node_type)  is Safe_Str__Id
            assert type(_.node_data)  is Type_Safe__Dict                                 # Type_Safe__Dict not raw dict
            assert _.auto_cache       is True                                            # Default value

            assert _.obj() == __(graph_id   = _.graph_id  ,
                                 node_type  = _.node_type ,
                                 node_data  = {}          ,
                                 auto_cache = True        )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id  = Random_Guid()
        node_type = Safe_Str__Id("Person")
        node_data = {Safe_Str__Key("name"): Safe_Str__Text("Alice")}

        with Schema__Graph__Add_Node__Request(graph_id   = graph_id   ,
                                              node_type  = node_type  ,
                                              node_data  = node_data  ,
                                              auto_cache = False      ) as _:
            assert _.graph_id   == graph_id
            assert _.node_type  == node_type
            assert _.node_data  == node_data
            assert _.auto_cache is False

    def test__type_safe_dict_enforcement(self):                                          # Test Dict uses type-safe keys/values
        with Schema__Graph__Add_Node__Request() as _:
            # Should accept type-safe dict
            _.node_data = {Safe_Str__Key("key1"): Safe_Str__Text("value1")}
            assert len(_.node_data) == 1

    def test__serialization_round_trip(self):                                            # Test JSON round-trip
        node_data = {Safe_Str__Key("name"): Safe_Str__Text("Bob")}
        with Schema__Graph__Add_Node__Request(node_type  = "Entity"   ,
                                              node_data  = node_data  ,
                                              auto_cache = False      ) as original:
            json_data = original.json()

            with Schema__Graph__Add_Node__Request.from_json(json_data) as restored:
                assert type(restored.graph_id)  is Random_Guid
                assert type(restored.node_type) is Safe_Str__Id


class test_Schema__Graph__Add_Node__Response(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Add_Node__Response() as _:
            assert type(_)           is Schema__Graph__Add_Node__Response
            assert base_classes(_)   == [Type_Safe, object]
            assert type(_.node_id)   is Obj_Id
            assert type(_.graph_id)  is Random_Guid
            assert type(_.cached)    is bool
            assert _.cached          is False

            assert _.obj() == __(node_id  = _.node_id  ,
                                 graph_id = _.graph_id ,
                                 cached   = False      )

    def test__with_values(self):                                                         # Test with explicit values
        node_id  = Obj_Id()
        graph_id = Random_Guid()

        with Schema__Graph__Add_Node__Response(node_id  = node_id  ,
                                               graph_id = graph_id ,
                                               cached   = True     ) as _:
            assert _.node_id  == node_id
            assert _.graph_id == graph_id
            assert _.cached   is True


class test_Schema__Graph__Add_Edge__Request(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Add_Edge__Request() as _:
            assert type(_)              is Schema__Graph__Add_Edge__Request
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.graph_id)     is Random_Guid
            assert type(_.from_node_id) is Obj_Id
            assert type(_.to_node_id)   is Obj_Id
            assert type(_.edge_type)    is Safe_Str__Id
            assert type(_.edge_data)    is Type_Safe__Dict
            assert _.auto_cache         is True

            assert _.obj() == __(graph_id     = _.graph_id     ,
                                 from_node_id = _.from_node_id ,
                                 to_node_id   = _.to_node_id   ,
                                 edge_type    = _.edge_type    ,
                                 edge_data    = {}             ,
                                 auto_cache   = True           )

    def test__with_values(self):                                                         # Test with explicit values
        graph_id     = Random_Guid()
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
                assert type(restored.graph_id)     is Random_Guid
                assert type(restored.from_node_id) is Obj_Id
                assert type(restored.to_node_id)   is Obj_Id
                assert type(restored.edge_type)    is Safe_Str__Id


class test_Schema__Graph__Add_Edge__Response(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Schema__Graph__Add_Edge__Response() as _:
            assert type(_)           is Schema__Graph__Add_Edge__Response
            assert base_classes(_)   == [Type_Safe, object]
            assert type(_.edge_id)   is Obj_Id
            assert type(_.graph_id)  is Random_Guid
            assert type(_.cached)    is bool
            assert _.cached          is False

            assert _.obj() == __(edge_id  = _.edge_id  ,
                                 graph_id = _.graph_id ,
                                 cached   = False      )

    def test__with_values(self):                                                         # Test with explicit values
        edge_id  = Obj_Id()
        graph_id = Random_Guid()

        with Schema__Graph__Add_Edge__Response(edge_id  = edge_id  ,
                                               graph_id = graph_id ,
                                               cached   = True     ) as _:
            assert _.edge_id  == edge_id
            assert _.graph_id == graph_id
            assert _.cached   is True