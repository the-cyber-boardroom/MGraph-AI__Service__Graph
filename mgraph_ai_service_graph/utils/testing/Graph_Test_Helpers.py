"""
Graph Test Helpers

Provides helper methods to create test state using graph service API methods.
Creates reusable test fixtures for graph testing with in-memory cache service.

Usage:
    helpers = Graph_Test_Helpers(area_crud=area_crud, area_edit=area_edit, area_query=area_query)
    graph   = helpers.create_empty_graph(namespace="test")
    graph   = helpers.create_graph_with_nodes(node_count=3)
    graph   = helpers.create_graph_with_edges(node_count=3, edge_count=2)
"""
from typing                                                                                 import Dict, List, Tuple
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client import Cache__Service__Fast_API__Client
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client
from mgraph_ai_service_graph.service.caching.Graph__Cache__Utils                            import Graph__Cache__Utils
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service
from osbot_utils.decorators.methods.cache_on_self                                           import cache_on_self
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.numerical.safe_int.Safe_Int__Positive         import Safe_Int__Positive
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                              import type_safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from osbot_utils.utils.Misc                                                                 import random_string
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response             import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request                 import Schema__Graph__Get__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response                import Schema__Graph__Get__Response
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Request      import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Response     import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Request      import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Response     import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request         import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response        import Schema__Graph__Find_Nodes__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query

NAMESPACE__GRAPH_TEST_HELPERS = 'test-graphs'


