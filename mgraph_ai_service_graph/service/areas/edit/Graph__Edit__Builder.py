from mgraph_ai_service_graph.schemas.graph_edit.builder.Schema__Graph__Builder__Add_Connected__Request      import Schema__Graph__Builder__Add_Connected__Request
from mgraph_ai_service_graph.schemas.graph_edit.builder.Schema__Graph__Builder__Add_Connected__Response     import Schema__Graph__Builder__Add_Connected__Response
from mgraph_db.mgraph.MGraph                                                                                import MGraph
from osbot_utils.type_safe.Type_Safe                                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                             import Safe_Str__Id
from mgraph_ai_service_graph.service.graph.Graph__Service                                                   import Graph__Service


DEFAULT_NAMESPACE = 'graph-service'

class Graph__Edit__Builder(Type_Safe):
    graph_service: Graph__Service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Core Operations - Map to MGraph__Builder methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def add_connected_node(self,                                        # Add node connected to existing node
                           request: Schema__Graph__Builder__Add_Connected__Request  # Wraps: builder.set_current_node().add_connected_node()
                          ) -> Schema__Graph__Builder__Add_Connected__Response:

        graph, namespace = self._get_graph(request)
        builder          = graph.builder()

        builder.set_current_node(request.from_node_id)

        if request.predicate:
            builder.add_connected_node(value     = request.value    ,
                                       predicate = request.predicate)
        else:
            builder.add_connected_node(value = request.value)

        node_id  = Obj_Id(str(builder.current_node().node_id))
        edge_id  = Obj_Id(str(builder.current_edge().edge_id)) if builder.current_edge() else None

        cached   = False
        cache_id = None

        if request.auto_cache:
            cache_id = self.graph_service.save_graph(mgraph    = graph    ,
                                                     namespace = namespace)
            cached = True

        return Schema__Graph__Builder__Add_Connected__Response(node_id  = node_id          ,
                                                               edge_id  = edge_id          ,
                                                               graph_id = request.graph_id ,
                                                               cache_id = cache_id         ,
                                                               cached   = cached           ,
                                                               success  = True             )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _get_graph(self, request) -> tuple[MGraph, Safe_Str__Id]:
        namespace = request.namespace or DEFAULT_NAMESPACE
        graph     = self.graph_service.get_or_create_graph(graph_id  = request.graph_id,
                                                           namespace = namespace       )
        return graph, namespace