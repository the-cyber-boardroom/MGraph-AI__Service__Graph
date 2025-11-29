from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request         import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response        import Schema__Graph__Find_Nodes__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Node__Response         import Schema__Graph__Find_Node__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Edges__Response        import Schema__Graph__Find_Edges__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query


TAG__ROUTES_GRAPH_QUERY   = 'graph-query'
ROUTES_PATHS__GRAPH_QUERY = [ '/graph-query/find/nodes'    ,
                              '/graph-query/find/node'     ,
                              '/graph-query/find/edges'    ]


class Routes__Graph__Query(Fast_API__Routes):                                               # Graph query routes
    tag        : str               = TAG__ROUTES_GRAPH_QUERY
    area_query : Area__Graph__Query

    def find__nodes(self,                                                                   # Find nodes by type with pagination
                    request: Schema__Graph__Find_Nodes__Request
                   ) -> Schema__Graph__Find_Nodes__Response:
        return self.area_query.find_nodes_by_type(request)

    def find__node(self,                                                                    # Find specific node by ID
                   graph_ref : Schema__Graph__Ref,
                   node_id   : Obj_Id
                  ) -> Schema__Graph__Find_Node__Response:
        return self.area_query.find_node_by_id(graph_ref = graph_ref,
                                               node_id   = node_id  )

    def find__edges(self,                                                                   # Find edges by type
                    graph_ref : Schema__Graph__Ref,
                    edge_type : Safe_Str__Id
                   ) -> Schema__Graph__Find_Edges__Response:
        return self.area_query.find_edges_by_type(graph_ref = graph_ref,
                                                  edge_type = str(edge_type))

    def setup_routes(self):
        self.add_route_post(self.find__nodes)
        self.add_route_post(self.find__node )
        self.add_route_post(self.find__edges)
        return self