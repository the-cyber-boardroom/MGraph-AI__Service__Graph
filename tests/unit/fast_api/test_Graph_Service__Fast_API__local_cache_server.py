from unittest                                                                                                   import TestCase
from fastapi                                                                                                    import FastAPI
from osbot_utils.testing.Pytest import skip_if_in_github_action

from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Server import Routes__Graph__Server
from mgraph_db.mgraph.MGraph                                                                                    import MGraph
from starlette.testclient                                                                                       import TestClient
from mgraph_ai_service_cache_client.utils.Version                                                               import version__mgraph_ai_service_cache_client
from mgraph_ai_service_cache.fast_api.Cache_Service__Fast_API                                                   import Cache_Service__Fast_API
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                                import Obj_Id
from mgraph_ai_service_cache_client.schemas.cache.Schema__Cache__Retrieve__Success                              import Schema__Cache__Retrieve__Success
from mgraph_ai_service_cache_client.client.client_contract.retrieve.Service__Fast_API__Client__File__Retrieve   import Service__Fast_API__Client__File__Retrieve
from mgraph_ai_service_cache_client.client.client_contract.namespaces.Service__Fast_API__Client__Namespace      import Service__Fast_API__Client__Namespaces
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client__Config             import Cache__Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client                     import Cache__Service__Fast_API__Client
from osbot_fast_api.api.routes.Routes__Set_Cookie                                                               import Routes__Set_Cookie
from osbot_fast_api.utils.Fast_API_Server                                                                       import Fast_API_Server
from osbot_fast_api_serverless.fast_api.routes.Routes__Info                                                     import Routes__Info
from osbot_utils.testing.Temp_Env_Vars                                                                          import Temp_Env_Vars
from osbot_utils.testing.__                                                                                     import __, __SKIP__
from osbot_utils.utils.Misc                                                                                     import random_text
from mgraph_ai_service_graph.fast_api.Graph_Service__Fast_API                                                   import Graph_Service__Fast_API
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Batch                                               import Routes__Graph__Batch
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__CRUD                                                import Routes__Graph__CRUD, TAG__ROUTES_GRAPH_CRUD
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Edit                                                import Routes__Graph__Edit
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Query                                               import Routes__Graph__Query
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request                                  import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response                                 import Schema__Graph__Create__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                                    import Area__Graph__CRUD
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                                               import Graph__Cache__Client
from mgraph_ai_service_graph.service.graph.Graph__Service                                                       import Graph__Service
from mgraph_ai_service_graph.utils.Version                                                                      import version__mgraph_ai_service_graph


