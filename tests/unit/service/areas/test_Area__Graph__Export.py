import pytest
from unittest                                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Env                                                                  import env_value
from osbot_utils.utils.Objects                                                              import base_classes
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                          import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Json__Request      import Schema__Graph__Export__Json__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Json__Response     import Schema__Graph__Export__Json__Response
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Dot__Request       import Schema__Graph__Export__Dot__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Dot__Response      import Schema__Graph__Export__Dot__Response
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Mermaid__Request   import Schema__Graph__Export__Mermaid__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Export__Mermaid__Response  import Schema__Graph__Export__Mermaid__Response
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Screenshot__Request        import Schema__Graph__Screenshot__Request
from mgraph_ai_service_graph.schemas.graph_export.Schema__Graph__Screenshot__Response       import Schema__Graph__Screenshot__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request
from mgraph_ai_service_graph.service.areas.Area__Graph__Export                              import Area__Graph__Export, ENV_VAR_URL__MGRAPH_DB_SERVERLESS
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Request      import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Request      import Schema__Graph__Add_Edge__Request
from tests.unit.Graph__Service__Fast_API__Test_Objs                                         import client_cache_service


class test_Area__Graph__Export(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client, cls.cache_service = client_cache_service()
        cls.graph_cache_client              = Graph__Cache__Client(cache_client=cls.cache_client)
        cls.graph_service                   = Graph__Service(graph_cache_client=cls.graph_cache_client)

        cls.area_export = Area__Graph__Export(graph_service=cls.graph_service)
        cls.area_crud   = Area__Graph__CRUD  (graph_service=cls.graph_service)
        cls.area_edit   = Area__Graph__Edit  (graph_service=cls.graph_service)

        cls.test_namespace = Safe_Str__Id('test-area-export')

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Area__Graph__Export() as _:
            assert type(_)               is Area__Graph__Export
            assert base_classes(_)       == [Type_Safe, object]
            assert type(_.graph_service) is Graph__Service

    def test__graph_service_dependency(self):                                               # Test graph service is injected
        with self.area_export as _:
            assert _.graph_service is not None
            assert type(_.graph_service) is Graph__Service
            assert _.graph_service       is self.graph_service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _create_test_graph(self):                                                           # Helper to create a graph with nodes and edges
        graph_ref = Schema__Graph__Ref(namespace=self.test_namespace)
        request   = Schema__Graph__Create__Request(graph_ref=graph_ref, auto_cache=True)
        response  = self.area_crud.create_graph(request)
        return response.graph_ref

    def _create_graph_with_structure(self):                                                 # Helper to create graph with nodes and edges
        graph_ref = self._create_test_graph()
        graph_id  = graph_ref.graph_id
        cache_id  = graph_ref.cache_id

        # Add nodes
        node_graph_ref_1 = Schema__Graph__Ref(graph_id=graph_id, cache_id=cache_id,
                                              namespace=self.test_namespace)
        node_request_1   = Schema__Graph__Add_Node__Request(graph_ref=node_graph_ref_1, auto_cache=True)
        node_response_1  = self.area_edit.add_node.add_node(node_request_1)
        cache_id         = node_response_1.graph_ref.cache_id

        node_graph_ref_2 = Schema__Graph__Ref(graph_id=graph_id, cache_id=cache_id,
                                              namespace=self.test_namespace)
        node_request_2   = Schema__Graph__Add_Node__Request(graph_ref=node_graph_ref_2, auto_cache=True)
        node_response_2  = self.area_edit.add_node.add_node(node_request_2)
        cache_id         = node_response_2.graph_ref.cache_id

        # Add edge
        edge_graph_ref = Schema__Graph__Ref(graph_id=graph_id, cache_id=cache_id,
                                            namespace=self.test_namespace)
        edge_request   = Schema__Graph__Add_Edge__Request(graph_ref    = edge_graph_ref          ,
                                                          from_node_id = node_response_1.node_id ,
                                                          to_node_id   = node_response_2.node_id ,
                                                          auto_cache   = True                    )
        edge_response = self.area_edit.add_edge.add_edge(edge_request)

        return edge_response.graph_ref

    def _delete_graph(self, graph_ref) -> bool:                                                     # Helper to delete graph
        delete_ref = Schema__Graph__Ref(graph_id  = graph_ref.graph_id ,
                                        namespace = graph_ref.namespace)
        return self.area_crud.delete_graph(graph_ref=delete_ref)

    # ═══════════════════════════════════════════════════════════════════════════════
    # JSON Export Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export_json__empty_graph(self):                                                # Test JSON export of empty graph
        graph_ref = self._create_test_graph()

        with self.area_export as _:
            request  = Schema__Graph__Export__Json__Request(graph_ref  = graph_ref,
                                                            compressed = False    )
            response = _.export_json(request)

            assert type(response)            is Schema__Graph__Export__Json__Response
            assert type(response.graph_ref)  is Schema__Graph__Ref
            assert response.success          is True
            assert response.graph_json       is not None
            assert type(response.graph_json) is dict

        self._delete_graph(graph_ref)

    def test_export_json__with_structure(self):                                             # Test JSON export of graph with nodes/edges
        graph_ref = self._create_graph_with_structure()

        with self.area_export as _:
            request  = Schema__Graph__Export__Json__Request(graph_ref  = graph_ref,
                                                            compressed = False    )
            response = _.export_json(request)

            assert response.success   is True
            assert response.graph_json is not None

            # Verify JSON contains graph data
            json_data = response.graph_json
            assert 'graph' in json_data

        self._delete_graph(graph_ref)

    def test_export_json__compressed(self):                                                 # Test compressed JSON export
        graph_ref = self._create_test_graph()

        with self.area_export as _:
            request  = Schema__Graph__Export__Json__Request(graph_ref  = graph_ref,
                                                            compressed = True     )
            response = _.export_json(request)

            assert response.success   is True
            assert response.graph_json is not None

            # Compressed format should have _type_registry
            json_data = response.graph_json
            assert '_type_registry' in json_data

        self._delete_graph(graph_ref)

    def test_export_json__creates_new_graph_if_empty_ref(self):                             # Test that empty graph_ref creates new graph
        with self.area_export as _:
            graph_ref = Schema__Graph__Ref(namespace=self.test_namespace)
            request   = Schema__Graph__Export__Json__Request(graph_ref=graph_ref, compressed=False)
            response  = _.export_json(request)

            assert response.success             is True
            assert response.graph_ref.cache_id  != ''                                       # New graph was created and cached
            assert response.graph_ref.graph_id  != ''

            # Cleanup
            assert self._delete_graph(response.graph_ref) is True

    def test_export_json__response_types(self):                                             # Test response field types
        graph_ref = self._create_test_graph()

        with self.area_export as _:
            request  = Schema__Graph__Export__Json__Request(graph_ref=graph_ref, compressed=False)
            response = _.export_json(request)

            assert type(response.graph_ref)           is Schema__Graph__Ref
            assert type(response.graph_ref.graph_id)  is Graph_Id
            assert type(response.graph_ref.cache_id)  is Cache_Id
            assert type(response.success)             is bool
            assert type(response.graph_json)          is dict

        self._delete_graph(graph_ref)

    # ═══════════════════════════════════════════════════════════════════════════════
    # DOT Export Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export_dot__empty_graph(self):                                                 # Test DOT export of empty graph
        graph_ref = self._create_test_graph()

        with self.area_export as _:
            request  = Schema__Graph__Export__Dot__Request(graph_ref=graph_ref)
            response = _.export_dot(request)

            assert type(response)           is Schema__Graph__Export__Dot__Response
            assert type(response.graph_ref) is Schema__Graph__Ref
            assert response.success         is True
            assert response.dot             is not None
            assert type(response.dot)       is str

        self._delete_graph(graph_ref)

    def test_export_dot__with_structure(self):                                              # Test DOT export of graph with nodes/edges
        graph_ref = self._create_graph_with_structure()

        with self.area_export as _:
            request  = Schema__Graph__Export__Dot__Request(graph_ref=graph_ref)
            response = _.export_dot(request)

            assert response.success is True
            assert response.dot     is not None

            # DOT format should contain digraph
            assert type(response) is Schema__Graph__Export__Dot__Response
            assert 'digraph' in response.dot

        self._delete_graph(graph_ref)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Mermaid Export Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export_mermaid__empty_graph(self):                                             # Test Mermaid export of empty graph
        graph_ref = self._create_test_graph()

        with self.area_export as _:
            request  = Schema__Graph__Export__Mermaid__Request(graph_ref=graph_ref)
            response = _.export_mermaid(request)

            assert type(response)           is Schema__Graph__Export__Mermaid__Response
            assert type(response.graph_ref) is Schema__Graph__Ref
            assert response.success         is True
            assert response.mermaid         is not None
            assert type(response.mermaid)   is str

        self._delete_graph(graph_ref)

    def test_export_mermaid__with_structure(self):                                          # Test Mermaid export of graph with nodes/edges
        graph_ref = self._create_graph_with_structure()

        with self.area_export as _:
            request  = Schema__Graph__Export__Mermaid__Request(graph_ref=graph_ref)
            response = _.export_mermaid(request)

            assert response.success is True
            assert response.mermaid is not None

            # Mermaid format should contain graph or flowchart
            mermaid_lower = response.mermaid.lower()
            assert 'graph' in mermaid_lower or 'flowchart' in mermaid_lower

        self._delete_graph(graph_ref)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Screenshot Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_screenshot__png_format(self):                                                  # Test PNG screenshot
        if env_value(ENV_VAR_URL__MGRAPH_DB_SERVERLESS) is None:
            pytest.skip(f"can't test the screenshot because {ENV_VAR_URL__MGRAPH_DB_SERVERLESS} is not set")

        graph_ref = self._create_test_graph()

        with self.area_export as _:
            request  = Schema__Graph__Screenshot__Request(graph_ref = graph_ref,)
            response = _.screenshot(request)

            assert type(response)            is Schema__Graph__Screenshot__Response
            assert type(response.graph_ref)  is Schema__Graph__Ref
            assert response.content_type     == 'image/png'
            assert len(response.image_base64) > 100

        self._delete_graph(graph_ref)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Graph Ref Resolution Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_export__resolves_graph_ref_by_cache_id(self):                                  # Test export resolves by cache_id
        graph_ref = self._create_test_graph()

        with self.area_export as _:
            # Use only cache_id
            lookup_ref = Schema__Graph__Ref(cache_id  = graph_ref.cache_id ,
                                            namespace = graph_ref.namespace)
            request    = Schema__Graph__Export__Json__Request(graph_ref=lookup_ref, compressed=False)
            response   = _.export_json(request)

            assert response.success                 is True
            assert response.graph_ref.cache_id      == graph_ref.cache_id
            assert response.graph_ref.graph_id      != ''                                   # graph_id should be resolved

        self._delete_graph(graph_ref)

    def test_export__resolves_graph_ref_by_graph_id(self):                                  # Test export resolves by graph_id
        graph_ref = self._create_test_graph()

        with self.area_export as _:
            # Use only graph_id
            lookup_ref = Schema__Graph__Ref(graph_id  = graph_ref.graph_id ,
                                            namespace = graph_ref.namespace)
            request    = Schema__Graph__Export__Json__Request(graph_ref=lookup_ref, compressed=False)
            response   = _.export_json(request)

            assert response.success                 is True
            assert response.graph_ref.graph_id      == graph_ref.graph_id
            assert response.graph_ref.cache_id      != ''                                   # cache_id should be resolved

        self._delete_graph(graph_ref)