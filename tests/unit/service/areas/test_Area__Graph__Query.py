import inspect
from unittest                                                                               import TestCase
from mgraph_ai_service_graph.schemas.graph_ref.Node_Id                                      import Node_Id
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                       import Type_Safe__List
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request         import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response        import Schema__Graph__Find_Nodes__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Node__Response         import Schema__Graph__Find_Node__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Edges__Response        import Schema__Graph__Find_Edges__Response
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Request      import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Request      import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service
from tests.unit.Graph__Service__Fast_API__Test_Objs                                         import client_cache_service


class test_Area__Graph__Query(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client, cls.cache_service = client_cache_service()
        cls.graph_cache_client              = Graph__Cache__Client(cache_client=cls.cache_client)
        cls.graph_service                   = Graph__Service(graph_cache_client=cls.graph_cache_client)

        cls.area_crud  = Area__Graph__CRUD (graph_service=cls.graph_service)
        cls.area_edit  = Area__Graph__Edit (graph_service=cls.graph_service)
        cls.area_query = Area__Graph__Query(graph_service=cls.graph_service)

        cls.test_namespace = Safe_Str__Id('test-area-query')

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Area__Graph__Query() as _:
            assert type(_)               is Area__Graph__Query
            assert base_classes(_)       == [Type_Safe, object]
            assert type(_.graph_service) is Graph__Service

    def test__graph_service_dependency(self):                                               # Test graph service is injected
        with self.area_query as _:
            assert _.graph_service is not None
            assert type(_.graph_service) is Graph__Service
            assert _.graph_service       is self.graph_service

    def test__method_signatures(self):                                                      # Test all methods exist
        with Area__Graph__Query() as _:
            assert hasattr(_, 'find_nodes_by_type')
            assert hasattr(_, 'find_node_by_id')
            assert hasattr(_, 'find_edges_by_type')

            assert callable(_.find_nodes_by_type)
            assert callable(_.find_node_by_id)
            assert callable(_.find_edges_by_type)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Method Signature Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__find_nodes_by_type__method_signature(self):                                   # Test find_nodes_by_type signature
        with Area__Graph__Query() as _:
            sig    = inspect.signature(_.find_nodes_by_type)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Find_Nodes__Request
            assert sig.return_annotation == Schema__Graph__Find_Nodes__Response

    def test__find_node_by_id__method_signature(self):                                      # Test find_node_by_id signature
        with Area__Graph__Query() as _:
            sig    = inspect.signature(_.find_node_by_id)
            params = list(sig.parameters.keys())

            assert 'graph_ref' in params
            assert 'node_id'   in params

    def test__find_edges_by_type__method_signature(self):                                   # Test find_edges_by_type signature
        with Area__Graph__Query() as _:
            sig    = inspect.signature(_.find_edges_by_type)
            params = list(sig.parameters.keys())

            assert 'graph_ref' in params
            assert 'edge_type' in params

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _create_test_graph(self):                                                           # Helper to create empty graph
        graph_ref = Schema__Graph__Ref(namespace=self.test_namespace)
        request   = Schema__Graph__Create__Request(graph_ref=graph_ref, auto_cache=True)
        response  = self.area_crud.create_graph(request)
        return response.graph_ref

    def _add_node(self, graph_ref):                                                         # Helper to add a node
        request  = Schema__Graph__Add_Node__Request(graph_ref=graph_ref, auto_cache=True)
        response = self.area_edit.add_node.add_node(request)
        return response

    def _add_edge(self, graph_ref, from_node_id, to_node_id):                               # Helper to add an edge
        request  = Schema__Graph__Add_Edge__Request(graph_ref    = graph_ref   ,
                                                    from_node_id = from_node_id,
                                                    to_node_id   = to_node_id  ,
                                                    auto_cache   = True        )
        response = self.area_edit.add_edge.add_edge(request)
        return response

    def _delete_graph(self, graph_ref):                                                     # Helper to delete graph
        delete_ref = Schema__Graph__Ref(graph_id  = graph_ref.graph_id ,
                                        namespace = graph_ref.namespace)
        return self.area_crud.delete_graph(graph_ref=delete_ref)

    def _create_graph_with_nodes_and_edges(self):                                           # Helper to create graph with structure
        graph_ref = self._create_test_graph()

        # Add 3 nodes
        node_1 = self._add_node(graph_ref)
        graph_ref = node_1.graph_ref

        node_2 = self._add_node(graph_ref)
        graph_ref = node_2.graph_ref

        node_3 = self._add_node(graph_ref)
        graph_ref = node_3.graph_ref

        # Add edges: 1->2, 2->3
        edge_1 = self._add_edge(graph_ref, node_1.node_id, node_2.node_id)
        graph_ref = edge_1.graph_ref

        edge_2 = self._add_edge(graph_ref, node_2.node_id, node_3.node_id)
        graph_ref = edge_2.graph_ref

        return {
            'graph_ref': graph_ref                ,
            'node_ids' : [node_1.node_id, node_2.node_id, node_3.node_id],
            'edge_ids' : [edge_1.edge_id, edge_2.edge_id]
        }

    # ═══════════════════════════════════════════════════════════════════════════════
    # find_nodes_by_type Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_find_nodes_by_type__empty_graph(self):                                         # Test finding nodes in empty graph
        graph_ref = self._create_test_graph()

        with self.area_query as _:
            request  = Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref    ,
                                                          node_type = 'SomeType'   ,
                                                          limit     = 100          ,
                                                          offset    = 0            )
            response = _.find_nodes_by_type(request)

            assert type(response)           is Schema__Graph__Find_Nodes__Response
            assert type(response.graph_ref) is Schema__Graph__Ref
            assert type(response.node_ids)  is Type_Safe__List
            assert type(response.total_found) is Safe_UInt
            assert len(response.node_ids)   == 0
            assert response.total_found     == 0
            assert response.has_more        is False

        self._delete_graph(graph_ref)

    def test_find_nodes_by_type__with_nodes(self):                                          # Test finding nodes that exist
        test_data = self._create_graph_with_nodes_and_edges()
        graph_ref = test_data['graph_ref']

        with self.area_query as _:
            # Query for default node type (MGraph uses Schema__MGraph__Node)
            request  = Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref                         ,
                                                          node_type = 'Schema__MGraph__Node'            ,
                                                          limit     = 100                               ,
                                                          offset    = 0                                 )
            response = _.find_nodes_by_type(request)

            assert type(response) is Schema__Graph__Find_Nodes__Response
            # Note: actual results depend on how MGraph query works

        self._delete_graph(graph_ref)

    def test_find_nodes_by_type__pagination(self):                                          # Test pagination works
        test_data = self._create_graph_with_nodes_and_edges()
        graph_ref = test_data['graph_ref']

        with self.area_query as _:
            # Request with limit 1
            request  = Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref ,
                                                          node_type = 'SomeType',
                                                          limit     = 1         ,
                                                          offset    = 0         )
            response = _.find_nodes_by_type(request)

            assert type(response.total_found) is Safe_UInt
            assert type(response.has_more)    is bool

        self._delete_graph(graph_ref)

    def test_find_nodes_by_type__response_types(self):                                      # Test response field types
        graph_ref = self._create_test_graph()

        with self.area_query as _:
            request  = Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref ,
                                                          node_type = 'SomeType',
                                                          limit     = 10        ,
                                                          offset    = 0         )
            response = _.find_nodes_by_type(request)

            assert type(response.graph_ref)           is Schema__Graph__Ref
            assert type(response.graph_ref.graph_id)  is Graph_Id
            assert type(response.graph_ref.cache_id)  is Cache_Id
            assert type(response.node_ids)            is Type_Safe__List
            assert type(response.total_found)         is Safe_UInt
            assert type(response.has_more)            is bool

        self._delete_graph(graph_ref)

    # ═══════════════════════════════════════════════════════════════════════════════
    # find_node_by_id Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_find_node_by_id__found(self):                                                  # Test finding existing node
        test_data = self._create_graph_with_nodes_and_edges()
        graph_ref = test_data['graph_ref']
        node_id   = test_data['node_ids'][0]

        assert type(graph_ref) is Schema__Graph__Ref
        assert type(node_id  ) is Node_Id

        with self.area_query as _:
            response = _.find_node_by_id(graph_ref = graph_ref,
                                         node_id   = node_id  )

            assert type(response)           is Schema__Graph__Find_Node__Response
            assert type(response.graph_ref) is Schema__Graph__Ref
            assert response.found           is True
            assert response.node_id         == node_id
            assert response.obj()           == __( graph_ref  = graph_ref.obj(),
                                                   node_id   = node_id,
                                                   found     = True,
                                                   node_data = __(node_data = __()              ,
                                                                  node_id   = Obj_Id(node_id)   ,
                                                                  node_type = 'mgraph_db.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node'))

        self._delete_graph(graph_ref)

    def test_find_node_by_id__not_found(self):                                              # Test finding non-existent node
        graph_ref    = self._create_test_graph()
        fake_node_id = Node_Id(Obj_Id())

        with self.area_query as _:
            response = _.find_node_by_id(graph_ref = graph_ref   ,
                                         node_id   = fake_node_id)

            assert type(response) is Schema__Graph__Find_Node__Response
            assert response.found is False
            assert response.node_id == fake_node_id

        self._delete_graph(graph_ref)

    def test_find_node_by_id__response_types(self):                                         # Test response field types
        test_data = self._create_graph_with_nodes_and_edges()
        graph_ref = test_data['graph_ref']
        node_id   = test_data['node_ids'][0]

        with self.area_query as _:
            response = _.find_node_by_id(graph_ref=graph_ref, node_id=node_id)

            assert type(response.graph_ref)           is Schema__Graph__Ref
            assert type(response.graph_ref.graph_id)  is Graph_Id
            assert type(response.graph_ref.cache_id)  is Cache_Id
            assert type(response.node_id)             is Node_Id
            assert type(response.found)               is bool

        self._delete_graph(graph_ref)

    # ═══════════════════════════════════════════════════════════════════════════════
    # find_edges_by_type Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_find_edges_by_type__empty_graph(self):                                         # Test finding edges in empty graph
        graph_ref = self._create_test_graph()

        with self.area_query as _:
            response = _.find_edges_by_type(graph_ref = graph_ref  ,
                                            edge_type = 'SOME_TYPE')

            assert type(response)           is Schema__Graph__Find_Edges__Response
            assert type(response.graph_ref) is Schema__Graph__Ref
            assert response.edge_type       == 'SOME_TYPE'
            assert len(response.edges)      == 0
            assert response.total_found     == 0

        self._delete_graph(graph_ref)

    def test_find_edges_by_type__with_edges(self):                                          # Test finding edges that exist
        test_data = self._create_graph_with_nodes_and_edges()
        graph_ref = test_data['graph_ref']

        with self.area_query as _:
            # Query for default edge type
            response = _.find_edges_by_type(graph_ref = graph_ref           ,
                                            edge_type = 'Schema__MGraph__Edge')

            assert type(response) is Schema__Graph__Find_Edges__Response
            # Note: actual results depend on MGraph edge types

        self._delete_graph(graph_ref)

    def test_find_edges_by_type__response_types(self):                                      # Test response field types
        graph_ref = self._create_test_graph()

        with self.area_query as _:
            response = _.find_edges_by_type(graph_ref=graph_ref, edge_type='SOME_TYPE')

            assert type(response.graph_ref)           is Schema__Graph__Ref
            assert type(response.graph_ref.graph_id)  is Graph_Id
            assert type(response.graph_ref.cache_id)  is Cache_Id
            assert type(response.edges)               is Type_Safe__List
            assert type(response.total_found)         is Safe_UInt

        self._delete_graph(graph_ref)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Graph Ref Resolution Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_query__resolves_graph_ref_by_cache_id(self):                                   # Test query resolves by cache_id
        graph_ref = self._create_test_graph()

        with self.area_query as _:
            # Use only cache_id
            lookup_ref = Schema__Graph__Ref(cache_id  = graph_ref.cache_id ,
                                            namespace = graph_ref.namespace)
            request    = Schema__Graph__Find_Nodes__Request(graph_ref = lookup_ref,
                                                            node_type = 'SomeType',
                                                            limit     = 10        )
            response = _.find_nodes_by_type(request)

            assert type(response.graph_ref)    is Schema__Graph__Ref
            assert response.graph_ref.cache_id == graph_ref.cache_id
            assert response.graph_ref.graph_id != ''                                        # graph_id should be resolved

        self._delete_graph(graph_ref)

    def test_query__resolves_graph_ref_by_graph_id(self):                                   # Test query resolves by graph_id
        graph_ref = self._create_test_graph()

        with self.area_query as _:
            # Use only graph_id
            lookup_ref = Schema__Graph__Ref(graph_id  = graph_ref.graph_id ,
                                            namespace = graph_ref.namespace)
            request    = Schema__Graph__Find_Nodes__Request(graph_ref = lookup_ref,
                                                            node_type = 'SomeType',
                                                            limit     = 10        )
            response = _.find_nodes_by_type(request)

            assert type(response.graph_ref)    is Schema__Graph__Ref
            assert response.graph_ref.graph_id == graph_ref.graph_id
            assert response.graph_ref.cache_id != ''                                        # cache_id should be resolved

        self._delete_graph(graph_ref)