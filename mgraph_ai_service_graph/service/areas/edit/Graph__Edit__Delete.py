from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
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
                    namespace : Safe_Str__Id = DEFAULT_NAMESPACE
               ) -> bool:

        graph = self.graph_service.get_or_create_graph(graph_id  = graph_id ,
                                                       namespace = namespace)
        if graph is None:
            return False

        result = graph.edit().delete_node(node_id=node_id)

        if result:
            self.graph_service.save_graph(mgraph    = graph    ,
                                          namespace = namespace)
        return result

    def delete_edge(self,                                               # Delete an edge from graph
                    graph_id  : Obj_Id                       ,          # Wraps: graph.edit().delete_edge()
                    edge_id   : Obj_Id                       ,
                    namespace : Safe_Str__Id = DEFAULT_NAMESPACE
               ) -> bool:

        graph = self.graph_service.get_or_create_graph(graph_id  = graph_id ,
                                                       namespace = namespace)
        if graph is None:
            return False

        result = graph.edit().delete_edge(edge_id=edge_id)

        if result:
            self.graph_service.save_graph(mgraph    = graph    ,
                                          namespace = namespace)
        return result