from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import is_obj_id
from osbot_utils.utils.Misc                                                                 import is_guid
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_db.mgraph.MGraph                                                                import MGraph
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response             import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Response     import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Response     import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.utils.testing.Graph_Test_Helpers                               import Graph_Test_Helpers, DEFAULT_NAMESPACE
from tests.unit.Graph__Service__Fast_API__Test_Objs                                         import client_cache_service


class test_Graph_Test_Helpers(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Setup shared test infrastructure
        cls.cache_client, cls.cache_service = client_cache_service()
        cls.graph_cache_client = Graph__Cache__Client(cache_client       = cls.cache_client       )
        cls.graph_service      = Graph__Service      (graph_cache_client = cls.graph_cache_client )
        cls.area_crud          = Area__Graph__CRUD   (graph_service      = cls.graph_service      )
        cls.area_edit          = Area__Graph__Edit   (graph_service      = cls.graph_service      )
        cls.area_query         = Area__Graph__Query  (graph_service      = cls.graph_service      )
        cls.helpers            = Graph_Test_Helpers  (area_crud          = cls.area_crud          ,
                                                      area_edit          = cls.area_edit          ,
                                                      area_query         = cls.area_query         )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test helper class initialization
        with self.helpers as _:
            assert type(_)            is Graph_Test_Helpers
            assert base_classes(_)    == [Type_Safe, object]
            assert type(_.area_crud)  is Area__Graph__CRUD
            assert type(_.area_edit)  is Area__Graph__Edit
            assert type(_.area_query) is Area__Graph__Query

    def test__init__creates_new_instance(self):                                             # Test creating new helper instance
        new_helpers = Graph_Test_Helpers(area_crud  = self.area_crud ,
                                         area_edit  = self.area_edit ,
                                         area_query = self.area_query)

        assert new_helpers            is not None
        assert type(new_helpers)      is Graph_Test_Helpers
        assert new_helpers            is not self.helpers                                   # Different instance

    # ═══════════════════════════════════════════════════════════════════════════════
    # Empty Graph Creation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__create_empty_graph__defaults(self):                                           # Test creating empty graph with defaults
        result = self.helpers.create_empty_graph()

        assert type(result)                 is Schema__Graph__Create__Response
        assert is_obj_id(result.graph_id)   is True
        assert is_guid(result.cache_id)     is True
        assert result.cached                is True
        assert result.cache_namespace       == DEFAULT_NAMESPACE

        assert self.helpers.delete_graph(graph_id=result.graph_id, namespace=DEFAULT_NAMESPACE) is True   # Cleanup

    def test__create_empty_graph__custom_namespace(self):                                   # Test creating empty graph with custom namespace
        namespace = 'test-helpers-custom'
        result    = self.helpers.create_empty_graph(namespace=namespace)

        assert type(result)        is Schema__Graph__Create__Response
        assert result.cache_namespace == namespace

        self.helpers.delete_graph(graph_id=result.graph_id, namespace=namespace)            # Cleanup

    def test__create_empty_graph__no_cache(self):                                           # Test creating empty graph without caching
        result = self.helpers.create_empty_graph(auto_cache=False)

        assert type(result)        is Schema__Graph__Create__Response
        assert is_obj_id(result.graph_id) is True
        assert result.cached       is False
        assert result.cache_id     is None                                                  # No cache ID when not cached

    # ═══════════════════════════════════════════════════════════════════════════════
    # Graph with Nodes Creation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__create_graph_with_nodes__defaults(self):                                      # Test creating graph with default nodes
        create_response, node_responses = self.helpers.create_graph_with_nodes()

        assert type(create_response) is Schema__Graph__Create__Response
        assert len(node_responses)   == 3                                                   # Default is 3 nodes

        for i, node_response in enumerate(node_responses):
            assert type(node_response) is Schema__Graph__Add_Node__Response
            assert is_obj_id(node_response.node_id) is True
            assert node_response.graph_id == create_response.graph_id

        self.helpers.delete_graph(graph_id=create_response.graph_id)                        # Cleanup

    def test__create_graph_with_nodes__custom_count(self):                                  # Test creating graph with custom node count
        node_count = 5
        create_response, node_responses = self.helpers.create_graph_with_nodes(node_count=node_count)

        assert len(node_responses) == node_count

        node_ids = [r.node_id for r in node_responses]                                      # All nodes should have unique IDs
        assert len(set(node_ids)) == node_count

        self.helpers.delete_graph(graph_id=create_response.graph_id)                        # Cleanup

    # ═══════════════════════════════════════════════════════════════════════════════
    # Graph with Edges Creation Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__create_graph_with_edges__defaults(self):                                      # Test creating graph with default edges
        create_response, node_responses, edge_responses = self.helpers.create_graph_with_edges()

        assert type(create_response)   is Schema__Graph__Create__Response
        assert len(node_responses)     == 3                                                 # Default nodes
        assert len(edge_responses)     == 2                                                 # Chain: 3 nodes = 2 edges

        for edge_response in edge_responses:
            assert type(edge_response) is Schema__Graph__Add_Edge__Response
            assert is_obj_id(edge_response.edge_id) is True
            assert edge_response.graph_id == create_response.graph_id

        self.helpers.delete_graph(graph_id=create_response.graph_id)                        # Cleanup

    def test__create_graph_with_edges__custom_edge_type(self):                              # Test creating graph with custom edge type
        edge_type = 'KNOWS'
        create_response, node_responses, edge_responses = self.helpers.create_graph_with_edges(
            edge_type  = edge_type,
            node_count = 4)

        assert len(node_responses) == 4
        assert len(edge_responses) == 3                                                     # Chain: 4 nodes = 3 edges

        self.helpers.delete_graph(graph_id=create_response.graph_id)                        # Cleanup

    def test__create_complete_graph(self):                                                  # Test creating fully connected graph
        node_count = 4
        create_response, node_responses, edge_responses = self.helpers.create_complete_graph(
            node_count=node_count)

        expected_edges = (node_count * (node_count - 1)) // 2                               # Complete graph: n*(n-1)/2 edges
        assert len(node_responses) == node_count
        assert len(edge_responses) == expected_edges                                        # 4 nodes = 6 edges

        self.helpers.delete_graph(graph_id=create_response.graph_id)                        # Cleanup

    # ═══════════════════════════════════════════════════════════════════════════════
    # Multiple Node Types Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__create_graph_with_multiple_node_types__defaults(self):                        # Test creating graph with default multiple types
        create_response, nodes_by_type = self.helpers.create_graph_with_multiple_node_types()

        assert 'Person'  in nodes_by_type
        assert 'Company' in nodes_by_type
        assert 'Product' in nodes_by_type
        assert len(nodes_by_type['Person'])  == 2
        assert len(nodes_by_type['Company']) == 1
        assert len(nodes_by_type['Product']) == 3

        self.helpers.delete_graph(graph_id=create_response.graph_id)                        # Cleanup

    def test__create_graph_with_multiple_node_types__custom(self):                          # Test creating graph with custom node types
        node_types = {'User': 3, 'Role': 2}
        create_response, nodes_by_type = self.helpers.create_graph_with_multiple_node_types(
            node_types=node_types)

        assert len(nodes_by_type)       == 2
        assert len(nodes_by_type['User']) == 3
        assert len(nodes_by_type['Role']) == 2

        self.helpers.delete_graph(graph_id=create_response.graph_id)                        # Cleanup

    # ═══════════════════════════════════════════════════════════════════════════════
    # Multiple Edge Types Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__create_graph_with_multiple_edge_types__defaults(self):                        # Test creating graph with default edge types
        create_response, node_responses, edges_by_type = self.helpers.create_graph_with_multiple_edge_types()

        assert 'KNOWS'    in edges_by_type
        assert 'WORKS_AT' in edges_by_type
        assert 'OWNS'     in edges_by_type

        self.helpers.delete_graph(graph_id=create_response.graph_id)                        # Cleanup

    def test__create_graph_with_multiple_edge_types__custom(self):                          # Test creating graph with custom edge types
        edge_types = ['PARENT_OF', 'CHILD_OF']
        create_response, node_responses, edges_by_type = self.helpers.create_graph_with_multiple_edge_types(
            edge_types=edge_types)

        assert len(edges_by_type) == 2
        assert 'PARENT_OF' in edges_by_type
        assert 'CHILD_OF'  in edges_by_type

        self.helpers.delete_graph(graph_id=create_response.graph_id)                        # Cleanup

    # ═══════════════════════════════════════════════════════════════════════════════
    # Verification Operations Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__verify_graph_exists(self):                                                    # Test verifying graph exists
        create_response = self.helpers.create_empty_graph()
        graph_id        = create_response.graph_id

        assert self.helpers.verify_graph_exists(graph_id=graph_id) is True

        self.helpers.delete_graph(graph_id=graph_id)
        assert self.helpers.verify_graph_exists(graph_id=graph_id) is False

    def test__verify_graph_exists_by_cache_id(self):                                        # Test verifying graph exists by cache_id
        create_response = self.helpers.create_empty_graph()
        cache_id        = create_response.cache_id
        graph_id        = create_response.graph_id

        assert self.helpers.verify_graph_exists_by_cache_id(cache_id=cache_id) is True

        self.helpers.delete_graph(graph_id=graph_id)
        assert self.helpers.verify_graph_exists_by_cache_id(cache_id=cache_id) is False

    def test__get_graph(self):                                                              # Test retrieving graph
        create_response = self.helpers.create_empty_graph()
        graph_id        = create_response.graph_id

        get_response = self.helpers.get_graph(graph_id=graph_id)

        assert get_response.success    is True
        assert get_response.graph_id   == graph_id
        assert type(get_response.mgraph) is MGraph

        self.helpers.delete_graph(graph_id=graph_id)                                        # Cleanup

    # ═══════════════════════════════════════════════════════════════════════════════
    # Assertion Helper Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__assert_graph_exists__success(self):                                           # Test assert_graph_exists with existing graph
        create_response = self.helpers.create_empty_graph()
        graph_id        = create_response.graph_id

        result = self.helpers.assert_graph_exists(graph_id=graph_id)
        assert result is True

        self.helpers.delete_graph(graph_id=graph_id)                                        # Cleanup

    def test__assert_graph_not_exists__success(self):                                       # Test assert_graph_not_exists with deleted graph
        create_response = self.helpers.create_empty_graph()
        graph_id        = create_response.graph_id

        self.helpers.delete_graph(graph_id=graph_id)

        result = self.helpers.assert_graph_not_exists(graph_id=graph_id)
        assert result is True

    # ═══════════════════════════════════════════════════════════════════════════════
    # Integration Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__integration__create_verify_delete_workflow(self):                             # Test complete create-verify-delete workflow
        namespace = 'test-integration'
        create_response = self.helpers.create_empty_graph(namespace=namespace)              # Step 1: Create
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        assert self.helpers.verify_graph_exists(graph_id=graph_id, namespace=namespace) is True     # Step 2: Verify exists
        assert self.helpers.verify_graph_exists_by_cache_id(cache_id=cache_id, namespace=namespace) is True

        get_response = self.helpers.get_graph(graph_id=graph_id, namespace=namespace)       # Step 3: Get graph
        assert get_response.success is True

        deleted = self.helpers.delete_graph(graph_id=graph_id, namespace=namespace)         # Step 4: Delete
        assert deleted is True

        assert self.helpers.verify_graph_exists(graph_id=graph_id, namespace=namespace) is False    # Step 5: Verify deleted

    def test__integration__add_nodes_and_edges_to_existing_graph(self):                     # Test adding nodes and edges to existing graph
        create_response = self.helpers.create_empty_graph()                                 # Step 1: Create empty graph
        graph_id        = create_response.graph_id
        cache_id        = create_response.cache_id

        node_responses = self.helpers.add_nodes(graph_id=graph_id, cache_id=cache_id, count=3)    # Step 2: Add nodes
        assert len(node_responses) == 3

        last_cache_id = node_responses[-1].cache_id
        edge_response = self.helpers.add_edge(graph_id     = graph_id                ,      # Step 3: Add edge
                                              cache_id     = last_cache_id           ,
                                              from_node_id = node_responses[0].node_id,
                                              to_node_id   = node_responses[1].node_id)
        assert is_obj_id(edge_response.edge_id) is True

        self.helpers.delete_graph(graph_id=graph_id)                                        # Cleanup

    def test__integration__multiple_graphs_isolation(self):                                 # Test multiple graphs are isolated
        create_1 = self.helpers.create_empty_graph(namespace='ns1')                         # Create graphs in different namespaces
        create_2 = self.helpers.create_empty_graph(namespace='ns2')

        assert create_1.graph_id != create_2.graph_id                                       # Different graph IDs

        assert self.helpers.verify_graph_exists(graph_id=create_1.graph_id, namespace='ns1') is True  # Each exists in own namespace
        assert self.helpers.verify_graph_exists(graph_id=create_2.graph_id, namespace='ns2') is True

        self.helpers.delete_graph(graph_id=create_1.graph_id, namespace='ns1')              # Cleanup
        self.helpers.delete_graph(graph_id=create_2.graph_id, namespace='ns2')