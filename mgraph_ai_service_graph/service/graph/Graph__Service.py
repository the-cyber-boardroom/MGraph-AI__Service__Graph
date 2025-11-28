from typing                                                                      import Dict

from mgraph_ai_service_graph.service.graph.Graph__Ref__Resolver                  import Graph__Ref__Resolver
from mgraph_db.mgraph.MGraph                                                     import MGraph
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                 import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid            import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id  import Safe_Str__Id
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                import Graph__Cache__Client
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                   import type_safe

# todo: rename all this from Graph to MGraph (including methods) , since we at this level we are dealing with MGraph objects
class Graph__Service(Type_Safe):                                            # Main orchestration service for graph operations

    graph_cache_client : Graph__Cache__Client                                      # Injected cache client for storage and retrieval
    graph_ref_resolver : Graph__Ref__Resolver = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)                                                                        # this will create a new instance of Graph__Ref__Resolver (if it has not been provided)
        self.graph_ref_resolver = Graph__Ref__Resolver(graph_cache_client = self.graph_cache_client)      # Initialize resolver with same cache client |  todo: see if there is a better way to do this (without needing to have this code in the __init_()


    def create_new_graph(self                                               # Create a new empty MGraph instance
                    ) -> MGraph:                                            # Freshly initialized MGraph with no nodes or edges
        return MGraph()

    def get_graph(self,                                                     # Retrieve existing graph from cache
                  cache_id  : Random_Guid  = None  ,                        # Graph Cache_Id
                  graph_id  : Obj_Id       = None  ,                        # Unique identifier for graph
                  namespace : Safe_Str__Id = None                           # Cache namespace to search
             ) -> MGraph:                                         # Existing graph from cache, or new empty graph

        mgraph = self.graph_cache_client.retrieve_graph(cache_id  =cache_id  ,
                                                        graph_id  = graph_id ,
                                                        namespace = namespace)
        return mgraph

    def get_or_create_graph(self,                                           # Retrieve existing graph from cache or create new one if not found
                            cache_id  : Random_Guid  = None ,
                            graph_id  : Obj_Id       = None ,               # Unique identifier for graph
                            namespace : Safe_Str__Id = None                 # Cache namespace to search
                       ) -> MGraph:                                         # Existing graph from cache, or new empty graph

        mgraph = self.graph_cache_client.retrieve_graph(graph_id=graph_id, cache_id=cache_id ,namespace=namespace)
        if mgraph is None:
            mgraph = self.create_new_graph()

        return mgraph

    @type_safe
    def save_graph(self,                                                # Persist graph to cache service
                   mgraph    : MGraph                    ,              # MGraph instance to save
                   namespace : Safe_Str__Id = "graphs"   ,              # Cache namespace for organization
                   cache_id  : Random_Guid  = None                      # Optional: existing cache_id to update
              ) -> Random_Guid:                                         # Cache id identifying stored graph

        if cache_id:                                                    # Update existing cache entry
            update_response = self.graph_cache_client.update_graph(mgraph    = mgraph   ,
                                                                   cache_id  = cache_id ,
                                                                   namespace = namespace)
            return update_response.cache_id
        else:                                                           # Create new cache entry
            store_response = self.graph_cache_client.store_graph(mgraph    = mgraph   ,
                                                                 namespace = namespace)
            return store_response.cache_id

    @type_safe
    def delete_graph(self,                                              # Delete graph from cache
                     cache_id  : Random_Guid  = None,                   # Cache_id for graph to delete
                     graph_id  : Obj_Id      = None,                    # Unique identifier of graph to delete
                     namespace : Safe_Str__Id = None                    # Cache namespace
                ) -> Dict:                                              # True if deleted successfully

        return self.graph_cache_client.delete_graph(cache_id  = cache_id ,
                                                    graph_id  = graph_id ,
                                                    namespace = namespace)           # todo: this needs to be a Type_Safe class (current bug in Cache-Client)

    def graph_exists(self,                                              # Check if graph exists in cache
                     cache_id  : Random_Guid  = None,                   # Cache_id for graph to retrieve
                     graph_id  : Obj_Id       = None,                   # Unique identifier to check
                     namespace : Safe_Str__Id = None                    # Cache namespace
                ) -> bool:                                              # True if graph exists

        return self.graph_cache_client.graph_exists(cache_id  = cache_id ,
                                                    graph_id  = graph_id ,
                                                    namespace = namespace)
