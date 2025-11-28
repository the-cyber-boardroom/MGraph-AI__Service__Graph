
from mgraph_ai_service_cache_client.client.requests.schemas.enums.Enum__Client__Mode        import Enum__Client__Mode
from osbot_fast_api.api.schemas.safe_str.Safe_Str__Fast_API__Route__Tag                     import Safe_Str__Fast_API__Route__Tag
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Header__Name    import Safe_Str__Http__Header__Name
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url                    import Safe_Str__Url
from mgraph_ai_service_cache_client.utils.Version                                           import version__mgraph_ai_service_cache_client
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client import Cache__Service__Fast_API__Client
from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version             import Safe_Str__Version
from mgraph_ai_service_graph.utils.Version                                                  import version__mgraph_ai_service_graph

TAG__ROUTES_GRAPH_SERVER   = 'graph/server'
ROUTES_PATHS__GRAPH_SERVER = [ '/graph/server/config']

class Schema__Graph__Server__Config__Response(Type_Safe):
    graph_service__version          : Safe_Str__Version
    cache_service__client__version  : Safe_Str__Version
    cache_service__base_url         : Safe_Str__Url
    cache_service__api_key_header   : Safe_Str__Http__Header__Name
    cache_service__mode             : Enum__Client__Mode


class Routes__Graph__Server(Fast_API__Routes):
    tag                    : Safe_Str__Fast_API__Route__Tag  = TAG__ROUTES_GRAPH_SERVER
    graph_service__version : Cache__Service__Fast_API__Client

    def config(self) -> Schema__Graph__Server__Config__Response:
        self.graph_service__version.requests()                      # will trigger the server config
        with self.graph_service__version.config as _:
            kwargs = dict(graph_service__version         = version__mgraph_ai_service_graph       ,
                          cache_service__client__version = version__mgraph_ai_service_cache_client,
                          cache_service__base_url        = _.base_url                             ,
                          cache_service__api_key_header  = _.api_key_header                       ,
                          cache_service__mode            = _.mode                                 )

        return Schema__Graph__Server__Config__Response(**kwargs)

    def setup_routes(self):
        self.add_route_get(self.config)