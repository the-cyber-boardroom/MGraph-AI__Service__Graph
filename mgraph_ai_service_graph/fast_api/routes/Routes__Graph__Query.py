from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text

from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request         import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response        import Schema__Graph__Find_Nodes__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Node__Request          import Schema__Graph__Find_Node__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Node__Response         import Schema__Graph__Find_Node__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Edges__Request         import Schema__Graph__Find_Edges__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Edges__Response        import Schema__Graph__Find_Edges__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Edge__Data                  import Schema__Graph__Edge__Data
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Neighbors__Request          import Schema__Graph__Neighbors__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Neighbors__Response         import Schema__Graph__Neighbors__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query


TAG__ROUTES_GRAPH_QUERY   = 'graph-query'
ROUTES_PATHS__GRAPH_QUERY = [ '/graph-query/find/nodes'                           ,
                              '/graph-query/find/node/{graph_id}/{node_id}'       ,
                              '/graph-query/find/edges/{graph_id}/{edge_type}'    ,
                              '/graph-query/neighbors/{graph_id}/{node_id}'       ]


class Routes__Graph__Query(Fast_API__Routes):                                               # Graph query routes - search and exploration
    tag        : str               = TAG__ROUTES_GRAPH_QUERY
    area_query : Area__Graph__Query                                                         # Query operations

    def find__nodes(self,                                                                   # Find nodes by type with pagination
                    request: Schema__Graph__Find_Nodes__Request                             # Query parameters with type filter
                   ) -> Schema__Graph__Find_Nodes__Response:                                # Response with list of node_ids
        return self.area_query.find_nodes_by_type(request)

    def find__node__graph_id__node_id(self,                                                 # Find specific node by ID
                                      graph_id: Obj_Id        ,                             # Target graph
                                      node_id : Obj_Id                                      # Node to find
                                     ) -> Schema__Graph__Find_Node__Response:               # Node data
        try:
            result = self.area_query.find_node_by_id(graph_id = str(graph_id),
                                                     node_id  = str(node_id) )
            node_data_typed = {Safe_Str__Key(k): Safe_Str__Text(str(v))                     # Convert node_data to type-safe dict
                               for k, v in result.get('node_data', {}).items()}

            return Schema__Graph__Find_Node__Response(graph_id  = graph_id                            ,
                                                      node_id   = Obj_Id(result.get('node_id' , ''))  ,
                                                      node_type = result.get('node_type', '')         ,
                                                      node_data = node_data_typed                     ,
                                                      found     = True                                )
        except KeyError:
            return Schema__Graph__Find_Node__Response(graph_id = graph_id,
                                                      node_id  = node_id ,
                                                      found    = False   )

    def find__edges__graph_id__edge_type(self,                                              # Find edges by type
                                         graph_id : Obj_Id       ,                          # Target graph
                                         edge_type: Safe_Str__Id                            # Edge type to find
                                        ) -> Schema__Graph__Find_Edges__Response:           # List of edge data
        edges_raw = self.area_query.find_edges_by_type(graph_id  = str(graph_id) ,
                                                       edge_type = str(edge_type))
        edges_typed = []
        for edge in edges_raw:
            edge_data_typed = {Safe_Str__Key(k): Safe_Str__Text(str(v))                     # Convert edge_data to type-safe dict
                               for k, v in edge.get('edge_data', {}).items()}

            edges_typed.append(Schema__Graph__Edge__Data(
                edge_id      = Obj_Id(edge.get('edge_id'     , '')),
                from_node_id = Obj_Id(edge.get('from_node_id', '')),
                to_node_id   = Obj_Id(edge.get('to_node_id'  , '')),
                edge_type    = edge.get('edge_type', '')           ,
                edge_data    = edge_data_typed                     ))

        return Schema__Graph__Find_Edges__Response(graph_id    = graph_id           ,
                                                   edge_type   = edge_type          ,
                                                   edges       = edges_typed        ,
                                                   total_found = len(edges_typed)   )

    def neighbors__graph_id__node_id(self,                                                  # Get neighboring nodes
                                     graph_id: Obj_Id         ,                             # Target graph
                                     node_id : Obj_Id                                       # Node to get neighbors for
                                    ) -> Schema__Graph__Neighbors__Response:                # List of neighbor node IDs
        neighbor_ids_raw = self.area_query.get_neighbors(graph_id = str(graph_id),
                                                         node_id  = str(node_id) )
        neighbor_ids_typed = [Obj_Id(nid) for nid in neighbor_ids_raw]

        return Schema__Graph__Neighbors__Response(graph_id     = graph_id               ,
                                                  node_id      = node_id                ,
                                                  neighbor_ids = neighbor_ids_typed     ,
                                                  total_found  = len(neighbor_ids_typed))

    def setup_routes(self):                                                                 # Register query route handlers
        self.add_route_post(self.find__nodes                     )
        self.add_route_get (self.find__node__graph_id__node_id   )
        self.add_route_get (self.find__edges__graph_id__edge_type)
        self.add_route_get (self.neighbors__graph_id__node_id    )
        return self
