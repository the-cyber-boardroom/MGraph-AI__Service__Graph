import inspect
from unittest                                                                                   import TestCase
from mgraph_ai_service_cache.service.cache.Cache__Service                                       import Cache__Service
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                           import Type_Safe__List
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client     import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.schemas.cache.file.Schema__Cache__File__Refs                import Schema__Cache__File__Refs
from mgraph_db.mgraph.MGraph                                                                    import MGraph
from osbot_utils.helpers.cache.Cache__Hash__Generator                                           import Cache__Hash__Generator
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                import is_obj_id
from osbot_utils.utils.Misc                                                                     import is_guid
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                               import Graph__Cache__Client
from osbot_utils.testing.__                                                                     import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.utils.Objects                                                                  import base_classes
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                    import Area__Graph__CRUD
from mgraph_ai_service_graph.service.caching.Graph__Cache__Utils                                import Graph__Cache__Utils
from mgraph_ai_service_graph.service.graph.Graph__Service                                       import Graph__Service
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request                  import Schema__Graph__Create__Request, NAMESPACE__DEFAULT__GRAPH__CREATE
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response                 import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request                     import Schema__Graph__Get__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response                    import Schema__Graph__Get__Response
from tests.unit.Graph__Service__Fast_API__Test_Objs                                             import client_cache_service


