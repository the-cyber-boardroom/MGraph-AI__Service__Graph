class Area__Graph__Edit(Type_Safe):
    graph_service: Graph__Service

    @staticmethod
    def add_node(request: Schema__Graph__Add_Node__Request
                ) -> Schema__Graph__Add_Node__Response:
        """Add a node to a graph"""
        # 1. Retrieve graph from cache
        graph = retrieve_graph(request.graph_id)

        # 2. Add node using MGraph
        node = graph.edit().new_node(
            node_type = request.node_type,
            node_data = request.node_data
        )

        # 3. Update cache
        update_cached_graph(request.graph_id, graph)

        return Schema__Graph__Add_Node__Response(
            node_id = node.node_id,
            graph_id = request.graph_id
        )

    @staticmethod
    def add_edge(request: Schema__Graph__Add_Edge__Request
                ) -> Schema__Graph__Add_Edge__Response:
        """Add an edge between nodes"""
        pass