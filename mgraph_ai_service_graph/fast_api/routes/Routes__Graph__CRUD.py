from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response             import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request                 import Schema__Graph__Get__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response                import Schema__Graph__Get__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Delete__Response             import Schema__Graph__Delete__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Exists__Response             import Schema__Graph__Exists__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD


TAG__ROUTES_GRAPH_CRUD = 'graph-crud'
ROUTES_PATHS__GRAPH_CRUD = [ '/graph-crud/create'                     ,
                             '/graph-crud/get/by-id/{graph_id}'       ,
                             '/graph-crud/get/by-cache-id/{cache_id}' ,
                             '/graph-crud/delete/{graph_id}'          ,
                             '/graph-crud/exists/{graph_id}'          ]


class Routes__Graph__CRUD(Fast_API__Routes):                                                # Graph CRUD routes - lifecycle management
    tag       : str              = TAG__ROUTES_GRAPH_CRUD
    area_crud : Area__Graph__CRUD                                                           # CRUD operations

    def create(self,                                                                        # Create a new empty graph
               request: Schema__Graph__Create__Request                                      # Graph creation parameters
              ) -> Schema__Graph__Create__Response:                                         # Response with graph_id and cache status
        return self.area_crud.create_graph(request)

    def get__by_id__graph_id(self,                                                          # Retrieve graph by graph_id
                             graph_id : Obj_Id                        ,                     # Unique graph identifier
                             namespace: Safe_Str__Id = 'graph-service'                      # Cache namespace
                            ) -> Schema__Graph__Get__Response:                              # Response with graph metadata
        request = Schema__Graph__Get__Request(graph_id  = graph_id ,
                                              namespace = namespace)
        return self.area_crud.get_graph(request)

    def get__by_cache_id__cache_id(self,                                                    # Retrieve graph by cache_id
                                   cache_id : Random_Guid                  ,                # Cache identifier
                                   namespace: Safe_Str__Id = 'graph-service'                # Cache namespace
                                  ) -> Schema__Graph__Get__Response:                        # Response with graph metadata
        request = Schema__Graph__Get__Request(cache_id  = cache_id ,
                                              namespace = namespace)
        return self.area_crud.get_graph(request)

    def delete__graph_id(self,                                                              # Delete graph by ID
                         graph_id  : Obj_Id                       ,                         # Graph to delete
                         namespace : Safe_Str__Id = 'graph-service'                         # Cache namespace
                        ) -> Schema__Graph__Delete__Response:                               # Response with deletion status
        deleted = self.area_crud.delete_graph(graph_id  = graph_id ,
                                              namespace = namespace)
        return Schema__Graph__Delete__Response(graph_id  = graph_id ,
                                               namespace = namespace,
                                               deleted   = deleted  )

    def exists__graph_id(self,                                                              # Check if graph exists
                         graph_id  : Obj_Id                       ,                         # Graph to check
                         namespace : Safe_Str__Id = 'graph-service'                         # Cache namespace
                        ) -> Schema__Graph__Exists__Response:                               # Response with exists status
        exists = self.area_crud.graph_exists(graph_id  = graph_id ,
                                             namespace = namespace)
        return Schema__Graph__Exists__Response(graph_id  = graph_id ,
                                               namespace = namespace,
                                               exists    = exists   )

    def setup_routes(self):                                                                 # Register CRUD route handlers
        self.add_route_post  (self.create                    )
        self.add_route_get   (self.get__by_id__graph_id      )
        self.add_route_get   (self.get__by_cache_id__cache_id)
        self.add_route_delete(self.delete__graph_id          )
        self.add_route_get   (self.exists__graph_id          )
        return self
