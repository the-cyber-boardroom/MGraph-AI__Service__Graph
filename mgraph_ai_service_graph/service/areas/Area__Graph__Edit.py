from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Request            import Schema__Graph__Add_Node__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Node__Response           import Schema__Graph__Add_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Request            import Schema__Graph__Add_Edge__Request
from mgraph_ai_service_graph.schemas.graph_edit.Schema__Graph__Add_Edge__Response           import Schema__Graph__Add_Edge__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service



class Area__Graph__Edit(Type_Safe):                                         # Graph editing operations area - handles adding/removing/updating nodes and edges
                                                                            # This area provides mutation operations on graphs with automatic
                                                                            # cache synchronization.

    graph_service: Graph__Service                                           # Injected graph service dependency

    def add_node(self,                                                     # Add a node to an existing graph
                 request: Schema__Graph__Add_Node__Request                 # Node addition request with graph_id, type, data
            ) -> Schema__Graph__Add_Node__Response:                        # Response with created node_id, graph_id, cache status


        graph = self.graph_service.get_or_create_graph(graph_id  = str(request.graph_id),   # Retrieve graph from cache
                                                       namespace = "graphs")

        # todo: see if we need this conversion
        node_data_dict = {str(k): str(v) for k, v in request.node_data.items()}             # Convert Safe_Str__Key dict to regular dict for MGraph

        node = graph.edit().new_node(node_type = str(request.node_type),                    # Add node using MGraph's edit API
                                     node_data = node_data_dict)

        node_id = Obj_Id(str(node.node_id))

        cached = False
        if request.auto_cache:
            self.graph_service.save_graph(graph_id  = str(request.graph_id),
                                          graph     = graph                ,
                                          namespace = "graphs"             )
            cached = True

        return Schema__Graph__Add_Node__Response(node_id  = node_id        ,
                                                 graph_id = request.graph_id,
                                                 cached   = cached         )

    def add_edge(self,                                                     # Add an edge between two nodes in a graph
                 request: Schema__Graph__Add_Edge__Request                 # Edge addition request with graph_id, from/to nodes, type, data
            ) -> Schema__Graph__Add_Edge__Response:                        # Response with created edge_id, graph_id, cache status


        graph = self.graph_service.get_or_create_graph(graph_id  = str(request.graph_id),   # Retrieve graph
                                                       namespace = "graphs")

        # todo: see if we need this
        edge_data_dict = {str(k): str(v) for k, v in request.edge_data.items()}             # Convert Safe_Str__Key dict to regular dict

        edge = graph.edit().new_edge(from_node_id = str(request.from_node_id),              # Add edge using MGraph's edit API
                                     to_node_id   = str(request.to_node_id)  ,
                                     edge_type    = str(request.edge_type)   ,
                                     edge_data    = edge_data_dict)

        edge_id = Obj_Id(str(edge.edge_id))

        cached = False
        if request.auto_cache:
            self.graph_service.save_graph(graph_id  = str(request.graph_id),
                                          graph     = graph               ,
                                          namespace = "graphs")
            cached = True

        return Schema__Graph__Add_Edge__Response(edge_id  = edge_id        ,
                                                 graph_id = request.graph_id,
                                                 cached   = cached         )

    def delete_node(self,                                # Delete a node from graph
                    graph_id: str,                       # Target graph
                    node_id : str                        # Node to delete
               ) -> bool:                                # True if deleted successfully


        graph  = self.graph_service.get_or_create_graph(graph_id, "graphs")
        result = graph.edit().delete_node(node_id)                                  # Use MGraph's delete API

        self.graph_service.save_graph(graph_id, graph, "graphs")                    # Update cache

        return result

    def delete_edge(self,                                # Delete an edge from graph
                    graph_id: str,                       # Target graph
                    edge_id : str                        # Edge to delete
               ) -> bool:                                # True if deleted successfully

        graph  = self.graph_service.get_or_create_graph(graph_id, "graphs")
        result = graph.edit().delete_edge(edge_id)                                  # Use MGraph's delete API

        self.graph_service.save_graph(graph_id, graph, "graphs")                    # Update cache

        return result
