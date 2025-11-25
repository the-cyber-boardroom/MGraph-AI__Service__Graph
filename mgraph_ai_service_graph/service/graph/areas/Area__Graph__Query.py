from osbot_utils.type_safe.Type_Safe import Type_Safe


class Area__Graph__Query(Type_Safe):
    graph_service: Graph__Service

    @staticmethod
    def find_nodes_by_type(request: Schema__Graph__Find_Nodes__Request
                          ) -> Schema__Graph__Find_Nodes__Response:
        """Find all nodes of a specific type"""
        graph = retrieve_graph(request.graph_id)

        node_ids = (graph.query()
                        .by_type(request.node_type)
                        .nodes_ids())

        return Schema__Graph__Find_Nodes__Response(
            graph_id = request.graph_id,
            node_ids = list(node_ids),
            total_found = len(node_ids)
        )