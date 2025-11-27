from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                              import type_safe
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Request              import Schema__Graph__Create__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Create__Response             import Schema__Graph__Create__Response
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Request                 import Schema__Graph__Get__Request
from mgraph_ai_service_graph.schemas.graph_crud.Schema__Graph__Get__Response                import Schema__Graph__Get__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service



class Area__Graph__CRUD(Type_Safe):                                         # Graph CRUD operations area - handles create, read, update, delete

    graph_service: Graph__Service                                           # Injected graph service dependency

    def create_graph(self,                                                  # Create a new empty graph with optional auto-caching
                     request: Schema__Graph__Create__Request                # Creation request with name, auto_cache flag, namespace
                ) -> Schema__Graph__Create__Response:                       # Response with graph_id, counts, and cache status

        mgraph    = self.graph_service.create_new_graph()                   # Create new empty graph
        graph_id  = mgraph.graph.graph_id()
        cached    = False
        cache_id  = None

        if request.auto_cache:                                              # Handle caching if requested
            cache_id = self.graph_service.save_graph(mgraph    = mgraph        ,
                                                     namespace = request.namespace)
            cached    = True

        return Schema__Graph__Create__Response(graph_id       = graph_id          ,
                                               cached         = cached            ,
                                               cache_id       = cache_id          ,
                                               cache_namespace = request.namespace)

    def get_graph(self,                                                    # Retrieve a graph from cache
                  request: Schema__Graph__Get__Request                     # Get request with graph_id and namespace
                 ) -> Schema__Graph__Get__Response:                        # Response with graph metadata and status

        graph_id  = request.graph_id
        cache_id  = request.cache_id
        namespace = request.namespace
        # Retrieve graph from cache
        mgraph = self.graph_service.get_graph(cache_id = cache_id ,
                                              graph_id = graph_id ,
                                              namespace= namespace)

        # Get counts
        success = False

        if mgraph:
            success  = True
            graph_id = mgraph.graph.graph_id()          # use the graph_id from the mgraph


        return Schema__Graph__Get__Response(cache_id =  cache_id ,
                                            graph_id = graph_id  ,
                                            mgraph   = mgraph    ,
                                            #cached     = True         ,        # todo: see how we can figure out here if the value was cached
                                            success = success    )


    @type_safe
    def delete_graph(self,                                                  # Delete a graph from cache
                     cache_id  : Random_Guid  = None,                       # Cache_id for graph to delete
                     graph_id  : Obj_Id       = None,                       # Graph to delete
                     namespace : Safe_Str__Id = None                        # Cache namespace
                    ) -> bool:                                              # True if deleted successfully

        delete_response =  self.graph_service.delete_graph(cache_id  = cache_id ,
                                                           graph_id  = graph_id ,
                                                           namespace = namespace)
        if delete_response:
            return delete_response.get('status') == 'success'                            # todo: this should be strongly typed
        return False

    @type_safe
    def graph_exists(self,                                                  # Check if graph exists in cache
                     cache_id  : Random_Guid  = None,                       # Cache_id for graph to retrieve
                     graph_id  : Obj_Id       = None,                       # Graph to check
                     namespace : Safe_Str__Id = None,                       # Cache namespace
                ) -> bool:                                                  # True if exists

        return self.graph_service.graph_exists(cache_id  = cache_id ,
                                               graph_id  = graph_id ,
                                               namespace = namespace)
