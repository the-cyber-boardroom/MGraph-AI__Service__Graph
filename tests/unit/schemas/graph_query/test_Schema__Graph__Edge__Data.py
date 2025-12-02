from unittest                                                                               import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                                      import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                                      import Node_Id
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                       import Type_Safe__Dict
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Edge__Data                  import Schema__Graph__Edge__Data


class test_Schema__Graph__Edge__Data(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Schema__Graph__Edge__Data() as _:
            assert type(_)              is Schema__Graph__Edge__Data
            assert base_classes(_)      == [Type_Safe, object]
            assert type(_.edge_id)      is Edge_Id
            assert type(_.from_node_id) is Node_Id
            assert type(_.to_node_id)   is Node_Id
            assert type(_.edge_type)    is Safe_Str__Id
            assert type(_.edge_data)    is Type_Safe__Dict

    def test__init__obj_comparison(self):                                                   # Test .obj() with default values
        with Schema__Graph__Edge__Data() as _:
            assert _.obj() == __(edge_id      = _.edge_id     ,
                                 from_node_id = _.from_node_id,
                                 to_node_id   = _.to_node_id  ,
                                 edge_type    = _.edge_type   ,
                                 edge_data    = __()          )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Assignment Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__with_values(self):                                                            # Test with explicit values
        edge_id      = Edge_Id(Obj_Id())
        from_node_id = Node_Id(Obj_Id())
        to_node_id   = Node_Id(Obj_Id())
        edge_type    = Safe_Str__Id('KNOWS')
        edge_data    = {Safe_Str__Key('since'): '2024'}

        with Schema__Graph__Edge__Data(edge_id      = edge_id     ,
                                       from_node_id = from_node_id,
                                       to_node_id   = to_node_id  ,
                                       edge_type    = edge_type   ,
                                       edge_data    = edge_data   ) as _:
            assert _.edge_id      == edge_id
            assert _.from_node_id == from_node_id
            assert _.to_node_id   == to_node_id
            assert _.edge_type    == edge_type

    def test__with_self_loop(self):                                                         # Test self-referential edge
        node_id   = Obj_Id()
        edge_id   = Obj_Id()
        edge_type = Safe_Str__Id('SELF_REF')

        with Schema__Graph__Edge__Data(edge_id      = edge_id  ,
                                       from_node_id = node_id  ,
                                       to_node_id   = node_id  ,
                                       edge_type    = edge_type) as _:
            assert _.from_node_id == _.to_node_id                                           # Self-loop

    def test__with_multiple_data_fields(self):                                              # Test edge with multiple data fields
        edge_id   = Obj_Id()
        edge_type = Safe_Str__Id('CONNECTS')
        edge_data = {Safe_Str__Key('weight')  : '1.5'   ,
                     Safe_Str__Key('label')   : 'link'  ,
                     Safe_Str__Key('created') : 'today' }

        with Schema__Graph__Edge__Data(edge_id   = edge_id  ,
                                       edge_type = edge_type,
                                       edge_data = edge_data) as _:
            assert len(_.edge_data) == 3

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Validation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__field_types(self):                                                            # Test all field types
        edge_id      = Obj_Id()
        from_node_id = Obj_Id()
        to_node_id   = Obj_Id()
        edge_type    = Safe_Str__Id('RELATES')

        with Schema__Graph__Edge__Data(edge_id      = edge_id     ,
                                       from_node_id = from_node_id,
                                       to_node_id   = to_node_id  ,
                                       edge_type    = edge_type   ) as _:
            assert type(_.edge_id)      is Edge_Id
            assert type(_.from_node_id) is Node_Id
            assert type(_.to_node_id)   is Node_Id
            assert type(_.edge_type)    is Safe_Str__Id
            assert type(_.edge_data)    is Type_Safe__Dict

    def test__id_validity(self):                                                            # Test that IDs are valid UUIDs
        with Schema__Graph__Edge__Data() as _:
            assert len(_.edge_id)      == 0
            assert len(_.from_node_id) == 0
            assert len(_.to_node_id)   == 0

    # ═══════════════════════════════════════════════════════════════════════════════
    # Serialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__serialization_round_trip__minimal(self):                                      # Test JSON round-trip with minimal data
        with Schema__Graph__Edge__Data() as original:
            json_data = original.json()

            with Schema__Graph__Edge__Data.from_json(json_data) as restored:
                assert restored.edge_id      == original.edge_id
                assert restored.from_node_id == original.from_node_id
                assert restored.to_node_id   == original.to_node_id
                assert restored.edge_type    == original.edge_type

    def test__serialization_round_trip__complete(self):                                     # Test JSON round-trip with all fields
        edge_data = {Safe_Str__Key('weight'): '2.5'}

        with Schema__Graph__Edge__Data(edge_id      = Obj_Id()           ,
                                       from_node_id = Obj_Id()           ,
                                       to_node_id   = Obj_Id()           ,
                                       edge_type    = Safe_Str__Id('HAS'),
                                       edge_data    = edge_data          ) as original:
            json_data = original.json()

            with Schema__Graph__Edge__Data.from_json(json_data) as restored:
                assert restored.edge_id      == original.edge_id
                assert restored.from_node_id == original.from_node_id
                assert restored.to_node_id   == original.to_node_id
                assert restored.edge_type    == original.edge_type

    def test__serialization_preserves_types(self):                                          # Test that types are preserved
        with Schema__Graph__Edge__Data(edge_type = Safe_Str__Id('LINK')) as original:
            json_data = original.json()

            with Schema__Graph__Edge__Data.from_json(json_data) as restored:
                assert type(restored.edge_id)      is Edge_Id
                assert type(restored.from_node_id) is Node_Id
                assert type(restored.to_node_id)   is Node_Id
                assert type(restored.edge_type)    is Safe_Str__Id
                assert type(restored.edge_data)    is Type_Safe__Dict

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__empty_edge_data(self):                                                        # Test with empty edge_data
        with Schema__Graph__Edge__Data(edge_type = Safe_Str__Id('SIMPLE')) as _:
            assert len(_.edge_data) == 0
            assert type(_.edge_data) is Type_Safe__Dict

    def test__edge_type_sanitization(self):                                                 # Test edge type with special chars
        with Schema__Graph__Edge__Data(edge_type = 'HAS-RELATIONSHIP') as _:
            assert type(_.edge_type) is Safe_Str__Id                                        # Auto-converted