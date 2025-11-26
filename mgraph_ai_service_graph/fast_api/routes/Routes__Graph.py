from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid

from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response             import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request                 import Schema__Graph__Get__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response                import Schema__Graph__Get__Response

from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Request            import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Response           import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Request            import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Response           import Schema__Graph__Add_Edge__Response

from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request         import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response        import Schema__Graph__Find_Nodes__Response

from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query


TAG__ROUTES_GRAPH = 'graph'


class Routes__Graph(Fast_API__Routes):              # Graph operation routes - single execution endpoints

    area_crud  : Area__Graph__CRUD                                                          # CRUD operations
    area_edit  : Area__Graph__Edit                                                          # Edit operations
    area_query : Area__Graph__Query                                                         # Query operations
    #area_cache : Area__Graph__Cache                                                        # Future: Cache operations
    #area_export: Area__Graph__Export                                                       # Future: Export operations

    def create(self,                                                # Create a new empty graph
               request: Schema__Graph__Create__Request              # Graph creation parameters
              ) -> Schema__Graph__Create__Response:                 # Response with graph_id and cache status
        return self.area_crud.create_graph(request)

    def get__by_id__graph_id(self,                                  # Retrieve graph by ID
                             graph_id: Random_Guid                  # Unique graph identifier
                        ) -> Schema__Graph__Get__Response:          # Response with graph metadata
        request = Schema__Graph__Get__Request(graph_id=graph_id)
        return self.area_crud.get_graph(request)

    # ============================================================================
    # Edit Endpoints
    # ============================================================================

    def add__node(self,                                             # Add a node to a graph
                  request: Schema__Graph__Add_Node__Request         # Node addition parameters
                 ) -> Schema__Graph__Add_Node__Response:            # Response with created node_id
        return self.area_edit.add_node(request)

    def add__edge(self,                                             # Add an edge between two nodes
                  request: Schema__Graph__Add_Edge__Request         # Edge addition parameters
                 ) -> Schema__Graph__Add_Edge__Response:            # Response with created edge_id
        return self.area_edit.add_edge(request)

    # ============================================================================
    # Query Endpoints
    # ============================================================================

    def find__nodes(self,                                           # Find nodes by type with pagination
                    request: Schema__Graph__Find_Nodes__Request     # Query parameters with type filter
                   ) -> Schema__Graph__Find_Nodes__Response:        # Response with list of node_ids
        return self.area_query.find_nodes_by_type(request)

    # ============================================================================
    # Route Registration
    # ============================================================================

    def setup_routes(self):                                         # Register all route handlers with FastAPI

        self.add_route_post(self.create)                            # CRUD routes
        self.add_route_get (self.get__by_id__graph_id)

        self.add_route_post(self.add__node)                         # Edit routes
        self.add_route_post(self.add__edge)

        self.add_route_post(self.find__nodes)                       # Query routes

        return self
