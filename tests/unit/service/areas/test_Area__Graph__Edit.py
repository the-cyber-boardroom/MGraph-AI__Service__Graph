from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from osbot_utils.utils.Objects                                                              import base_classes

from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service

from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Request            import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Response           import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Request            import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Response           import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.utils.testing.Graph_Test_Helpers                               import Graph_Test_Helpers
from tests.unit.Graph__Service__Fast_API__Test_Objs                                         import client_cache_service


class test_Area__Graph__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client, cls.cache_service = client_cache_service()                        # Create in-memory cache service
        cls.graph_cache_client              = Graph__Cache__Client(cache_client=cls.cache_client)
        cls.graph_service                   = Graph__Service(graph_cache_client=cls.graph_cache_client)

        cls.area_crud                       = Area__Graph__CRUD (graph_service=cls.graph_service)    # Create areas
        cls.area_edit                       = Area__Graph__Edit (graph_service=cls.graph_service)
        cls.area_query                      = Area__Graph__Query(graph_service=cls.graph_service)

        cls.helpers                         = Graph_Test_Helpers(area_crud  = cls.area_crud  ,       # Create helpers
                                                                 area_edit  = cls.area_edit  ,
                                                                 area_query = cls.area_query )
        cls.test_namespace                  = Safe_Str__Id('test-area-edit')                         # Test namespace

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

    def test__method_exists(self):                                                          # Test all methods exist and are callable
        with self.area_edit as _:
            assert hasattr(_, 'add_node')    and callable(_.add_node)
            assert hasattr(_, 'add_edge')    and callable(_.add_edge)
            assert hasattr(_, 'delete_node') and callable(_.delete_node)
            assert hasattr(_, 'delete_edge') and callable(_.delete_edge)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Add Node Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_add_node(self):                                                                # Test basic node addition
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.area_edit as _:
            node_data = { Safe_Str__Key('name')  : Safe_Str__Text('test_node')  ,
                          Safe_Str__Key('value') : Safe_Str__Text('123')        }
            request   = Schema__Graph__Add_Node__Request(graph_id   = graph_id    ,
                                                         #node_type  = 'TestNode'  ,
                                                         node_data  = node_data   ,
                                                         auto_cache = True        )


            response = _.add_node(request)

            assert type(response)          is Schema__Graph__Add_Node__Response             # Verify response type
            assert type(response.node_id)  is Obj_Id                                        # Verify field types
            assert type(response.graph_id) is Obj_Id
            assert response.graph_id       == graph_id                                      # Same graph
            assert response.success        is True

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)         # Cleanup

    def test_add_node__without_cache(self):                                                 # Test node addition without caching
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Node__Request(graph_id   = graph_id   ,
                                                        node_type  = 'TestNode' ,
                                                        auto_cache = False      )
            response = _.add_node(request)

            assert type(response)    is Schema__Graph__Add_Node__Response
            assert response.success  is True
            assert response.cached   is False                                               # Not cached

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_add_node__with_custom_node_type(self):                                         # Test node with custom type
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Node__Request(graph_id   = graph_id       ,
                                                        node_type  = 'CustomEntity' ,
                                                        auto_cache = True           )
            response = _.add_node(request)

            assert type(response)    is Schema__Graph__Add_Node__Response
            assert response.success  is True
            assert response.node_id  is not None

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_add_node__multiple_nodes(self):                                                # Test adding multiple nodes
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id
        node_ids        = []

        with self.area_edit as _:
            for i in range(5):
                node_data = { Safe_Str__Key('index') : Safe_Str__Text(str(i)) }
                request   = Schema__Graph__Add_Node__Request(graph_id   = graph_id    ,
                                                             node_type  = 'TestNode'  ,
                                                             node_data  = node_data   ,
                                                             auto_cache = True        )
                response = _.add_node(request)

                assert type(response)   is Schema__Graph__Add_Node__Response
                assert response.success is True
                node_ids.append(response.node_id)

            assert len(node_ids)      == 5                                                  # All nodes created
            assert len(set(node_ids)) == 5                                                  # All unique IDs

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_add_node__response_structure(self):                                            # Test complete response structure
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.area_edit as _:
            node_data = { Safe_Str__Key('name') : Safe_Str__Text('structured_node') }
            request   = Schema__Graph__Add_Node__Request(graph_id   = graph_id   ,
                                                         node_type  = 'TestNode' ,
                                                         node_data  = node_data  ,
                                                         auto_cache = True       )
            response = _.add_node(request)

            assert response.obj().contains(__(node_id   = __SKIP__ ,                        # Use obj() for comparison
                                              graph_id  = graph_id ,
                                              cache_id  = __SKIP__ ,
                                              success   = True     ,
                                              cached    = True     ))

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_add_node__verify_in_graph(self):                                               # Test node is actually in graph
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Node__Request(graph_id   = graph_id   ,
                                                        node_type  = 'TestNode' ,
                                                        auto_cache = True       )
            response = _.add_node(request)
            node_id  = response.node_id

            find_result = self.helpers.find_nodes_by_type(graph_id  = graph_id   ,          # Verify node exists via query
                                                          node_type = 'TestNode' )
            assert find_result.total_found >= 1

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Add Edge Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_add_edge(self):                                                                # Test basic edge addition
        create_response, node_responses = self.helpers.create_graph_with_nodes(
                                              namespace  = self.test_namespace,
                                              node_count = 2                  )
        graph_id     = create_response.graph_id
        from_node_id = node_responses[0].node_id
        to_node_id   = node_responses[1].node_id

        with self.area_edit as _:
            edge_data = { Safe_Str__Key('weight') : Safe_Str__Text('1.0') }
            request   = Schema__Graph__Add_Edge__Request(graph_id     = graph_id     ,
                                                         from_node_id = from_node_id ,
                                                         to_node_id   = to_node_id   ,
                                                         edge_type    = 'CONNECTS'   ,
                                                         edge_data    = edge_data    ,
                                                         auto_cache   = True         )
            response = _.add_edge(request)

            assert type(response)              is Schema__Graph__Add_Edge__Response         # Verify response type
            assert type(response.edge_id)      is Obj_Id                                    # Verify field types
            assert type(response.graph_id)     is Obj_Id
            assert type(response.from_node_id) is Obj_Id
            assert type(response.to_node_id)   is Obj_Id
            assert response.graph_id           == graph_id                                  # Correct graph
            assert response.from_node_id       == from_node_id                              # Correct from node
            assert response.to_node_id         == to_node_id                                # Correct to node
            assert response.success            is True

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_add_edge__without_cache(self):                                                 # Test edge addition without caching
        create_response, node_responses = self.helpers.create_graph_with_nodes(
                                              namespace  = self.test_namespace,
                                              node_count = 2                  )
        graph_id     = create_response.graph_id
        from_node_id = node_responses[0].node_id
        to_node_id   = node_responses[1].node_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Edge__Request(graph_id     = graph_id     ,
                                                        from_node_id = from_node_id ,
                                                        to_node_id   = to_node_id   ,
                                                        edge_type    = 'CONNECTS'   ,
                                                        auto_cache   = False        )
            response = _.add_edge(request)

            assert type(response)   is Schema__Graph__Add_Edge__Response
            assert response.success is True
            assert response.cached  is False                                                # Not cached

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_add_edge__with_custom_edge_type(self):                                         # Test edge with custom type
        create_response, node_responses = self.helpers.create_graph_with_nodes(
                                              namespace  = self.test_namespace,
                                              node_count = 2                  )
        graph_id     = create_response.graph_id
        from_node_id = node_responses[0].node_id
        to_node_id   = node_responses[1].node_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Edge__Request(graph_id     = graph_id       ,
                                                        from_node_id = from_node_id   ,
                                                        to_node_id   = to_node_id     ,
                                                        edge_type    = 'CUSTOM_LINK'  ,
                                                        auto_cache   = True           )
            response = _.add_edge(request)

            assert type(response)   is Schema__Graph__Add_Edge__Response
            assert response.success is True
            assert response.edge_id is not None

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_add_edge__multiple_edges(self):                                                # Test adding multiple edges (chain)
        create_response, node_responses = self.helpers.create_graph_with_nodes(
                                              namespace  = self.test_namespace,
                                              node_count = 4                  )
        graph_id = create_response.graph_id
        edge_ids = []

        with self.area_edit as _:
            for i in range(len(node_responses) - 1):                                        # Create chain: 0->1->2->3
                from_node_id = node_responses[i].node_id
                to_node_id   = node_responses[i + 1].node_id
                edge_data    = { Safe_Str__Key('index') : Safe_Str__Text(str(i)) }
                request      = Schema__Graph__Add_Edge__Request(graph_id     = graph_id     ,
                                                                from_node_id = from_node_id ,
                                                                to_node_id   = to_node_id   ,
                                                                edge_type    = 'CONNECTS'   ,
                                                                edge_data    = edge_data    ,
                                                                auto_cache   = True         )
                response = _.add_edge(request)

                assert type(response)   is Schema__Graph__Add_Edge__Response
                assert response.success is True
                edge_ids.append(response.edge_id)

            assert len(edge_ids)      == 3                                                  # 3 edges for 4 nodes
            assert len(set(edge_ids)) == 3                                                  # All unique IDs

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_add_edge__response_structure(self):                                            # Test complete response structure
        create_response, node_responses = self.helpers.create_graph_with_nodes(
                                              namespace  = self.test_namespace,
                                              node_count = 2                  )
        graph_id     = create_response.graph_id
        from_node_id = node_responses[0].node_id
        to_node_id   = node_responses[1].node_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Edge__Request(graph_id     = graph_id     ,
                                                        from_node_id = from_node_id ,
                                                        to_node_id   = to_node_id   ,
                                                        edge_type    = 'CONNECTS'   ,
                                                        auto_cache   = True         )
            response = _.add_edge(request)

            assert response.obj().contains(__(edge_id      = __SKIP__     ,                 # Use obj() for comparison
                                              graph_id     = graph_id     ,
                                              from_node_id = from_node_id ,
                                              to_node_id   = to_node_id   ,
                                              cache_id     = __SKIP__     ,
                                              success      = True         ,
                                              cached       = True         ))

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Delete Node Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_delete_node(self):                                                             # Test basic node deletion
        create_response, node_responses = self.helpers.create_graph_with_nodes(
                                              namespace  = self.test_namespace,
                                              node_count = 3                  )
        graph_id = create_response.graph_id
        node_id  = node_responses[0].node_id

        with self.area_edit as _:
            result = _.delete_node(graph_id = graph_id ,
                                   node_id  = node_id  )

            assert result is True                                                           # Successfully deleted

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_delete_node__non_existent(self):                                               # Test deleting non-existent node
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id
        fake_node_id    = Obj_Id()

        with self.area_edit as _:
            result = _.delete_node(graph_id = graph_id     ,
                                   node_id  = fake_node_id )

            assert result is False                                                          # Nothing to delete

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_delete_node__verify_removed(self):                                             # Test node is actually removed
        create_response, node_responses = self.helpers.create_graph_with_nodes(
                                              namespace  = self.test_namespace,
                                              node_count = 2                  ,
                                              node_type  = 'DeleteTestNode'   )
        graph_id = create_response.graph_id
        node_id  = node_responses[0].node_id

        find_before = self.helpers.find_nodes_by_type(graph_id  = graph_id          ,       # Count nodes before
                                                      node_type = 'DeleteTestNode'  )
        count_before = int(find_before.total_found)

        with self.area_edit as _:
            result = _.delete_node(graph_id = graph_id ,
                                   node_id  = node_id  )
            assert result is True

        find_after = self.helpers.find_nodes_by_type(graph_id  = graph_id          ,        # Count nodes after
                                                     node_type = 'DeleteTestNode'  )
        count_after = int(find_after.total_found)

        assert count_after == count_before - 1                                              # One less node

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Delete Edge Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_delete_edge(self):                                                             # Test basic edge deletion
        create_response, node_responses, edge_responses = self.helpers.create_graph_with_edges(
                                                              namespace  = self.test_namespace,
                                                              node_count = 3                  )
        graph_id = create_response.graph_id
        edge_id  = edge_responses[0].edge_id

        with self.area_edit as _:
            result = _.delete_edge(graph_id = graph_id ,
                                   edge_id  = edge_id  )

            assert result is True                                                           # Successfully deleted

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_delete_edge__non_existent(self):                                               # Test deleting non-existent edge
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id
        fake_edge_id    = Obj_Id()

        with self.area_edit as _:
            result = _.delete_edge(graph_id = graph_id     ,
                                   edge_id  = fake_edge_id )

            assert result is False                                                          # Nothing to delete

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_delete_edge__multiple(self):                                                   # Test deleting multiple edges
        create_response, node_responses, edge_responses = self.helpers.create_graph_with_edges(
                                                              namespace  = self.test_namespace,
                                                              node_count = 4                  )
        graph_id = create_response.graph_id

        with self.area_edit as _:
            for edge_response in edge_responses:
                result = _.delete_edge(graph_id = graph_id            ,
                                       edge_id  = edge_response.edge_id)
                assert result is True                                                       # Each delete succeeds

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Integration Workflow Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_workflow__add_nodes_and_edges(self):                                           # Test complete workflow
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.area_edit as _:
            node_request_1 = Schema__Graph__Add_Node__Request(graph_id   = graph_id  ,      # Step 1: Add nodes
                                                              node_type  = 'Person'  ,
                                                              auto_cache = True      )
            node_request_2 = Schema__Graph__Add_Node__Request(graph_id   = graph_id  ,
                                                              node_type  = 'Person'  ,
                                                              auto_cache = True      )
            node_response_1 = _.add_node(node_request_1)
            node_response_2 = _.add_node(node_request_2)

            assert node_response_1.success is True
            assert node_response_2.success is True

            edge_request = Schema__Graph__Add_Edge__Request(graph_id     = graph_id               ,     # Step 2: Add edge
                                                            from_node_id = node_response_1.node_id,
                                                            to_node_id   = node_response_2.node_id,
                                                            edge_type    = 'KNOWS'                ,
                                                            auto_cache   = True                   )
            edge_response = _.add_edge(edge_request)

            assert edge_response.success is True

            find_result = self.helpers.find_nodes_by_type(graph_id  = graph_id ,            # Step 3: Verify
                                                          node_type = 'Person' )
            assert int(find_result.total_found) == 2

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_workflow__add_then_delete_nodes(self):                                         # Test add and delete cycle
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.area_edit as _:
            node_request = Schema__Graph__Add_Node__Request(graph_id   = graph_id    ,      # Add node
                                                            node_type  = 'TempNode'  ,
                                                            auto_cache = True        )
            node_response = _.add_node(node_request)
            node_id       = node_response.node_id

            assert node_response.success is True

            find_before = self.helpers.find_nodes_by_type(graph_id  = graph_id   ,          # Verify exists
                                                          node_type = 'TempNode' )
            assert int(find_before.total_found) >= 1

            delete_result = _.delete_node(graph_id = graph_id ,                             # Delete node
                                          node_id  = node_id  )
            assert delete_result is True

            find_after = self.helpers.find_nodes_by_type(graph_id  = graph_id   ,           # Verify deleted
                                                         node_type = 'TempNode' )
            assert int(find_after.total_found) == int(find_before.total_found) - 1

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_workflow__add_then_delete_edges(self):                                         # Test add and delete edges
        create_response, node_responses = self.helpers.create_graph_with_nodes(
                                              namespace  = self.test_namespace,
                                              node_count = 2                  )
        graph_id     = create_response.graph_id
        from_node_id = node_responses[0].node_id
        to_node_id   = node_responses[1].node_id

        with self.area_edit as _:
            edge_request = Schema__Graph__Add_Edge__Request(graph_id     = graph_id     ,   # Add edge
                                                            from_node_id = from_node_id ,
                                                            to_node_id   = to_node_id   ,
                                                            edge_type    = 'TEMP_LINK'  ,
                                                            auto_cache   = True         )
            edge_response = _.add_edge(edge_request)
            edge_id       = edge_response.edge_id

            assert edge_response.success is True

            delete_result = _.delete_edge(graph_id = graph_id ,                             # Delete edge
                                          edge_id  = edge_id  )
            assert delete_result is True

            delete_again = _.delete_edge(graph_id = graph_id ,                              # Try delete again
                                         edge_id  = edge_id  )
            assert delete_again is False                                                    # Already deleted

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_workflow__complete_graph_operations(self):                                     # Test complete graph with many nodes/edges
        create_response, node_responses, edge_responses = self.helpers.create_complete_graph(
                                                              namespace  = self.test_namespace,
                                                              node_count = 4                  )
        graph_id = create_response.graph_id

        assert len(node_responses) == 4                                                     # 4 nodes
        assert len(edge_responses) == 6                                                     # 6 edges (4 choose 2)

        with self.area_edit as _:
            node_request = Schema__Graph__Add_Node__Request(graph_id   = graph_id   ,       # Add one more node
                                                            node_type  = 'TestNode' ,
                                                            auto_cache = True       )
            new_node = _.add_node(node_request)
            assert new_node.success is True

            edge_request = Schema__Graph__Add_Edge__Request(graph_id     = graph_id                 ,    # Connect to first node
                                                            from_node_id = new_node.node_id         ,
                                                            to_node_id   = node_responses[0].node_id,
                                                            edge_type    = 'CONNECTS'               ,
                                                            auto_cache   = True                     )
            new_edge = _.add_edge(edge_request)
            assert new_edge.success is True

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_types__add_node_response_fields(self):                                         # Test all field types in add_node response
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Node__Request(graph_id   = graph_id   ,
                                                        node_type  = 'TestNode' ,
                                                        auto_cache = True       )
            response = _.add_node(request)

            assert type(response)          is Schema__Graph__Add_Node__Response             # Response type
            assert type(response.node_id)  is Obj_Id                                        # Field types
            assert type(response.graph_id) is Obj_Id
            assert type(response.cache_id) is Random_Guid
            assert type(response.success)  is bool
            assert type(response.cached)   is bool

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_types__add_edge_response_fields(self):                                         # Test all field types in add_edge response
        create_response, node_responses = self.helpers.create_graph_with_nodes(
                                              namespace  = self.test_namespace,
                                              node_count = 2                  )
        graph_id     = create_response.graph_id
        from_node_id = node_responses[0].node_id
        to_node_id   = node_responses[1].node_id

        with self.area_edit as _:
            request  = Schema__Graph__Add_Edge__Request(graph_id     = graph_id     ,
                                                        from_node_id = from_node_id ,
                                                        to_node_id   = to_node_id   ,
                                                        edge_type    = 'CONNECTS'   ,
                                                        auto_cache   = True         )
            response = _.add_edge(request)

            assert type(response)              is Schema__Graph__Add_Edge__Response         # Response type
            assert type(response.edge_id)      is Obj_Id                                    # Field types
            assert type(response.graph_id)     is Obj_Id
            assert type(response.from_node_id) is Obj_Id
            assert type(response.to_node_id)   is Obj_Id
            assert type(response.cache_id)     is Random_Guid
            assert type(response.success)      is bool
            assert type(response.cached)       is bool

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_types__delete_node_return(self):                                               # Test delete_node return type
        create_response, node_responses = self.helpers.create_graph_with_nodes(
                                              namespace  = self.test_namespace,
                                              node_count = 1                  )
        graph_id = create_response.graph_id
        node_id  = node_responses[0].node_id

        with self.area_edit as _:
            result = _.delete_node(graph_id = graph_id ,
                                   node_id  = node_id  )

            assert type(result) is bool                                                     # Returns bool

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_types__delete_edge_return(self):                                               # Test delete_edge return type
        create_response, node_responses, edge_responses = self.helpers.create_graph_with_edges(
                                                              namespace  = self.test_namespace,
                                                              node_count = 2                  )
        graph_id = create_response.graph_id
        edge_id  = edge_responses[0].edge_id

        with self.area_edit as _:
            result = _.delete_edge(graph_id = graph_id ,
                                   edge_id  = edge_id  )

            assert type(result) is bool                                                     # Returns bool

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)