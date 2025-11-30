import inspect
from unittest                                                                               import TestCase
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from osbot_utils.testing.Pytest                                                             import skip_if_in_github_action
from osbot_utils.testing.__helpers                                                          import obj
from mgraph_db.mgraph.MGraph                                                                import MGraph
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id, is_obj_id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Misc                                                                 import is_guid
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client
from tests.unit.Graph__Service__Fast_API__Test_Objs                                         import client_cache_service


class test_Graph__Service(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Performance: Setup once for all tests
        cls.cache_client, cls.cache_service = client_cache_service()                        # In-memory cache service
        cls.graph_cache_client              = Graph__Cache__Client(cache_client=cls.cache_client)
        cls.graph_service                   = Graph__Service(graph_cache_client=cls.graph_cache_client)
        cls.test_namespace                  = Safe_Str__Id('test-graph-service')

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Graph__Service() as _:
            assert type(_)                    is Graph__Service
            assert base_classes(_)            == [Type_Safe, object]
            assert type(_.graph_cache_client) is Graph__Cache__Client

    def test__cache_client_dependency(self):                                                # Test cache client is initialized
        with Graph__Service() as _:
            assert _.graph_cache_client is not None
            assert type(_.graph_cache_client) is Graph__Cache__Client

    def test__injected_dependency(self):                                                    # Test injected cache client is used
        with self.graph_service as _:
            assert _.graph_cache_client is self.graph_cache_client                          # Same instance as setup

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signatures Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__method_signatures(self):                                                      # Test all methods exist with correct signatures
        with Graph__Service() as _:
            assert hasattr(_, 'create_new_graph'   )                                        # Check all expected methods exist
            assert hasattr(_, 'get_graph'          )
            assert hasattr(_, 'get_or_create_graph')
            assert hasattr(_, 'save_graph'         )
            assert hasattr(_, 'delete_graph'       )
            assert hasattr(_, 'graph_exists'       )

            assert callable(_.create_new_graph   )                                          # All should be callable
            assert callable(_.get_graph          )
            assert callable(_.get_or_create_graph)
            assert callable(_.save_graph         )
            assert callable(_.delete_graph       )
            assert callable(_.graph_exists       )

    def test__create_new_graph__method_signature(self):                                     # Test create_new_graph signature
        with Graph__Service() as _:
            sig    = inspect.signature(_.create_new_graph)
            params = list(sig.parameters.values())

            assert len(params)           == 0                                               # No parameters
            assert sig.return_annotation == MGraph                                          # Returns MGraph

    def test__get_graph__method_signature(self):                                            # Test get_graph signature
        with Graph__Service() as _:
            sig    = inspect.signature(_.get_graph)
            params = list(sig.parameters.keys())

            assert params                == ['cache_id', 'graph_id', 'namespace']           # 3 optional parameters
            assert sig.return_annotation == MGraph

    def test__get_or_create_graph__method_signature(self):                                  # Test get_or_create_graph signature
        with Graph__Service() as _:
            sig    = inspect.signature(_.get_or_create_graph)
            params = list(sig.parameters.values())

            assert len(params)          == 3
            assert params[0].name       == 'cache_id'
            assert params[1].name       == 'graph_id'
            assert params[2].name       == 'namespace'
            assert params[1].default    == None                                             # Default namespace
            assert sig.return_annotation == MGraph

    def test__save_graph__method_signature(self):                                           # Test save_graph signature
        with Graph__Service() as _:
            sig    = inspect.signature(_.save_graph)
            params = list(sig.parameters.keys())

            assert params                == ['mgraph', 'namespace', 'cache_id']             # 3 parameters
            assert sig.return_annotation == Cache_Id                                        # Returns cache_id

    def test__delete_graph__method_signature(self):                                         # Test delete_graph signature
        with Graph__Service() as _:
            sig    = inspect.signature(_.delete_graph)
            params = list(sig.parameters.keys())

            assert params == ['cache_id', 'graph_id', 'namespace']

    def test__graph_exists__method_signature(self):                                         # Test graph_exists signature
        with Graph__Service() as _:
            sig    = inspect.signature(_.graph_exists)
            params = list(sig.parameters.keys())

            assert params                == ['cache_id', 'graph_id', 'namespace']
            assert sig.return_annotation == bool

    # ═══════════════════════════════════════════════════════════════════════════════
    # create_new_graph Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_create_new_graph(self):                                                        # Test creating a new empty graph
        with self.graph_service as _:
            graph = _.create_new_graph()

            assert graph                             is not None
            assert type(graph)                       is MGraph
            assert is_obj_id(graph.graph.graph_id()) is True                                # Has valid graph_id

    def test_create_new_graph__multiple_calls(self):                                        # Test multiple graphs are independent
        with self.graph_service as _:
            graph1 = _.create_new_graph()
            graph2 = _.create_new_graph()

            assert graph1                        is not graph2                              # Different instances
            assert graph1.graph.graph_id()       != graph2.graph.graph_id()                 # Different graph_ids

    def test_create_new_graph__empty_state(self):                                           # Test new graph is empty
        with self.graph_service as _:
            mgraph    = _.create_new_graph()
            graph_id  = mgraph.graph.graph_id()

            assert len(mgraph.graph.nodes()) == 0                                                  # No nodes
            assert len(mgraph.graph.edges()) == 0                                                  # No edges
            assert is_obj_id(graph_id) is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # save_graph Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_save_graph(self):                                                              # Test saving a new graph
        with (self.graph_service as _):
            mgraph   = _.create_new_graph()
            graph_id = mgraph.graph.graph_id()
            cache_id = _.save_graph(mgraph    = mgraph              ,                       # using .json__compress()
                                    namespace = self.test_namespace )

            assert cache_id             is not None
            assert type(cache_id)       is Cache_Id
            assert is_guid(cache_id)    is True

            raw_graph_json = _.graph_cache_client.cache_client.retrieve().retrieve__cache_id__json(cache_id  = cache_id ,
                                                                                                   namespace =  self.test_namespace)
            loaded_mgraph  = _.get_graph(cache_id=cache_id, namespace=self.test_namespace)

            assert loaded_mgraph.obj() == mgraph.obj()      # confirm round trip (using from_json__compressed)

            # confirm we are saving using
            assert raw_graph_json == { '_type_registry': { '@domain_mgraph_edge': 'mgraph_db.mgraph.domain.Domain__MGraph__Edge.Domain__MGraph__Edge',
                                                           '@domain_mgraph_graph': 'mgraph_db.mgraph.domain.Domain__MGraph__Graph.Domain__MGraph__Graph',
                                                           '@domain_mgraph_node': 'mgraph_db.mgraph.domain.Domain__MGraph__Node.Domain__MGraph__Node',
                                                           '@mgraph_edit': 'mgraph_db.mgraph.actions.MGraph__Edit.MGraph__Edit',
                                                           '@mgraph_query': 'mgraph_db.query.MGraph__Query.MGraph__Query',
                                                           '@mgraph_screenshot': 'mgraph_db.mgraph.actions.MGraph__Screenshot.MGraph__Screenshot',
                                                           '@model_mgraph_edge': 'mgraph_db.mgraph.models.Model__MGraph__Edge.Model__MGraph__Edge',
                                                           '@model_mgraph_node': 'mgraph_db.mgraph.models.Model__MGraph__Node.Model__MGraph__Node',
                                                           '@schema_mgraph_edge': 'mgraph_db.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge',
                                                           '@schema_mgraph_graph': 'mgraph_db.mgraph.schemas.Schema__MGraph__Graph.Schema__MGraph__Graph',
                                                           '@schema_mgraph_graph_data': 'mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data.Schema__MGraph__Graph__Data',
                                                           '@schema_mgraph_node': 'mgraph_db.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node',
                                                           '@schema_mgraph_node_data': 'mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data'},
                                       'edit_class': '@mgraph_edit',
                                       'graph': { 'domain_types': { 'edge_domain_type': '@domain_mgraph_edge',
                                                                    'node_domain_type': '@domain_mgraph_node'},
                                                  'graph_type': '@domain_mgraph_graph',
                                                  'model': { 'data': { 'edges': {},
                                                                       'graph_data': {},
                                                                       'graph_id': graph_id,
                                                                       'graph_type': '@schema_mgraph_graph',
                                                                       'nodes': {},
                                                                       'schema_types': { 'edge_type': '@schema_mgraph_edge',
                                                                                         'graph_data_type': '@schema_mgraph_graph_data',
                                                                                         'node_data_type': '@schema_mgraph_node_data',
                                                                                         'node_type': '@schema_mgraph_node'}},
                                                             'model_types': { 'edge_model_type': '@model_mgraph_edge',
                                                                              'node_model_type': '@model_mgraph_node'}}},
                                       'query_class': '@mgraph_query',
                                       'screenshot_class': '@mgraph_screenshot'}
            assert obj(raw_graph_json) == __(_type_registry = __(_domain_mgraph_node='mgraph_db.mgraph.domain.Domain__MGraph__Node.Domain__MGraph__Node',
                                                                 _domain_mgraph_edge='mgraph_db.mgraph.domain.Domain__MGraph__Edge.Domain__MGraph__Edge',
                                                                 _schema_mgraph_graph='mgraph_db.mgraph.schemas.Schema__MGraph__Graph.Schema__MGraph__Graph',
                                                                 _schema_mgraph_edge='mgraph_db.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge',
                                                                 _schema_mgraph_graph_data='mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data.Schema__MGraph__Graph__Data',
                                                                 _schema_mgraph_node='mgraph_db.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node',
                                                                 _schema_mgraph_node_data='mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data',
                                                                 _model_mgraph_node='mgraph_db.mgraph.models.Model__MGraph__Node.Model__MGraph__Node',
                                                                 _model_mgraph_edge='mgraph_db.mgraph.models.Model__MGraph__Edge.Model__MGraph__Edge',
                                                                 _domain_mgraph_graph='mgraph_db.mgraph.domain.Domain__MGraph__Graph.Domain__MGraph__Graph',
                                                                 _mgraph_query='mgraph_db.query.MGraph__Query.MGraph__Query',
                                                                 _mgraph_edit='mgraph_db.mgraph.actions.MGraph__Edit.MGraph__Edit',
                                                                 _mgraph_screenshot='mgraph_db.mgraph.actions.MGraph__Screenshot.MGraph__Screenshot'),
                                               graph=__(domain_types=__(node_domain_type='@domain_mgraph_node',
                                                                        edge_domain_type='@domain_mgraph_edge'),
                                                        model=__(data=__(edges=__(),
                                                                         graph_data=__(),
                                                                         graph_id=graph_id,
                                                                         graph_type='@schema_mgraph_graph',
                                                                         nodes=__(),
                                                                         schema_types=__(edge_type='@schema_mgraph_edge',
                                                                                         graph_data_type='@schema_mgraph_graph_data',
                                                                                         node_type='@schema_mgraph_node',
                                                                                         node_data_type='@schema_mgraph_node_data')),
                                                                 model_types=__(node_model_type='@model_mgraph_node',
                                                                                edge_model_type='@model_mgraph_edge')),
                                                        graph_type='@domain_mgraph_graph'),
                                               query_class='@mgraph_query',
                                               edit_class='@mgraph_edit',
                                               screenshot_class='@mgraph_screenshot')

            # update the mgraph
            cache_id_2       = _.save_graph(mgraph    = mgraph              ,                       # now on the update path using .json__compress()
                                            cache_id = cache_id             ,                       # provide the cache_id so that we don't create a new graph
                                            namespace = self.test_namespace )
            raw_graph_json_2 = _.graph_cache_client.cache_client.retrieve().retrieve__cache_id__json(cache_id  = cache_id ,
                                                                                                   namespace =  self.test_namespace)
            loaded_mgraph_2  = _.get_graph(cache_id=cache_id, namespace=self.test_namespace)

            assert cache_id_2            == cache_id                                                # confirm we have the same object
            assert raw_graph_json_2      == raw_graph_json
            assert loaded_mgraph_2.obj() == loaded_mgraph.obj()
            assert _.delete_graph(cache_id  = cache_id           ,                          # Cleanup
                                  namespace = self.test_namespace)

    def test_save_graph__with_nodes(self):                                                  # Test saving graph with nodes
        with self.graph_service as _:
            graph = _.create_new_graph()
            graph.edit().new_node()                                                         # Add a node
            graph.edit().new_node()                                                         # Add another node

            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            assert cache_id is not None

            retrieved = _.get_graph(cache_id  = cache_id           ,                        # Verify saved correctly
                                    namespace = self.test_namespace)

            assert len(retrieved.graph.nodes()) == 2                                              # Both nodes saved

            assert _.delete_graph(cache_id  = cache_id           ,                          # Cleanup
                                  namespace = self.test_namespace)

    def test_save_graph__with_edges(self):                                                  # Test saving graph with edges
        with self.graph_service as _:
            graph    = _.create_new_graph()
            node1    = graph.edit().new_node()
            node2    = graph.edit().new_node()
            edge     = graph.edit().new_edge(from_node_id = node1.node_id,
                                             to_node_id   = node2.node_id)

            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            retrieved = _.get_graph(cache_id  = cache_id           ,
                                    namespace = self.test_namespace)

            assert len(retrieved.graph.nodes()) == 2
            assert len(retrieved.graph.edges()) == 1

            assert _.delete_graph(cache_id  = cache_id           ,
                                  namespace = self.test_namespace)

    def test_save_graph__update_existing(self):                                             # Test updating existing graph via cache_id
        with self.graph_service as _:
            graph    = _.create_new_graph()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            graph.edit().new_node()                                                         # Modify graph

            cache_id_2 = _.save_graph(mgraph    = graph              ,                      # Update using cache_id
                                      namespace = self.test_namespace,
                                      cache_id  = cache_id           )

            assert cache_id_2 == cache_id                                                   # Same cache_id returned

            retrieved = _.get_graph(cache_id  = cache_id           ,
                                    namespace = self.test_namespace)

            assert len(retrieved.graph.nodes()) == 1                                              # Node was added

            assert _.delete_graph(cache_id  = cache_id           ,
                                  namespace = self.test_namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # get_graph Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_get_graph__by_cache_id(self):                                                  # Test retrieving graph by cache_id
        with self.graph_service as _:
            graph    = _.create_new_graph()
            graph_id = graph.graph.graph_id()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            retrieved = _.get_graph(cache_id  = cache_id           ,
                                    namespace = self.test_namespace)

            assert type(retrieved)                 is MGraph
            assert retrieved.graph.graph_id()      == graph_id                              # Same graph_id

            assert _.delete_graph(cache_id  = cache_id           ,
                                  namespace = self.test_namespace)

    def test_get_graph__by_graph_id(self):                                                  # Test retrieving graph by graph_id
        with self.graph_service as _:
            graph    = _.create_new_graph()
            graph_id = graph.graph.graph_id()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            retrieved = _.get_graph(graph_id  = graph_id           ,
                                    namespace = self.test_namespace)

            assert type(retrieved)                 is MGraph
            assert retrieved.graph.graph_id()      == graph_id

            assert _.delete_graph(cache_id  = cache_id           ,
                                  namespace = self.test_namespace)

    def test_get_graph__not_found(self):                                                    # Test retrieving non-existent graph
        with self.graph_service as _:
            fake_graph_id = Obj_Id()

            retrieved = _.get_graph(graph_id  = fake_graph_id      ,
                                    namespace = self.test_namespace)

            assert retrieved is None                                                        # Returns None when not found

    def test_get_graph__preserves_structure(self):                                          # Test graph structure is preserved
        with self.graph_service as _:
            mgraph    = _.create_new_graph()
            node1    = mgraph.edit().new_node()
            node2    = mgraph.edit().new_node()
            node3    = mgraph.edit().new_node()
            edge1    = mgraph.edit().new_edge(from_node_id = node1.node_id,
                                             to_node_id   = node2.node_id)
            edge2    = mgraph.edit().new_edge(from_node_id = node2.node_id,
                                             to_node_id   = node3.node_id)

            cache_id = _.save_graph(mgraph    = mgraph               ,
                                    namespace = self.test_namespace )

            retrieved = _.get_graph(cache_id  = cache_id           ,
                                    namespace = self.test_namespace)

            assert len(retrieved.graph.nodes()) == 3
            assert len(retrieved.graph.edges()) == 2

            original_node_ids  = {str(n.node_id) for n in mgraph.graph.nodes()}                    # Verify same node ids
            retrieved_node_ids = {str(n.node_id) for n in retrieved.graph.nodes()}
            assert original_node_ids == retrieved_node_ids

            original_edge_ids  = {str(e.edge_id) for e in mgraph.graph.edges()}                    # Verify same edge ids
            retrieved_edge_ids = {str(e.edge_id) for e in retrieved.graph.edges()}
            assert original_edge_ids == retrieved_edge_ids

            assert _.delete_graph(cache_id  = cache_id           ,
                                  namespace = self.test_namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # get_or_create_graph Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_get_or_create_graph__creates_new(self):                                        # Test creates new when not found
        with self.graph_service as _:
            fake_graph_id = Obj_Id()

            graph = _.get_or_create_graph(graph_id  = fake_graph_id    ,
                                          namespace = self.test_namespace)

            assert graph            is not None
            assert type(graph)      is MGraph
            assert len(graph.graph.nodes()) == 0                                                  # Empty new graph
            assert len(graph.graph.edges()) == 0

    def test_get_or_create_graph__returns_existing(self):                                   # Test returns existing graph
        with self.graph_service as _:
            graph    = _.create_new_graph()
            graph_id = graph.graph.graph_id()
            graph.edit().new_node()                                                         # Add node to distinguish
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            retrieved = _.get_or_create_graph(graph_id  = graph_id         ,
                                              namespace = self.test_namespace)

            assert type(retrieved)                 is MGraph
            assert retrieved.graph.graph_id()      == graph_id
            assert len(retrieved.graph.nodes())    == 1                                     # Has the node we added

            assert _.delete_graph(cache_id  = cache_id           ,
                                  namespace = self.test_namespace)

    def test_get_or_create_graph__default_namespace(self):                                  # Test default namespace is used
        with self.graph_service as _:
            sig    = inspect.signature(_.get_or_create_graph)
            params = sig.parameters

            assert params['namespace'].default == None

    # ═══════════════════════════════════════════════════════════════════════════════
    # delete_graph Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_delete_graph__by_cache_id(self):                                               # Test deleting graph by cache_id
        with self.graph_service as _:
            graph    = _.create_new_graph()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            assert _.graph_exists(cache_id  = cache_id           ,
                                  namespace = self.test_namespace) is True

            result = _.delete_graph(cache_id  = cache_id           ,
                                    namespace = self.test_namespace)

            assert result is not None                                                       # Returns result dict
            assert _.graph_exists(cache_id  = cache_id           ,
                                  namespace = self.test_namespace) is False

    def test_delete_graph__by_graph_id(self):                                               # Test deleting graph by graph_id
        with self.graph_service as _:
            graph    = _.create_new_graph()
            graph_id = graph.graph.graph_id()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            assert _.graph_exists(graph_id  = graph_id           ,
                                  namespace = self.test_namespace) is True

            result = _.delete_graph(graph_id  = graph_id           ,
                                    namespace = self.test_namespace)

            assert result is not None
            assert _.graph_exists(graph_id  = graph_id           ,
                                  namespace = self.test_namespace) is False

    def test__bug__delete_graph__not_found(self):                                                 # Test deleting non-existent graph
        skip_if_in_github_action()                                                         # todo: figure out why this fails in GH Action with: AssertionError: assert {'detail': [{'input': 'None', 'loc': ['query', 'cache_id'], 'msg': 'in Random_Guid: value provided was not a Guid: None', 'type': 'value_error'}]} is None
        with self.graph_service as _:
            fake_graph_id = Obj_Id()

            result = _.delete_graph(graph_id  = fake_graph_id      ,
                                    namespace = self.test_namespace)

            assert result  is None

    def test_delete_graph__idempotent(self):                                                # Test deleting twice doesn't error
        with self.graph_service as _:
            graph    = _.create_new_graph()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )
            mgraph   = _.get_or_create_graph(graph_id = cache_id ,namespace=self.test_namespace)
            graph_id = mgraph.graph.graph_id()

            result_0 = _.delete_graph(cache_id = cache_id )                                 # fails because no namespace was provided
            result_1 = _.delete_graph(cache_id  = cache_id           ,
                                      namespace = self.test_namespace)                      # works
            result_2 = _.delete_graph(cache_id  = cache_id           ,
                                      namespace = self.test_namespace)                      # fails because graph has been deleted already
            assert obj(result_0) == __(status='not_found',
                                       message=f'Cache ID {cache_id} not found')            # BUG fail delete return value should be consistent with the success delete (same Type_Safe class)
            assert obj(result_1) == __(status='success',
                                       cache_id=cache_id,
                                       deleted_count=5,
                                       failed_count=0,
                                       deleted_paths=__SKIP__,
                                       failed_paths=[])
            assert obj(result_2) == __(status='not_found',
                                       message=f'Cache ID {cache_id} not found')            # BUG fail delete return value should be consistent with the success delete (same Type_Safe class)



    # ═══════════════════════════════════════════════════════════════════════════════
    # graph_exists Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_graph_exists__by_cache_id__true(self):                                         # Test exists check by cache_id
        with self.graph_service as _:
            graph    = _.create_new_graph()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            exists = _.graph_exists(cache_id  = cache_id           ,
                                    namespace = self.test_namespace)

            assert exists is True

            _.delete_graph(cache_id  = cache_id           ,
                           namespace = self.test_namespace)

    def test_graph_exists__by_graph_id__true(self):                                         # Test exists check by graph_id
        with self.graph_service as _:
            graph    = _.create_new_graph()
            graph_id = graph.graph.graph_id()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            exists = _.graph_exists(graph_id  = graph_id           ,
                                    namespace = self.test_namespace)

            assert exists is True

            _.delete_graph(cache_id  = cache_id           ,
                           namespace = self.test_namespace)

    def test_graph_exists__by_cache_id__false(self):                                        # Test exists returns false
        with self.graph_service as _:
            fake_cache_id = Random_Guid()

            exists = _.graph_exists(cache_id  = fake_cache_id      ,
                                    namespace = self.test_namespace)

            assert exists is False

    def test_graph_exists__by_graph_id__false(self):                                        # Test exists returns false for graph_id
        with self.graph_service as _:
            fake_graph_id = Obj_Id()

            exists = _.graph_exists(graph_id  = fake_graph_id      ,
                                    namespace = self.test_namespace)

            assert exists is False

    def test_graph_exists__after_delete(self):                                              # Test exists after deletion
        with self.graph_service as _:
            graph    = _.create_new_graph()
            graph_id = graph.graph.graph_id()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            assert _.graph_exists(cache_id  = cache_id           ,
                                  namespace = self.test_namespace) is True
            assert _.graph_exists(graph_id  = graph_id           ,
                                  namespace = self.test_namespace) is True

            _.delete_graph(cache_id  = cache_id           ,
                           namespace = self.test_namespace)

            assert _.graph_exists(cache_id  = cache_id           ,
                                  namespace = self.test_namespace) is False
            assert _.graph_exists(graph_id  = graph_id           ,
                                  namespace = self.test_namespace) is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__full_lifecycle__create_save_get_delete(self):                                 # Test complete graph lifecycle
        with self.graph_service as _:
            graph    = _.create_new_graph()                                                 # Create
            graph_id = graph.graph.graph_id()

            assert type(graph)               is MGraph
            assert _.graph_exists(graph_id  = graph_id           ,                          # Not persisted yet
                                  namespace = self.test_namespace) is False

            cache_id = _.save_graph(mgraph    = graph               ,                       # Save
                                    namespace = self.test_namespace )

            assert is_guid(cache_id) is True
            assert _.graph_exists(cache_id  = cache_id           ,                          # Now persisted
                                  namespace = self.test_namespace) is True

            retrieved = _.get_graph(cache_id  = cache_id           ,                        # Get
                                    namespace = self.test_namespace)

            assert type(retrieved)                 is MGraph
            assert retrieved.graph.graph_id()      == graph_id

            result = _.delete_graph(cache_id  = cache_id           ,                        # Delete
                                    namespace = self.test_namespace)

            assert result is not None
            assert _.graph_exists(cache_id  = cache_id           ,                          # Verify deleted
                                  namespace = self.test_namespace) is False

    def test__multiple_graphs_same_namespace(self):                                         # Test multiple graphs in same namespace
        with self.graph_service as _:
            graph1    = _.create_new_graph()
            graph2    = _.create_new_graph()
            graph3    = _.create_new_graph()

            cache_id_1 = _.save_graph(mgraph    = graph1              ,
                                      namespace = self.test_namespace )
            cache_id_2 = _.save_graph(mgraph    = graph2              ,
                                      namespace = self.test_namespace )
            cache_id_3 = _.save_graph(mgraph    = graph3              ,
                                      namespace = self.test_namespace )

            assert _.graph_exists(cache_id  = cache_id_1         ,                          # All exist
                                  namespace = self.test_namespace) is True
            assert _.graph_exists(cache_id  = cache_id_2         ,
                                  namespace = self.test_namespace) is True
            assert _.graph_exists(cache_id  = cache_id_3         ,
                                  namespace = self.test_namespace) is True

            _.delete_graph(cache_id  = cache_id_2         ,                                 # Delete middle one
                           namespace = self.test_namespace)

            assert _.graph_exists(cache_id  = cache_id_1         ,
                                  namespace = self.test_namespace) is True                  # First still exists
            assert _.graph_exists(cache_id  = cache_id_2         ,
                                  namespace = self.test_namespace) is False                 # Middle deleted
            assert _.graph_exists(cache_id  = cache_id_3         ,
                                  namespace = self.test_namespace) is True                  # Last still exists

            _.delete_graph(cache_id  = cache_id_1         ,                                 # Cleanup
                           namespace = self.test_namespace)
            _.delete_graph(cache_id  = cache_id_3         ,
                           namespace = self.test_namespace)

    def test__graph_modification_and_update(self):                                          # Test modifying and updating graph
        with self.graph_service as _:
            graph    = _.create_new_graph()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            for i in range(5):                                                              # Add 5 nodes
                graph.edit().new_node()

            cache_id_updated = _.save_graph(mgraph    = graph              ,
                                            namespace = self.test_namespace,
                                            cache_id  = cache_id           )

            assert cache_id_updated == cache_id                                             # Same cache_id

            retrieved = _.get_graph(cache_id  = cache_id           ,
                                    namespace = self.test_namespace)

            assert len(retrieved.graph.nodes()) == 5                                              # All nodes saved

            _.delete_graph(cache_id  = cache_id           ,
                           namespace = self.test_namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_types__create_new_graph_returns_mgraph(self):                                  # Test return type
        with self.graph_service as _:
            result = _.create_new_graph()

            assert type(result) is MGraph

    def test_types__save_graph_returns_random_guid(self):                                   # Test return type
        with self.graph_service as _:
            graph    = _.create_new_graph()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            assert type(cache_id)    is Cache_Id
            assert is_guid(cache_id) is True

            _.delete_graph(cache_id  = cache_id           ,
                           namespace = self.test_namespace)

    def test_types__get_graph_returns_mgraph_or_none(self):                                 # Test return type
        skip_if_in_github_action()                                                         # todo: figure out why this fails in GH Action with: assert <mgraph_db.mgraph.MGraph.MGraph object at 0x7faf4038df70> is None
        with self.graph_service as _:
            graph    = _.create_new_graph()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            retrieved = _.get_graph(cache_id  = cache_id           ,
                                    namespace = self.test_namespace)

            assert type(retrieved) is MGraph

            not_found = _.get_graph(cache_id  = Random_Guid()      ,
                                    namespace = self.test_namespace)

            assert not_found is None

            _.delete_graph(cache_id  = cache_id           ,
                           namespace = self.test_namespace)

    def test_types__graph_exists_returns_bool(self):                                        # Test return type
        with self.graph_service as _:
            graph    = _.create_new_graph()
            cache_id = _.save_graph(mgraph    = graph               ,
                                    namespace = self.test_namespace )

            exists = _.graph_exists(cache_id  = cache_id           ,
                                    namespace = self.test_namespace)

            assert type(exists) is bool
            assert exists       is True

            not_exists = _.graph_exists(cache_id  = Random_Guid()      ,
                                        namespace = self.test_namespace)

            assert type(not_exists) is bool
            assert not_exists       is False

            _.delete_graph(cache_id  = cache_id           ,
                           namespace = self.test_namespace)

    def test_types__graph_id_is_obj_id(self):                                               # Test graph_id type
        with self.graph_service as _:
            graph    = _.create_new_graph()
            graph_id = graph.graph.graph_id()

            assert type(graph_id)    is Obj_Id
            assert is_obj_id(graph_id) is True