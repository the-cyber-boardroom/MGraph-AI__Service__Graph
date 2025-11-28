from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request         import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response        import Schema__Graph__Find_Nodes__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Node__Response         import Schema__Graph__Find_Node__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Edges__Response        import Schema__Graph__Find_Edges__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Edge__Data                  import Schema__Graph__Edge__Data
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Neighbors__Response         import Schema__Graph__Neighbors__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service

# todo this section has quite a number of bugs in how to access the graph data and it is also not using the cache_id when needed

class Area__Graph__Query(Type_Safe):                                            # Graph query operations area

    graph_service: Graph__Service

    def find_nodes_by_type(self,                                                # Find all nodes of a specific type
                           request: Schema__Graph__Find_Nodes__Request
                          ) -> Schema__Graph__Find_Nodes__Response:

        graph_ref                = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref     = self.graph_service.resolve_graph_ref(graph_ref)

        query_result   = mgraph.query().by_type(str(request.node_type))
        all_node_ids   = list(query_result.nodes_ids())

        offset = int(request.offset)
        limit  = int(request.limit)

        paginated_node_ids = all_node_ids[offset:offset + limit]
        node_ids_typed     = [Obj_Id(str(node_id)) for node_id in paginated_node_ids]
        total_found        = Safe_UInt(len(all_node_ids))
        has_more           = (offset + limit) < len(all_node_ids)

        return Schema__Graph__Find_Nodes__Response(graph_ref   = resolved_ref  ,
                                                   node_ids    = node_ids_typed,
                                                   total_found = total_found   ,
                                                   has_more    = has_more      )

    def find_node_by_id(self,                                                   # Find a specific node by ID
                        graph_ref : Schema__Graph__Ref,
                        node_id   : Obj_Id
                   ) -> Schema__Graph__Find_Node__Response:

        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)
        node                 = mgraph.query().mgraph_data.node(str(node_id))

        if node is None:
            return Schema__Graph__Find_Node__Response(graph_ref = resolved_ref,
                                                      node_id   = node_id     ,
                                                      found     = False       )

        node_data_typed = {Safe_Str__Key(k): Safe_Str__Text(str(v))
                          for k, v in (node.node_data or {}).items()}

        return Schema__Graph__Find_Node__Response(graph_ref = resolved_ref              ,
                                                  node_id   = Obj_Id(str(node.node_id)) ,
                                                  node_type = str(node.node_type)       ,
                                                  node_data = node_data_typed           ,
                                                  found     = True                      )

    def get_neighbors(self,                                                     # Get all neighboring nodes
                      graph_ref : Schema__Graph__Ref,
                      node_id   : Obj_Id
                 ) -> Schema__Graph__Neighbors__Response:

        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)
        query                = mgraph.query()
        outgoing             = query.from_node(str(node_id)).edges()
        incoming             = query.to_node(str(node_id)).edges()

        neighbor_ids = set()

        for edge in outgoing:
            neighbor_ids.add(str(edge.to_node_id))

        for edge in incoming:
            neighbor_ids.add(str(edge.from_node_id))

        neighbor_ids_typed = [Obj_Id(nid) for nid in neighbor_ids]

        return Schema__Graph__Neighbors__Response(graph_ref    = resolved_ref          ,
                                                  node_id      = node_id               ,
                                                  neighbor_ids = neighbor_ids_typed    ,
                                                  total_found  = Safe_UInt(len(neighbor_ids_typed)))

    def find_edges_by_type(self,                                                # Find all edges of a specific type
                           graph_ref : Schema__Graph__Ref,
                           edge_type : str
                      ) -> Schema__Graph__Find_Edges__Response:

        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)
        edges                = mgraph.query().by_edge_type(edge_type).edges()

        edges_typed = []
        for edge in edges:
            edge_data_typed = {Safe_Str__Key(k): Safe_Str__Text(str(v))
                               for k, v in (edge.edge_data or {}).items()}

            edges_typed.append(Schema__Graph__Edge__Data(
                edge_id      = Obj_Id(str(edge.edge_id))     ,
                from_node_id = Obj_Id(str(edge.from_node_id)),
                to_node_id   = Obj_Id(str(edge.to_node_id))  ,
                edge_type    = str(edge.edge_type)           ,
                edge_data    = edge_data_typed               ))

        return Schema__Graph__Find_Edges__Response(graph_ref   = resolved_ref       ,
                                                   edge_type   = edge_type          ,
                                                   edges       = edges_typed        ,
                                                   total_found = Safe_UInt(len(edges_typed)))