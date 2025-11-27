from osbot_fast_api.api.routes.Fast_API__Routes                                                     import Fast_API__Routes
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                     import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Predicate__Request   import Schema__Graph__Add_Edge__Predicate__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Response             import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Typed__Request       import Schema__Graph__Add_Edge__Typed__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Delete_Edge__Response          import Schema__Graph__Delete_Edge__Response
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Request              import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Response             import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Typed__Request       import Schema__Graph__Add_Node__Typed__Request
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Delete_Node__Response          import Schema__Graph__Delete_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.values.Schema__Graph__Add_Value__Request            import Schema__Graph__Add_Value__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Request              import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.values.Schema__Graph__Add_Value__Response           import Schema__Graph__Add_Value__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                        import Area__Graph__Edit


TAG__ROUTES_GRAPH_EDIT = 'graph-edit'


class Routes__Graph__Edit(Fast_API__Routes):
    tag       : str              = TAG__ROUTES_GRAPH_EDIT
    area_edit : Area__Graph__Edit

    # ═══════════════════════════════════════════════════════════════════════════════
    # Node Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def add__node(self,                                                 # Add basic node
                  request: Schema__Graph__Add_Node__Request
             ) -> Schema__Graph__Add_Node__Response:

        return self.area_edit.add_node.add_node(request)

    def add__node__typed(self,                                          # Add typed node
                         request: Schema__Graph__Add_Node__Typed__Request
                     ) -> Schema__Graph__Add_Node__Response:

        return self.area_edit.add_node.add_typed_node(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def add__value(self,                                                # Add value node
                   request: Schema__Graph__Add_Value__Request
              ) -> Schema__Graph__Add_Value__Response:

        return self.area_edit.add_value.add_value(request)

    def add__value__get_or_create(self,                                 # Get or create value node
                                  request: Schema__Graph__Add_Value__Request
                             ) -> Schema__Graph__Add_Value__Response:

        return self.area_edit.add_value.get_or_create_value(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def add__edge(self,                                                 # Add basic edge
                  request: Schema__Graph__Add_Edge__Request
             ) -> Schema__Graph__Add_Edge__Response:

        return self.area_edit.add_edge.add_edge(request)

    def add__edge__typed(self,                                          # Add typed edge
                         request: Schema__Graph__Add_Edge__Typed__Request
                    ) -> Schema__Graph__Add_Edge__Response:

        return self.area_edit.add_edge.add_typed_edge(request)

    def add__edge__predicate(self,                                      # Add predicate edge
                             request: Schema__Graph__Add_Edge__Predicate__Request
                        ) -> Schema__Graph__Add_Edge__Response:

        return self.area_edit.add_edge.add_predicate_edge(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Delete Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def delete__node__graph_id__node_id(self,
                                        graph_id  : Obj_Id      ,
                                        node_id   : Obj_Id      ,
                                        namespace : Safe_Str__Id = 'graph-service'      # todo: use static config value
                                   ) -> Schema__Graph__Delete_Node__Response:

        deleted = self.area_edit.delete.delete_node(graph_id  = graph_id ,
                                                    node_id   = node_id  ,
                                                    namespace = namespace)

        return Schema__Graph__Delete_Node__Response(graph_id = graph_id,
                                                    node_id  = node_id ,
                                                    deleted  = deleted )

    def delete__edge__graph_id__edge_id(self,
                                        graph_id  : Obj_Id      ,
                                        edge_id   : Obj_Id      ,
                                        namespace : Safe_Str__Id = 'graph-service'          # todo: use static config value
                                   ) -> Schema__Graph__Delete_Edge__Response:

        deleted = self.area_edit.delete.delete_edge(graph_id  = graph_id ,
                                                    edge_id   = edge_id  ,
                                                    namespace = namespace)

        return Schema__Graph__Delete_Edge__Response(graph_id = graph_id,
                                                    edge_id  = edge_id ,
                                                    deleted  = deleted )

    def setup_routes(self):
        # Nodes
        self.add_route_post(self.add__node              )
        self.add_route_post(self.add__node__typed       )
        # Values
        self.add_route_post(self.add__value             )
        self.add_route_post(self.add__value__get_or_create)
        # Edges
        self.add_route_post(self.add__edge              )
        self.add_route_post(self.add__edge__typed       )
        self.add_route_post(self.add__edge__predicate   )
        # Deletes
        self.add_route_delete(self.delete__node__graph_id__node_id)
        self.add_route_delete(self.delete__edge__graph_id__edge_id)
        return self