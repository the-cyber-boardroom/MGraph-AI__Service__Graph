from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_ref.Node_Id                                      import Node_Id
from mgraph_ai_service_graph.schemas.graph_ref.Edge_Id                                      import Edge_Id
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request         import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response        import Schema__Graph__Find_Nodes__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Node__Response         import Schema__Graph__Find_Node__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Edges__Response        import Schema__Graph__Find_Edges__Response
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Edge__Data                  import Schema__Graph__Edge__Data
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service


class Area__Graph__Query(Type_Safe):                                            # Graph query operations area

    graph_service: Graph__Service

    def find_nodes_by_type(self,                                                # Find all nodes of a specific type
                           request: Schema__Graph__Find_Nodes__Request
                          ) -> Schema__Graph__Find_Nodes__Response:

        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)

        node_type_str  = str(request.node_type)
        mgraph_index   = mgraph.index()
        all_node_ids   = list(mgraph_index.nodes_by_type().get(node_type_str, set()))   # Use index for O(1) lookup by type

        offset = int(request.offset)
        limit  = int(request.limit )

        paginated_node_ids = all_node_ids[offset:offset + limit]
        node_ids_typed     = [Node_Id(str(node_id)) for node_id in paginated_node_ids]
        total_found        = Safe_UInt(len(all_node_ids))
        has_more           = (offset + limit) < len(all_node_ids)

        return Schema__Graph__Find_Nodes__Response(graph_ref   = resolved_ref  ,
                                                   node_ids    = node_ids_typed,
                                                   total_found = total_found   ,
                                                   has_more    = has_more      )

    def find_node_by_id(self,                                                   # Find a specific node by ID
                        graph_ref : Schema__Graph__Ref,
                        node_id   : Node_Id
                   ) -> Schema__Graph__Find_Node__Response:

        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)
        mgraph_data          = mgraph.data()
        domain_node          = mgraph_data.node(Obj_Id(node_id))                        # Returns Domain__MGraph__Node or None

        if domain_node is None:
            return Schema__Graph__Find_Node__Response(graph_ref = resolved_ref,
                                                      node_id   = node_id     ,
                                                      found     = False       )

        node_data = domain_node.node.data
        return Schema__Graph__Find_Node__Response(graph_ref = resolved_ref  ,
                                                  node_id   = node_id       ,
                                                  node_data = node_data     ,
                                                  found     = True          )

    def find_edges_by_type(self,                                                # Find all edges of a specific type
                           graph_ref : Schema__Graph__Ref,
                           edge_type : str
                      ) -> Schema__Graph__Find_Edges__Response:

        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)
        mgraph_index         = mgraph.index()
        mgraph_data          = mgraph.data()

        edge_ids = mgraph_index.edges_by_type().get(edge_type, set())           # Use index for O(1) lookup by type

        edges_typed = []
        for edge_id in edge_ids:
            domain_edge = mgraph_data.edge(edge_id)
            if domain_edge:
                edge_schema   = domain_edge.edge.data                           # Access schema via domain -> model -> schema
                edge_data_obj = edge_schema.edge_data

                edge_data_typed = {}                                            # Convert edge_data to dict
                if edge_data_obj:
                    edge_data_dict = edge_data_obj.json() if hasattr(edge_data_obj, 'json') else {}
                    edge_data_typed = {Safe_Str__Key(str(k)): Safe_Str__Text(str(v))
                                       for k, v in edge_data_dict.items()}

                edge_type_name = edge_schema.edge_type.__name__ if edge_schema.edge_type else edge_type

                edges_typed.append(Schema__Graph__Edge__Data(
                    edge_id      = Edge_Id(str(edge_schema.edge_id))      ,
                    from_node_id = Node_Id(str(edge_schema.from_node_id)) ,
                    to_node_id   = Node_Id(str(edge_schema.to_node_id))   ,
                    edge_type    = edge_type_name                         ,
                    edge_data    = edge_data_typed                        ))

        return Schema__Graph__Find_Edges__Response(graph_ref   = resolved_ref              ,
                                                   edge_type   = edge_type                 ,
                                                   edges       = edges_typed               ,
                                                   total_found = Safe_UInt(len(edges_typed)))