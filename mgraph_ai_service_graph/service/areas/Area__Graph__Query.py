from typing                                                                                 import List
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Request         import Schema__Graph__Find_Nodes__Request
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Find_Nodes__Response        import Schema__Graph__Find_Nodes__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                                   import Graph__Service


class Area__Graph__Query(Type_Safe):                                        # Graph query operations area - handles searching and exploration
                                                                            # This area provides read-only query operations on graphs using
                                                                            # MGraph's powerful query system.

    graph_service: Graph__Service                                           # Injected graph service dependency

    def find_nodes_by_type(self,                                           # Find all nodes of a specific type in a graph
                           request: Schema__Graph__Find_Nodes__Request     # Query request with graph_id, node_type, limit, offset
                          ) -> Schema__Graph__Find_Nodes__Response:        # Response with list of node_ids and pagination info


        graph = self.graph_service.get_or_create_graph(graph_id  = str(request.graph_id),           # Retrieve graph
                                                       namespace = "graphs")

        query_result = graph.query().by_type(str(request.node_type))                                # Query nodes by type using MGraph's query API
        all_node_ids = list(query_result.nodes_ids())

        offset = int(request.offset)                                                                # Apply pagination
        limit  = int(request.limit)

        paginated_node_ids = all_node_ids[offset:offset + limit]

        # todo: see if we need this
        node_ids_typed = [Obj_Id(str(node_id)) for node_id in paginated_node_ids]                   # Convert to Obj_Id type

        total_found = Safe_UInt(len(all_node_ids))                                                  # Calculate pagination info
        has_more    = (offset + limit) < len(all_node_ids)

        return Schema__Graph__Find_Nodes__Response(graph_id    = request.graph_id,
                                                   node_ids    = node_ids_typed   ,
                                                   total_found = total_found      ,
                                                   has_more    = has_more         )

    def find_node_by_id(self,                           # Find a specific node by ID
                        graph_id: str,                  # Target graph
                        node_id : str                   # Node to find
                   ) -> dict:                           # Node data as dict | todo: convert to type_safe class

        graph = self.graph_service.get_or_create_graph(graph_id, "graphs")

        node = graph.query().node(node_id)                                                      # Use MGraph's query API

        if node is None:
            raise KeyError(f"Node {node_id} not found in graph {graph_id}")

        # todo: convert to type_safe class
        return { "node_id"  : str(node.node_id),
                 "node_type": str(node.node_type),
                 "node_data": node.node_data
        }

    # todo: see if there is not a better way to calculate this using MGraph (for example using the indexes)
    def get_neighbors(self,                             # Get all neighboring nodes (connected by edges)
                      graph_id: str,                    # Target graph
                      node_id : str                     # Node to get neighbors for
                 ) -> List[str]:                        # List of neighbor node IDs | todo: return type_safe list

        graph    = self.graph_service.get_or_create_graph(graph_id, "graphs")
        query    = graph.query()                                                # Use MGraph's query API to get edges
        outgoing = query.from_node(node_id).edges()                             # Get outgoing edges
        incoming = query.to_node(node_id).edges()                               # Get incoming edges

        neighbor_ids = set()                                                    # Collect unique neighbor IDs

        for edge in outgoing:
            neighbor_ids.add(str(edge.to_node_id))

        for edge in incoming:
            neighbor_ids.add(str(edge.from_node_id))

        return list(neighbor_ids)                                                    # todo: return type_safe list

    def find_edges_by_type(self,                         # Find all edges of a specific type
                           graph_id : str,               # Target graph
                           edge_type: str                # Type of edges to find
                      ) -> List[dict]:                  # List of edge data dicts    | todo: return type_safe Dict

        graph = self.graph_service.get_or_create_graph(graph_id, "graphs")

        edges = graph.query().by_edge_type(edge_type).edges()                       # Query edges by type

        return [ {                                                                  # todo: return type_safe Dict
                    "edge_id"     : str(edge.edge_id)     ,
                    "from_node_id": str(edge.from_node_id),
                    "to_node_id"  : str(edge.to_node_id)  ,
                    "edge_type"   : str(edge.edge_type)   ,
                    "edge_data"   : edge.edge_data
                 } for edge in edges ]
