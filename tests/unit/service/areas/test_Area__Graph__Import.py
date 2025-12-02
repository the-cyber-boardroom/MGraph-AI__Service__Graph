import inspect
from unittest                                                                                   import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Index__Data                                       import Schema__MGraph__Index__Data
from mgraph_db.mgraph.actions.MGraph__Index                                                     import MGraph__Index
from osbot_utils.testing.__                                                                     import __, __SKIP__
from mgraph_ai_service_graph.utils.testing.Graph_Test_Helpers                                   import Graph_Test_Helpers
from mgraph_db.mgraph.MGraph                                                                    import MGraph
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Objects                                                                  import base_classes
from mgraph_ai_service_graph.service.areas.Area__Graph__Import                                  import Area__Graph__Import
from mgraph_ai_service_graph.service.graph.Graph__Service                                       import Graph__Service
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                               import Graph__Cache__Client
from mgraph_ai_service_graph.schemas.graph_import.Schema__Graph__Import                         import Schema__Graph__Import__Request
from mgraph_ai_service_graph.schemas.graph_import.Schema__Graph__Import                         import Schema__Graph__Import__Compressed__Request
from mgraph_ai_service_graph.schemas.graph_import.Schema__Graph__Import                         import Schema__Graph__Import__Response
from tests.unit.Graph__Service__Fast_API__Test_Objs                                             import client_cache_service


