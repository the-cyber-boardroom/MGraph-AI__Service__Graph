from typing                                                                         import Tuple
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                  import Cache_Id
from mgraph_db.mgraph.MGraph                                                        import MGraph
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from mgraph_ai_service_graph.exceptions.Graph__Ref__Not_Found__Error                import Graph__Ref__Not_Found__Error
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                   import Schema__Graph__Ref
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                   import Graph__Cache__Client


class Graph__Ref__Resolver(Type_Safe):                                              # Centralized resolution of Schema__Graph__Ref to MGraph. This is the ONLY place that understands graph_ref semantics

    graph_cache_client: Graph__Cache__Client                                        # Cache client for storage operations

    def resolve(self,                                                               # Resolve a graph_ref to an MGraph instance
                graph_ref: Schema__Graph__Ref                                       # The reference to resolve
           ) -> Tuple[MGraph, Schema__Graph__Ref]:                                  # Returns (mgraph, resolved_ref with cache_id)

        #self._validate_ref(graph_ref)                                              # removed, since this was causing too many side effects, Step 1: Validate - raise if both cache_id and graph_id provided

        if graph_ref.cache_id:                                                      # (cache_id will take precedence in resolving the graph) Step 2a: Resolve by cache_id (most efficient)
            mgraph = self._resolve_by_cache_id(graph_ref)
            cache_id = graph_ref.cache_id
        elif graph_ref.graph_id:                                                    # Step 2b: Resolve by graph_id
            mgraph, cache_id = self._resolve_by_graph_id(graph_ref)
        else:                                                                       # Step 2c: Create new graph
            mgraph, cache_id = self._create_new_graph(graph_ref)

        resolved_ref = self._build_resolved_ref(cache_id  = cache_id               ,     # Step 3: Build resolved ref (always has cache_id)
                                                graph_id  = mgraph.graph.graph_id(),
                                                namespace = graph_ref.namespace    )
        return mgraph, resolved_ref

    # note : this was removed, since although it makes sense to only want one of these values (graph_id or cache_id)
    #        in practice this would require the caller to always have to remove the graph_id from the graph_ref received from the previous call
    # def _validate_ref(self,                                                         # Validate graph_ref - raise if conflicting identifiers
    #                   graph_ref: Schema__Graph__Ref
    #                  ) -> None:
    #
    #     if graph_ref.cache_id and graph_ref.graph_id:
    #         raise Graph__Ref__Conflict__Error(
    #             details = dict(cache_id  = graph_ref.cache_id  ,
    #                            graph_id  = graph_ref.graph_id  ,
    #                            namespace = graph_ref.namespace))

    def _resolve_by_cache_id(self,                                                  # Retrieve graph directly by cache_id
                             graph_ref: Schema__Graph__Ref
                        ) -> MGraph:

        mgraph = self.graph_cache_client.retrieve_graph(cache_id  = graph_ref.cache_id ,
                                                        namespace = graph_ref.namespace)
        if mgraph is None:
            raise Graph__Ref__Not_Found__Error(
                message = f'Graph not found for cache_id: {graph_ref.cache_id}',
                details = dict(cache_id  = graph_ref.cache_id  ,
                               namespace = graph_ref.namespace))
        return mgraph

    def _resolve_by_graph_id(self,                                                  # Retrieve graph by graph_id (via cache hash lookup)
                             graph_ref: Schema__Graph__Ref
                    ) -> Tuple[MGraph, Cache_Id]:

        mgraph = self.graph_cache_client.retrieve_graph(graph_id  = graph_ref.graph_id ,
                                                        namespace = graph_ref.namespace)
        if mgraph is None:
            raise Graph__Ref__Not_Found__Error(
                message = f'Graph not found for graph_id: {graph_ref.graph_id}',
                details = dict(graph_id  = graph_ref.graph_id  ,
                               namespace = graph_ref.namespace))

        cache_id = self.graph_cache_client.cache_utils().graph_id__to__cache_id(    # Get the cache_id for the resolved ref
                        graph_id  = graph_ref.graph_id ,
                        namespace = graph_ref.namespace)

        return mgraph, cache_id

    def _create_new_graph(self,                                                     # Create a new graph and cache it
                          graph_ref: Schema__Graph__Ref
                     ) -> Tuple[MGraph, Cache_Id]:

        mgraph       = MGraph()                                                     # Create new empty graph
        store_result = self.graph_cache_client.store_graph(mgraph    = mgraph          ,    # Store in cache
                                                           namespace = graph_ref.namespace)
        cache_id     = store_result.cache_id
        return (mgraph, cache_id)

    def _build_resolved_ref(self,                                                   # Build a resolved graph_ref with cache_id populated
                            cache_id  : str,
                            graph_id  : str,
                            namespace : str
                       ) -> Schema__Graph__Ref:

        return Schema__Graph__Ref(cache_id  = cache_id ,
                                  graph_id  = graph_id ,
                                  namespace = namespace)

    def save_graph(self,                                                            # Save graph back to cache (for after modifications)
                   mgraph    : MGraph           ,
                   graph_ref : Schema__Graph__Ref
              ) -> Schema__Graph__Ref:

        if graph_ref.cache_id:                                                      # Update existing cache entry
            self.graph_cache_client.update_graph(mgraph    = mgraph             ,
                                                 cache_id  = graph_ref.cache_id ,
                                                 namespace = graph_ref.namespace)
            return graph_ref
        else:                                                                       # Store as new entry (shouldn't happen after resolve, but safe)
            store_result = self.graph_cache_client.store_graph(mgraph    = mgraph             ,
                                                               namespace = graph_ref.namespace)
            return Schema__Graph__Ref(cache_id  = store_result.cache_id        ,
                                      graph_id  = mgraph.graph.graph_id()      ,
                                      namespace = graph_ref.namespace          )