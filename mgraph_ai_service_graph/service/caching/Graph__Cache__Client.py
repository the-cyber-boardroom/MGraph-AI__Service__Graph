from mgraph_ai_service_cache_client.Service__Fast_API__Client import Service__Fast_API__Client

class Graph__Cache__Client(Type_Safe):
    """Wrapper around cache service for graph storage"""

    cache_client: Service__Fast_API__Client

    def store_graph(self, graph_id  : Safe_Id       ,
                          graph     : MGraph        ,
                          namespace : Safe_Str__Namespace = "graphs"
                   ) -> Safe_Str__Cache_Hash:
        """Store graph in cache service"""

        # Serialize graph to JSON
        graph_json = graph.export().to_json()

        # Store using cache service
        result = self.cache_client.store().store__json(
            strategy  = "direct",
            namespace = namespace,
            body      = graph_json
        )

        return result.cache_hash

    def retrieve_graph(self, graph_id  : Safe_Id,
                             namespace : Safe_Str__Namespace = "graphs"
                      ) -> MGraph:
        """Retrieve graph from cache"""

        cache_key = f"graph:{graph_id}"

        result = self.cache_client.retrieve().retrieve__cache_id__json(
            cache_id  = cache_key,
            namespace = namespace
        )

        # Deserialize JSON → MGraph
        graph = MGraph()
        graph.import_from_json(result)

        return graph