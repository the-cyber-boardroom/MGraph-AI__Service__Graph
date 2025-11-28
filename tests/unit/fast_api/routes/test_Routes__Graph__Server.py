from unittest                                                       import TestCase
from fastapi                                                        import FastAPI
from mgraph_ai_service_cache.utils.Version                          import version__mgraph_ai_service_cache
from mgraph_ai_service_cache_client.utils.Version                   import version__mgraph_ai_service_cache_client
from osbot_utils.testing.__                                         import __
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Server  import Routes__Graph__Server, ROUTES_PATHS__GRAPH_SERVER, Schema__Graph__Server__Config__Response
from mgraph_ai_service_graph.utils.Version                          import version__mgraph_ai_service_graph


class test_Routes__Graph__Server(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app          = FastAPI()
        cls.graph_server = Routes__Graph__Server(app=cls.app).setup()

    def test_setup(self):
        with self.graph_server as _:
            assert type(_) is Routes__Graph__Server
            assert _.routes_paths() == ['/config']

    def test_config(self):
        with self.graph_server as _:
            result = _.config()
            assert type(result) is Schema__Graph__Server__Config__Response
            assert result.obj() == __(graph_service__version         = version__mgraph_ai_service_graph       ,
                                      cache_service__client__version = version__mgraph_ai_service_cache_client,
                                      cache_service__base_url        = ''                                     ,
                                      cache_service__api_key_header  = ''                                     ,
                                      cache_service__mode            = 'in_memory'                            )
