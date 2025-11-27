from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                       import Type_Safe__Dict
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Edge__Data                  import Schema__Graph__Edge__Data


class test_Schema__Graph__Edge__Data(TestCase):

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Edge__Data() as _:
            assert type(_)              is Schema__Graph__Edge__Data
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.edge_id)      is Obj_Id
            assert type(_.from_node_id) is Obj_Id
            assert type(_.to_node_id)   is Obj_Id
            assert type(_.edge_type)    is Safe_Str__Id
            assert type(_.edge_data)    is Type_Safe__Dict

    def test__with_values(self):                                                            # Test with explicit values
        edge_id      = Obj_Id()
        from_node_id = Obj_Id()
        to_node_id   = Obj_Id()
        edge_type    = Safe_Str__Id('KNOWS')
        edge_data    = {Safe_Str__Key('since'): Safe_Str__Text('2024')}

        with Schema__Graph__Edge__Data(edge_id      = edge_id     ,
                                       from_node_id = from_node_id,
                                       to_node_id   = to_node_id  ,
                                       edge_type    = edge_type   ,
                                       edge_data    = edge_data   ) as _:
            assert _.edge_id      == edge_id
            assert _.from_node_id == from_node_id
            assert _.to_node_id   == to_node_id
            assert _.edge_type    == edge_type




