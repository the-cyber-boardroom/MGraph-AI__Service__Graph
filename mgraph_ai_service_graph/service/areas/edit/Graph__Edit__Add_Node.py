from mgraph_db.mgraph.MGraph                                                                    import MGraph
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                import Obj_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                               import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Request          import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Response         import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Typed__Request   import Schema__Graph__Add_Node__Typed__Request
from mgraph_ai_service_graph.service.graph.Graph__Service                                       import Graph__Service


class Graph__Edit__Add_Node(Type_Safe):
    graph_service: Graph__Service

    def add_node(self,                                                          # Add basic node
                 request: Schema__Graph__Add_Node__Request
                ) -> Schema__Graph__Add_Node__Response:

        graph_ref                = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref     = self.graph_service.resolve_graph_ref(graph_ref)
        node                     = mgraph.edit().new_node()

        return self._create_response(node       = node              ,
                                     mgraph     = mgraph            ,
                                     graph_ref  = resolved_ref      ,
                                     auto_cache = request.auto_cache)

    def add_typed_node(self,                                                    # Add typed node
                       request: Schema__Graph__Add_Node__Typed__Request
                      ) -> Schema__Graph__Add_Node__Response:

        graph_ref                = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref     = self.graph_service.resolve_graph_ref(graph_ref)

        kwargs = {}
        if request.node_type:
            kwargs['node_type'] = request.node_type
        if request.node_data:
            kwargs['node_data'] = request.node_data

        node = mgraph.edit().new_node(**kwargs)

        return self._create_response(node       = node              ,
                                     mgraph     = mgraph            ,
                                     graph_ref  = resolved_ref      ,
                                     auto_cache = request.auto_cache)

    def _create_response(self,                                                  # Build standardized response
                         node                    ,
                         mgraph     : MGraph     ,
                         graph_ref  : Schema__Graph__Ref,
                         auto_cache : bool
                        ) -> Schema__Graph__Add_Node__Response:

        node_id = Obj_Id(str(node.node_id))
        cached  = False

        if auto_cache:
            graph_ref = self.graph_service.save_graph_ref(mgraph    = mgraph   ,
                                                          graph_ref = graph_ref)
            cached = True

        return Schema__Graph__Add_Node__Response(graph_ref = graph_ref,
                                                 node_id   = node_id  ,
                                                 cached    = cached   ,
                                                 success   = True     )