class test_Area__Graph__CRUD(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client, cls.cache_service = client_cache_service()
        cls.graph_cache_client = Graph__Cache__Client(cache_client =  cls.cache_client )
        cls.graph_cache_utils  = Graph__Cache__Utils (cache_client =  cls.cache_client )
        cls.graph_service      = Graph__Service      (graph_cache_client  = cls.graph_cache_client )
        cls.area_crud          = Area__Graph__CRUD   (graph_service = cls.graph_service)
        cls.hash_generator     = Cache__Hash__Generator()

    def test__init__(self):                                                              # Test auto-initialization
        with Area__Graph__CRUD() as _:
            assert type(_)               is Area__Graph__CRUD
            assert base_classes(_)       == [Type_Safe, object]
            assert type(_.graph_service) is Graph__Service

    def test__graph_service_dependency(self):                                            # Test graph service is injected
        with Area__Graph__CRUD() as _:
            assert _.graph_service is not None
            assert type(_.graph_service) is Graph__Service

    def test__method_signatures(self):                                                   # Test all methods exist
        with Area__Graph__CRUD() as _:
            # Check all expected methods exist
            assert hasattr(_, 'create_graph')
            assert hasattr(_, 'get_graph')
            assert hasattr(_, 'delete_graph')
            assert hasattr(_, 'graph_exists')

            # All should be callable
            assert callable(_.create_graph)
            assert callable(_.get_graph)
            assert callable(_.delete_graph)
            assert callable(_.graph_exists)

    def test__create_graph__method_signature(self):                                      # Test create_graph signature
        with Area__Graph__CRUD() as _:
            sig = inspect.signature(_.create_graph)
            params = list(sig.parameters.values())

            # Should have exactly 1 request parameter
            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Create__Request
            assert sig.return_annotation == Schema__Graph__Create__Response

    def test__get_graph__method_signature(self):                                         # Test get_graph signature
        with Area__Graph__CRUD() as _:
            sig = inspect.signature(_.get_graph)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Get__Request
            assert sig.return_annotation == Schema__Graph__Get__Response

    def test__delete_graph__method_signature(self):                                      # Test delete_graph signature
        with Area__Graph__CRUD() as _:
            sig    = inspect.signature(_.delete_graph)
            with Type_Safe__List(expected_type=str, initial_data=sig.parameters) as _:
                assert _       == ['cache_id', 'graph_id', 'namespace']
                assert _.obj() == ['cache_id', 'graph_id', 'namespace']

    def test__graph_exists__method_signature(self):                                      # Test graph_exists signature
        with Area__Graph__CRUD() as _:
            sig    = inspect.signature(_.graph_exists)
            with Type_Safe__List(expected_type=str, ) as _:
                _.extend(sig.parameters)
                assert _.obj() == ['cache_id', 'graph_id', 'namespace']
                assert _       == ['cache_id', 'graph_id', 'namespace']


    def test_create_graph(self):
        with self.area_crud as _:
            request                 =  Schema__Graph__Create__Request(auto_cache=True)         # with cache

            response                = _.create_graph(request=request)
            cache_id                = response.cache_id
            graph_id                = response.graph_id
            cache_namespace         = response.cache_namespace
            cache_data_folder       = f"{cache_namespace}/data/key-based/graphs/{graph_id}"
            cache_hash              = self.graph_cache_utils .graph_id__to__cache_hash(graph_id=graph_id)
            cache_id_refs           = self.graph_cache_client.cache_id__refs(cache_id  = cache_id       ,
                                                                             namespace = cache_namespace)
            mgraph                  = self.graph_cache_client.retrieve_graph(cache_id  = cache_id       ,                 # here we will use cache_id
                                                                             namespace = cache_namespace)

            assert type(response)     is Schema__Graph__Create__Response
            assert cache_hash         == self.hash_generator.from_string(graph_id)
            assert request.auto_cache == True
            assert response.obj()     == __(cache_id         = cache_id         ,
                                            cache_namespace  = cache_namespace  ,
                                            graph_id         = graph_id         ,
                                            cached           = True             )


            assert type(cache_id_refs) is Schema__Cache__File__Refs
            assert cache_id_refs.obj() == __(all_paths=__(data    = [ f'{cache_data_folder}/mgraph.json',
                                                                      f'{cache_data_folder}/mgraph.json.config',
                                                                      f'{cache_data_folder}/mgraph.json.metadata'],
                                                          by_hash = [ f'{cache_namespace}/refs/by-hash/{cache_hash[0:2]}/{cache_hash[2:4]}/{cache_hash}.json'],
                                                          by_id   = [ f'{cache_namespace}/refs/by-id/{cache_id[0:2]}/{cache_id[2:4]}/{cache_id}.json']),
                                             cache_id   = cache_id          ,
                                             cache_hash = cache_hash        ,
                                             file_type  = 'json'            ,
                                             namespace  = cache_namespace   ,
                                             file_paths = __(content_files  = [f'{cache_data_folder}/mgraph.json'],
                                                             data_folders   = [f'{cache_data_folder}/mgraph/data']),
                                             strategy   = 'key_based'       ,
                                             timestamp  = __SKIP__          )




            assert type(mgraph) is MGraph
            assert mgraph.graph.graph_id() == graph_id

            mgraph_from_graph_id = self.graph_cache_client.retrieve_graph(graph_id  = graph_id        ,           # here we will use graph_id
                                                                          namespace = cache_namespace)

            assert type(mgraph_from_graph_id) is MGraph
            assert mgraph_from_graph_id.obj() == mgraph.obj()

            assert _.delete_graph(graph_id  = graph_id       ,
                                  namespace = 'graph-service')  is True

    def test_create_graph__no_cache(self):
        with self.area_crud as _:
            request  =  Schema__Graph__Create__Request(auto_cache=False)         # with no cache
            response = _.create_graph(request=request)
            graph_id = response.graph_id
            assert type(response) is Schema__Graph__Create__Response
            assert response.obj() == __(cache_id        = None           ,
                                        cache_namespace = 'graph-service',
                                        graph_id        = __SKIP__       ,
                                        cached          = False          )
            # assert _.delete_graph(graph_id  = graph_id       ,
            #                       namespace = 'graph-service')  is False      # cache file was not created

    def test_delete_graph(self):
        with self.area_crud as _:
            create_request  =  Schema__Graph__Create__Request()
            create_response = _.create_graph(request=create_request)
            cache_id        = create_response.cache_id
            graph_id        = create_response.graph_id
            cache_hash      = self.graph_cache_utils.graph_id__to__cache_hash(graph_id=graph_id)
            namespace       = create_response.cache_namespace
            assert is_guid  (cache_id) is True
            assert is_obj_id(graph_id) is True

            assert type(self.cache_service      ) is Cache__Service                                   # from mgraph_ai_service_cache
            assert type(self.cache_client       ) is Cache__Service__Fast_API__Client                 # from mgraph_ai_service_cache_client
            assert type(self.graph_cache_client ) is Graph__Cache__Client                             # from this project

            with self.graph_cache_utils as utils:
                assert utils.namespaces() == [namespace]
                assert utils.namespace__cache_ids   (namespace=namespace) == [cache_id]
                assert utils.namespace__cache_hashes(namespace=namespace) == [cache_hash]

                assert _.graph_exists(graph_id=graph_id, namespace=namespace) is True               # confirm it exists (before delete) check using graph_id
                assert _.graph_exists(cache_id=cache_id, namespace=namespace) is True               # also check using cache_id
                assert _.delete_graph(cache_id=cache_id, namespace=namespace) is True               # delete using cache__id
                assert utils.namespace__cache_ids   (namespace=namespace) == []                     # confirm deletion from namespace
                assert utils.namespace__cache_hashes(namespace=namespace) == []

                assert _.graph_exists(cache_id=cache_id, namespace=namespace) is False
                assert _.graph_exists(graph_id=graph_id, namespace=namespace) is False               # check using graph_id

                assert _.delete_graph(cache_id=cache_id, namespace=namespace) is False               # delete again using cache__id
                assert _.delete_graph(graph_id=graph_id, namespace=namespace) is False               # delete using graph_id

                create_response_2 = _.create_graph(request=create_request)                           # create another file
                graph_id_2        = create_response_2.graph_id
                cache_hash_2      = create_response_2.cache_id
                cache_id_2        = create_response_2.cache_id

                assert cache_id   != cache_id_2                                                     # confirm all are different
                assert cache_hash != cache_hash_2
                assert graph_id   != graph_id_2

                assert _.graph_exists(graph_id=graph_id_2, namespace=namespace) is True             # confirm the new file exists
                assert _.delete_graph(graph_id=graph_id_2, namespace=namespace) is True             # delete using graph_id (above we used cache_id)
                assert _.graph_exists(graph_id=graph_id_2, namespace=namespace) is False            # confirm the file doesn't exist anymore
                assert _.delete_graph(graph_id=graph_id_2, namespace=namespace) is False            # delete same graph_id should fail


    def test__bug__get_graph(self):
        with self.area_crud as _:
            create_request  =  Schema__Graph__Create__Request()
            create_response = _.create_graph(request=create_request)
            cache_id        = create_response.cache_id
            namespace       = create_response.cache_namespace
            get_request     = Schema__Graph__Get__Request(cache_id = cache_id, namespace = namespace)
            get_response    = _.get_graph(request=get_request)
            graph_id        = get_response.graph_id
            cache_id        = get_response.cache_id

            assert type(get_response) is Schema__Graph__Get__Response

            #assert get_response.mgraph.graph.model.data.graph_id == graph_id           # expected
            assert get_response.mgraph.graph.model.data.graph_id != graph_id            # BUG
            assert get_response.obj() == __(cache_id=cache_id,
                                            graph_id=graph_id,
                                            mgraph=__(graph=__(domain_types=__(node_domain_type='mgraph_db.mgraph.domain.Domain__MGraph__Node.Domain__MGraph__Node',
                                                                              edge_domain_type='mgraph_db.mgraph.domain.Domain__MGraph__Edge.Domain__MGraph__Edge'),
                                                              model=__(data=__(edges=__(),
                                                                               graph_data = __(),
                                                                               #graph_id   = graph_id,          # BUG
                                                                               graph_id   = __SKIP__,           # BUG
                                                                               graph_type='mgraph_db.mgraph.schemas.Schema__MGraph__Graph.Schema__MGraph__Graph',
                                                                               nodes=__(),
                                                                               schema_types=__(edge_type='mgraph_db.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge',
                                                                                               graph_data_type='mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data.Schema__MGraph__Graph__Data',
                                                                                               node_type='mgraph_db.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node',
                                                                                               node_data_type='mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data')),
                                                                       model_types=__(node_model_type='mgraph_db.mgraph.models.Model__MGraph__Node.Model__MGraph__Node',
                                                                                      edge_model_type='mgraph_db.mgraph.models.Model__MGraph__Edge.Model__MGraph__Edge')),
                                                              graph_type='mgraph_db.mgraph.domain.Domain__MGraph__Graph.Domain__MGraph__Graph'),
                                                     query_class='mgraph_db.query.MGraph__Query.MGraph__Query',
                                                     edit_class='mgraph_db.mgraph.actions.MGraph__Edit.MGraph__Edit',
                                                     screenshot_class='mgraph_db.mgraph.actions.MGraph__Screenshot.MGraph__Screenshot'),
                                            success=True)

