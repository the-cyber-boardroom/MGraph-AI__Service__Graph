from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response             import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request                 import Schema__Graph__Get__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response                import Schema__Graph__Get__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service



class Area__Graph__CRUD(Type_Safe):                                         # Graph CRUD operations area - handles create, read, update, delete
                                                                            # This area provides the fundamental graph lifecycle operations with
                                                                            # automatic cache integration.

    graph_service: Graph__Service                                           # Injected graph service dependency

    def create_graph(self,                                                  # Create a new empty graph with optional auto-caching
                     request: Schema__Graph__Create__Request                # Creation request with name, auto_cache flag, namespace
                    ) -> Schema__Graph__Create__Response:                   # Response with graph_id, counts, and cache status

        mgraph    = self.graph_service.create_new_graph()                   # Create new empty graph
        graph_id  = Random_Guid()

        cached    = False
        cache_id  = None

        if request.auto_cache:                                              # Handle caching if requested
            cache_hash = self.graph_service.save_graph(graph_id  = str(graph_id),
                                                        graph     = mgraph        ,
                                                        namespace = request.namespace)

            cached    = True
            cache_id  = Random_Guid(str(cache_hash))


        node_count = len(list(mgraph.nodes()))                              # Get actual counts from graph
        edge_count = len(list(mgraph.edges()))

        return Schema__Graph__Create__Response(graph_id   = graph_id  ,
                                               node_count = node_count,
                                               edge_count = edge_count,
                                               cached     = cached    ,
                                               cache_id   = cache_id  )

    def get_graph(self,                                                    # Retrieve a graph from cache
                  request: Schema__Graph__Get__Request                     # Get request with graph_id and namespace
                 ) -> Schema__Graph__Get__Response:                        # Response with graph metadata and status


        # Retrieve graph from cache
        mgraph = self.graph_service.cache_client.retrieve_graph(graph_id  = str(request.graph_id),
                                                                namespace = request.namespace)

        # Get counts
        node_count = len(list(mgraph.nodes()))
        edge_count = len(list(mgraph.edges()))

        return Schema__Graph__Get__Response(graph_id   = request.graph_id,
                                            node_count = node_count      ,
                                            edge_count = edge_count      ,
                                            cached     = True            ,
                                            cache_id   = request.graph_id)       # Using graph_id as cache_id

    def delete_graph(self,                                                  # Delete a graph from cache
                     graph_id  : Random_Guid             ,                  # Graph to delete
                     namespace : str         = "graphs"                     # Cache namespace
                    ) -> bool:                                              # True if deleted successfully

        return self.graph_service.delete_graph(graph_id  = str(graph_id),
                                               namespace = namespace    )

    def graph_exists(self,                                                  # Check if graph exists in cache
                     graph_id  : Random_Guid             ,                  # Graph to check
                     namespace : str         = "graphs"                     # Cache namespace
                    ) -> bool:                                              # True if exists

        return self.graph_service.graph_exists(graph_id  = str(graph_id),
                                               namespace = namespace    )
