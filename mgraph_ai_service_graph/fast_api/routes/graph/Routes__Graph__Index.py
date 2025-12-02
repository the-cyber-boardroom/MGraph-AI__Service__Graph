from osbot_fast_api.api.routes.Fast_API__Routes                                                 import Fast_API__Routes
from osbot_fast_api.api.schemas.safe_str.Safe_Str__Fast_API__Route__Tag                         import Safe_Str__Fast_API__Route__Tag
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                               import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Request            import Schema__Graph__Index__Full__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Response           import Schema__Graph__Index__Full__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Node_Edges               import Schema__Graph__Index__Node_Edges__Request, Schema__Graph__Index__Node_Edges__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__By_Predicate             import Schema__Graph__Index__By_Predicate__Request, Schema__Graph__Index__By_Predicate__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Value_Lookup             import Schema__Graph__Index__Value_Lookup__Request, Schema__Graph__Index__Value_Lookup__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Stats                    import Schema__Graph__Index__Stats__Request, Schema__Graph__Index__Stats__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__ReIndex                  import Schema__Graph__Index__ReIndex__Request, Schema__Graph__Index__ReIndex__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__Index                                   import Area__Graph__Index


TAG__ROUTES_GRAPH_INDEX   = 'graph-index'
ROUTES_PATHS__GRAPH_INDEX = [ '/graph-index/full'           ,
                              '/graph-index/node-edges'     ,
                              '/graph-index/by-predicate'   ,
                              '/graph-index/value-lookup'   ,
                              '/graph-index/stats'          ,
                              '/graph-index/re-index'       ,
                              '/graph-index/cache'          ]


class Routes__Graph__Index(Fast_API__Routes):                                   # Graph index routes - expose index operations
    tag        : Safe_Str__Fast_API__Route__Tag = TAG__ROUTES_GRAPH_INDEX       # FastAPI route tag
    area_index : Area__Graph__Index                                             # Index operations area

    # ═══════════════════════════════════════════════════════════════════════════════
    # Full Index Retrieval
    # ═══════════════════════════════════════════════════════════════════════════════

    def full(self,                                                              # Get complete index for a graph
             request: Schema__Graph__Index__Full__Request
            ) -> Schema__Graph__Index__Full__Response:
        return self.area_index.get_full_index(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Node Edges Lookup
    # ═══════════════════════════════════════════════════════════════════════════════

    def node_edges(self,                                                        # Get edges for a specific node
                   request: Schema__Graph__Index__Node_Edges__Request
                  ) -> Schema__Graph__Index__Node_Edges__Response:
        return self.area_index.get_node_edges(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Predicate-Based Lookup
    # ═══════════════════════════════════════════════════════════════════════════════

    def by_predicate(self,                                                      # Find nodes by predicate relationship
                     request: Schema__Graph__Index__By_Predicate__Request
                    ) -> Schema__Graph__Index__By_Predicate__Response:
        return self.area_index.get_by_predicate(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Lookup
    # ═══════════════════════════════════════════════════════════════════════════════

    def value_lookup(self,                                                      # Lookup value node by value or hash
                     request: Schema__Graph__Index__Value_Lookup__Request
                    ) -> Schema__Graph__Index__Value_Lookup__Response:
        return self.area_index.value_lookup(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Index Statistics
    # ═══════════════════════════════════════════════════════════════════════════════

    def stats(self,                                                             # Get index statistics
              request: Schema__Graph__Index__Stats__Request
             ) -> Schema__Graph__Index__Stats__Response:
        return self.area_index.get_stats(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Re-Index
    # ═══════════════════════════════════════════════════════════════════════════════

    def re_index(self,                                                          # Force rebuild and cache index
                 request: Schema__Graph__Index__ReIndex__Request
                ) -> Schema__Graph__Index__ReIndex__Response:
        return self.area_index.re_index(request)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Cache Index
    # ═══════════════════════════════════════════════════════════════════════════════

    def cache(self,                                                             # Cache current index for a graph
              graph_ref: Schema__Graph__Ref
             ) -> dict:
        success = self.area_index.cache_index(graph_ref)
        return {"graph_ref": graph_ref.json(), "index_cached": success}

    # ═══════════════════════════════════════════════════════════════════════════════
    # Route Setup
    # ═══════════════════════════════════════════════════════════════════════════════

    def setup_routes(self):
        self.add_route_post(self.full        )
        self.add_route_post(self.node_edges  )
        self.add_route_post(self.by_predicate)
        self.add_route_post(self.value_lookup)
        self.add_route_post(self.stats       )
        self.add_route_post(self.re_index    )
        self.add_route_post(self.cache       )
        return self
