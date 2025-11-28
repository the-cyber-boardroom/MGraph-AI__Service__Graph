from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from mgraph_ai_service_graph.schemas.graph_edit.values.Schema__Graph__Add_Value__Response   import Schema__Graph__Add_Value__Response
from mgraph_db.mgraph.MGraph                                                                import MGraph
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_edit.values.Schema__Graph__Add_Value__Request    import Schema__Graph__Add_Value__Request
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service


DEFAULT_NAMESPACE = 'graph-service'


class Graph__Edit__Add_Value(Type_Safe):
    graph_service: Graph__Service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Core Operations - Map directly to MGraph value operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def add_value(self,                                                 # Add value node
                  request: Schema__Graph__Add_Value__Request            # Wraps: graph.edit().new_value()
             ) -> Schema__Graph__Add_Value__Response:

        graph, namespace = self._get_graph(request)

        node = graph.edit().new_value(value = request.value,
                                      key   = request.key  )

        return self._create_response(node       = node              ,
                                     graph      = graph             ,
                                     graph_id   = request.graph_id  ,
                                     namespace  = namespace         ,
                                     value      = request.value     ,
                                     auto_cache = request.auto_cache,
                                     cache_id   = request.cache_id  )   # Pass cache_id

    def get_or_create_value(self,                                       # Get existing or create new value node
                            request: Schema__Graph__Add_Value__Request  # Wraps: graph.values().get_or_create()
                       ) -> Schema__Graph__Add_Value__Response:

        graph, namespace = self._get_graph(request)

        node = graph.values().get_or_create(value = request.value,
                                            key   = request.key  )

        return self._create_response(node       = node              ,
                                     graph      = graph             ,
                                     graph_id   = request.graph_id  ,
                                     namespace  = namespace         ,
                                     value      = request.value     ,
                                     auto_cache = request.auto_cache,
                                     cache_id   = request.cache_id  )   # Pass cache_id

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _get_graph(self,
                   request  : Schema__Graph__Add_Value__Request
              ) -> tuple[MGraph, Safe_Str__Id]:

        namespace = request.namespace or DEFAULT_NAMESPACE


        graph = self.graph_service.get_or_create_graph(cache_id  = request.cache_id,
                                                       graph_id  = request.graph_id,
                                                       namespace = namespace       )
        return graph, namespace

    def _create_response(self,
                         node                     ,
                         graph      : MGraph      ,
                         graph_id   : Obj_Id      ,
                         namespace  : Safe_Str__Id,
                         value      : str         ,
                         auto_cache : bool        ,
                         cache_id   : Random_Guid = None                # pass cache_id for updates
                    ) -> Schema__Graph__Add_Value__Response:

        node_id  = Obj_Id(str(node.node_id))
        cached   = False

        if auto_cache:
            cache_id = self.graph_service.save_graph(mgraph    = graph    ,
                                                     namespace = namespace,
                                                     cache_id  = cache_id )   # Pass cache_id for update
            cached = True

        return Schema__Graph__Add_Value__Response(node_id  = node_id ,
                                                  graph_id = graph_id,
                                                  cache_id = cache_id,
                                                  value    = value   ,
                                                  cached   = cached  ,
                                                  success  = True    )