from mgraph_db.mgraph.MGraph                                                                import MGraph
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                           import Safe_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Namespace      import Safe_Str__Namespace
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash    import Safe_Str__Cache_Hash


class Graph__Cache__Client(Type_Safe):                                   # Wrapper around cache service for graph storage and retrieval
    # todo: add cache_client class
    cache_client: object                                                 # Service__Fast_API__Client (avoiding import for now)

    def store_graph(self,                                                # Store graph in cache service
                    graph     : MGraph                     ,             # MGraph instance to store
                    namespace : Safe_Str__Namespace = "graphs"           # Cache namespace for organization
               ) -> Safe_Str__Cache_Hash:                                # Cache hash identifying stored graph

        graph_json = graph.json()                                       # Serialize graph to JSON using MGraph's export capabilities

        # Store using cache service
        result = self.cache_client.store().store__json(strategy  = "direct" ,
                                                       namespace = namespace ,
                                                       body      = graph_json)

        return result.cache_hash        # todo: review this return, since we should actually return more details,like the cache_id

    def retrieve_graph(self,                                             # Retrieve graph from cache service
                       graph_id  : Safe_Id                    ,          # Unique identifier of graph to retrieve
                       namespace : Safe_Str__Namespace = "graphs"        # Cache namespace to search in
                  ) -> MGraph:                                           # Deserialized MGraph instance

        cache_key = f"graph:{graph_id}"     # todo: this logic is wrong (since the cache_hash cannot be used as a cache_id)

        result = self.cache_client.retrieve().retrieve__cache_id__json(cache_id  = cache_key ,
                                                                       namespace = namespace)
        if result:
            # Deserialize JSON → MGraph
            graph = MGraph()
            graph.load_from_json(result)                                     # todo: this logic is wrong and we should

            return graph                                                     # todo: see if we should be returning an Domain__MGraph__Graph
        return None

    def delete_graph(self,                                               # Delete graph from cache service
                     graph_id  : Safe_Id                    ,            # Unique identifier of graph to delete
                     namespace : Safe_Str__Namespace = "graphs"          # Cache namespace
                ) -> bool:                                               # True if deleted successfully

        cache_key = f"graph:{graph_id}"

        return self.cache_client.delete().delete__cache_id(cache_id  = cache_key ,
                                                           namespace = namespace)

    def graph_exists(self,                                               # Check if graph exists in cache
                     graph_id  : Safe_Id                    ,            # Unique identifier to check
                     namespace : Safe_Str__Namespace = "graphs"          # Cache namespace
                ) -> bool:                                               # True if graph exists in cache

        cache_key = f"graph:{graph_id}"

        return self.cache_client.exists().exists__cache_id(cache_id  = cache_key ,
                                                           namespace = namespace)