class Graph_Test_Helpers(Type_Safe):                # Helper methods to create and verify test state for graph operations

    cache_client : Cache__Service__Fast_API__Client

    # ═══════════════════════════════════════════════════════════════════════════════
    # Core objects
    # ═══════════════════════════════════════════════════════════════════════════════

    @cache_on_self
    def graph_cache_client(self) -> Graph__Cache__Client:
        return Graph__Cache__Client(cache_client = self.cache_client)


    @cache_on_self
    def graph_service(self) -> Graph__Service:
        return Graph__Service(graph_cache_client = self.graph_cache_client())

    @cache_on_self
    def cache_utils(self) -> Graph__Cache__Utils:
        return self.graph_cache_client().cache_utils()
    @cache_on_self
    def area_crud(self):
        return Area__Graph__CRUD (graph_service = self.graph_service() )

    @cache_on_self
    def area_edit(self):
        return Area__Graph__Edit (graph_service = self.graph_service() )
    
    @cache_on_self
    def area_query(self):
        return Area__Graph__Query(graph_service = self.graph_service() )
    # ═══════════════════════════════════════════════════════════════════════════════
    # Graph Creation - Basic Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_empty_graph(self,
                           namespace  : str  = NAMESPACE__GRAPH_TEST_HELPERS,
                           auto_cache : bool = True
                           ) -> Schema__Graph__Create__Response:                             # Create an empty graph and return response
        graph_ref = Schema__Graph__Ref(namespace = namespace)
        request   = Schema__Graph__Create__Request(graph_ref  = graph_ref ,
                                                   auto_cache = auto_cache)
        return self.area_crud().create_graph(request)

    @type_safe
    def create_graph_with_nodes(self,
                                namespace  : str  = NAMESPACE__GRAPH_TEST_HELPERS,
                                node_count : int  = 3,
                                node_type  : str  = 'TestNode',
                                auto_cache : bool = True
                                ) -> Tuple[Schema__Graph__Create__Response, List[Schema__Graph__Add_Node__Response]]:
        create_response = self.create_empty_graph(namespace  = namespace ,                  # Create graph first
                                                  auto_cache = auto_cache)
        graph_ref       = create_response.graph_ref                                         # Use the returned graph_ref
        node_responses  = []

        for i in range(node_count):                                                         # Add nodes
            node_request = Schema__Graph__Add_Node__Request(graph_ref  = graph_ref ,
                                                            auto_cache = auto_cache)
            node_response = self.area_edit().add_node.add_node(node_request)
            graph_ref     = node_response.graph_ref                                         # Update graph_ref for next iteration
            node_responses.append(node_response)

        return create_response, node_responses

    @type_safe
    def create_graph_with_edges(self,
                                namespace  : str  = NAMESPACE__GRAPH_TEST_HELPERS,
                                node_count : int  = 3,
                                edge_type  : str  = 'CONNECTS',
                                auto_cache : bool = True
                                ) -> Tuple[Schema__Graph__Create__Response,
                                          List[Schema__Graph__Add_Node__Response],
                                          List[Schema__Graph__Add_Edge__Response]]:
        create_response, node_responses = self.create_graph_with_nodes(namespace  = namespace  ,    # Create graph with nodes first
                                                                       node_count = node_count ,
                                                                       auto_cache = auto_cache )
        graph_ref      = node_responses[-1].graph_ref if node_responses else create_response.graph_ref
        edge_responses = []

        for i in range(len(node_responses) - 1):                                            # Create chain of edges: node_0 -> node_1 -> node_2 -> ...
            from_node_id = node_responses[i].node_id
            to_node_id   = node_responses[i + 1].node_id
            edge_request = Schema__Graph__Add_Edge__Request(graph_ref    = graph_ref    ,
                                                            from_node_id = from_node_id ,
                                                            to_node_id   = to_node_id   ,
                                                            auto_cache   = auto_cache   )
            edge_response = self.area_edit().add_edge.add_edge(edge_request)
            graph_ref     = edge_response.graph_ref
            edge_responses.append(edge_response)

        return create_response, node_responses, edge_responses

    @type_safe
    def create_complete_graph(self,
                              namespace  : Safe_Str__Id        = NAMESPACE__GRAPH_TEST_HELPERS,
                              node_count : Safe_Int__Positive  = 4,
                              edge_type  : Safe_Str__Id  = 'CONNECTS',
                              auto_cache : bool = True
                              ) -> Tuple[Schema__Graph__Create__Response,
                                        List[Schema__Graph__Add_Node__Response],
                                        List[Schema__Graph__Add_Edge__Response]]:
        create_response, node_responses = self.create_graph_with_nodes(namespace  = namespace  ,    # Create fully connected graph (every node connects to every other node)
                                                                       node_count = node_count ,
                                                                       auto_cache = auto_cache )
        graph_ref      = node_responses[-1].graph_ref if node_responses else create_response.graph_ref
        edge_responses = []

        for i in range(len(node_responses)):                                                # Connect every node to every other node
            for j in range(i + 1, len(node_responses)):
                from_node_id = node_responses[i].node_id
                to_node_id   = node_responses[j].node_id
                edge_request = Schema__Graph__Add_Edge__Request(graph_ref    = graph_ref    ,
                                                                from_node_id = from_node_id ,
                                                                to_node_id   = to_node_id   ,
                                                                auto_cache   = auto_cache   )
                edge_response = self.area_edit().add_edge.add_edge(edge_request)
                graph_ref     = edge_response.graph_ref
                edge_responses.append(edge_response)

        return create_response, node_responses, edge_responses

    # ═══════════════════════════════════════════════════════════════════════════════
    # Graph Creation - Specialized Scenarios
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_graph_with_multiple_node_types(self,
                                              namespace  : str                = NAMESPACE__GRAPH_TEST_HELPERS,
                                              node_types : Dict[str, int]     = None,
                                              auto_cache : bool               = True
                                              ) -> Tuple[Schema__Graph__Create__Response,
                                                        Dict[str, List[Schema__Graph__Add_Node__Response]]]:
        if node_types is None:                                                              # Create graph with different node types
            node_types = {'Person': 2, 'Company': 1, 'Product': 3}

        create_response = self.create_empty_graph(namespace  = namespace ,
                                                  auto_cache = auto_cache)
        graph_ref       = create_response.graph_ref
        nodes_by_type   = {}

        for node_type, count in node_types.items():
            nodes_by_type[node_type] = []
            for i in range(count):
                node_request = Schema__Graph__Add_Node__Request(graph_ref  = graph_ref ,
                                                                auto_cache = auto_cache)
                node_response = self.area_edit().add_node.add_node(node_request)
                graph_ref     = node_response.graph_ref
                nodes_by_type[node_type].append(node_response)

        return create_response, nodes_by_type

    @type_safe
    def create_graph_with_multiple_edge_types(self,
                                              namespace  : str            = NAMESPACE__GRAPH_TEST_HELPERS,
                                              edge_types : List[str]      = None,
                                              auto_cache : bool           = True
                                              ) -> Tuple[Schema__Graph__Create__Response,
                                                        List[Schema__Graph__Add_Node__Response],
                                                        Dict[str, List[Schema__Graph__Add_Edge__Response]]]:
        if edge_types is None:                                                              # Create graph with different edge types
            edge_types = ['KNOWS', 'WORKS_AT', 'OWNS']

        create_response, node_responses = self.create_graph_with_nodes(namespace  = namespace ,
                                                                       node_count = 4        ,
                                                                       auto_cache = auto_cache)
        graph_ref     = node_responses[-1].graph_ref if node_responses else create_response.graph_ref
        edges_by_type = {}

        for i, edge_type in enumerate(edge_types):                                          # Create one edge of each type
            from_idx     = i % len(node_responses)
            to_idx       = (i + 1) % len(node_responses)
            from_node_id = node_responses[from_idx].node_id
            to_node_id   = node_responses[to_idx].node_id

            edge_request = Schema__Graph__Add_Edge__Request(graph_ref    = graph_ref    ,
                                                            from_node_id = from_node_id ,
                                                            to_node_id   = to_node_id   ,
                                                            auto_cache   = auto_cache   )
            edge_response = self.area_edit().add_edge.add_edge(edge_request)
            graph_ref     = edge_response.graph_ref
            edges_by_type[edge_type] = [edge_response]

        return create_response, node_responses, edges_by_type

    # ═══════════════════════════════════════════════════════════════════════════════
    # Node Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def add_node(self,
                 graph_ref  : Schema__Graph__Ref                     ,
                 node_type  : str                   = 'TestNode'     ,
                 node_data  : Dict[str, str]        = None           ,
                 auto_cache : bool                  = True
                ) -> Schema__Graph__Add_Node__Response:                                     # Add a single node to an existing graph
        node_request = Schema__Graph__Add_Node__Request(graph_ref  = graph_ref ,
                                                        auto_cache = auto_cache)
        return self.area_edit().add_node.add_node(node_request)

    @type_safe
    def add_nodes(self,
                  graph_ref  : Schema__Graph__Ref                     ,
                  count      : int      = 3                           ,
                  node_type  : str      = 'TestNode'                  ,
                  auto_cache : bool     = True
                 ) -> List[Schema__Graph__Add_Node__Response]:                              # Add multiple nodes to an existing graph
        responses = []
        current_ref = graph_ref
        for i in range(count):
            node_request = Schema__Graph__Add_Node__Request(graph_ref  = current_ref,
                                                            auto_cache = auto_cache )
            response    = self.area_edit().add_node.add_node(node_request)
            current_ref = response.graph_ref                                                # Update graph_ref for next iteration
            responses.append(response)
        return responses

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def add_edge(self,
                 graph_ref    : Schema__Graph__Ref                     ,
                 from_node_id : Obj_Id                                 ,
                 to_node_id   : Obj_Id                                 ,
                 edge_type    : str                   = 'CONNECTS'     ,
                 edge_data    : Dict[str, str]        = None           ,
                 auto_cache   : bool                  = True
                ) -> Schema__Graph__Add_Edge__Response:                                     # Add a single edge between two nodes
        edge_request = Schema__Graph__Add_Edge__Request(graph_ref    = graph_ref    ,
                                                        from_node_id = from_node_id ,
                                                        to_node_id   = to_node_id   ,
                                                        auto_cache   = auto_cache   )
        return self.area_edit().add_edge.add_edge(edge_request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Verification Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def verify_graph_exists(self,
                            graph_id  : Obj_Id                             ,
                            namespace : str        = NAMESPACE__GRAPH_TEST_HELPERS
                           ) -> bool:                                                       # Verify a graph exists in cache
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       namespace = namespace)
        return self.area_crud().graph_exists(graph_ref = graph_ref)

    @type_safe
    def verify_graph_exists_by_cache_id(self,
                                        cache_id  : Cache_Id                           ,
                                        namespace : str         = NAMESPACE__GRAPH_TEST_HELPERS
                                       ) -> bool:                                           # Verify a graph exists by cache_id
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       namespace = namespace)
        return self.area_crud().graph_exists(graph_ref = graph_ref)

    @type_safe
    def get_graph(self,
                  graph_id  : Obj_Id                             ,
                  namespace : str        = NAMESPACE__GRAPH_TEST_HELPERS
                 ) -> Schema__Graph__Get__Response:                                         # Retrieve a graph
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       namespace = namespace)
        request   = Schema__Graph__Get__Request(graph_ref = graph_ref)
        return self.area_crud().get_graph(request)

    @type_safe
    def get_graph_by_cache_id(self,
                              cache_id  : Cache_Id                           ,
                              namespace : str         = NAMESPACE__GRAPH_TEST_HELPERS
                             ) -> Schema__Graph__Get__Response:                             # Retrieve a graph by cache_id
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       namespace = namespace)
        request   = Schema__Graph__Get__Request(graph_ref = graph_ref)
        return self.area_crud().get_graph(request)

    @type_safe
    def find_nodes_by_type(self,
                           graph_ref : Schema__Graph__Ref                     ,
                           node_type : str                                    ,
                           limit     : int         = 100                      ,
                           offset    : int         = 0
                          ) -> Schema__Graph__Find_Nodes__Response:                         # Find nodes of a specific type
        request = Schema__Graph__Find_Nodes__Request(graph_ref = graph_ref,
                                                     node_type = node_type,
                                                     limit     = limit    ,
                                                     offset    = offset   )
        return self.area_query().find_nodes_by_type(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Cleanup Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def delete_graph(self,
                     graph_id  : Obj_Id                             ,
                     namespace : str        = NAMESPACE__GRAPH_TEST_HELPERS
                    ) -> bool:                                                              # Delete a graph
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       namespace = namespace)
        return self.area_crud().delete_graph(graph_ref = graph_ref)

    @type_safe
    def delete_graph_by_cache_id(self,
                                 cache_id  : Cache_Id                           ,
                                 namespace : str         = NAMESPACE__GRAPH_TEST_HELPERS
                                ) -> bool:                                                  # Delete a graph by cache_id
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       namespace = namespace)
        return self.area_crud().delete_graph(graph_ref = graph_ref)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Test Data Generators
    # ═══════════════════════════════════════════════════════════════════════════════

    @staticmethod
    def random_node_data(prefix: str = 'node') -> Dict[Safe_Str__Key, Safe_Str__Text]:      # Generate random node data for testing
        return { Safe_Str__Key('name')       : Safe_Str__Text(random_string(f'{prefix}_')) ,
                 Safe_Str__Key('created_by') : Safe_Str__Text('test')                      ,
                 Safe_Str__Key('random_id')  : Safe_Str__Text(random_string())             }

    @staticmethod
    def random_edge_data(prefix: str = 'edge') -> Dict[Safe_Str__Key, Safe_Str__Text]:      # Generate random edge data for testing
        return { Safe_Str__Key('label')      : Safe_Str__Text(random_string(f'{prefix}_')) ,
                 Safe_Str__Key('weight')     : Safe_Str__Text('1.0')                       ,
                 Safe_Str__Key('created_by') : Safe_Str__Text('test')                      }

    # ═══════════════════════════════════════════════════════════════════════════════
    # Assertion Helpers
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def assert_node_count(self,
                          graph_ref      : Schema__Graph__Ref     ,
                          node_type      : str                    ,
                          expected_count : int
                         ) -> bool:                                                         # Assert expected number of nodes of a type
        result = self.find_nodes_by_type(graph_ref = graph_ref,
                                         node_type = node_type)
        actual_count = int(result.total_found)
        if actual_count != expected_count:
            raise AssertionError(f"Expected {expected_count} nodes of type '{node_type}', found {actual_count}")
        return True

    @type_safe
    def assert_graph_exists(self,
                            graph_id  : Obj_Id                             ,
                            namespace : str        = NAMESPACE__GRAPH_TEST_HELPERS
                           ) -> bool:                                                       # Assert graph exists (raises if not)
        if not self.verify_graph_exists(graph_id  = graph_id ,
                                        namespace = namespace):
            raise AssertionError(f"Graph {graph_id} does not exist in namespace '{namespace}'")
        return True

    @type_safe
    def assert_graph_not_exists(self,
                                graph_id  : Obj_Id                             ,
                                namespace : str        = NAMESPACE__GRAPH_TEST_HELPERS
                               ) -> bool:                                                   # Assert graph does NOT exist (raises if exists)
        if self.verify_graph_exists(graph_id  = graph_id ,
                                    namespace = namespace):
            raise AssertionError(f"Graph {graph_id} exists in namespace '{namespace}' but should not")
        return True