from osbot_fast_api.api.routes.Fast_API__Routes                                             import Fast_API__Routes
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id                          import Cache_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref, GRAPH_REF__DEFAULT_NAMESPACE
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response             import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request                 import Schema__Graph__Get__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response                import Schema__Graph__Get__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Delete__Response             import Schema__Graph__Delete__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Exists__Response             import Schema__Graph__Exists__Response
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD


TAG__ROUTES_GRAPH_CRUD   = 'graph-crud'
ROUTES_PATHS__GRAPH_CRUD = [ '/graph-crud/create'                     ,
                             '/graph-crud/get'                        ,
                             '/graph-crud/get/by-cache-id/{cache_id}' ,
                             '/graph-crud/get/by-graph-id/{graph_id}' ,
                             '/graph-crud/delete'                     ,
                             '/graph-crud/exists'                     ]


class Routes__Graph__CRUD(Fast_API__Routes):                                                # Graph CRUD routes
    tag       : str              = TAG__ROUTES_GRAPH_CRUD
    area_crud : Area__Graph__CRUD

    def create(self,                                                                        # Create a new empty graph
               request: Schema__Graph__Create__Request
              ) -> Schema__Graph__Create__Response:
        return self.area_crud.create_graph(request)

    def get(self,                                                                           # Get graph using graph_ref in body
            request: Schema__Graph__Get__Request
           ) -> Schema__Graph__Get__Response:
        return self.area_crud.get_graph(request)

    def get__by_cache_id__cache_id(self,                                                    # Get graph by cache_id (URL param)
                                   cache_id : Cache_Id                             ,
                                   namespace: Safe_Str__Id = GRAPH_REF__DEFAULT_NAMESPACE
                                  ) -> Schema__Graph__Get__Response:
        graph_ref = Schema__Graph__Ref(cache_id  = cache_id ,
                                       namespace = namespace)
        request   = Schema__Graph__Get__Request(graph_ref = graph_ref)
        return self.area_crud.get_graph(request)

    def get__by_graph_id__graph_id(self,                                                    # Get graph by graph_id (URL param)
                                   graph_id : Obj_Id                               ,
                                   namespace: Safe_Str__Id = GRAPH_REF__DEFAULT_NAMESPACE
                                  ) -> Schema__Graph__Get__Response:
        graph_ref = Schema__Graph__Ref(graph_id  = graph_id ,
                                       namespace = namespace)
        request   = Schema__Graph__Get__Request(graph_ref = graph_ref)
        return self.area_crud.get_graph(request)

    def delete(self,                                                                        # Delete graph
               graph_ref: Schema__Graph__Ref
              ) -> Schema__Graph__Delete__Response:
        deleted = self.area_crud.delete_graph(graph_ref = graph_ref)
        return Schema__Graph__Delete__Response(graph_ref = graph_ref,
                                               deleted   = deleted  )

    def exists(self,                                                                        # Check if graph exists
               graph_ref: Schema__Graph__Ref
              ) -> Schema__Graph__Exists__Response:
        exists = self.area_crud.graph_exists(graph_ref = graph_ref)
        return Schema__Graph__Exists__Response(graph_ref = graph_ref,
                                               exists    = exists   )

    def setup_routes(self):
        self.add_route_post(self.create                    )
        self.add_route_post(self.get                       )
        self.add_route_get (self.get__by_cache_id__cache_id)
        self.add_route_get (self.get__by_graph_id__graph_id)
        self.add_route_post(self.delete                    )
        self.add_route_post(self.exists                    )
        return self