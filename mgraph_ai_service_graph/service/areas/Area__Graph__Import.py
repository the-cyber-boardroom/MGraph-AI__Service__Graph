from mgraph_db.mgraph.MGraph                                                        import MGraph
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                   import Schema__Graph__Ref
from mgraph_ai_service_graph.schemas.graph_import.Schema__Graph__Import             import (Schema__Graph__Import__Request,
                                                                                            Schema__Graph__Import__Compressed__Request,
                                                                                            Schema__Graph__Import__Response)
from mgraph_ai_service_graph.service.graph.Graph__Service                           import Graph__Service


class Area__Graph__Import(Type_Safe):                                           # Graph import operations area

    graph_service: Graph__Service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Import Standard Format
    # ═══════════════════════════════════════════════════════════════════════════════

    def import_graph(self,                                                      # Import a full graph from standard JSON format
                     request: Schema__Graph__Import__Request
                    ) -> Schema__Graph__Import__Response:

        validation_errors = []

        if request.validate:                                                    # Validate graph structure if requested
            validation_errors = self._validate_graph_data(request.graph_data)
            if validation_errors:
                return Schema__Graph__Import__Response(validation_errors = validation_errors,
                                                       success           = False            )

        try:
            mgraph = MGraph.from_json(request.graph_data)                       # Create MGraph from JSON
        except Exception as e:
            return Schema__Graph__Import__Response(
                validation_errors = [f"Failed to parse graph data: {str(e)}"],
                success           = False                                     )

        nodes_count = len(mgraph.data().nodes_ids())
        edges_count = len(mgraph.data().edges_ids())

        graph_ref    = Schema__Graph__Ref(namespace = str(request.namespace))   # Create graph reference
        cached       = False
        index_cached = False

        if request.auto_cache:                                                  # Cache the graph
            resolved_ref = self.graph_service.save_graph_ref(mgraph    = mgraph   ,
                                                             graph_ref = graph_ref)
            graph_ref = resolved_ref
            cached = True

            if request.build_index:                                             # Build and cache index
                index_cached = self._build_and_cache_index(mgraph, graph_ref)
        else:
            graph_ref = Schema__Graph__Ref(graph_id  = mgraph.graph.graph_id() ,
                                           namespace = str(request.namespace)  )

        return Schema__Graph__Import__Response(
            graph_ref         = graph_ref                   ,
            nodes_count       = Safe_UInt(nodes_count)      ,
            edges_count       = Safe_UInt(edges_count)      ,
            index_cached      = index_cached                ,
            cached            = cached                      ,
            validation_errors = validation_errors           ,
            success           = True                        )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Import Compressed Format
    # ═══════════════════════════════════════════════════════════════════════════════

    def import_graph_compressed(self,                                           # Import a full graph from compressed JSON format
                                request: Schema__Graph__Import__Compressed__Request
                               ) -> Schema__Graph__Import__Response:

        try:
            mgraph = MGraph.from_json__compressed(request.graph_data)           # Create MGraph from compressed JSON
        except Exception as e:
            return Schema__Graph__Import__Response(
                validation_errors = [f"Failed to parse compressed graph data: {str(e)}"],
                success           = False                                              )

        nodes_count = len(mgraph.data().nodes_ids())
        edges_count = len(mgraph.data().edges_ids())

        graph_ref    = Schema__Graph__Ref(namespace = str(request.namespace))   # Create graph reference
        cached       = False
        index_cached = False

        if request.auto_cache:                                                  # Cache the graph
            resolved_ref = self.graph_service.save_graph_ref(mgraph    = mgraph   ,
                                                             graph_ref = graph_ref)
            graph_ref = resolved_ref
            cached = True

            if request.build_index:                                             # Build and cache index
                index_cached = self._build_and_cache_index(mgraph, graph_ref)
        else:
            graph_ref = Schema__Graph__Ref(graph_id  = mgraph.graph.graph_id() ,
                                           namespace = str(request.namespace)  )

        return Schema__Graph__Import__Response(
            graph_ref         = graph_ref                   ,
            nodes_count       = Safe_UInt(nodes_count)      ,
            edges_count       = Safe_UInt(edges_count)      ,
            index_cached      = index_cached                ,
            cached            = cached                      ,
            validation_errors = []                          ,
            success           = True                        )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Private Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════
    # todo: see if this can be done with a MGraph.from_json (or even better use MGraph as the graph_data_
    def _validate_graph_data(self, graph_data: dict) -> list:           # Validate graph data structure before import
        errors = []

        if not graph_data:
            errors.append("Graph data is empty or None")
            return errors

        if not isinstance(graph_data, dict):
            errors.append(f"Graph data must be a dictionary, got {type(graph_data).__name__}")
            return errors

        # Check for required top-level keys (based on MGraph JSON structure)
        # The structure can vary - standard vs compressed format
        # Standard format has: graph.model.data.nodes, graph.model.data.edges
        # Compressed format has a different structure

        if 'graph' not in graph_data:
            errors.append("Missing 'graph' key in graph data")
            return errors

        graph = graph_data.get('graph', {})

        if isinstance(graph, dict):
            model = graph.get('model', {})
            if isinstance(model, dict):
                data = model.get('data', {})
                if isinstance(data, dict):
                    if 'nodes' not in data:
                        errors.append("Missing 'nodes' in graph.model.data")
                    if 'edges' not in data:
                        errors.append("Missing 'edges' in graph.model.data")
                else:
                    errors.append("graph.model.data must be a dictionary")
            else:
                errors.append("graph.model must be a dictionary")

        return errors

    def _build_and_cache_index(self, mgraph: MGraph, graph_ref: Schema__Graph__Ref) -> bool:
        """Build and cache index using Area__Graph__Index"""
        #try:
        from mgraph_ai_service_graph.service.areas.Area__Graph__Index import Area__Graph__Index

        area_index = Area__Graph__Index(graph_service = self.graph_service)
        return area_index.cache_index(graph_ref)
        #except Exception:
        #    return False
