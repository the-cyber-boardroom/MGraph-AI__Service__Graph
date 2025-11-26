from mgraph_db.mgraph.MGraph                                                                import MGraph
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                           import Safe_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Namespace      import Safe_Str__Namespace
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash    import Safe_Str__Cache_Hash
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client


class Graph__Service(Type_Safe):                                            # Main orchestration service for graph operations

    cache_client: Graph__Cache__Client                                      # Injected cache client for storage and retrieval

    def create_new_graph(self                                               # Create a new empty MGraph instance
                    ) -> MGraph:                                            # Freshly initialized MGraph with no nodes or edges
        return MGraph()

    def get_or_create_graph(self,                                           # Retrieve existing graph from cache or create new one if not found
                            graph_id  : Safe_Id             ,               # Unique identifier for graph
                            namespace : Safe_Str__Namespace = "graphs"      # Cache namespace to search
                       ) -> MGraph:                                         # Existing graph from cache, or new empty graph

        mgraph = self.cache_client.retrieve_graph(graph_id, namespace)
        if mgraph is None:
            mgraph = self.create_new_graph()

        return mgraph

    def save_graph(self,                                               # Persist graph to cache service
                   graph     : MGraph              ,                   # MGraph instance to save
                   namespace : Safe_Str__Namespace = "graphs"          # Cache namespace for organization
              ) -> Safe_Str__Cache_Hash:                               # Cache hash identifying stored graph

        return self.cache_client.store_graph(graph, namespace)

    def delete_graph(self,                                             # Delete graph from cache
                     graph_id  : Safe_Id             ,                 # Unique identifier of graph to delete
                     namespace : Safe_Str__Namespace = "graphs"        # Cache namespace
                ) -> bool:                                             # True if deleted successfully

        return self.cache_client.delete_graph(graph_id, namespace)

    def graph_exists(self,                                             # Check if graph exists in cache
                     graph_id  : Safe_Id             ,                 # Unique identifier to check
                     namespace : Safe_Str__Namespace = "graphs"        # Cache namespace
                ) -> bool:                                             # True if graph exists

        return self.cache_client.graph_exists(graph_id, namespace)
