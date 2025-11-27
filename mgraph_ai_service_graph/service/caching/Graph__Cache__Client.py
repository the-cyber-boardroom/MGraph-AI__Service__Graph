from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.schemas.cache.Schema__Cache__Store__Response            import Schema__Cache__Store__Response
from mgraph_ai_service_cache_client.schemas.cache.enums.Enum__Cache__Store__Strategy        import Enum__Cache__Store__Strategy
from mgraph_ai_service_cache_client.schemas.cache.file.Schema__Cache__File__Refs            import Schema__Cache__File__Refs
from mgraph_db.mgraph.MGraph                                                                import MGraph
from osbot_utils.decorators.methods.cache_on_self                                           import cache_on_self
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                              import type_safe
from mgraph_ai_service_graph.service.caching.Graph__Cache__Utils                            import Graph__Cache__Utils


class Graph__Cache__Client(Type_Safe):                                   # Wrapper around cache service for graph storage and retrieval
    cache_client   : Cache__Service__Fast_API__Client                       # Service__Fast_API__Client (avoiding import for now)

    @cache_on_self
    def cache_utils(self) -> Graph__Cache__Utils:
        return Graph__Cache__Utils(cache_client = self.cache_client)

    def store_graph(self,                                                                                   # Store graph in cache service
                    mgraph     : MGraph                     ,                                               # MGraph instance to store
                    namespace : Safe_Str__Id                                                                # Cache namespace for organization
                    ) -> Schema__Cache__Store__Response:                                                    # return details from stored cache entry
        graph_id = mgraph.graph.graph_id()
        graph_json = mgraph.json()                                                                          # Serialize graph to JSON using Type_Safe serialisation capabilities
        strategy = Enum__Cache__Store__Strategy.KEY_BASED                                                   # todo: refactor these values to a config value (or look at using the Cache_Decorator here)
        cache_key       = f'graphs/{graph_id}'
        file_id         = 'mgraph'
        json_field_path = 'graph.model.data.graph_id'                                                       # uses the graph_id to calculate the graph hash

        result = self.cache_client.store().store__json__cache_key(namespace       = namespace       ,       # Store using cache service
                                                                  strategy        = strategy        ,
                                                                  cache_key       = cache_key       ,
                                                                  file_id         = file_id         ,
                                                                  json_field_path = json_field_path ,
                                                                  body            = graph_json      )
        return result

    def retrieve_graph(self,                                            # Retrieve graph from cache service
                       cache_id  : Random_Guid         = None,          # Cache_id for graph to retrieve
                       graph_id  : Obj_Id              = None,          # Obj_id
                       namespace : Safe_Str__Id        = None           # Cache namespace to search in
                       ) -> MGraph:                                     # Deserialized MGraph instance
        mgraph_json = None
        if cache_id:
            mgraph_json = self.cache_client.retrieve().retrieve__cache_id__json(cache_id  = cache_id ,
                                                                                namespace = namespace)
        elif graph_id:
            cache_hash = self.cache_utils().graph_id__to__cache_hash(graph_id=graph_id)
            mgraph_json = self.cache_client.retrieve().retrieve__hash__cache_hash__json(cache_hash  = cache_hash,
                                                                                        namespace = namespace)
        if mgraph_json:
             return MGraph.from_json(mgraph_json)
        return None




    def delete_graph(self,                                               # Delete graph from cache service
                     cache_id  : Random_Guid  = None,                    # Cache_id for graph to delete
                     graph_id  : Obj_Id       = None,                    # Unique identifier of graph to delete
                     namespace : Safe_Str__Id = None                     # Cache namespace
                     ) -> bool:                                          # True if deleted successfully

        result = False
        if cache_id:
            result = self.cache_client.delete().delete__cache_id(cache_id  = cache_id ,
                                                                 namespace = namespace)
        elif graph_id:
            cache_id = self.cache_utils().graph_id__to__cache_id(graph_id=graph_id    ,
                                                                 namespace = namespace)
            result = self.cache_client.delete().delete__cache_id(cache_id  = cache_id ,
                                                                 namespace = namespace)
        return result

    def graph_exists(self,                                              # Check if graph exists in cache
                     cache_id  : Random_Guid  = None,                   # Cache_id for graph to retrieve
                     graph_id  : Obj_Id       = None,                   # Unique identifier to check
                     namespace : Safe_Str__Id = None,                   # Cache namespace
                ) -> bool:                                              # True if graph exists in cache
        result = False
        if cache_id:                                                                                                    # if we have the cache_id
            refs = self.cache_client.retrieve().retrieve__cache_id__refs(cache_id=cache_id, namespace=namespace)                # get the refs file | todo: BUG: we should be using the (to be added) exists__cache_id
            if refs:                                                                                                            # and see if it exists
                result = True
        elif graph_id:                                                                                                          # if we have the graph_id
            cache_hash    = self.cache_utils().graph_id__to__cache_hash(graph_id = graph_id )                                   # convert it to cache_hash
            exists_result = self.cache_client.exists().exists__hash__cache_hash(cache_hash=cache_hash, namespace=namespace)     #  and check of the cache_has exists
            result = exists_result.get('exists')

        return result

    @type_safe
    def cache_id__refs(self, cache_id : Random_Guid        ,
                       namespace: Safe_Str__Id) -> Schema__Cache__File__Refs:
        return self.cache_client.retrieve().retrieve__cache_id__refs(cache_id  = cache_id ,
                                                                     namespace = namespace)