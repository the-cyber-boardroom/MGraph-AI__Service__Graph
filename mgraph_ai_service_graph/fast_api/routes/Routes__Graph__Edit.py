from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id

from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Request            import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Response           import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Request            import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Response           import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Delete_Node__Response        import Schema__Graph__Delete_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Delete_Edge__Response        import Schema__Graph__Delete_Edge__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit


TAG__ROUTES_GRAPH_EDIT = 'graph-edit'
ROUTES_PATHS__GRAPH_EDIT = [ '/graph-edit/add/node'                            ,
                             '/graph-edit/add/edge'                            ,
                             '/graph-edit/delete/node/{graph_id}/{node_id}'    ,
                             '/graph-edit/delete/edge/{graph_id}/{edge_id}'    ]


class Routes__Graph__Edit(Fast_API__Routes):                                                # Graph edit routes - node/edge manipulation
    tag       : str             = TAG__ROUTES_GRAPH_EDIT
    area_edit : Area__Graph__Edit                                                           # Edit operations

    def add__node(self,                                                                     # Add a node to a graph
                  request: Schema__Graph__Add_Node__Request                                 # Node addition parameters
                 ) -> Schema__Graph__Add_Node__Response:                                    # Response with created node_id
        return self.area_edit.add_node(request)

    def add__edge(self,                                                                     # Add an edge between two nodes
                  request: Schema__Graph__Add_Edge__Request                                 # Edge addition parameters
                 ) -> Schema__Graph__Add_Edge__Response:                                    # Response with created edge_id
        return self.area_edit.add_edge(request)

    def delete__node__graph_id__node_id(self,                                               # Delete a node from graph
                                        graph_id: Obj_Id      ,                             # Target graph
                                        node_id : Obj_Id                                    # Node to delete
                                       ) -> Schema__Graph__Delete_Node__Response:           # Response with deletion status
        deleted = self.area_edit.delete_node(graph_id = str(graph_id),
                                             node_id  = str(node_id) )
        return Schema__Graph__Delete_Node__Response(graph_id = graph_id,
                                                    node_id  = node_id ,
                                                    deleted  = deleted )

    def delete__edge__graph_id__edge_id(self,                                               # Delete an edge from graph
                                        graph_id: Obj_Id      ,                             # Target graph
                                        edge_id : Obj_Id                                    # Edge to delete
                                       ) -> Schema__Graph__Delete_Edge__Response:           # Response with deletion status
        deleted = self.area_edit.delete_edge(graph_id = str(graph_id),
                                             edge_id  = str(edge_id) )
        return Schema__Graph__Delete_Edge__Response(graph_id = graph_id,
                                                    edge_id  = edge_id ,
                                                    deleted  = deleted )

    def setup_routes(self):                                                                 # Register edit route handlers
        self.add_route_post  (self.add__node                      )
        self.add_route_post  (self.add__edge                      )
        self.add_route_delete(self.delete__node__graph_id__node_id)
        self.add_route_delete(self.delete__edge__graph_id__edge_id)
        return self
