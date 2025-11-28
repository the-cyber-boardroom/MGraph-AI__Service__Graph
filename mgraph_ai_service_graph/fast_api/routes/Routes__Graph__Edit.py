from osbot_fast_api.api.routes.Fast_API__Routes                                                     import Fast_API__Routes
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                    import Obj_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                                   import Schema__Graph__Ref
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


TAG__ROUTES_GRAPH_EDIT   = 'graph-edit'
ROUTES_PATHS__GRAPH_EDIT = ['/graph-edit/add/edge'          ,
                            '/graph-edit/add/edge/predicate',
                            '/graph-edit/add/edge/typed'    ,
                            '/graph-edit/add/node'          ,
                            '/graph-edit/add/node/typed'    ,
                            '/graph-edit/add/value'         ,
                            '/graph-edit/add/value/get-or-create',
                            '/graph-edit/delete/node'       ,
                            '/graph-edit/delete/edge'       ]


class Routes__Graph__Edit(Fast_API__Routes):
    tag       : str              = TAG__ROUTES_GRAPH_EDIT
    area_edit : Area__Graph__Edit

    # ═══════════════════════════════════════════════════════════════════════════════
    # Node Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def add__node(self,
                  request: Schema__Graph__Add_Node__Request
             ) -> Schema__Graph__Add_Node__Response:
        return self.area_edit.add_node.add_node(request)

    def add__node__typed(self,
                         request: Schema__Graph__Add_Node__Typed__Request
                     ) -> Schema__Graph__Add_Node__Response:
        return self.area_edit.add_node.add_typed_node(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def add__value(self,
                   request: Schema__Graph__Add_Value__Request
              ) -> Schema__Graph__Add_Value__Response:
        return self.area_edit.add_value.add_value(request)

    def add__value__get_or_create(self,
                                  request: Schema__Graph__Add_Value__Request
                             ) -> Schema__Graph__Add_Value__Response:
        return self.area_edit.add_value.get_or_create_value(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def add__edge(self,
                  request: Schema__Graph__Add_Edge__Request
             ) -> Schema__Graph__Add_Edge__Response:
        return self.area_edit.add_edge.add_edge(request)

    def add__edge__typed(self,
                         request: Schema__Graph__Add_Edge__Typed__Request
                    ) -> Schema__Graph__Add_Edge__Response:
        return self.area_edit.add_edge.add_typed_edge(request)

    def add__edge__predicate(self,
                             request: Schema__Graph__Add_Edge__Predicate__Request
                        ) -> Schema__Graph__Add_Edge__Response:
        return self.area_edit.add_edge.add_predicate_edge(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Delete Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def delete__node(self,
                     graph_ref : Schema__Graph__Ref,
                     node_id   : Obj_Id
                ) -> Schema__Graph__Delete_Node__Response:
        return self.area_edit.delete.delete_node(graph_ref = graph_ref,
                                                 node_id   = node_id  )

    def delete__edge(self,
                     graph_ref : Schema__Graph__Ref,
                     edge_id   : Obj_Id
                ) -> Schema__Graph__Delete_Edge__Response:
        return self.area_edit.delete.delete_edge(graph_ref = graph_ref,
                                                 edge_id   = edge_id  )

    def setup_routes(self):
        self.add_route_post(self.add__node                )
        self.add_route_post(self.add__node__typed         )
        self.add_route_post(self.add__value               )
        self.add_route_post(self.add__value__get_or_create)
        self.add_route_post(self.add__edge                )
        self.add_route_post(self.add__edge__typed         )
        self.add_route_post(self.add__edge__predicate     )
        self.add_route_post(self.delete__node             )
        self.add_route_post(self.delete__edge             )
        return self