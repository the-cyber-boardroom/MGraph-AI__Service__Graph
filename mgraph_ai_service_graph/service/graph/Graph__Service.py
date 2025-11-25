class Graph__Service(Type_Safe):
    """Main orchestration service for graph operations"""

    cache_client: Graph__Cache__Client

    def create_new_graph(self) -> MGraph:
        """Create a new empty MGraph"""
        return MGraph()

    def get_or_create_graph(self, graph_id  : Safe_Id,
                                  namespace : Safe_Str__Namespace = "graphs"
                           ) -> MGraph:
        """Retrieve existing graph or create new one"""
        try:
            return self.cache_client.retrieve_graph(graph_id, namespace)
        except:
            return self.create_new_graph()

    def save_graph(self, graph_id  : Safe_Id,
                         graph     : MGraph,
                         namespace : Safe_Str__Namespace = "graphs"
                  ) -> Safe_Str__Cache_Hash:
        """Save graph to cache"""
        return self.cache_client.store_graph(graph_id, graph, namespace)
