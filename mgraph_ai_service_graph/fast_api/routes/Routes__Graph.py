from osbot_fast_api.api.routes.Fast_API__Routes import Fast_API__Routes
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid import Random_Guid

from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response import Schema__Graph__Create__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query import Area__Graph__Query

TAG__ROUTES_GRAPH = 'graph'

class Routes__Graph(Fast_API__Routes):
    tag: str = TAG__ROUTES_GRAPH

    # Area classes injected
    area_crud  : Area__Graph__CRUD
    area_edit  : Area__Graph__Edit
    area_query : Area__Graph__Query
    #area_cache : Area__Graph__Cache
    #area_export: Area__Graph__Export

    # CRUD endpoints
    def create(self, request: Schema__Graph__Create__Request
              ) -> Schema__Graph__Create__Response:
        return self.area_crud.create_graph(request)

    def get__by_id__graph_id(self, graph_id: Random_Guid
                            ) -> Schema__Graph__Get__Response:
        request = Schema__Graph__Get__Request(graph_id=graph_id)
        return self.area_crud.get_graph(request)

    # Edit endpoints
    def add__node(self, request: Schema__Graph__Add_Node__Request
                 ) -> Schema__Graph__Add_Node__Response:
        return self.area_edit.add_node(request)

    def add__edge(self, request: Schema__Graph__Add_Edge__Request
                 ) -> Schema__Graph__Add_Edge__Response:
        return self.area_edit.add_edge(request)

    # Query endpoints
    def find__nodes(self, request: Schema__Graph__Find_Nodes__Request
                   ) -> Schema__Graph__Find_Nodes__Response:
        return self.area_query.find_nodes_by_type(request)

    def setup_routes(self):
        self.add_route_post(self.create)
        self.add_route_get(self.get__by_id__graph_id)
        self.add_route_post(self.add__node)
        self.add_route_post(self.add__edge)
        self.add_route_post(self.find__nodes)
        return self