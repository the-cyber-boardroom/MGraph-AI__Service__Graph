from typing                                                                      import Dict
from mgraph_db.mgraph.MGraph                                                     import MGraph
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                 import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id  import Safe_Str__Id
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                       import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                import Schema__Graph__Ref
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                import Graph__Cache__Client
from mgraph_ai_service_graph.service.graph.Graph__Ref__Resolver                  import Graph__Ref__Resolver
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                   import type_safe

# todo: see if we should rename most references from mgraph to graph
class Graph__Service(Type_Safe):                                                # Main orchestration service for graph operations

    graph_cache_client : Graph__Cache__Client                                   # Injected cache client for storage and retrieval
    ref_resolver       : Graph__Ref__Resolver       = None                      # Centralized ref resolution

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.graph_cache_client and not self.ref_resolver:                   # Initialize resolver with same cache client
            self.ref_resolver = Graph__Ref__Resolver(graph_cache_client=self.graph_cache_client)

    def resolve_graph_ref(self,                                                 # Delegate to resolver - main entry point for all operations
                          graph_ref: Schema__Graph__Ref
                     ) -> tuple[MGraph, Schema__Graph__Ref]:
        return self.ref_resolver.resolve(graph_ref)

    def save_graph_ref(self,                                                    # Save graph and return updated ref
                       mgraph    : MGraph           ,
                       graph_ref : Schema__Graph__Ref
                  ) -> Schema__Graph__Ref:
        return self.ref_resolver.save_graph(mgraph=mgraph, graph_ref=graph_ref)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Legacy methods - kept for backward compatibility during migration
    # These should eventually be removed once all code uses graph_ref pattern
    # ═══════════════════════════════════════════════════════════════════════════════

    def create_new_graph(self) -> MGraph:                                       # Create a new empty MGraph instance
        return MGraph()

    def get_graph(self,                                                         # Retrieve existing graph from cache
                  cache_id  : Cache_Id      = None,
                  graph_id  : Obj_Id        = None,
                  namespace : Safe_Str__Id  = None
             ) -> MGraph:
        return self.graph_cache_client.retrieve_graph(cache_id  = cache_id ,
                                                      graph_id  = graph_id ,
                                                      namespace = namespace)

    def get_or_create_graph(self,                                               # Retrieve existing or create new
                            cache_id  : Cache_Id     = None,
                            graph_id  : Obj_Id       = None,
                            namespace : Safe_Str__Id = None
                       ) -> MGraph:
        mgraph = self.graph_cache_client.retrieve_graph(graph_id  = graph_id ,
                                                        cache_id  = cache_id ,
                                                        namespace = namespace)
        if mgraph is None:
            mgraph = self.create_new_graph()
        return mgraph

    @type_safe
    def save_graph(self,                                                        # Persist graph to cache service
                   mgraph    : MGraph                  ,
                   namespace : Safe_Str__Id = "graphs" ,
                   cache_id  : Cache_Id     = None
              ) -> Cache_Id:
        if cache_id:
            update_response = self.graph_cache_client.update_graph(mgraph    = mgraph   ,
                                                                   cache_id  = cache_id ,
                                                                   namespace = namespace)
            return update_response.cache_id
        else:
            store_response = self.graph_cache_client.store_graph(mgraph    = mgraph   ,
                                                                 namespace = namespace)
            return store_response.cache_id

    @type_safe
    def delete_graph(self,                                                      # Delete graph from cache
                     cache_id  : Cache_Id     = None,
                     graph_id  : Obj_Id       = None,
                     namespace : Safe_Str__Id = None
                ) -> Dict:
        return self.graph_cache_client.delete_graph(cache_id  = cache_id ,
                                                    graph_id  = graph_id ,
                                                    namespace = namespace)

    def graph_exists(self,                                                      # Check if graph exists in cache
                     cache_id  : Cache_Id     = None,
                     graph_id  : Obj_Id       = None,
                     namespace : Safe_Str__Id = None
                ) -> bool:
        return self.graph_cache_client.graph_exists(cache_id  = cache_id ,
                                                    graph_id  = graph_id ,
                                                    namespace = namespace)