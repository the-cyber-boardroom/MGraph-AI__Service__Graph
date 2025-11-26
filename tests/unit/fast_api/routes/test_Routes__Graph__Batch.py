from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Objects                                                           import base_classes
from osbot_fast_api.api.routes.Fast_API__Routes                                          import Fast_API__Routes
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__Batch                        import Routes__Graph__Batch
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Request       import Schema__Graph__Batch__Request
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Response      import Schema__Graph__Batch__Response
from mgraph_ai_service_graph.service.batch_execution.Graph__Batch__Executor              import Graph__Batch__Executor


class test_Routes__Graph__Batch(TestCase):

    def test__init__(self):                                                              # Test auto-initialization
        with Routes__Graph__Batch() as _:
            assert type(_)                 is Routes__Graph__Batch
            assert base_classes(_)         == [Fast_API__Routes, Type_Safe, object]
            assert _.tag                   == 'graph-batch'
            assert type(_.batch_executor)  is Graph__Batch__Executor

    def test__tag(self):                                                                 # Test tag value
        with Routes__Graph__Batch() as _:
            assert _.tag == 'graph-batch'

    def test__batch_executor_dependency(self):                                           # Test batch executor is injected
        with Routes__Graph__Batch() as _:
            assert _.batch_executor is not None
            assert type(_.batch_executor) is Graph__Batch__Executor

    def test__execute_method_signature(self):                                            # Test execute method exists with correct signature
        with Routes__Graph__Batch() as _:
            assert hasattr(_, 'execute')
            assert callable(_.execute)

            import inspect
            sig = inspect.signature(_.execute)
            params = list(sig.parameters.values())

            assert len(params)           == 1
            assert params[0].name        == 'request'
            assert params[0].annotation  == Schema__Graph__Batch__Request
            assert sig.return_annotation == Schema__Graph__Batch__Response

    def test__setup_routes(self):                                                        # Test setup_routes method
        with Routes__Graph__Batch() as _:
            assert hasattr(_, 'setup_routes')
            assert callable(_.setup_routes)

            result = _.setup_routes()
            assert result is _                                                           # Returns self for chaining