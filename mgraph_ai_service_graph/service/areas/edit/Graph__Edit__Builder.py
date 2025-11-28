from osbot_utils.type_safe.Type_Safe                                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                        import Obj_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                                       import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_edit.builder.Schema__Graph__Builder__Add_Connected__Request  import Schema__Graph__Builder__Add_Connected__Request
from mgraph_ai_service_graph.schemas.graph_edit.builder.Schema__Graph__Builder__Add_Connected__Response import Schema__Graph__Builder__Add_Connected__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                                               import Graph__Service


class Graph__Edit__Builder(Type_Safe):
    graph_service: Graph__Service

    def add_connected_node(self,                                                # Add node connected to existing node
                           request: Schema__Graph__Builder__Add_Connected__Request
                          ) -> Schema__Graph__Builder__Add_Connected__Response:

        graph_ref                = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref     = self.graph_service.resolve_graph_ref(graph_ref)
        builder                  = mgraph.builder()

        builder.set_current_node(request.from_node_id)

        if request.predicate:
            builder.add_connected_node(value     = request.value    ,
                                       predicate = request.predicate)
        else:
            builder.add_connected_node(value = request.value)

        node_id = Obj_Id(str(builder.current_node().node_id))
        edge_id = Obj_Id(str(builder.current_edge().edge_id)) if builder.current_edge() else None
        cached  = False

        if request.auto_cache:
            resolved_ref = self.graph_service.save_graph_ref(mgraph    = mgraph      ,
                                                             graph_ref = resolved_ref)
            cached = True

        return Schema__Graph__Builder__Add_Connected__Response(graph_ref = resolved_ref,
                                                               node_id   = node_id     ,
                                                               edge_id   = edge_id     ,
                                                               cached    = cached      ,
                                                               success   = True        )