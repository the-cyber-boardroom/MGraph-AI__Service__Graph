import pytest
from unittest                                               import TestCase
from mgraph_db.mgraph.MGraph                                import MGraph
from osbot_utils.utils.Env                                  import load_dotenv
from osbot_utils.utils.Files                                import path_combine
from mgraph_ai_service_graph.service.graph.Graph__Service   import Graph__Service
from tests                                                  import integration


class test_experiment_with_graph_rendering(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("manually execution")
        env_file = path_combine(integration.path, '.env')
        load_dotenv(dotenv_path=env_file)
        cls.graph_service = Graph__Service()
        cls.cache_id = "d93e4e9e-cc43-4abe-aaa6-a8192c58eb7e"       # graph we created earlier
        cls.namespace = 'graph-service'

    def test_get_graph(self):

        with self.graph_service as _:
            mgraph = _.get_graph(cache_id=self.cache_id, namespace=self.namespace)
            #mgraph.print_obj()
            assert type(mgraph) is MGraph
            save_to = './tests/integration/test-graph.png'
            result = (mgraph.screenshot().save_to(save_to)
                                         .show_node_value()
                                         .dot())
