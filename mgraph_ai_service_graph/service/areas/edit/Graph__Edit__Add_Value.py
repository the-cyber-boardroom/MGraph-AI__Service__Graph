from mgraph_db.mgraph.MGraph                                                                import MGraph
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_edit.values.Schema__Graph__Add_Value__Request    import Schema__Graph__Add_Value__Request
from mgraph_ai_service_graph.schemas.graph_edit.values.Schema__Graph__Add_Value__Response   import Schema__Graph__Add_Value__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service


class Graph__Edit__Add_Value(Type_Safe):
    graph_service: Graph__Service

    def add_value(self,                                                         # Add value node
                  request: Schema__Graph__Add_Value__Request
             ) -> Schema__Graph__Add_Value__Response:

        graph_ref                = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref     = self.graph_service.resolve_graph_ref(graph_ref)

        node = mgraph.edit().new_value(value = request.value,
                                       key   = request.key  )

        return self._create_response(node       = node              ,
                                     mgraph     = mgraph            ,
                                     graph_ref  = resolved_ref      ,
                                     value      = request.value     ,
                                     auto_cache = request.auto_cache)

    def get_or_create_value(self,                                               # Get existing or create new value node
                            request: Schema__Graph__Add_Value__Request
                       ) -> Schema__Graph__Add_Value__Response:

        graph_ref                = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref     = self.graph_service.resolve_graph_ref(graph_ref)

        node = mgraph.values().get_or_create(value = request.value,
                                             key   = request.key  )

        return self._create_response(node       = node              ,
                                     mgraph     = mgraph            ,
                                     graph_ref  = resolved_ref      ,
                                     value      = request.value     ,
                                     auto_cache = request.auto_cache)

    def _create_response(self,
                         node                   ,
                         mgraph     : MGraph    ,
                         graph_ref  : Schema__Graph__Ref,
                         value      : str       ,
                         auto_cache : bool
                    ) -> Schema__Graph__Add_Value__Response:

        node_id = Obj_Id(str(node.node_id))
        cached  = False

        if auto_cache:
            graph_ref = self.graph_service.save_graph_ref(mgraph    = mgraph   ,
                                                          graph_ref = graph_ref)
            cached = True

        return Schema__Graph__Add_Value__Response(graph_ref = graph_ref,
                                                  node_id   = node_id  ,
                                                  value     = value    ,
                                                  cached    = cached   ,
                                                  success   = True     )