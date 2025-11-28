from unittest                                                                            import TestCase

from osbot_fast_api.api.Fast_API import Fast_API
from osbot_fast_api.api.routes.Routes__Set_Cookie                                        import Routes__Set_Cookie
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API                             import Serverless__Fast_API
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_graph.config                                                      import FAST_API__TITLE
from mgraph_ai_service_graph.fast_api.Graph_Service__Fast_API                            import Graph_Service__Fast_API
from mgraph_ai_service_graph.utils.Version                                               import version__mgraph_ai_service_graph


class test_Graph_Service__Fast_API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fast_api = Graph_Service__Fast_API()

    def test__init__(self):                                                              # Test initialization
        with Graph_Service__Fast_API() as _:
            assert type(_)         is Graph_Service__Fast_API
            assert base_classes(_) == [Serverless__Fast_API, Fast_API, Type_Safe, object]

    def test_setup(self):                                                                # Test FastAPI setup
        with Graph_Service__Fast_API() as _:
            result = _.setup()

            assert result           is _                                                 # Returns self for chaining
            assert _.config.title   == FAST_API__TITLE
            assert _.config.version == version__mgraph_ai_service_graph

    def test_app(self):                                                                  # Test FastAPI app creation
        with Graph_Service__Fast_API() as _:
            _.setup()
            app = _.app()

            assert app              is not None
            assert app.title        == 'Graph_Service__Fast_API' #FAST_API__TITLE
            assert app.version      == version__mgraph_ai_service_graph

    def test_client(self):                                                               # Test TestClient creation
        with Graph_Service__Fast_API() as _:
            _.setup()
            client = _.client()

            assert client is not None

            # Test client can make requests
            response = client.get('/info/health')
            assert response.status_code in [200, 401]                                    # 401 if auth enabled

    def test_handler(self):                                                              # Test Lambda handler creation
        with Graph_Service__Fast_API() as _:
            _.setup()
            handler = _.handler()

            assert handler          is not None
            assert callable(handler)