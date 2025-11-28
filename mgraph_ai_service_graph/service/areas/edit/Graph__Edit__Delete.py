from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid               import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id     import Safe_Str__Id
from mgraph_ai_service_graph.service.graph.Graph__Service                           import Graph__Service


DEFAULT_NAMESPACE = 'graph-service'


class Graph__Edit__Delete(Type_Safe):
    graph_service: Graph__Service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Core Operations - Map directly to MGraph__Edit methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def delete_node(self,                                               # Delete a node from graph
                    graph_id  : Obj_Id                       ,          # Wraps: graph.edit().delete_node()
                    node_id   : Obj_Id                       ,
                    cache_id  : Random_Guid  = None          ,          # NEW: optional cache_id
                    namespace : Safe_Str__Id = DEFAULT_NAMESPACE
               ) -> bool:

        graph = self._get_graph(graph_id  = graph_id ,
                                cache_id  = cache_id ,
                                namespace = namespace)
        if graph is None:
            return False

        result = graph.edit().delete_node(node_id=node_id)

        if result:
            self.graph_service.save_graph(mgraph    = graph    ,
                                          namespace = namespace,
                                          cache_id  = cache_id )        # Pass cache_id for update
        return result

    def delete_edge(self,                                               # Delete an edge from graph
                    graph_id  : Obj_Id                       ,          # Wraps: graph.edit().delete_edge()
                    edge_id   : Obj_Id                       ,
                    cache_id  : Random_Guid  = None          ,          # NEW: optional cache_id
                    namespace : Safe_Str__Id = DEFAULT_NAMESPACE
               ) -> bool:

        graph = self._get_graph(graph_id  = graph_id ,
                                cache_id  = cache_id ,
                                namespace = namespace)
        if graph is None:
            return False

        result = graph.edit().delete_edge(edge_id=edge_id)

        if result:
            self.graph_service.save_graph(mgraph    = graph    ,
                                          namespace = namespace,
                                          cache_id  = cache_id )        # Pass cache_id for update
        return result

    # ═══════════════════════════════════════════════════════════════════════════════
    # Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _get_graph(self,
                   graph_id  : Obj_Id       ,
                   cache_id  : Random_Guid  ,
                   namespace : Safe_Str__Id ):

        if cache_id:                                                    # Retrieve from cache if cache_id provided
            return self.graph_service.get_graph(cache_id  = cache_id ,
                                                namespace = namespace)
        else:                                                           # Otherwise get or create by graph_id
            return self.graph_service.get_or_create_graph(graph_id  = graph_id ,
                                                          namespace = namespace)