from typing                                                                                 import List
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Graph_Id                                     import Graph_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Namespace      import Safe_Str__Namespace
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                              import type_safe
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client import Cache__Service__Fast_API__Client
from osbot_utils.helpers.cache.Cache__Hash__Generator                                       import Cache__Hash__Generator
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash    import Safe_Str__Cache_Hash
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id


class Graph__Cache__Utils(Type_Safe):
    cache_client   : Cache__Service__Fast_API__Client
    hash_generator : Cache__Hash__Generator

    def cache_ids(self, namespace: Safe_Str__Id):                           # todo : look at refactoring all the name space Safe_Str__Id with Cache__Namespace
        return self.cache_client.namespace().cache_ids(namespace=namespace)

    def cache_hashes(self, namespace: Safe_Str__Namespace):
        return self.cache_client.namespace().cache_hashes(namespace=Safe_Str__Id(namespace))
    @type_safe
    def graph_id__to__cache_id(self, graph_id : Graph_Id     ,
                                     namespace : Safe_Str__Id
                                ) -> Safe_Str__Id:
        cache_hash      = self.graph_id__to__cache_hash(graph_id=graph_id)
        cache_id_result = self.cache_client.retrieve().retrieve__hash__cache_hash__cache_id(cache_hash = cache_hash,
                                                                                            namespace  = namespace )
        if cache_id_result:
            return cache_id_result.get('cache_id')
        return None

    @type_safe
    def graph_id__to__cache_hash(self,
                                 graph_id : Graph_Id   ,
                            ) -> Safe_Str__Cache_Hash:
        if graph_id:
            return self.hash_generator.from_string(graph_id)        # todo: hash_generator.from_string should handle None values
        return None

    @type_safe
    def graph_ref__to__cache_hash(self, graph_ref: Schema__Graph__Ref):
        return self.graph_id__to__cache_hash(graph_id=graph_ref.graph_id)

    @type_safe
    def namespace__cache_hashes(self, namespace: Safe_Str__Id):
        return self.cache_client.namespace().cache_hashes(namespace=namespace)

    @type_safe
    def namespace__cache_ids(self, namespace: Safe_Str__Id) -> List[Cache_Id]:
        return self.cache_client.namespace().cache_ids(namespace=namespace)

    @type_safe
    def namespaces(self):
        return self.cache_client.namespaces().list()