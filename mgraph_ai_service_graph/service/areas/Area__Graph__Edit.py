from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Request            import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Response           import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Request            import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Response           import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service


DEFAULT_NAMESPACE = 'graph-service'


class Area__Graph__Edit(Type_Safe):                                                         # Graph editing operations area - handles adding/removing/updating nodes and edges

    graph_service: Graph__Service                                                           # Injected graph service dependency

    def add_node(self,                                                                      # Add a node to an existing graph
                 request: Schema__Graph__Add_Node__Request                                  # Node addition request with graph_id, type, data
                ) -> Schema__Graph__Add_Node__Response:                                     # Response with created node_id, graph_id, cache status

        namespace = request.namespace or DEFAULT_NAMESPACE                                  # Use request namespace or default
        graph     = self.graph_service.get_or_create_graph(graph_id  = request.graph_id,
                                                           namespace = namespace       )

        node_data_dict = {}                                                                 # Convert Safe_Str__Key dict to regular dict for MGraph
        if request.node_data:
            node_data_dict = {str(k): str(v) for k, v in request.node_data.items()}

        node    = graph.edit().new_node(node_type = request.node_type ,                     # Add node using MGraph's edit API
                                        node_data = node_data_dict    )
        node_id = Obj_Id(str(node.node_id))

        cached   = False
        cache_id = None
        if request.auto_cache:
            cache_id = self.graph_service.save_graph(graph_id  = request.graph_id ,
                                                     graph     = graph            ,
                                                     namespace = namespace        )
            cached = True
            if cache_id:
                cache_id = Random_Guid(cache_id)

        return Schema__Graph__Add_Node__Response(node_id  = node_id          ,
                                                 graph_id = request.graph_id ,
                                                 cache_id = cache_id         ,
                                                 cached   = cached           ,
                                                 success  = True             )

    def add_edge(self,                                                                      # Add an edge between two nodes in a graph
                 request: Schema__Graph__Add_Edge__Request                                  # Edge addition request with graph_id, from/to nodes, type, data
                ) -> Schema__Graph__Add_Edge__Response:                                     # Response with created edge_id, graph_id, cache status

        namespace = request.namespace or DEFAULT_NAMESPACE                                  # Use request namespace or default
        graph     = self.graph_service.get_or_create_graph(graph_id  = request.graph_id,
                                                           namespace = namespace       )

        edge_data_dict = {}                                                                 # Convert Safe_Str__Key dict to regular dict
        if request.edge_data:
            edge_data_dict = {str(k): str(v) for k, v in request.edge_data.items()}

        edge    = graph.edit().new_edge(from_node_id = request.from_node_id ,               # Add edge using MGraph's edit API
                                        to_node_id   = request.to_node_id   ,
                                        edge_type    = request.edge_type    ,
                                        edge_data    = edge_data_dict       )
        edge_id = Obj_Id(str(edge.edge_id))

        cached   = False
        cache_id = None
        if request.auto_cache:
            cache_id = self.graph_service.save_graph(graph_id  = request.graph_id ,
                                                     graph     = graph            ,
                                                     namespace = namespace        )
            cached = True
            if cache_id:
                cache_id = Random_Guid(cache_id)

        return Schema__Graph__Add_Edge__Response(edge_id      = edge_id              ,
                                                 graph_id     = request.graph_id     ,
                                                 from_node_id = request.from_node_id ,
                                                 to_node_id   = request.to_node_id   ,
                                                 cache_id     = cache_id             ,
                                                 cached       = cached               ,
                                                 success      = True                 )

    def delete_node(self,                                                                   # Delete a node from graph
                    graph_id  : Obj_Id                       ,                              # Target graph
                    node_id   : Obj_Id                       ,                              # Node to delete
                    namespace : str    = DEFAULT_NAMESPACE                                  # Cache namespace
                   ) -> bool:                                                               # True if deleted successfully

        graph  = self.graph_service.get_or_create_graph(graph_id  = graph_id ,
                                                        namespace = namespace)
        if graph is None:
            return False

        result = graph.edit().delete_node(node_id=node_id)                                  # Use MGraph's delete API

        if result:
            self.graph_service.save_graph(graph_id  = graph_id ,                            # Update cache only if deletion succeeded
                                          graph     = graph    ,
                                          namespace = namespace)
        return result

    def delete_edge(self,                                                                   # Delete an edge from graph
                    graph_id  : Obj_Id                       ,                              # Target graph
                    edge_id   : Obj_Id                       ,                              # Edge to delete
                    namespace : str    = DEFAULT_NAMESPACE                                  # Cache namespace
                   ) -> bool:                                                               # True if deleted successfully

        graph  = self.graph_service.get_or_create_graph(graph_id  = graph_id ,
                                                        namespace = namespace)
        if graph is None:
            return False

        result = graph.edit().delete_edge(edge_id=edge_id)                                  # Use MGraph's delete API

        if result:
            self.graph_service.save_graph(graph_id  = graph_id ,                            # Update cache only if deletion succeeded
                                          graph     = graph    ,
                                          namespace = namespace)
        return result