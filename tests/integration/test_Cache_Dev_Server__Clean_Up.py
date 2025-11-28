from unittest                                                                               import TestCase

import pytest
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from mgraph_ai_service_cache_client.client.client_contract.Cache__Service__Fast_API__Client import Cache__Service__Fast_API__Client
from mgraph_ai_service_cache_client.utils.Version                                           import version__mgraph_ai_service_cache_client
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                       import Type_Safe__List
from osbot_utils.utils.Env                                                                  import load_dotenv
from osbot_utils.utils.Files                                                                import path_combine
from tests                                                                                  import integration

NAMESPACES__NON_PROD__PREFIXES = ['test-',
                                  'namespace',
                                  'upd-',
                                  'abc',
                                  'qa-tests',
                                  'pytests' ,
                                  'test',
                                  'customer-x',
                                  'live-demo',
                                  'proxy-cache-tests']

class Cache_Dev_Server__Clean_Up(Type_Safe):
    cache_client   : Cache__Service__Fast_API__Client

    def current_namespaces(self):
        with self.cache_client as _:
            return _.namespaces().list()

    def delete_files(self, files_to_delete):
        delete_files_result = []
        for file_to_delete in files_to_delete:
            delete_file_result = self.cache_client.admin_storage().file__delete(path=file_to_delete)
            delete_files_result.append(delete_file_result)
        return delete_files_result


    def files_in_namespace(self, namespace):
        return self.cache_client.admin_storage().files__all__path(path=namespace).files

    def non_prod_namespaces(self):
        result = []
        for namespace in self.current_namespaces():
            for non_prod_namespace in NAMESPACES__NON_PROD__PREFIXES:
                if namespace.startswith(non_prod_namespace):
                    result.append(namespace)
        return result

class test_Cache_Dev_Server__Clean_Up(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pytest.skip("needs manual execution")
        env_file = path_combine(integration.path, '.env')
        load_dotenv(dotenv_path=env_file)
        cls.clean_up_cache_dev = Cache_Dev_Server__Clean_Up()

    def test_setUpClass(self):
        with self.clean_up_cache_dev as _:
            _.cache_client.requests()                                           # will trigger the load of the config (so that we can test it bellow
            assert type(_             ) is Cache_Dev_Server__Clean_Up
            assert type(_.cache_client) is Cache__Service__Fast_API__Client
            assert _.obj()              == __(cache_client=__(config=__(base_url        = __SKIP__ ,
                                                                        api_key         = __SKIP__ ,
                                                                        api_key_header  = __SKIP__ ,
                                                                        mode            = 'remote' ,              # confirms remote server is configured
                                                                        fast_api_app    = None     ,
                                                                        timeout         = 30       ,
                                                                        service_name    = 'Cache__Service__Fast_API'             ,
                                                                        service_version = version__mgraph_ai_service_cache_client)))

    def test_current_namespaces(self):
        with self.clean_up_cache_dev as _:
            assert _.current_namespaces() != []

    def test_delete_files(self):
        print()
        max_namespaces = 1
        with self.clean_up_cache_dev as _:
            for namespace in _.non_prod_namespaces()[0:max_namespaces]:
                files_in_namespace = _.files_in_namespace(namespace)
                assert type(files_in_namespace) is Type_Safe__List
                result = _.delete_files(files_in_namespace)
                print(f"in namespace {namespace}, deleted {len(result)} files")


    def test_non_prod_namespaces(self):
        with self.clean_up_cache_dev as _:
            result = _.non_prod_namespaces()
            assert type(result) is list

    def test_files_in_namespace(self):
        with self.clean_up_cache_dev as _:
            for namespace in _.non_prod_namespaces():
                files_in_namespace = _.files_in_namespace(namespace)
                assert type(files_in_namespace) is Type_Safe__List
                break