class test_Area__Graph__Import(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client, cls.cache_service = client_cache_service()
        cls.graph_cache_client              = Graph__Cache__Client(cache_client = cls.cache_client)
        cls.graph_service                   = Graph__Service      (graph_cache_client = cls.graph_cache_client)
        cls.area_import                     = Area__Graph__Import (graph_service      = cls.graph_service)
        cls.graph_test_helpers              = Graph_Test_Helpers  (cache_client       = cls.cache_client)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _create_sample_graph_json(self) -> dict:                                                # Create a sample graph JSON for import testing
        mgraph    = MGraph()
        graph_id  = str(mgraph.graph.model.data.graph_id)
        mgraph.edit().new_node()                                                                # Add a node
        mgraph.edit().new_node()                                                                # Add another node
        return mgraph.json()

    def _create_sample_graph_compressed_json(self) -> dict:                                     # Create a sample compressed graph JSON
        mgraph = MGraph()
        mgraph.edit().new_node()
        mgraph.edit().new_node()
        return mgraph.json__compress()

    def _create_graph_with_edges_json(self) -> dict:                                            # Create graph with nodes and edges
        mgraph     = MGraph()
        node_1     = mgraph.edit().new_node()
        node_2     = mgraph.edit().new_node()
        node_1_id  = node_1.node_id
        node_2_id  = node_2.node_id
        mgraph.edit().new_edge(from_node_id=node_1_id, to_node_id=node_2_id)
        return mgraph.json()

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                     # Test auto-initialization
        with Area__Graph__Import() as _:
            assert type(_)               is Area__Graph__Import
            assert base_classes(_)       == [Type_Safe, object]
            assert type(_.graph_service) is Graph__Service

    def test__graph_service_dependency(self):                                                   # Test graph service is injected
        with Area__Graph__Import() as _:
            assert _.graph_service is not None
            assert type(_.graph_service) is Graph__Service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__method_signatures(self):                                                          # Test all methods exist
        with Area__Graph__Import() as _:
            assert hasattr(_, 'import_graph')                                                   # Check all expected methods exist
            assert hasattr(_, 'import_graph_compressed')

            assert callable(_.import_graph)                                                     # All should be callable
            assert callable(_.import_graph_compressed)

    def test__import_graph__method_signature(self):                                             # Test import_graph signature
        with Area__Graph__Import() as _:
            sig    = inspect.signature(_.import_graph)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Import__Request
            assert sig.return_annotation == Schema__Graph__Import__Response

    def test__import_graph_compressed__method_signature(self):                                  # Test import_graph_compressed signature
        with Area__Graph__Import() as _:
            sig    = inspect.signature(_.import_graph_compressed)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Import__Compressed__Request
            assert sig.return_annotation == Schema__Graph__Import__Response

    # ═══════════════════════════════════════════════════════════════════════════════
    # Import Graph Tests - Standard Format
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__import_graph__basic(self):                                                        # Test basic graph import
        with self.area_import as _:
            graph_json = self._create_sample_graph_json()
            namespace  = 'test-import'

            request  = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                      namespace   = namespace ,
                                                      auto_cache  = True      ,
                                                      build_index = False     ,
                                                      validate    = True      )
            response = _.import_graph(request)
            graph_ref = response.graph_ref
            cache_id  = graph_ref.cache_id
            graph_id  = graph_ref.graph_id
            assert type(response)                   is Schema__Graph__Import__Response
            assert response.obj()                   == __(graph_ref=__( cache_id = cache_id,
                                                                        graph_id = graph_id,
                                                                        namespace='test-import'),
                                                           index_cached=False,
                                                           cached=True,
                                                           success=True,
                                                           nodes_count=2,
                                                           edges_count=0,
                                                           validation_errors=[])
            assert response.nodes_count             >= 2                                         # At least 2 nodes
            assert response.cached                  is True                                      # auto_cache was True
            assert response.index_cached            is False                                     # build_index was False
            assert len(response.validation_errors)  == 0                                         # No validation errors

            assert response.graph_ref           is not None
            assert response.graph_ref.cache_id  is not None
            assert response.graph_ref.namespace == namespace

            graph_dict = self.graph_test_helpers.get_graph(graph_ref=response.graph_ref).mgraph
            assert graph_dict == graph_json

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    def test__import_graph__with_validation(self):                                              # Test import with validation enabled
        with self.area_import as _:
            graph_json = self._create_graph_with_edges_json()
            namespace  = 'test-import-validate'

            request  = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                       namespace   = namespace ,
                                                       auto_cache  = True      ,
                                                       build_index = False     ,
                                                       validate    = True      )
            response = _.import_graph(request)

            assert type(response)                  is Schema__Graph__Import__Response
            assert response.obj()                  == __(graph_ref         = response.graph_ref.obj(),
                                                         index_cached      = False,
                                                         cached            = True ,
                                                         success           = True ,
                                                         nodes_count       = 2    ,
                                                         edges_count       = 1    ,
                                                         validation_errors = []   )
            assert response.nodes_count            >= 2
            assert response.edges_count            >= 1                                                    # Has edge
            assert len(response.validation_errors) == 0

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    def test__regression__set__json__serialisation_issue(self):
        import json
        from typing import Dict, Set
        from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id import Safe_Id
        from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id import Edge_Id

        class An_Class(Type_Safe):
            an_dict : Dict[Safe_Id  , Set[Edge_Id ]]
        safe_id = Safe_Id('safe-id_jlqsh')
        edge_id = Edge_Id('6106b8e7')
        an_class = An_Class()
        an_class.an_dict[safe_id] = {edge_id}
        # assert an_class.obj () == __(an_dict=__(safe_id_jlqsh={'6106b8e7'}))              # BUG, this should be list,  i.e. ('6106b8e7')
        # assert an_class.json() == {'an_dict': {'safe-id_jlqsh': {'6106b8e7'}}}            # BUG, this should be list,  i.e. ('6106b8e7')
        assert an_class.obj () == __(an_dict=__(safe_id_jlqsh=['6106b8e7']))                # FIXED
        assert an_class.json() == {'an_dict': {'safe-id_jlqsh': ['6106b8e7']}}              # FIXED

        # error_message = "Object of type set is not JSON serializable"
        # with pytest.raises(TypeError, match=error_message):                             # BUG
        #     json.dumps(an_class.json())
        assert json.dumps(an_class.json()) == '{"an_dict": {"safe-id_jlqsh": ["6106b8e7"]}}'    # FIXED
        assert type(an_class.json().get('an_dict')                     ) is dict
        #assert type(an_class.json().get('an_dict').get('safe-id_jlqsh')) is set         # BUG
        assert type(an_class.json().get('an_dict').get('safe-id_jlqsh')) is list         # FIXED

    def test__regression__mgraph_index_serialisation_issue(self):
        with MGraph() as mgraph:
            with mgraph.index() as _:
                assert type(_)            is MGraph__Index
                assert type(_.index_data) is Schema__MGraph__Index__Data
                assert _.index_data.obj() == __(edges_by_path=__(),
                                               edges_by_predicate=__(),
                                               edges_by_incoming_label=__(),
                                               edges_by_outgoing_label=__(),
                                               edges_by_type=__(),
                                               edges_predicates=__(),
                                               edges_to_nodes=__(),
                                               edges_types=__(),
                                               nodes_by_path=__(),
                                               nodes_by_type=__(),
                                               nodes_to_incoming_edges=__(),
                                               nodes_to_incoming_edges_by_type=__(),
                                               nodes_to_outgoing_edges=__(),
                                               nodes_to_outgoing_edges_by_type=__(),
                                               nodes_types=__())
                assert _.index_data.json() == {  'edges_by_incoming_label': {},
                                                 'edges_by_outgoing_label': {},
                                                 'edges_by_path': {},
                                                 'edges_by_predicate': {},
                                                 'edges_by_type': {},
                                                 'edges_predicates': {},
                                                 'edges_to_nodes': {},
                                                 'edges_types': {},
                                                 'nodes_by_path': {},
                                                 'nodes_by_type': {},
                                                 'nodes_to_incoming_edges': {},
                                                 'nodes_to_incoming_edges_by_type': {},
                                                 'nodes_to_outgoing_edges': {},
                                                 'nodes_to_outgoing_edges_by_type': {},
                                                 'nodes_types': {}}

                import json
                assert json.dumps(_.index_data.json()) == ('{"edges_by_path": {}, "edges_by_predicate": {}, "edges_by_incoming_label": '
                                                             '{}, "edges_by_outgoing_label": {}, "edges_by_type": {}, "edges_predicates": '
                                                             '{}, "edges_to_nodes": {}, "edges_types": {}, "nodes_by_path": {}, '
                                                             '"nodes_by_type": {}, "nodes_to_incoming_edges": {}, '
                                                             '"nodes_to_incoming_edges_by_type": {}, "nodes_to_outgoing_edges": {}, '
                                                             '"nodes_to_outgoing_edges_by_type": {}, "nodes_types": {}}')
                with mgraph.edit() as edit:
                    node_id = '3fc3b36f'
                    edit.new_node(node_id=node_id)
                assert type(_.index_data.json()) is dict
                assert type(_.index_data.obj()) is __
                assert _.index_data.json()  == {'edges_by_incoming_label': {},
                                                 'edges_by_outgoing_label': {},
                                                 'edges_by_path': {},
                                                 'edges_by_predicate': {},
                                                 'edges_by_type': {},
                                                 'edges_predicates': {},
                                                 'edges_to_nodes': {},
                                                 'edges_types': {},
                                                 'nodes_by_path': {},
                                                 'nodes_by_type': {'Schema__MGraph__Node': ['3fc3b36f']},
                                                 'nodes_to_incoming_edges': {'3fc3b36f': []},
                                                 'nodes_to_incoming_edges_by_type': {},
                                                 'nodes_to_outgoing_edges': {'3fc3b36f': []},
                                                 'nodes_to_outgoing_edges_by_type': {},
                                                 'nodes_types': {'3fc3b36f': 'Schema__MGraph__Node'}}

                # error_message = "Object of type set is not JSON serializable"
                # with pytest.raises(TypeError, match = error_message) as e:
                #     assert type(json.dumps(_.index_data.json())) is str
                assert type(json.dumps(_.index_data.json()))       == str
                assert json.loads(json.dumps(_.index_data.json())) == _.index_data.json()



    def test__import_graph__with_index_build(self):                                             # Test import with index building
        with self.area_import as _:
            graph_json = self._create_graph_with_edges_json()                    # todo: move to setUpClass
            namespace  = 'test-import-index'

            request  = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                       namespace   = namespace ,
                                                       auto_cache  = True      ,
                                                       build_index = True      ,
                                                       validate    = True      )
            response = _.import_graph(request)

            assert type(response)        is Schema__Graph__Import__Response
            assert response.obj()        == __(graph_ref         = response.graph_ref.obj(),
                                               index_cached      = True,                        # BUG
                                               cached            = True ,
                                               success           = True ,
                                               nodes_count       = 2    ,
                                               edges_count       = 1    ,
                                               validation_errors = []   )
            assert response.nodes_count  >= 2
            assert response.cached       is True
            assert response.index_cached is True                                                # Index was built
            #assert response.index_cached is False            # BUG

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    def test__import_graph__no_auto_cache(self):                                                # Test import without auto-cache
        with self.area_import as _:
            graph_json = self._create_sample_graph_json()
            namespace  = 'test-import-no-cache'

            request  = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                       namespace   = namespace ,
                                                       auto_cache  = False     ,
                                                       build_index = False     ,
                                                       validate    = False     )
            response = _.import_graph(request)

            assert type(response)    is Schema__Graph__Import__Response
            assert response.cached   is False                                                   # Not cached
            assert response.graph_ref is not None

    def test__import_graph__invalid_data(self):                                                 # Test import with invalid graph data
        with self.area_import as _:
            invalid_json = {'invalid': 'data'}                                                  # Missing required structure
            namespace    = 'test-import-invalid'

            request  = Schema__Graph__Import__Request(graph_data  = invalid_json,
                                                       namespace   = namespace  ,
                                                       auto_cache  = True       ,
                                                       build_index = False      ,
                                                       validate    = True       )
            response = _.import_graph(request)

            assert type(response) is Schema__Graph__Import__Response
            assert len(response.validation_errors) > 0                                          # Should have errors

    def test__import_graph__empty_graph(self):                                                  # Test import of empty graph
        with self.area_import as _:
            mgraph     = MGraph()
            graph_json = mgraph.json()
            namespace  = 'test-import-empty'

            request  = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                       namespace   = namespace ,
                                                       auto_cache  = True      ,
                                                       build_index = False     ,
                                                       validate    = True      )
            response = _.import_graph(request)

            assert type(response)       is Schema__Graph__Import__Response
            assert response.nodes_count == 0                                                    # Empty graph
            assert response.edges_count == 0
            assert len(response.validation_errors) == 0

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Import Graph Tests - Compressed Format
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__import_graph_compressed__basic(self):                                             # Test compressed graph import
        with self.area_import as _:
            compressed_json = self._create_sample_graph_compressed_json()
            namespace       = 'test-import-compressed'

            request  = Schema__Graph__Import__Compressed__Request(graph_data  = compressed_json,
                                                                   namespace   = namespace      ,
                                                                   auto_cache  = True           ,
                                                                   build_index = False          )
            response = _.import_graph_compressed(request)

            assert type(response)       is Schema__Graph__Import__Response
            assert response.nodes_count >= 2
            assert response.cached      is True

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    def test__import_graph_compressed__with_index(self):                                        # Test compressed import with index
        with self.area_import as _:
            compressed_json = self._create_sample_graph_compressed_json()
            namespace       = 'test-import-compressed-index'

            request  = Schema__Graph__Import__Compressed__Request(graph_data  = compressed_json,
                                                                   namespace   = namespace      ,
                                                                   auto_cache  = True           ,
                                                                   build_index = True           )
            response = _.import_graph_compressed(request)

            assert type(response)        is Schema__Graph__Import__Response
            assert response.index_cached is True                                                # Index built

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Import and Retrieve Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__import_then_retrieve(self):                                                       # Test import then retrieve graph
        with self.area_import as _:
            graph_json = self._create_graph_with_edges_json()
            namespace  = 'test-import-retrieve'

            request  = Schema__Graph__Import__Request(graph_data  = graph_json,
                                                       namespace   = namespace ,
                                                       auto_cache  = True      ,
                                                       build_index = False     ,
                                                       validate    = True      )
            response = _.import_graph(request)

            assert response.graph_ref is not None
            cache_id = response.graph_ref.cache_id

            # Retrieve the graph using test helpers
            get_response = self.graph_test_helpers.get_graph_by_cache_id(cache_id  = cache_id ,
                                                                          namespace = namespace)

            assert get_response.success is True
            assert get_response.mgraph  is not None

            # Convert back to MGraph and verify structure
            retrieved_mgraph = MGraph.from_json(get_response.mgraph)
            assert len(retrieved_mgraph.graph.model.data.nodes) >= 2
            assert len(retrieved_mgraph.graph.model.data.edges) >= 1

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = cache_id ,
                                                              namespace = namespace)

    def test__import_preserves_graph_structure(self):                                           # Test that import preserves graph structure
        with self.area_import as _:
            # Create a graph with known structure
            original_mgraph = MGraph()
            node_1          = original_mgraph.edit().new_node()
            node_2          = original_mgraph.edit().new_node()
            node_3          = original_mgraph.edit().new_node()
            original_mgraph.edit().new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            original_mgraph.edit().new_edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id)

            original_json       = original_mgraph.json()
            original_node_count = len(original_mgraph.graph.model.data.nodes)
            original_edge_count = len(original_mgraph.graph.model.data.edges)
            namespace           = 'test-preserve-structure'

            # Import
            request  = Schema__Graph__Import__Request(graph_data  = original_json,
                                                       namespace   = namespace   ,
                                                       auto_cache  = True        ,
                                                       build_index = False       ,
                                                       validate    = True        )
            response = _.import_graph(request)

            assert response.nodes_count == original_node_count
            assert response.edges_count == original_edge_count

            # Retrieve and verify
            get_response     = self.graph_test_helpers.get_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                                              namespace = namespace                  )
            retrieved_mgraph = MGraph.from_json(get_response.mgraph)

            assert len(retrieved_mgraph.graph.model.data.nodes) == original_node_count
            assert len(retrieved_mgraph.graph.model.data.edges) == original_edge_count

            # Cleanup
            self.graph_test_helpers.delete_graph_by_cache_id(cache_id  = response.graph_ref.cache_id,
                                                              namespace = namespace                  )
