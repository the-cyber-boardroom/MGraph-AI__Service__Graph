from mgraph_db.mgraph.MGraph                                                                        import MGraph
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                    import Obj_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                                   import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Request              import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Response             import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Typed__Request       import Schema__Graph__Add_Edge__Typed__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Predicate__Request   import Schema__Graph__Add_Edge__Predicate__Request
from mgraph_ai_service_graph.service.graph.Graph__Service                                           import Graph__Service


class Graph__Edit__Add_Edge(Type_Safe):
    graph_service: Graph__Service

    def add_edge(self,                                                          # Add basic edge
                 request: Schema__Graph__Add_Edge__Request
            ) -> Schema__Graph__Add_Edge__Response:

        graph_ref                = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref     = self.graph_service.resolve_graph_ref(graph_ref)

        edge = mgraph.edit().new_edge(from_node_id = request.from_node_id,
                                      to_node_id   = request.to_node_id  )

        return self._create_response(edge         = edge                ,
                                     mgraph       = mgraph              ,
                                     graph_ref    = resolved_ref        ,
                                     from_node_id = request.from_node_id,
                                     to_node_id   = request.to_node_id  ,
                                     auto_cache   = request.auto_cache  )

    def add_typed_edge(self,                                                    # Add typed edge
                       request: Schema__Graph__Add_Edge__Typed__Request
                  ) -> Schema__Graph__Add_Edge__Response:

        graph_ref                = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref     = self.graph_service.resolve_graph_ref(graph_ref)

        edge = mgraph.edit().new_edge(from_node_id = request.from_node_id,
                                      to_node_id   = request.to_node_id  ,
                                      edge_type    = request.edge_type   )

        return self._create_response(edge         = edge                ,
                                     mgraph       = mgraph              ,
                                     graph_ref    = resolved_ref        ,
                                     from_node_id = request.from_node_id,
                                     to_node_id   = request.to_node_id  ,
                                     auto_cache   = request.auto_cache  )

    def add_predicate_edge(self,                                                # Add predicate edge
                           request: Schema__Graph__Add_Edge__Predicate__Request
                      ) -> Schema__Graph__Add_Edge__Response:

        graph_ref                = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref     = self.graph_service.resolve_graph_ref(graph_ref)

        edge = mgraph.edit().get_or_create_edge(from_node_id = request.from_node_id    ,
                                                to_node_id   = request.to_node_id      ,
                                                predicate    = str(request.predicate)  )

        return self._create_response(edge         = edge                ,
                                     mgraph       = mgraph              ,
                                     graph_ref    = resolved_ref        ,
                                     from_node_id = request.from_node_id,
                                     to_node_id   = request.to_node_id  ,
                                     auto_cache   = request.auto_cache  )

    def _create_response(self,
                         edge                    ,
                         mgraph       : MGraph   ,
                         graph_ref    : Schema__Graph__Ref,
                         from_node_id : Obj_Id   ,
                         to_node_id   : Obj_Id   ,
                         auto_cache   : bool
                    ) -> Schema__Graph__Add_Edge__Response:

        edge_id = Obj_Id(edge.edge_id)
        cached  = False

        if auto_cache:
            graph_ref = self.graph_service.save_graph_ref(mgraph    = mgraph   ,
                                                          graph_ref = graph_ref)
            cached = True

        return Schema__Graph__Add_Edge__Response(graph_ref    = graph_ref   ,
                                                 edge_id      = edge_id     ,
                                                 from_node_id = from_node_id,
                                                 to_node_id   = to_node_id  ,
                                                 cached       = cached      ,
                                                 success      = True        )