class test_Graph_Service__Fast_API__local_cache_server(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_key_name            = random_text("api_key_name" , lowercase=True)
        cls.api_key_value           = random_text("api_key_value", lowercase=True)
        cls.env_vars__cache_service = dict(FAST_API__AUTH__API_KEY__NAME                 =  cls.api_key_name    ,
                                           FAST_API__AUTH__API_KEY__VALUE                =  cls.api_key_value   )
        cls.auth_headers            = { cls.api_key_name: cls.api_key_value }

        # setup temp cache service running on ephemeral Fast_API
        with Temp_Env_Vars(env_vars=cls.env_vars__cache_service):
            cls.cache_service__fast_api = Cache_Service__Fast_API().setup()
            cls.cache_service__app      = cls.cache_service__fast_api.app()
            cls.fast_api_server         = Fast_API_Server(app=cls.cache_service__app)
            cls.cache_server_url        = cls.fast_api_server.url()
            cls.fast_api_server.start()

            cls.graph_service = Graph_Service__Fast_API().setup()

        cls.env_vars__cache_client = dict(AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME  = cls.api_key_name     ,
                                          AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE = cls.api_key_value    ,
                                          URL__TARGET_SERVER__CACHE_SERVICE             = cls.cache_server_url ,
                                          **cls.env_vars__cache_service                                        )



    @classmethod
    def tearDownClass(cls):
        cls.fast_api_server.stop()

    def test__setUpClass(self):
        assert self.fast_api_server.running is True
        assert self.fast_api_server.requests_get('/info/health', headers=self.auth_headers).status_code == 200

    def test__graph_service__cache_server_setup(self):
        skip_if_in_github_action()                      # todo: figure out why we get an error in: "assert {'detail': 'Not Found'} == ['an-namespace_A3ZJKQFMLSE0']"
        with self.graph_service as _:
            assert type(_) is Graph_Service__Fast_API
            assert _.obj() == __(config         = __(enable_cors=True,
                                                     enable_api_key=True,
                                                     default_routes=False,
                                                     base_path='/',
                                                     add_admin_ui=False,
                                                     docs_offline=True,
                                                     name='Graph_Service__Fast_API',
                                                     version=version__mgraph_ai_service_graph,
                                                     description=None,
                                                     title='MGraph-AI Service Graph'),
                                 server_id      = __SKIP__,
                                 routes_classes = __SKIP__)
            assert type(_.app()) is FastAPI

            assert _.routes_classes.keys()       == [Routes__Info        ,
                                                     Routes__Set_Cookie  ,
                                                     Routes__Graph__CRUD ,
                                                     Routes__Graph__Edit ,
                                                     Routes__Graph__Query,
                                                     Routes__Graph__Batch,
                                                     Routes__Graph__Server ,]
            assert _.routes_classes.keys().obj() == [ 'osbot_fast_api_serverless.fast_api.routes.Routes__Info.Routes__Info',
                                                      'osbot_fast_api.api.routes.Routes__Set_Cookie.Routes__Set_Cookie',
                                                      'mgraph_ai_service_graph.fast_api.routes.Routes__Graph__CRUD.Routes__Graph__CRUD',
                                                      'mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Edit.Routes__Graph__Edit',
                                                      'mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Query.Routes__Graph__Query',
                                                      'mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Batch.Routes__Graph__Batch',
                                                      'mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Server.Routes__Graph__Server']

            routes_graph_crud = _.routes_classes[Routes__Graph__CRUD]
            assert type(routes_graph_crud                                           ) == Routes__Graph__CRUD
            assert type(routes_graph_crud.area_crud                                 ) == Area__Graph__CRUD
            assert type(routes_graph_crud.area_crud.graph_service                   ) == Graph__Service
            assert type(routes_graph_crud.area_crud.graph_service.graph_cache_client) == Graph__Cache__Client
            assert routes_graph_crud.tag                                              == TAG__ROUTES_GRAPH_CRUD == 'graph-crud'
            assert _.routes_instance(Routes__Graph__CRUD)                             == routes_graph_crud

            graph_cache_client = routes_graph_crud.area_crud.graph_service.graph_cache_client

            assert type(graph_cache_client.cache_client       ) is Cache__Service__Fast_API__Client
            assert type(graph_cache_client.cache_client.config) is Cache__Service__Fast_API__Client__Config
            assert graph_cache_client.cache_client.config.obj() == __( base_url         = None          ,    # ok, since we have not executed any request
                                                                       api_key          = None          ,    # ok, since we have not executed any request
                                                                       api_key_header   = None          ,    # ok, since we have not executed any request
                                                                       mode             = 'in_memory'   ,    # ok, since we have not executed any request
                                                                       fast_api_app     = None          ,
                                                                       timeout          = 30            ,
                                                                       service_name     = 'Cache__Service__Fast_API',
                                                                       service_version  = version__mgraph_ai_service_cache_client)

        # cls.env_vars__cache_service = dict(FAST_API__AUTH__API_KEY__NAME                 =  cls.api_key_name    ,
        #                                    FAST_API__AUTH__API_KEY__VALUE                =  cls.api_key_value   )

        with Temp_Env_Vars(env_vars=self.env_vars__cache_client):
            graph_name = random_text('an-graph')
            namespace  = random_text('an-namespace')
            with self.graph_service.client() as _:
                assert type(_) is TestClient
                create_request = Schema__Graph__Create__Request(graph_name = graph_name,
                                                                namespace  = namespace )
                post_data      = create_request.json()
                response = _.post(url     = '/graph-crud/create',
                                  headers = self.auth_headers   ,
                                  json    = post_data           )
                create_response = Schema__Graph__Create__Response.from_json(response.json())
                cache_id        = create_response.cache_id
                graph_id        = create_response.graph_id
                assert response.status_code  == 200
                assert create_response.obj() == __(cache_id        = cache_id ,
                                                   cache_namespace = namespace,
                                                   graph_id        = graph_id ,
                                                   cached          = True     )

            assert graph_cache_client.cache_client.config.obj() == __( base_url         = self.cache_server_url,                    # after the first request these values should be set correctly
                                                                       api_key          = self.api_key_value   ,
                                                                       api_key_header   = self.api_key_name    ,
                                                                       mode             = 'remote'             ,
                                                                       fast_api_app     = None                 ,
                                                                       timeout          = 30                   ,
                                                                       service_name     = 'Cache__Service__Fast_API',
                                                                       service_version  = version__mgraph_ai_service_cache_client)

        with graph_cache_client.cache_client as _:                                          # check the data via an HTTP call to the local cache client
            assert type(_)              is Cache__Service__Fast_API__Client
            assert type(_.namespaces()) is Service__Fast_API__Client__Namespaces
            assert type(_.retrieve  ()) is Service__Fast_API__Client__File__Retrieve
            assert _.namespaces().list() == [namespace]

            retrieve                                 = _.retrieve().retrieve__cache_id(cache_id= cache_id, namespace= namespace)
            default_mgraph                           = MGraph()
            default_mgraph.graph.model.data.graph_id = Obj_Id(graph_id)
            expected_retrieve_data                   = __( data    = default_mgraph.obj(),
                                                                 metadata = __(cache_id         = cache_id,
                                                                               cache_hash       = __SKIP__,
                                                                               cache_key        = __SKIP__,
                                                                               file_id          = 'mgraph',
                                                                               namespace        = namespace,
                                                                               strategy         = 'key_based',
                                                                               stored_at        = __SKIP__,
                                                                               file_type        = 'json',
                                                                               content_encoding = None,
                                                                               content_size     = 0),
                                                                 data_type='json')
            assert type(retrieve)       is Schema__Cache__Retrieve__Success
            assert retrieve.obj()       == expected_retrieve_data


        with self.cache_service__fast_api as _:                                                 # test by going directly to the cache service :)
            assert type(_) is Cache_Service__Fast_API
            path = f"/{namespace}/retrieve/{cache_id}"
            response = _.client().get(url     = path              ,
                                      headers = self.auth_headers)

            assert response.status_code == 200
            retrieve_success = Schema__Cache__Retrieve__Success.from_json(response.json())
            assert retrieve_success.json() == response.json()
            assert retrieve_success.obj () == expected_retrieve_data

