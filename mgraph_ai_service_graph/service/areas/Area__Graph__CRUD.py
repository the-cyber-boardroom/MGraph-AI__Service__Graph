from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                      import type_safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                   import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request      import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response     import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request         import Schema__Graph__Get__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response        import Schema__Graph__Get__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                           import Graph__Service


class Area__Graph__CRUD(Type_Safe):                                             # Graph CRUD operations area

    graph_service: Graph__Service

    def create_graph(self,                                                      # Create a new empty graph
                     request: Schema__Graph__Create__Request
                ) -> Schema__Graph__Create__Response:

        graph_ref = request.graph_ref or Schema__Graph__Ref()                   # Use provided ref or create default
        mgraph    = self.graph_service.create_new_graph()                       # Always create new graph for create operation
        cached    = False

        if request.auto_cache:
            resolved_ref = self.graph_service.save_graph_ref(mgraph    = mgraph   ,
                                                             graph_ref = graph_ref)
            cached = True
        else:
            resolved_ref = Schema__Graph__Ref(graph_id  = mgraph.graph.graph_id(),
                                              namespace = graph_ref.namespace    )

        return Schema__Graph__Create__Response(graph_ref = resolved_ref,
                                               cached    = cached      )

    def get_graph(self,                                                         # Retrieve a graph
                  request: Schema__Graph__Get__Request
                 ) -> Schema__Graph__Get__Response:

        try:
            mgraph, resolved_ref = self.graph_service.resolve_graph_ref(request.graph_ref)
            return Schema__Graph__Get__Response(graph_ref = resolved_ref,
                                                mgraph    = mgraph      ,
                                                success   = True        )
        except Exception:                                                       # Graph not found - return failure response
            return Schema__Graph__Get__Response(graph_ref = request.graph_ref,
                                                success   = False            )

    @type_safe
    def delete_graph(self,                                                      # Delete a graph from cache
                     graph_ref: Schema__Graph__Ref
                    ) -> bool:

        delete_response = self.graph_service.delete_graph(cache_id  = graph_ref.cache_id ,
                                                          graph_id  = graph_ref.graph_id ,
                                                          namespace = graph_ref.namespace)
        if delete_response:
            return delete_response.get('status') == 'success'
        return False

    @type_safe
    def graph_exists(self,                                                      # Check if graph exists in cache
                     graph_ref: Schema__Graph__Ref
                ) -> bool:

        return self.graph_service.graph_exists(cache_id  = graph_ref.cache_id ,
                                               graph_id  = graph_ref.graph_id ,
                                               namespace = graph_ref.namespace)