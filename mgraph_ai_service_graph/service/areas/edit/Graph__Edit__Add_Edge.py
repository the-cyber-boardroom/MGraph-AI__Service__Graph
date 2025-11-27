from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Predicate__Request   import Schema__Graph__Add_Edge__Predicate__Request
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Response             import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Typed__Request       import Schema__Graph__Add_Edge__Typed__Request
from mgraph_db.mgraph.MGraph                                                                        import MGraph
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                     import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Add_Edge__Request              import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.service.graph.Graph__Service                                           import Graph__Service


DEFAULT_NAMESPACE = 'graph-service'      # todo remove this namespace logic from here


class Graph__Edit__Add_Edge(Type_Safe):
    graph_service: Graph__Service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Core Operations - Map directly to MGraph__Edit methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def add_edge(self,                                                  # Basic edge between two nodes
                 request: Schema__Graph__Add_Edge__Request              # Wraps: graph.edit().new_edge()
            ) -> Schema__Graph__Add_Edge__Response:

        graph, namespace = self._get_graph(request)

        edge = graph.edit().new_edge(from_node_id = request.from_node_id,
                                     to_node_id   = request.to_node_id  )

        return self._create_response(edge         = edge                ,
                                     graph        = graph               ,
                                     graph_id     = request.graph_id    ,
                                     from_node_id = request.from_node_id,
                                     to_node_id   = request.to_node_id  ,
                                     namespace    = namespace           ,
                                     auto_cache   = request.auto_cache  )

    def add_typed_edge(self,                                                # Edge with specific type
                       request: Schema__Graph__Add_Edge__Typed__Request     # Wraps: graph.edit().new_edge(edge_type=...)
                  ) -> Schema__Graph__Add_Edge__Response:

        graph, namespace = self._get_graph(request)

        edge = graph.edit().new_edge(from_node_id = request.from_node_id,
                                     to_node_id   = request.to_node_id  ,
                                     edge_type    = request.edge_type   )

        return self._create_response(edge         = edge                ,
                                     graph        = graph               ,
                                     graph_id     = request.graph_id    ,
                                     from_node_id = request.from_node_id,
                                     to_node_id   = request.to_node_id  ,
                                     namespace    = namespace           ,
                                     auto_cache   = request.auto_cache  )

    def add_predicate_edge(self,                                                 # Semantic edge with predicate
                           request: Schema__Graph__Add_Edge__Predicate__Request  # Wraps: graph.edit().get_or_create_edge() with predicate
                      ) -> Schema__Graph__Add_Edge__Response:

        graph, namespace = self._get_graph(request)

        edge = graph.edit().get_or_create_edge(from_node_id = request.from_node_id,
                                               to_node_id   = request.to_node_id  ,
                                               predicate    = str(request.predicate))

        return self._create_response(edge         = edge                ,
                                     graph        = graph               ,
                                     graph_id     = request.graph_id    ,
                                     from_node_id = request.from_node_id,
                                     to_node_id   = request.to_node_id  ,
                                     namespace    = namespace           ,
                                     auto_cache   = request.auto_cache  )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════


    def _get_graph(self,
                   request: Schema__Graph__Add_Edge__Request
              ) -> tuple[MGraph, Safe_Str__Id]:                                 # should just return MGraph or a new schema (which has for example the cache_id and graph_id
        namespace = request.namespace or DEFAULT_NAMESPACE                      # todo: fix namespace pattern (should just return MGraph)

        if request.cache_id:
            graph = self.graph_service.get_graph(cache_id  = request.cache_id,
                                                 namespace = namespace       )
        else:
            graph = self.graph_service.get_or_create_graph(graph_id  = request.graph_id,
                                                           namespace = namespace       )
        return graph, namespace

    def _create_response(self,
                         edge                      ,
                         graph        : MGraph     ,
                         graph_id     : Obj_Id     ,
                         from_node_id : Obj_Id     ,
                         to_node_id   : Obj_Id     ,
                         namespace    : Safe_Str__Id,
                         auto_cache   : bool
                        ) -> Schema__Graph__Add_Edge__Response:

        edge_id  = Obj_Id(str(edge.edge_id))
        cached   = False
        cache_id = None

        if auto_cache:
            cache_id = self.graph_service.save_graph(mgraph    = graph    ,
                                                     namespace = namespace)
            cached = True

        return Schema__Graph__Add_Edge__Response(edge_id      = edge_id     ,
                                                 graph_id     = graph_id    ,
                                                 from_node_id = from_node_id,
                                                 to_node_id   = to_node_id  ,
                                                 cache_id     = cache_id    ,
                                                 cached       = cached      ,
                                                 success      = True        )