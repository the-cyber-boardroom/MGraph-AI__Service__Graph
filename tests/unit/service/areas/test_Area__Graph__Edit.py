from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query
from mgraph_ai_service_graph.service.areas.edit.Graph__Edit__Add_Node                       import Graph__Edit__Add_Node
from mgraph_ai_service_graph.service.areas.edit.Graph__Edit__Add_Value                      import Graph__Edit__Add_Value
from mgraph_ai_service_graph.service.areas.edit.Graph__Edit__Add_Edge                       import Graph__Edit__Add_Edge
from mgraph_ai_service_graph.service.areas.edit.Graph__Edit__Delete                         import Graph__Edit__Delete
from mgraph_ai_service_graph.service.areas.edit.Graph__Edit__Builder                        import Graph__Edit__Builder
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Request      import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Response     import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Request      import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Response     import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.schemas.graph_edit.values.Schema__Graph__Add_Value__Request    import Schema__Graph__Add_Value__Request
from mgraph_ai_service_graph.schemas.graph_edit.values.Schema__Graph__Add_Value__Response   import Schema__Graph__Add_Value__Response
from tests.unit.Graph__Service__Fast_API__Test_Objs                                         import client_cache_service


class test_Area__Graph__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client, cls.cache_service = client_cache_service()                        # Create in-memory cache service
        cls.graph_cache_client              = Graph__Cache__Client(cache_client=cls.cache_client)
        cls.graph_service                   = Graph__Service(graph_cache_client=cls.graph_cache_client)

        cls.area_crud                       = Area__Graph__CRUD (graph_service=cls.graph_service)
        cls.area_edit                       = Area__Graph__Edit (graph_service=cls.graph_service)
        cls.area_query                      = Area__Graph__Query(graph_service=cls.graph_service)

        cls.test_namespace                  = Safe_Str__Id('test-area-edit')

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Area__Graph__Edit() as _:
            assert type(_)               is Area__Graph__Edit
            assert base_classes(_)       == [Type_Safe, object]
            assert type(_.graph_service) is Graph__Service

    def test__graph_service_dependency(self):                                               # Test graph service is injected
        with self.area_edit as _:
            assert _.graph_service is not None
            assert type(_.graph_service) is Graph__Service
            assert _.graph_service       is self.graph_service                              # Same instance as setup

    def test__handlers_initialized(self):                                                   # Test all handlers are initialized
        with self.area_edit as _:
            assert _.add_node  is not None
            assert _.add_value is not None
            assert _.add_edge  is not None
            assert _.delete    is not None
            assert _.builder   is not None

            assert type(_.add_node)  is Graph__Edit__Add_Node
            assert type(_.add_value) is Graph__Edit__Add_Value
            assert type(_.add_edge)  is Graph__Edit__Add_Edge
            assert type(_.delete)    is Graph__Edit__Delete
            assert type(_.builder)   is Graph__Edit__Builder

    def test__handlers_share_graph_service(self):                                           # Test all handlers have same graph_service
        with self.area_edit as _:
            assert _.add_node.graph_service  is _.graph_service
            assert _.add_value.graph_service is _.graph_service
            assert _.add_edge.graph_service  is _.graph_service
            assert _.delete.graph_service    is _.graph_service
            assert _.builder.graph_service   is _.graph_service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _create_empty_graph(self, namespace=None):                                          # Helper to create empty graph
        namespace = namespace or self.test_namespace
        request   = Schema__Graph__Create__Request(namespace  = namespace,
                                                   auto_cache = True     )
        return self.area_crud.create_graph(request)

    def _delete_graph(self, graph_id, namespace=None):                                      # Helper to delete graph
        namespace = namespace or self.test_namespace
        return self.area_crud.delete_graph(graph_id  = graph_id ,
                                           namespace = namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Add Node Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_add_node__add_node(self):                                                      # Test basic node addition via handler
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,
                                                        cache_id   = cache_id          ,
                                                        namespace  = self.test_namespace,
                                                        auto_cache = True              )
            response = _.add_node.add_node(request)

            assert type(response)          is Schema__Graph__Add_Node__Response
            assert type(response.node_id)  is Obj_Id
            assert type(response.graph_id) is Obj_Id
            assert response.success        is True
            assert response.cached         is True

        self._delete_graph(graph_id=graph_id)

    def test_add_node__add_node__without_cache(self):                                       # Test node addition without caching
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,
                                                        cache_id   = cache_id          ,
                                                        namespace  = self.test_namespace,
                                                        auto_cache = False             )
            response = _.add_node.add_node(request)

            assert type(response)    is Schema__Graph__Add_Node__Response
            assert response.success  is True
            assert response.cached   is False

        self._delete_graph(graph_id=graph_id)

    def test_add_node__add_node__multiple_nodes(self):                                      # Test adding multiple nodes
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id
        node_ids        = []

        with self.area_edit as _:
            for i in range(5):
                request   = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,
                                                             cache_id   = cache_id          ,
                                                             namespace  = self.test_namespace,
                                                             auto_cache = True              )
                response = _.add_node.add_node(request)
                cache_id = response.cache_id                                                # Update cache_id for next iteration

                assert response.success is True
                node_ids.append(response.node_id)

            assert len(node_ids)      == 5                                                  # All nodes created
            assert len(set(node_ids)) == 5                                                  # All unique IDs

        self._delete_graph(graph_id=graph_id)

    def test_add_node__add_node__response_structure(self):                                  # Test complete response structure
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,
                                                        cache_id   = cache_id          ,
                                                        namespace  = self.test_namespace,
                                                        auto_cache = True              )
            response = _.add_node.add_node(request)

            assert response.obj().contains(__(node_id   = __SKIP__ ,
                                              graph_id  = graph_id ,
                                              cache_id  = __SKIP__ ,
                                              success   = True     ,
                                              cached    = True     ))

        self._delete_graph(graph_id=graph_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Add Value Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_add_value__add_value(self):                                                    # Test basic value node addition
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Value__Request(graph_id   = graph_id          ,
                                                         cache_id   = cache_id          ,
                                                         namespace  = self.test_namespace,
                                                         value      = 'test-value'      ,
                                                         auto_cache = True              )
            response = _.add_value.add_value(request)

            assert type(response)          is Schema__Graph__Add_Value__Response
            assert type(response.node_id)  is Obj_Id
            assert type(response.graph_id) is Obj_Id
            assert response.value          == 'test-value'
            assert response.success        is True
            assert response.cached         is True

        self._delete_graph(graph_id=graph_id)

    def test_add_value__get_or_create_value(self):                                          # Test get or create value node
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            request_1 = Schema__Graph__Add_Value__Request(graph_id   = graph_id          ,
                                                          cache_id   = cache_id          ,
                                                          namespace  = self.test_namespace,
                                                          value      = 'unique-value'    ,
                                                          auto_cache = True              )
            response_1 = _.add_value.get_or_create_value(request_1)

            assert response_1.success is True
            node_id_1 = response_1.node_id
            cache_id  = response_1.cache_id

            request_2 = Schema__Graph__Add_Value__Request(graph_id   = graph_id          ,     # Same value, should return same node
                                                          cache_id   = cache_id          ,
                                                          namespace  = self.test_namespace,
                                                          value      = 'unique-value'    ,
                                                          auto_cache = True              )
            response_2 = _.add_value.get_or_create_value(request_2)

            assert response_2.success is True
            assert response_2.node_id == node_id_1                                          # Same node returned

        self._delete_graph(graph_id=graph_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Add Edge Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_add_edge__add_edge(self):                                                      # Test basic edge addition
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            node_request_1 = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,     # Create two nodes first
                                                              cache_id   = cache_id          ,
                                                              namespace  = self.test_namespace,
                                                              auto_cache = True              )
            node_response_1 = _.add_node.add_node(node_request_1)
            cache_id        = node_response_1.cache_id
            from_node_id    = node_response_1.node_id

            node_request_2  = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,
                                                               cache_id   = cache_id          ,
                                                               namespace  = self.test_namespace,
                                                               auto_cache = True              )
            node_response_2 = _.add_node.add_node(node_request_2)
            cache_id        = node_response_2.cache_id
            to_node_id      = node_response_2.node_id

            edge_request = Schema__Graph__Add_Edge__Request(graph_id     = graph_id          ,     # Add edge between them
                                                            cache_id     = cache_id          ,
                                                            namespace    = self.test_namespace,
                                                            from_node_id = from_node_id      ,
                                                            to_node_id   = to_node_id        ,
                                                            auto_cache   = True              )
            edge_response = _.add_edge.add_edge(edge_request)

            assert type(edge_response)              is Schema__Graph__Add_Edge__Response
            assert type(edge_response.edge_id)      is Obj_Id
            assert type(edge_response.graph_id)     is Obj_Id
            assert type(edge_response.from_node_id) is Obj_Id
            assert type(edge_response.to_node_id)   is Obj_Id
            assert edge_response.from_node_id       == from_node_id
            assert edge_response.to_node_id         == to_node_id
            assert edge_response.success            is True
            assert edge_response.cached             is True

        self._delete_graph(graph_id=graph_id)

    def test_add_edge__add_edge__without_cache(self):                                       # Test edge addition without caching
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            node_request_1  = Schema__Graph__Add_Node__Request(graph_id=graph_id, cache_id=cache_id,     # Create two nodes
                                                               namespace=self.test_namespace, auto_cache=True)
            node_response_1 = _.add_node.add_node(node_request_1)
            cache_id        = node_response_1.cache_id

            node_request_2  = Schema__Graph__Add_Node__Request(graph_id=graph_id, cache_id=cache_id,
                                                               namespace=self.test_namespace, auto_cache=True)
            node_response_2 = _.add_node.add_node(node_request_2)
            cache_id        = node_response_2.cache_id

            edge_request = Schema__Graph__Add_Edge__Request(graph_id     = graph_id                ,
                                                            cache_id     = cache_id                ,
                                                            namespace    = self.test_namespace     ,
                                                            from_node_id = node_response_1.node_id ,
                                                            to_node_id   = node_response_2.node_id ,
                                                            auto_cache   = False                   )
            edge_response = _.add_edge.add_edge(edge_request)

            assert edge_response.success is True
            assert edge_response.cached  is False

        self._delete_graph(graph_id=graph_id)

    def test_add_edge__add_edge__multiple_edges(self):                                      # Test adding multiple edges (chain)
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id
        node_ids        = []
        edge_ids        = []

        with self.area_edit as _:
            for i in range(4):                                                              # Create 4 nodes
                node_request  = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,
                                                                 cache_id   = cache_id          ,
                                                                 namespace  = self.test_namespace,
                                                                 auto_cache = True              )
                node_response = _.add_node.add_node(node_request)
                cache_id      = node_response.cache_id
                node_ids.append(node_response.node_id)

            for i in range(len(node_ids) - 1):                                              # Create chain: 0->1->2->3
                edge_request = Schema__Graph__Add_Edge__Request(graph_id     = graph_id          ,
                                                                cache_id     = cache_id          ,
                                                                namespace    = self.test_namespace,
                                                                from_node_id = node_ids[i]       ,
                                                                to_node_id   = node_ids[i + 1]   ,
                                                                auto_cache   = True              )
                edge_response = _.add_edge.add_edge(edge_request)
                cache_id      = edge_response.cache_id

                assert edge_response.success is True
                edge_ids.append(edge_response.edge_id)

            assert len(edge_ids)      == 3                                                  # 3 edges for 4 nodes
            assert len(set(edge_ids)) == 3                                                  # All unique IDs

        self._delete_graph(graph_id=graph_id)

    def test_add_edge__add_edge__response_structure(self):                                  # Test complete response structure
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            node_request_1  = Schema__Graph__Add_Node__Request(graph_id=graph_id, cache_id=cache_id,
                                                               namespace=self.test_namespace, auto_cache=True)
            node_response_1 = _.add_node.add_node(node_request_1)
            cache_id        = node_response_1.cache_id

            node_request_2  = Schema__Graph__Add_Node__Request(graph_id=graph_id, cache_id=cache_id,
                                                               namespace=self.test_namespace, auto_cache=True)
            node_response_2 = _.add_node.add_node(node_request_2)
            cache_id        = node_response_2.cache_id

            from_node_id = node_response_1.node_id
            to_node_id   = node_response_2.node_id

            edge_request = Schema__Graph__Add_Edge__Request(graph_id     = graph_id          ,
                                                            cache_id     = cache_id          ,
                                                            namespace    = self.test_namespace,
                                                            from_node_id = from_node_id      ,
                                                            to_node_id   = to_node_id        ,
                                                            auto_cache   = True              )
            edge_response = _.add_edge.add_edge(edge_request)

            assert edge_response.obj().contains(__(edge_id      = __SKIP__     ,
                                                   graph_id     = graph_id     ,
                                                   from_node_id = from_node_id ,
                                                   to_node_id   = to_node_id   ,
                                                   cache_id     = __SKIP__     ,
                                                   success      = True         ,
                                                   cached       = True         ))

        self._delete_graph(graph_id=graph_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Delete Node Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_delete__delete_node(self):                                                     # Test basic node deletion
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            node_request = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,     # Create a node
                                                            cache_id   = cache_id          ,
                                                            namespace  = self.test_namespace,
                                                            auto_cache = True              )
            node_response = _.add_node.add_node(node_request)
            node_id       = node_response.node_id

            result = _.delete.delete_node(graph_id  = graph_id           ,                  # Delete the node
                                          node_id   = node_id            ,
                                          namespace = self.test_namespace)

            assert result is True

        self._delete_graph(graph_id=graph_id)

    def test_delete__delete_node__non_existent(self):                                       # Test deleting non-existent node
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        fake_node_id    = Obj_Id()

        with self.area_edit as _:
            result = _.delete.delete_node(graph_id  = graph_id           ,
                                          node_id   = fake_node_id       ,
                                          namespace = self.test_namespace)

            assert result is False

        self._delete_graph(graph_id=graph_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Delete Edge Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_delete__delete_edge(self):                                                     # Test basic edge deletion
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            node_request_1  = Schema__Graph__Add_Node__Request(graph_id=graph_id, cache_id=cache_id,     # Create two nodes
                                                               namespace=self.test_namespace, auto_cache=True)
            node_response_1 = _.add_node.add_node(node_request_1)
            cache_id        = node_response_1.cache_id

            node_request_2  = Schema__Graph__Add_Node__Request(graph_id=graph_id, cache_id=cache_id,
                                                               namespace=self.test_namespace, auto_cache=True)
            node_response_2 = _.add_node.add_node(node_request_2)
            cache_id        = node_response_2.cache_id

            edge_request = Schema__Graph__Add_Edge__Request(graph_id     = graph_id                ,     # Create edge
                                                            cache_id     = cache_id                ,
                                                            namespace    = self.test_namespace     ,
                                                            from_node_id = node_response_1.node_id ,
                                                            to_node_id   = node_response_2.node_id ,
                                                            auto_cache   = True                    )
            edge_response = _.add_edge.add_edge(edge_request)
            edge_id       = edge_response.edge_id

            result = _.delete.delete_edge(graph_id  = graph_id           ,                  # Delete edge
                                          edge_id   = edge_id            ,
                                          namespace = self.test_namespace)

            assert result is True

        self._delete_graph(graph_id=graph_id)

    def test_delete__delete_edge__non_existent(self):                                       # Test deleting non-existent edge
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        fake_edge_id    = Obj_Id()

        with self.area_edit as _:
            result = _.delete.delete_edge(graph_id  = graph_id           ,
                                          edge_id   = fake_edge_id       ,
                                          namespace = self.test_namespace)

            assert result is False

        self._delete_graph(graph_id=graph_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Integration Workflow Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_workflow__add_nodes_and_edges(self):                                           # Test complete workflow
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            node_request_1 = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,     # Step 1: Add nodes
                                                              cache_id   = cache_id          ,
                                                              namespace  = self.test_namespace,
                                                              auto_cache = True              )
            node_response_1 = _.add_node.add_node(node_request_1)
            cache_id        = node_response_1.cache_id
            assert node_response_1.success is True

            node_request_2 = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,
                                                              cache_id   = cache_id          ,
                                                              namespace  = self.test_namespace,
                                                              auto_cache = True              )
            node_response_2 = _.add_node.add_node(node_request_2)
            cache_id        = node_response_2.cache_id
            assert node_response_2.success is True

            edge_request = Schema__Graph__Add_Edge__Request(graph_id     = graph_id                ,     # Step 2: Add edge
                                                            cache_id     = cache_id                ,
                                                            namespace    = self.test_namespace     ,
                                                            from_node_id = node_response_1.node_id ,
                                                            to_node_id   = node_response_2.node_id ,
                                                            auto_cache   = True                    )
            edge_response = _.add_edge.add_edge(edge_request)
            assert edge_response.success is True

        self._delete_graph(graph_id=graph_id)

    def test_workflow__add_then_delete_nodes(self):                                         # Test add and delete cycle
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            node_request = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,     # Add node
                                                            cache_id   = cache_id          ,
                                                            namespace  = self.test_namespace,
                                                            auto_cache = True              )
            node_response = _.add_node.add_node(node_request)
            node_id       = node_response.node_id

            assert node_response.success is True

            delete_result = _.delete.delete_node(graph_id  = graph_id           ,                # Delete node
                                                 node_id   = node_id            ,
                                                 namespace = self.test_namespace)
            assert delete_result is True

            delete_again = _.delete.delete_node(graph_id  = graph_id           ,                 # Try delete again
                                                node_id   = node_id            ,
                                                namespace = self.test_namespace)
            assert delete_again is False                                                         # Already deleted

        self._delete_graph(graph_id=graph_id)

    def test_workflow__add_then_delete_edges(self):                                         # Test add and delete edges
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            node_request_1  = Schema__Graph__Add_Node__Request(graph_id=graph_id, cache_id=cache_id,     # Create nodes
                                                               namespace=self.test_namespace, auto_cache=True)
            node_response_1 = _.add_node.add_node(node_request_1)
            cache_id        = node_response_1.cache_id

            node_request_2  = Schema__Graph__Add_Node__Request(graph_id=graph_id, cache_id=cache_id,
                                                               namespace=self.test_namespace, auto_cache=True)
            node_response_2 = _.add_node.add_node(node_request_2)
            cache_id        = node_response_2.cache_id

            edge_request = Schema__Graph__Add_Edge__Request(graph_id     = graph_id                ,     # Add edge
                                                            cache_id     = cache_id                ,
                                                            namespace    = self.test_namespace     ,
                                                            from_node_id = node_response_1.node_id ,
                                                            to_node_id   = node_response_2.node_id ,
                                                            auto_cache   = True                    )
            edge_response = _.add_edge.add_edge(edge_request)
            edge_id       = edge_response.edge_id

            assert edge_response.success is True

            delete_result = _.delete.delete_edge(graph_id  = graph_id           ,                # Delete edge
                                                 edge_id   = edge_id            ,
                                                 namespace = self.test_namespace)
            assert delete_result is True

            delete_again = _.delete.delete_edge(graph_id  = graph_id           ,                 # Try delete again
                                                edge_id   = edge_id            ,
                                                namespace = self.test_namespace)
            assert delete_again is False                                                         # Already deleted

        self._delete_graph(graph_id=graph_id)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_types__add_node_response_fields(self):                                         # Test all field types in add_node response
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Node__Request(graph_id   = graph_id          ,
                                                        cache_id   = cache_id          ,
                                                        namespace  = self.test_namespace,
                                                        auto_cache = True              )
            response = _.add_node.add_node(request)

            assert type(response)          is Schema__Graph__Add_Node__Response
            assert type(response.node_id)  is Obj_Id
            assert type(response.graph_id) is Obj_Id
            assert type(response.cache_id) is Random_Guid
            assert type(response.success)  is bool
            assert type(response.cached)   is bool

        self._delete_graph(graph_id=graph_id)

    def test_types__add_edge_response_fields(self):                                         # Test all field types in add_edge response
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            node_request_1  = Schema__Graph__Add_Node__Request(graph_id=graph_id, cache_id=cache_id,
                                                               namespace=self.test_namespace, auto_cache=True)
            node_response_1 = _.add_node.add_node(node_request_1)
            cache_id        = node_response_1.cache_id

            node_request_2  = Schema__Graph__Add_Node__Request(graph_id=graph_id, cache_id=cache_id,
                                                               namespace=self.test_namespace, auto_cache=True)
            node_response_2 = _.add_node.add_node(node_request_2)
            cache_id        = node_response_2.cache_id

            edge_request = Schema__Graph__Add_Edge__Request(graph_id     = graph_id                ,
                                                            cache_id     = cache_id                ,
                                                            namespace    = self.test_namespace     ,
                                                            from_node_id = node_response_1.node_id ,
                                                            to_node_id   = node_response_2.node_id ,
                                                            auto_cache   = True                    )
            edge_response = _.add_edge.add_edge(edge_request)

            assert type(edge_response)              is Schema__Graph__Add_Edge__Response
            assert type(edge_response.edge_id)      is Obj_Id
            assert type(edge_response.graph_id)     is Obj_Id
            assert type(edge_response.from_node_id) is Obj_Id
            assert type(edge_response.to_node_id)   is Obj_Id
            assert type(edge_response.cache_id)     is Random_Guid
            assert type(edge_response.success)      is bool
            assert type(edge_response.cached)       is bool

        self._delete_graph(graph_id=graph_id)

    def test_types__add_value_response_fields(self):                                        # Test all field types in add_value response
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Value__Request(graph_id   = graph_id          ,
                                                         cache_id   = cache_id          ,
                                                         namespace  = self.test_namespace,
                                                         value      = 'test-value'      ,
                                                         auto_cache = True              )
            response = _.add_value.add_value(request)

            assert type(response)          is Schema__Graph__Add_Value__Response
            assert type(response.node_id)  is Obj_Id
            assert type(response.graph_id) is Obj_Id
            assert type(response.cache_id) is Random_Guid
            assert type(response.value)    is str
            assert type(response.success)  is bool
            assert type(response.cached)   is bool

        self._delete_graph(graph_id=graph_id)

    def test_types__delete_returns_bool(self):                                              # Test delete methods return bool
        create_response = self._create_empty_graph()
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        with self.area_edit as _:
            node_request = Schema__Graph__Add_Node__Request(graph_id=graph_id, cache_id=cache_id,
                                                            namespace=self.test_namespace, auto_cache=True)
            node_response = _.add_node.add_node(node_request)
            node_id       = node_response.node_id

            result = _.delete.delete_node(graph_id  = graph_id           ,
                                          node_id   = node_id            ,
                                          namespace = self.test_namespace)

            assert type(result) is bool

        self._delete_graph(graph_id=graph_id)