from types import NoneType
from unittest                                                                               import TestCase
from mgraph_db.mgraph.MGraph                                                                import MGraph
from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from osbot_utils.testing.__                                                                 import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.utils.Objects                                                              import base_classes
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__CRUD                            import Routes__Graph__CRUD
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__CRUD                            import TAG__ROUTES_GRAPH_CRUD
from mgraph_ai_service_graph.fast_api.routes.Routes__Graph__CRUD                            import ROUTES_PATHS__GRAPH_CRUD
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response             import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response                import Schema__Graph__Get__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Delete__Response             import Schema__Graph__Delete__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Exists__Response             import Schema__Graph__Exists__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query
from mgraph_ai_service_graph.service.caching.Graph__Cache__Client                           import Graph__Cache__Client
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service
from mgraph_ai_service_graph.utils.testing.Graph_Test_Helpers                               import Graph_Test_Helpers
from tests.unit.Graph__Service__Fast_API__Test_Objs                                         import client_cache_service


class test_Routes__Graph__CRUD(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache_client, cls.cache_service = client_cache_service()                        # Create in-memory cache service
        cls.graph_cache_client              = Graph__Cache__Client(cache_client=cls.cache_client)
        cls.graph_service                   = Graph__Service(graph_cache_client=cls.graph_cache_client)

        cls.area_crud                       = Area__Graph__CRUD (graph_service=cls.graph_service)    # Create areas
        cls.area_edit                       = Area__Graph__Edit (graph_service=cls.graph_service)
        cls.area_query                      = Area__Graph__Query(graph_service=cls.graph_service)

        cls.routes                          = Routes__Graph__CRUD(area_crud=cls.area_crud)           # Create routes
        cls.helpers                         = Graph_Test_Helpers(area_crud  = cls.area_crud  ,       # Create helpers
                                                                 area_edit  = cls.area_edit  ,
                                                                 area_query = cls.area_query )
        cls.test_namespace                  = Safe_Str__Id('test-routes-crud')                       # Test namespace

    # ═══════════════════════════════════════════════════════════════════════════════
    # Initialization Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                                 # Test auto-initialization
        with Routes__Graph__CRUD() as _:
            assert type(_)            is Routes__Graph__CRUD
            assert base_classes(_)    == [Fast_API__Routes, Type_Safe, object]
            assert _.tag              == TAG__ROUTES_GRAPH_CRUD
            assert _.tag              == 'graph-crud'
            assert type(_.area_crud)  is Area__Graph__CRUD

    def test__tag_constant(self):                                                           # Test tag constant
        assert TAG__ROUTES_GRAPH_CRUD == 'graph-crud'

    def test__routes_paths_constant(self):                                                  # Test routes paths constant
        assert ROUTES_PATHS__GRAPH_CRUD == [ '/graph-crud/create'                     ,
                                             '/graph-crud/get/by-id/{graph_id}'       ,
                                             '/graph-crud/get/by-cache-id/{cache_id}' ,
                                             '/graph-crud/delete/{graph_id}'          ,
                                             '/graph-crud/exists/{graph_id}'          ]

    def test__area_dependency(self):                                                        # Test area class is injected
        with self.routes as _:
            assert _.area_crud is not None
            assert type(_.area_crud) is Area__Graph__CRUD
            assert _.area_crud       is self.area_crud                                      # Same instance as setup

    def test__setup_routes(self):                                                           # Test setup_routes method
        with self.routes as _:
            assert hasattr(_, 'setup_routes')
            assert callable(_.setup_routes)
            result = _.setup_routes()
            assert result is _                                                              # Returns self for chaining

    # ═══════════════════════════════════════════════════════════════════════════════
    # Create Route Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_create(self):                                                                  # Test basic graph creation
        with self.routes as _:
            request  = Schema__Graph__Create__Request(namespace  = self.test_namespace,
                                                      auto_cache = True               )
            response = _.create(request)

            assert type(response)           is Schema__Graph__Create__Response              # Verify response type
            assert type(response.graph_id)  is Obj_Id                                       # Verify field types
            assert type(response.cache_id)  is Random_Guid
            assert response.cache_namespace == self.test_namespace
            assert response.cached          is True

            self.helpers.delete_graph(graph_id  = response.graph_id ,                       # Cleanup
                                      namespace = self.test_namespace)

    def test_create__without_cache(self):                                                   # Test creation without caching
        with self.routes as _:
            request  = Schema__Graph__Create__Request(namespace  = self.test_namespace,
                                                      auto_cache = False              )
            response = _.create(request)

            assert type(response)           is Schema__Graph__Create__Response
            assert type(response.graph_id)  is Obj_Id
            assert response.cached          is False                                        # Not cached

    def test_create__default_namespace(self):                                               # Test creation with default namespace
        with self.routes as _:
            request  = Schema__Graph__Create__Request(auto_cache = True)                    # No namespace specified
            response = _.create(request)

            assert type(response)           is Schema__Graph__Create__Response
            assert response.cache_namespace  == 'graph-service'                             # Default namespace

            self.helpers.delete_graph(graph_id  = response.graph_id       ,                 # Cleanup
                                      namespace = response.cache_namespace)

    def test_create__response_structure(self):                                              # Test complete response structure
        with self.routes as _:
            request  = Schema__Graph__Create__Request(namespace  = self.test_namespace,
                                                      auto_cache = True               )
            response = _.create(request)
            assert type(response) is Schema__Graph__Create__Response
            assert response.obj() == __(graph_id  = __SKIP__            ,             # Use obj() for comparison
                                        cache_id  = __SKIP__            ,
                                        cache_namespace = self.test_namespace ,
                                        cached    = True                )

            self.helpers.delete_graph(graph_id  = response.graph_id ,
                                      namespace = self.test_namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Get By ID Route Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_get__by_id__graph_id(self):                                                    # Test get by graph_id
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)    # Create graph via helpers
        graph_id        = create_response.graph_id

        with self.routes as _:
            response = _.get__by_id__graph_id(graph_id  = graph_id          ,
                                              namespace = self.test_namespace)

            assert type(response)           is Schema__Graph__Get__Response                 # Verify response type
            assert type(response.graph_id)  is Obj_Id
            assert response.graph_id        == graph_id                                     # Same graph_id
            assert response.success         is True
            assert response.mgraph          is not None                                     # Has graph data

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)         # Cleanup

    def test_get__by_id__graph_id__not_found(self):                                         # Test get with non-existent ID
        with self.routes as _:
            fake_graph_id = Obj_Id()                                                        # Random non-existent ID
            response = _.get__by_id__graph_id(graph_id  = fake_graph_id     ,
                                              namespace = self.test_namespace)

            assert type(response)    is Schema__Graph__Get__Response
            assert response.success  is False                                               # Not found
            assert response.mgraph   is None                                                # No graph data

    def test_get__by_id__graph_id__response_structure(self):                                # Test complete response structure
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.routes as _:
            response = _.get__by_id__graph_id(graph_id  = graph_id          ,
                                              namespace = self.test_namespace)

            assert response.obj().contains(__(graph_id  = graph_id ,
                                              cache_id  = __SKIP__ ,
                                              mgraph    = __SKIP__ ,
                                              success   = True     ))

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Get By Cache ID Route Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_get__by_cache_id__cache_id(self):                                              # Test get by cache_id
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        cache_id        = create_response.cache_id
        graph_id        = create_response.graph_id

        with self.routes as _:
            response = _.get__by_cache_id__cache_id(cache_id  = cache_id        ,
                                                    namespace = self.test_namespace)

            assert type(response)           is Schema__Graph__Get__Response
            assert type(response.cache_id)  is Random_Guid
            assert response.cache_id        == cache_id                                     # Same cache_id
            assert response.success         is True
            assert response.mgraph          is not None

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_get__by_cache_id__cache_id__not_found(self):                                   # Test get with non-existent cache_id
        with self.routes as _:
            fake_cache_id = Random_Guid()
            response = _.get__by_cache_id__cache_id(cache_id  = fake_cache_id   ,
                                                    namespace = self.test_namespace)

            assert type(response)    is Schema__Graph__Get__Response
            assert response.success  is False
            assert response.mgraph   is None

    # ═══════════════════════════════════════════════════════════════════════════════
    # Delete Route Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_delete__graph_id(self):                                                        # Test delete graph
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.routes as _:
            assert self.helpers.verify_graph_exists(graph_id  = graph_id          ,         # Verify graph exists before delete
                                                    namespace = self.test_namespace)

            response = _.delete__graph_id(graph_id  = graph_id          ,
                                          namespace = self.test_namespace)

            assert type(response)           is Schema__Graph__Delete__Response              # Verify response type
            assert type(response.graph_id)  is Obj_Id
            assert response.graph_id        == graph_id
            assert response.namespace       == self.test_namespace
            assert response.deleted         is True                                         # Successfully deleted

            assert not self.helpers.verify_graph_exists(graph_id  = graph_id        ,       # Verify graph no longer exists
                                                        namespace = self.test_namespace)

    def test_delete__graph_id__not_found(self):                                             # Test delete non-existent graph
        with self.routes as _:
            fake_graph_id = Obj_Id()
            response = _.delete__graph_id(graph_id  = fake_graph_id     ,
                                          namespace = self.test_namespace)

            assert type(response)    is Schema__Graph__Delete__Response
            assert response.graph_id == fake_graph_id
            assert response.deleted  is False                                               # Nothing to delete

    def test_delete__graph_id__response_structure(self):                                    # Test complete response structure
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.routes as _:
            response = _.delete__graph_id(graph_id  = graph_id          ,
                                          namespace = self.test_namespace)

            assert response.obj() == __(graph_id  = graph_id                 ,
                                        cache_id  = None                     ,              # Not set in delete response
                                        namespace = self.test_namespace      ,
                                        deleted   = True                     )

    def test_delete__graph_id__twice(self):                                                 # Test deleting same graph twice
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.routes as _:
            response1 = _.delete__graph_id(graph_id  = graph_id          ,                  # First delete
                                           namespace = self.test_namespace)
            assert response1.deleted is True

            response2 = _.delete__graph_id(graph_id  = graph_id          ,                  # Second delete
                                           namespace = self.test_namespace)
            assert response2.deleted is False                                               # Already deleted

    # ═══════════════════════════════════════════════════════════════════════════════
    # Exists Route Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_exists__graph_id(self):                                                        # Test exists for existing graph
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.routes as _:
            response = _.exists__graph_id(graph_id  = graph_id          ,
                                          namespace = self.test_namespace)

            assert type(response)           is Schema__Graph__Exists__Response              # Verify response type
            assert type(response.graph_id)  is Obj_Id
            assert response.graph_id        == graph_id
            assert response.namespace       == self.test_namespace
            assert response.exists          is True                                         # Graph exists

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_exists__graph_id__not_found(self):                                             # Test exists for non-existent graph
        with self.routes as _:
            fake_graph_id = Obj_Id()
            response = _.exists__graph_id(graph_id  = fake_graph_id     ,
                                          namespace = self.test_namespace)

            assert type(response)    is Schema__Graph__Exists__Response
            assert response.graph_id == fake_graph_id
            assert response.exists   is False                                               # Graph doesn't exist

    def test_exists__graph_id__response_structure(self):                                    # Test complete response structure
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.routes as _:
            response = _.exists__graph_id(graph_id  = graph_id          ,
                                          namespace = self.test_namespace)

            assert response.obj() == __(graph_id  = graph_id                 ,
                                        cache_id  = None                     ,
                                        namespace = self.test_namespace      ,
                                        exists    = True                     )

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)

    def test_exists__graph_id__after_delete(self):                                          # Test exists after deleting graph
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.routes as _:
            response1 = _.exists__graph_id(graph_id  = graph_id          ,                  # Before delete
                                           namespace = self.test_namespace)
            assert response1.exists is True

            _.delete__graph_id(graph_id  = graph_id          ,                              # Delete the graph
                              namespace = self.test_namespace)

            response2 = _.exists__graph_id(graph_id  = graph_id          ,                  # After delete
                                           namespace = self.test_namespace)
            assert response2.exists is False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Integration Workflow Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_workflow__create_get_delete(self):                                             # Test complete lifecycle
        with self.routes as _:
            request         = Schema__Graph__Create__Request(namespace  = self.test_namespace,     # Step 1: Create
                                                             auto_cache = True               )
            create_response = _.create(request)

            graph_id = create_response.graph_id
            cache_id = create_response.cache_id

            assert type(create_response) is Schema__Graph__Create__Response

            get_response = _.get__by_id__graph_id(graph_id  = graph_id          ,           # Step 2: Get by graph_id
                                                  namespace = self.test_namespace)
            assert type(get_response) is Schema__Graph__Get__Response
            assert get_response.success is True
            assert get_response.graph_id == graph_id

            get_by_cache_response = _.get__by_cache_id__cache_id(cache_id  = cache_id       ,     # Step 3: Get by cache_id
                                                                  namespace = self.test_namespace)
            assert type(get_by_cache_response)    is Schema__Graph__Get__Response
            assert get_by_cache_response.success  is True
            assert get_by_cache_response.cache_id == cache_id

            exists_response = _.exists__graph_id(graph_id  = graph_id          ,            # Step 4: Check exists
                                                 namespace = self.test_namespace)
            assert type(exists_response) is Schema__Graph__Exists__Response
            assert exists_response.exists is True

            delete_response = _.delete__graph_id(graph_id  = graph_id          ,            # Step 5: Delete
                                                 namespace = self.test_namespace)
            assert type(delete_response) is Schema__Graph__Delete__Response
            assert delete_response.deleted is True

            exists_after = _.exists__graph_id(graph_id  = graph_id          ,               # Step 6: Verify deleted
                                              namespace = self.test_namespace)
            assert exists_after.exists is False

    def test_workflow__multiple_graphs_isolation(self):                                     # Test multiple graphs are isolated
        create_response1 = self.helpers.create_empty_graph(namespace=self.test_namespace)
        create_response2 = self.helpers.create_empty_graph(namespace=self.test_namespace)

        graph_id1 = create_response1.graph_id
        graph_id2 = create_response2.graph_id

        assert graph_id1 != graph_id2                                                       # Different IDs

        with self.routes as _:
            _.delete__graph_id(graph_id  = graph_id1         ,                              # Delete first graph only
                              namespace = self.test_namespace)

            exists1 = _.exists__graph_id(graph_id  = graph_id1         ,                    # First should be deleted
                                         namespace = self.test_namespace)
            exists2 = _.exists__graph_id(graph_id  = graph_id2         ,                    # Second should still exist
                                         namespace = self.test_namespace)

            assert exists1.exists is False
            assert exists2.exists is True

        self.helpers.delete_graph(graph_id=graph_id2, namespace=self.test_namespace)        # Cleanup

    def test_workflow__graph_with_nodes(self):                                              # Test graph with nodes via routes
        create_response, node_responses = self.helpers.create_graph_with_nodes(             # Create graph with nodes
                                              namespace  = self.test_namespace,
                                              node_count = 3                  )
        graph_id = create_response.graph_id

        with self.routes as _:
            get_response = _.get__by_id__graph_id(graph_id  = graph_id          ,           # Get graph
                                                  namespace = self.test_namespace)

            assert get_response.success is True
            assert get_response.mgraph  is not None                                         # Graph has data

            delete_response = _.delete__graph_id(graph_id  = graph_id          ,            # Delete
                                                 namespace = self.test_namespace)
            assert delete_response.deleted is True

            get_after = _.get__by_id__graph_id(graph_id  = graph_id          ,              # Verify deleted
                                               namespace = self.test_namespace)
            assert get_after.success is False
            assert get_after.mgraph  is None

    # ═══════════════════════════════════════════════════════════════════════════════
    # Type Safety Tests
    # ═══════════════════════════════════════════════════════════════════════════════

    def test_types__create_response_fields(self):                                           # Test all field types in create response
        with self.routes as _:
            request  = Schema__Graph__Create__Request(namespace  = self.test_namespace,
                                                      auto_cache = True               )
            response = _.create(request)

            assert type(response)                 is Schema__Graph__Create__Response              # Response type
            assert type(response.graph_id)        is Obj_Id                                       # Field types
            assert type(response.cache_id)        is Random_Guid
            assert type(response.cache_namespace) is Safe_Str__Id
            assert type(response.cached)          is bool


            self.helpers.delete_graph(graph_id=response.graph_id, namespace=self.test_namespace)

    def test_types__get_response_fields(self):                                              # Test all field types in get response
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.routes as _:
            response = _.get__by_id__graph_id(graph_id  = graph_id          ,
                                              namespace = self.test_namespace)

            assert type(response)           is Schema__Graph__Get__Response
            assert type(response.graph_id)  is Obj_Id
            assert type(response.cache_id)  is NoneType
            assert type(response.success)   is bool
            assert type(response.mgraph)    is MGraph

        assert self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace) is True

    def test_types__delete_response_fields(self):                                           # Test all field types in delete response
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.routes as _:
            response = _.delete__graph_id(graph_id  = graph_id          ,
                                          namespace = self.test_namespace)

            assert type(response)           is Schema__Graph__Delete__Response
            assert type(response.graph_id)  is Obj_Id
            assert type(response.namespace) is Safe_Str__Id
            assert type(response.deleted)   is bool

    def test_types__exists_response_fields(self):                                           # Test all field types in exists response
        create_response = self.helpers.create_empty_graph(namespace=self.test_namespace)
        graph_id        = create_response.graph_id

        with self.routes as _:
            response = _.exists__graph_id(graph_id  = graph_id          ,
                                          namespace = self.test_namespace)

            assert type(response)           is Schema__Graph__Exists__Response
            assert type(response.graph_id)  is Obj_Id
            assert type(response.namespace) is Safe_Str__Id
            assert type(response.exists)    is bool

        self.helpers.delete_graph(graph_id=graph_id, namespace=self.test_namespace)