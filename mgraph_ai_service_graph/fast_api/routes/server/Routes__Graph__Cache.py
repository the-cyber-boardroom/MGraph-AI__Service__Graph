from typing                                                                                 import List
from fastapi.params                                                                         import Path
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                                  import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client
from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from osbot_utils.decorators.methods.cache_on_self                                           import cache_on_self
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Namespace      import Safe_Str__Namespace
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                              import type_safe

FAST_API__PARAM__NAMESPACE = Path(..., example=GRAPH_REF__DEFAULT_NAMESPACE      )

TAG__ROUTES_GRAPH_CACHE    = 'cache'
PREFIX__ROUTES_GRAPH_CACHE = '/{namespace}'
ROUTES_PATHS__GRAPH_CACHE  = [ PREFIX__ROUTES_GRAPH_CACHE + '/cache-ids']


class Routes__Graph__Cache(Fast_API__Routes):
    tag          = TAG__ROUTES_GRAPH_CACHE
    prefix       = PREFIX__ROUTES_GRAPH_CACHE
    cache_client : Cache__Service__Fast_API__Client

    # ═══════════════════════════════════════════════════════════════════════════════
    # Core objects
    # ═══════════════════════════════════════════════════════════════════════════════


    @cache_on_self
    def graph_cache_client(self):
        return Graph__Cache__Client(cache_client=self.cache_client)

    @cache_on_self
    def cache_utils(self):
        return self.graph_cache_client().cache_utils()


    # ═══════════════════════════════════════════════════════════════════════════════
    # Routes methods
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def cache_ids(self, namespace: Safe_Str__Namespace = FAST_API__PARAM__NAMESPACE ) -> List[Cache_Id]:
        return self.cache_utils().cache_ids(namespace=Safe_Str__Id(namespace))

    def cache_hashes(self, namespace: Safe_Str__Namespace = FAST_API__PARAM__NAMESPACE ):
        return self.cache_utils().cache_hashes(namespace=Safe_Str__Id(namespace))

    def setup_routes(self):
        self.add_route_get(self.cache_ids)