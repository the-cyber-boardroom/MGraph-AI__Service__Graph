from unittest                                                                               import TestCase

from mgraph_ai_service_graph.service.graph.Graph__Ref__Resolver import Graph__Ref__Resolver
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_db.mgraph.MGraph                                                                import MGraph
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                          import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.exceptions.Graph__Ref__Not_Found__Error                        import Graph__Ref__Not_Found__Error
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client
from tests.unit.Graph__Service__Fast_API__Test_Objs                                         import client_cache_service


class test_Graph__Ref__Resolver(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client, cls.cache_service = client_cache_service()
        cls.graph_cache_client              = Graph__Cache__Client(cache_client=cls.cache_client)
        cls.resolver                        = Graph__Ref__Resolver(graph_cache_client=cls.graph_cache_client)
        cls.test_namespace                  = Safe_Str__Id('test-ref-resolver')

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Graph__Ref__Resolver() as _:
            assert type(_)                    is Graph__Ref__Resolver
            assert base_classes(_)            == [Type_Safe, object]
            assert type(_.graph_cache_client) is Graph__Cache__Client

    def test__graph_cache_client_dependency(self):                                          # Test cache client is injected
        with self.resolver as _:
            assert _.graph_cache_client is not None
            assert type(_.graph_cache_client) is Graph__Cache__Client
            assert _.graph_cache_client       is self.graph_cache_client

    def test__method_signatures(self):                                                      # Test all methods exist
        with Graph__Ref__Resolver() as _:
            assert hasattr(_, 'resolve')
            assert hasattr(_, 'save_graph')
            assert hasattr(_, '_resolve_by_cache_id')
            assert hasattr(_, '_resolve_by_graph_id')
            assert hasattr(_, '_create_new_graph')
            assert hasattr(_, '_build_resolved_ref')

            assert callable(_.resolve)
            assert callable(_.save_graph)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _create_and_store_graph(self):                                                      # Helper to create and store a graph
        mgraph       = MGraph()
        store_result = self.graph_cache_client.store_graph(mgraph    = mgraph            ,
                                                           namespace = self.test_namespace)
        cache_id     = store_result.cache_id
        graph_id     = Graph_Id(mgraph.graph.graph_id())
        return mgraph, cache_id, graph_id

    def _delete_graph(self, cache_id):                                                      # Helper to delete graph
        self.graph_cache_client.delete_graph(cache_id  = cache_id          ,
                                             namespace = self.test_namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # resolve Tests - By cache_id
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_resolve__by_cache_id(self):                                                    # Test resolving by cache_id
        mgraph, cache_id, graph_id = self._create_and_store_graph()

        with self.resolver as _:
            graph_ref = Schema__Graph__Ref(cache_id  = cache_id          ,
                                           namespace = self.test_namespace)
            result_mgraph, resolved_ref = _.resolve(graph_ref)

            assert type(result_mgraph)            is MGraph
            assert type(resolved_ref)             is Schema__Graph__Ref
            assert resolved_ref.cache_id          == cache_id
            assert resolved_ref.graph_id          == graph_id                                 # graph_id populated
            assert resolved_ref.namespace         == self.test_namespace
            assert result_mgraph.graph.graph_id() == Graph_Id(graph_id)
            assert result_mgraph.graph.graph_id() == graph_id

        self._delete_graph(cache_id)

    def test_resolve__by_cache_id__not_found(self):                                         # Test cache_id not found raises error
        with self.resolver as _:
            fake_cache_id = Cache_Id(Random_Guid())
            graph_ref     = Schema__Graph__Ref(cache_id  = fake_cache_id     ,
                                               namespace = self.test_namespace)

            try:
                _.resolve(graph_ref)
                assert False, "Should have raised Graph__Ref__Not_Found__Error"
            except Graph__Ref__Not_Found__Error as e:
                assert 'not found' in str(e).lower()
                assert str(fake_cache_id) in str(e)

    def test_resolve__by_cache_id__returns_tuple(self):                                     # Test resolve returns tuple
        mgraph, cache_id, graph_id = self._create_and_store_graph()

        with self.resolver as _:
            graph_ref = Schema__Graph__Ref(cache_id  = cache_id          ,
                                           namespace = self.test_namespace)
            result = _.resolve(graph_ref)

            assert type(result) is tuple
            assert len(result)  == 2
            assert type(result[0]) is MGraph
            assert type(result[1]) is Schema__Graph__Ref

        self._delete_graph(cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # resolve Tests - By graph_id
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_resolve__by_graph_id(self):                                                    # Test resolving by graph_id
        mgraph, cache_id, graph_id = self._create_and_store_graph()

        with self.resolver as _:
            graph_ref = Schema__Graph__Ref(graph_id  = Graph_Id(graph_id)  ,
                                           namespace = self.test_namespace)
            result_mgraph, resolved_ref = _.resolve(graph_ref)

            assert type(result_mgraph)            is MGraph
            assert type(resolved_ref)             is Schema__Graph__Ref
            assert resolved_ref.graph_id          == graph_id
            assert resolved_ref.cache_id          != ''                                       # cache_id populated
            assert resolved_ref.namespace         == self.test_namespace
            assert result_mgraph.graph.graph_id() == graph_id

        self._delete_graph(cache_id)

    def test_resolve__by_graph_id__not_found(self):                                         # Test graph_id not found raises error
        with self.resolver as _:
            fake_graph_id = Graph_Id(Obj_Id())
            graph_ref     = Schema__Graph__Ref(graph_id  = fake_graph_id     ,
                                               namespace = self.test_namespace)

            try:
                _.resolve(graph_ref)
                assert False, "Should have raised Graph__Ref__Not_Found__Error"
            except Graph__Ref__Not_Found__Error as e:
                assert 'not found' in str(e).lower()

    # ═══════════════════════════════════════════════════════════════════════════════
    # resolve Tests - Create New Graph
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_resolve__empty_ref_creates_new_graph(self):                                    # Test empty ref creates new graph
        with self.resolver as _:
            graph_ref = Schema__Graph__Ref(namespace=self.test_namespace)                   # Empty cache_id and graph_id
            result_mgraph, resolved_ref = _.resolve(graph_ref)

            assert type(result_mgraph)      is MGraph
            assert type(resolved_ref)       is Schema__Graph__Ref
            assert resolved_ref.cache_id    != ''                                           # New cache_id created
            assert resolved_ref.graph_id    != ''                                           # New graph_id created
            assert resolved_ref.namespace   == self.test_namespace

            # Verify graph is empty
            assert len(result_mgraph.graph.nodes()) == 0
            assert len(result_mgraph.graph.edges()) == 0

            # Cleanup
            self._delete_graph(resolved_ref.cache_id)

    def test_resolve__empty_ref_creates_unique_graphs(self):                                # Test multiple empty refs create unique graphs
        with self.resolver as _:
            graph_ref_1 = Schema__Graph__Ref(namespace=self.test_namespace)
            graph_ref_2 = Schema__Graph__Ref(namespace=self.test_namespace)

            mgraph_1, resolved_1 = _.resolve(graph_ref_1)
            mgraph_2, resolved_2 = _.resolve(graph_ref_2)

            assert resolved_1.cache_id  != resolved_2.cache_id                              # Different cache IDs
            assert resolved_1.graph_id  != resolved_2.graph_id                              # Different graph IDs
            assert mgraph_1.graph.graph_id() != mgraph_2.graph.graph_id()

            # Cleanup
            self._delete_graph(resolved_1.cache_id)
            self._delete_graph(resolved_2.cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # resolve Tests - Precedence
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_resolve__cache_id_takes_precedence(self):                                      # Test cache_id is used when both provided
        mgraph, cache_id, graph_id = self._create_and_store_graph()

        with self.resolver as _:
            # Provide both cache_id and graph_id
            graph_ref = Schema__Graph__Ref(cache_id  = cache_id           ,
                                           graph_id  = Graph_Id(graph_id) ,
                                           namespace = self.test_namespace)
            result_mgraph, resolved_ref = _.resolve(graph_ref)

            # Should use cache_id (it takes precedence)
            assert resolved_ref.cache_id          == cache_id
            assert result_mgraph.graph.graph_id() == graph_id

        self._delete_graph(cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # _build_resolved_ref Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__build_resolved_ref(self):                                                     # Test building resolved ref
        with self.resolver as _:
            cache_id  = Cache_Id(Random_Guid())
            graph_id  = Graph_Id(Obj_Id())
            namespace = 'test-ns'

            result = _._build_resolved_ref(cache_id  = cache_id ,
                                           graph_id  = graph_id ,
                                           namespace = namespace)

            assert type(result)    is Schema__Graph__Ref
            assert result.cache_id == cache_id
            assert result.graph_id == graph_id
            assert result.namespace == namespace

    # ═══════════════════════════════════════════════════════════════════════════════
    # save_graph Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_save_graph__with_cache_id(self):                                               # Test saving graph with existing cache_id
        mgraph, cache_id, graph_id = self._create_and_store_graph()

        with self.resolver as _:
            # Modify graph
            mgraph.edit().new_node()

            graph_ref = Schema__Graph__Ref(cache_id  = cache_id          ,
                                           graph_id  = Graph_Id(graph_id),
                                           namespace = self.test_namespace)
            result_ref = _.save_graph(mgraph=mgraph, graph_ref=graph_ref)

            assert type(result_ref) is Schema__Graph__Ref
            assert result_ref.cache_id == cache_id                                          # Same cache_id

            # Verify graph was updated
            retrieved = self.graph_cache_client.retrieve_graph(cache_id  = cache_id          ,
                                                               namespace = self.test_namespace)
            assert len(retrieved.graph.nodes()) == 1                                        # Node was added

        self._delete_graph(cache_id)

    def test_save_graph__without_cache_id(self):                                            # Test saving graph without cache_id creates new
        mgraph = MGraph()

        with self.resolver as _:
            graph_ref  = Schema__Graph__Ref(namespace=self.test_namespace)                  # No cache_id
            result_ref = _.save_graph(mgraph=mgraph, graph_ref=graph_ref)

            assert type(result_ref)     is Schema__Graph__Ref
            assert result_ref.cache_id  != ''                                               # New cache_id created
            assert result_ref.graph_id  != ''                                               # graph_id populated
            assert result_ref.namespace == self.test_namespace

            # Cleanup
            self._delete_graph(result_ref.cache_id)

    def test_save_graph__returns_schema_graph_ref(self):                                    # Test save_graph returns Schema__Graph__Ref
        mgraph = MGraph()

        with self.resolver as _:
            graph_ref  = Schema__Graph__Ref(namespace=self.test_namespace)
            result_ref = _.save_graph(mgraph=mgraph, graph_ref=graph_ref)

            assert type(result_ref)           is Schema__Graph__Ref
            assert type(result_ref.cache_id)  is Cache_Id or type(result_ref.cache_id) is str
            assert type(result_ref.namespace) is Safe_Str__Id or type(result_ref.namespace) is str

            # Cleanup
            self._delete_graph(result_ref.cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # resolve + save_graph Workflow Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_workflow__resolve_modify_save(self):                                           # Test full workflow: resolve, modify, save
        with self.resolver as _:
            # Create new graph via resolve
            graph_ref = Schema__Graph__Ref(namespace=self.test_namespace)
            mgraph, resolved_ref = _.resolve(graph_ref)

            assert len(mgraph.graph.nodes()) == 0                                           # Empty

            # Modify graph
            mgraph.edit().new_node()
            mgraph.edit().new_node()

            # Save graph
            saved_ref = _.save_graph(mgraph=mgraph, graph_ref=resolved_ref)

            assert saved_ref.cache_id == resolved_ref.cache_id                              # Same cache_id

            # Resolve again to verify changes persisted
            re_resolved_mgraph, re_resolved_ref = _.resolve(saved_ref)

            assert len(re_resolved_mgraph.graph.nodes()) == 2                               # Nodes persisted

            # Cleanup
            self._delete_graph(resolved_ref.cache_id)

    def test_workflow__create_modify_retrieve_cycle(self):                                  # Test multiple modify/save cycles
        with self.resolver as _:
            # Create
            graph_ref = Schema__Graph__Ref(namespace=self.test_namespace)
            mgraph, resolved_ref = _.resolve(graph_ref)
            cache_id = resolved_ref.cache_id

            # First modification
            node_1 = mgraph.edit().new_node()
            _.save_graph(mgraph=mgraph, graph_ref=resolved_ref)

            # Retrieve and verify
            retrieve_ref        = Schema__Graph__Ref(cache_id=cache_id, namespace=self.test_namespace)
            mgraph_2, graph_ref = _.resolve(retrieve_ref)
            assert len(mgraph_2.graph.nodes()) == 1

            # Second modification
            node_2 = mgraph_2.edit().new_node()
            _.save_graph(mgraph=mgraph_2, graph_ref=retrieve_ref)

            # Retrieve and verify again
            mgraph_3, _ = _.resolve(retrieve_ref)
            assert len(mgraph_3.graph.nodes()) == 2
            assert node_1.node_id != node_2.node_id

            # Cleanup
            self._delete_graph(cache_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_resolve__return_types(self):                                                   # Test resolve return types
        mgraph, cache_id, graph_id = self._create_and_store_graph()

        with self.resolver as _:
            graph_ref = Schema__Graph__Ref(cache_id=cache_id, namespace=self.test_namespace)
            result_mgraph, resolved_ref = _.resolve(graph_ref)

            assert type(result_mgraph)          is MGraph
            assert type(resolved_ref)           is Schema__Graph__Ref
            assert type(resolved_ref.cache_id)  is Cache_Id or type(resolved_ref.cache_id)  is str
            assert type(resolved_ref.graph_id)  is Graph_Id or type(resolved_ref.graph_id)  is str
            assert type(resolved_ref.namespace) is Safe_Str__Id or type(resolved_ref.namespace) is str

        self._delete_graph(cache_id)

    def test_save_graph__return_type(self):                                                 # Test save_graph return type
        mgraph = MGraph()

        with self.resolver as _:
            graph_ref  = Schema__Graph__Ref(namespace=self.test_namespace)
            result_ref = _.save_graph(mgraph=mgraph, graph_ref=graph_ref)

            assert type(result_ref) is Schema__Graph__Ref

            # Cleanup
            self._delete_graph(result_ref.cache_id)