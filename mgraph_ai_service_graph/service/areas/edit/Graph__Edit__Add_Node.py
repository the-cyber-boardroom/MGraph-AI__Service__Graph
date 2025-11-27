from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Response         import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Typed__Request   import Schema__Graph__Add_Node__Typed__Request
from mgraph_db.mgraph.MGraph                                                                    import MGraph
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                 import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Add_Node__Request          import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.service.graph.Graph__Service                                       import Graph__Service


DEFAULT_NAMESPACE = 'graph-service'     # todo: move to central config file


class Graph__Edit__Add_Node(Type_Safe):
    graph_service: Graph__Service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Core Operations - Map directly to MGraph__Edit methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def add_node(self,                                                  # Basic node - uses MGraph defaults
                 request: Schema__Graph__Add_Node__Request              # Wraps: graph.edit().new_node()
                ) -> Schema__Graph__Add_Node__Response:

        graph, namespace = self._get_graph(request)
        node             = graph.edit().new_node()

        return self._create_response(node       = node            ,
                                     graph      = graph           ,
                                     graph_id   = request.graph_id,
                                     namespace  = namespace       ,
                                     auto_cache = request.auto_cache)

    def add_typed_node(self,                                                # Typed node - custom type and data
                       request: Schema__Graph__Add_Node__Typed__Request     # Wraps: graph.edit().new_node(node_type=..., node_data=...)
                      ) -> Schema__Graph__Add_Node__Response:

        graph, namespace = self._get_graph(request)

        kwargs = {}
        if request.node_type:
            kwargs['node_type'] = request.node_type
        if request.node_data:
            kwargs['node_data'] = request.node_data

        node = graph.edit().new_node(**kwargs)

        return self._create_response(node       = node            ,
                                     graph      = graph           ,
                                     graph_id   = request.graph_id,
                                     namespace  = namespace       ,
                                     auto_cache = request.auto_cache)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    # todo: this get graph is used in multiple Graph__Edit__* methods, refactor to a common Graph__Edit__Base class
    def _get_graph(self,
                   request: Schema__Graph__Add_Node__Typed__Request
              ) -> tuple[MGraph, Safe_Str__Id]:                                 # should just return MGraph or a new schema (which has for example the cache_id and graph_id
        namespace = request.namespace or DEFAULT_NAMESPACE                      # todo: fix namespace pattern (should just return MGraph)

        if request.cache_id:
            graph = self.graph_service.get_graph(cache_id  = request.cache_id,
                                                 namespace = namespace       )
        else:
            graph = self.graph_service.get_or_create_graph(graph_id  = request.graph_id,
                                                           namespace = namespace       )
        return graph, namespace

    def _create_response(self,                                          # Build standardized response
                         node                    ,
                         graph      : MGraph     ,
                         graph_id   : Obj_Id     ,
                         namespace  : Safe_Str__Id,
                         auto_cache : bool
                        ) -> Schema__Graph__Add_Node__Response:

        node_id  = Obj_Id(str(node.node_id))
        cached   = False
        cache_id = None

        if auto_cache:
            cache_id = self.graph_service.save_graph(mgraph    = graph    ,
                                                     namespace = namespace)
            cached = True

        return Schema__Graph__Add_Node__Response(node_id  = node_id ,
                                                 graph_id = graph_id,
                                                 cache_id = cache_id,
                                                 cached   = cached  ,
                                                 success  = True    )