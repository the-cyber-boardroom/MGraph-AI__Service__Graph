from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_edit.nodes.Schema__Graph__Delete_Node__Response  import Schema__Graph__Delete_Node__Response
from mgraph_ai_service_graph.schemas.graph_edit.edges.Schema__Graph__Delete_Edge__Response  import Schema__Graph__Delete_Edge__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service


class Graph__Edit__Delete(Type_Safe):
    graph_service: Graph__Service

    def delete_node(self,                                                       # Delete a node from graph
                    graph_ref : Schema__Graph__Ref,
                    node_id   : Obj_Id
               ) -> Schema__Graph__Delete_Node__Response:

        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)
        result               = mgraph.edit().delete_node(node_id=node_id)

        if result:
            resolved_ref = self.graph_service.save_graph_ref(mgraph    = mgraph      ,
                                                             graph_ref = resolved_ref)

        return Schema__Graph__Delete_Node__Response(graph_ref = resolved_ref,
                                                    node_id   = node_id     ,
                                                    deleted   = result      )

    def delete_edge(self,                                                       # Delete an edge from graph
                    graph_ref : Schema__Graph__Ref,
                    edge_id   : Obj_Id
               ) -> Schema__Graph__Delete_Edge__Response:

        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)
        result               = mgraph.edit().delete_edge(edge_id=edge_id)

        if result:
            resolved_ref = self.graph_service.save_graph_ref(mgraph    = mgraph      ,
                                                             graph_ref = resolved_ref)

        return Schema__Graph__Delete_Edge__Response(graph_ref = resolved_ref,
                                                    edge_id   = edge_id     ,
                                                    deleted   = result      )