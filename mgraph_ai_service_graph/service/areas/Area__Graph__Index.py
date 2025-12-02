from typing                                                                                      import Optional
from osbot_utils.type_safe.Type_Safe                                                             import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                             import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                                 import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id                  import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash         import Safe_Str__Cache_Hash
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                                import Schema__Graph__Ref
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                                import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                                import Edge_Id
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Request             import Schema__Graph__Index__Full__Request
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Full__Response            import Schema__Graph__Index__Full__Response, Schema__Graph__Index__Main, Schema__Graph__Index__Values
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Node_Edges                import Schema__Graph__Index__Node_Edges__Request, Schema__Graph__Index__Node_Edges__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__By_Predicate              import Schema__Graph__Index__By_Predicate__Request, Schema__Graph__Index__By_Predicate__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Value_Lookup              import Schema__Graph__Index__Value_Lookup__Request, Schema__Graph__Index__Value_Lookup__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__Stats                     import Schema__Graph__Index__Stats__Request, Schema__Graph__Index__Stats__Response
from mgraph_ai_service_graph.schemas.graph_index.Schema__Graph__Index__ReIndex                   import Schema__Graph__Index__ReIndex__Request, Schema__Graph__Index__ReIndex__Response
from mgraph_ai_service_graph.service.graph.Graph__Service                                        import Graph__Service


INDEX_DATA_FILE_ID__MAIN   = 'index__main'
INDEX_DATA_FILE_ID__VALUES = 'index__values'


class Area__Graph__Index(Type_Safe):                                            # Graph index operations area

    graph_service: Graph__Service

    # ═══════════════════════════════════════════════════════════════════════════════
    # Full Index Retrieval
    # ═══════════════════════════════════════════════════════════════════════════════

    def get_full_index(self,                                                    # Get complete index for a graph
                       request: Schema__Graph__Index__Full__Request
                      ) -> Schema__Graph__Index__Full__Response:

        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)

        from_cache   = False
        main_index   = None
        values_index = None

        if request.from_cache and resolved_ref.cache_id:                        # Try to load from cached index
            cached_main   = self._load_cached_index(resolved_ref, INDEX_DATA_FILE_ID__MAIN)
            cached_values = self._load_cached_index(resolved_ref, INDEX_DATA_FILE_ID__VALUES) if request.include_values else None

            if cached_main:
                main_index = Schema__Graph__Index__Main(**cached_main)
                from_cache = True
                if cached_values:
                    values_index = Schema__Graph__Index__Values(**cached_values)

        if not main_index:                                                      # Build index from graph if not cached
            mgraph_index = mgraph.index()
            main_index   = self._build_main_index_schema(mgraph_index)

            if request.include_values:
                values_index = self._build_values_index_schema(mgraph_index)

        return Schema__Graph__Index__Full__Response(graph_ref    = resolved_ref ,
                                                    main_index   = main_index   ,
                                                    values_index = values_index ,
                                                    from_cache   = from_cache   ,
                                                    success      = True         )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Node Edges Lookup
    # ═══════════════════════════════════════════════════════════════════════════════

    def get_node_edges(self,                                                    # Get edges for a specific node
                       request: Schema__Graph__Index__Node_Edges__Request
                      ) -> Schema__Graph__Index__Node_Edges__Response:

        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)

        mgraph_index = mgraph.index()
        node_id_obj  = Obj_Id(str(request.node_id))

        incoming_edges = []
        outgoing_edges = []

        if request.direction in ('incoming', 'both'):                           # Get incoming edges
            if request.edge_type:                                               # Filter by edge type (string name)
                node_edges_by_type = mgraph_index.nodes_to_incoming_edges_by_type().get(node_id_obj, {})
                edge_ids = self._get_edges_matching_type(node_edges_by_type, request.edge_type)
            else:
                edge_ids = mgraph_index.get_node_id_incoming_edges(node_id_obj)
            incoming_edges = [Edge_Id(str(eid)) for eid in edge_ids]

        if request.direction in ('outgoing', 'both'):                           # Get outgoing edges
            if request.edge_type:                                               # Filter by edge type (string name)
                node_edges_by_type = mgraph_index.nodes_to_outgoing_edges_by_type().get(node_id_obj, {})
                edge_ids = self._get_edges_matching_type(node_edges_by_type, request.edge_type)
            else:
                edge_ids = mgraph_index.get_node_id_outgoing_edges(node_id_obj)
            outgoing_edges = [Edge_Id(str(eid)) for eid in edge_ids]

        return Schema__Graph__Index__Node_Edges__Response(
            graph_ref      = resolved_ref                       ,
            node_id        = request.node_id                    ,
            incoming_edges = incoming_edges                     ,
            outgoing_edges = outgoing_edges                     ,
            incoming_count = Safe_UInt(len(incoming_edges))     ,
            outgoing_count = Safe_UInt(len(outgoing_edges))     ,
            from_cache     = False                              ,
            success        = True                               )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Predicate-Based Lookup
    # ═══════════════════════════════════════════════════════════════════════════════

    def get_by_predicate(self,                                                  # Find nodes by predicate relationship
                         request: Schema__Graph__Index__By_Predicate__Request
                        ) -> Schema__Graph__Index__By_Predicate__Response:

        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)

        mgraph_index  = mgraph.index()
        predicate_str = str(request.predicate) if request.predicate else ''

        target_node_ids = []
        edge_id_list    = []

        if request.from_node_id:                                                # Optimized path when from_node provided
            from_node_obj = Obj_Id(str(request.from_node_id))
            predicate_id  = Safe_Str__Id(predicate_str)

            if request.direction == 'outgoing':                                 # Use get_nodes_by_predicate for O(1) lookup
                target_nodes = mgraph_index.get_nodes_by_predicate(from_node_obj, predicate_id)
                target_node_ids = [Node_Id(str(n)) for n in target_nodes]

                edge_ids = mgraph_index.get_node_outgoing_edges_by_predicate(from_node_obj, predicate_id)
                edge_id_list = [Edge_Id(str(e)) for e in edge_ids]
            else:                                                               # Incoming direction
                edge_ids = mgraph_index.get_node_incoming_edges_by_predicate(from_node_obj, predicate_id)
                edge_id_list = [Edge_Id(str(e)) for e in edge_ids]

                for edge_id in edge_ids:                                        # Get source nodes from edges
                    edge_nodes = mgraph_index.edges_to_nodes().get(edge_id)
                    if edge_nodes:
                        from_node, _ = edge_nodes
                        target_node_ids.append(Node_Id(str(from_node)))
        else:                                                                   # No from_node - get all edges with predicate
            edge_ids = mgraph_index.index_data.edges_by_predicate.get(predicate_str, set())
            edge_id_list = [Edge_Id(str(e)) for e in edge_ids]

            for edge_id in edge_ids:                                            # Extract target nodes based on direction
                edge_nodes = mgraph_index.edges_to_nodes().get(edge_id)
                if edge_nodes:
                    from_node, to_node = edge_nodes
                    if request.direction == 'outgoing':
                        target_node_ids.append(Node_Id(str(to_node)))
                    else:
                        target_node_ids.append(Node_Id(str(from_node)))

        return Schema__Graph__Index__By_Predicate__Response(
            graph_ref       = resolved_ref                      ,
            predicate       = request.predicate                 ,
            from_node_id    = request.from_node_id              ,
            target_node_ids = target_node_ids                   ,
            edge_ids        = edge_id_list                      ,
            total_found     = Safe_UInt(len(target_node_ids))   ,
            from_cache      = False                             ,
            success         = True                              )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Value Lookup
    # ═══════════════════════════════════════════════════════════════════════════════

    def value_lookup(self,                                                      # Lookup value node by value or hash
                     request: Schema__Graph__Index__Value_Lookup__Request
                    ) -> Schema__Graph__Index__Value_Lookup__Response:

        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)

        mgraph_index = mgraph.index()
        values_index = mgraph_index.values_index

        node_id    = None
        value_hash = request.value_hash
        found      = False

        if request.value_hash:                                                  # Lookup by hash (O(1))
            hash_str    = str(request.value_hash)
            node_id_obj = values_index.get_node_id_by_hash(hash_str)
            if node_id_obj:
                node_id = Node_Id(str(node_id_obj))
                found   = True

        elif request.value is not None:                                         # Lookup by value
            value_type  = self._resolve_value_type(request.value_type)
            typed_value = self._convert_value(request.value, value_type)
            node_id_obj = values_index.get_node_id_by_value(value_type = value_type         ,
                                                            value      = typed_value        ,
                                                            key        = request.key or ''  )
            if node_id_obj:
                node_id = Node_Id(str(node_id_obj))
                raw_hash = values_index.index_data.node_to_hash.get(node_id_obj)
                if raw_hash:
                    value_hash = Safe_Str__Cache_Hash(str(raw_hash))
                found = True

        return Schema__Graph__Index__Value_Lookup__Response(
            graph_ref  = resolved_ref       ,
            node_id    = node_id            ,
            value      = request.value      ,
            value_type = request.value_type ,
            value_hash = value_hash         ,
            found      = found              ,
            from_cache = False              ,
            success    = True               )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Index Statistics
    # ═══════════════════════════════════════════════════════════════════════════════

    def get_stats(self,                                                         # Get index statistics
                  request: Schema__Graph__Index__Stats__Request
                 ) -> Schema__Graph__Index__Stats__Response:

        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)

        mgraph_index = mgraph.index()
        values_index = mgraph_index.values_index

        nodes_by_type  = mgraph_index.nodes_by_type()
        edges_by_type  = mgraph_index.edges_by_type()
        edges_by_pred  = mgraph_index.index_data.edges_by_predicate
        values_by_type = values_index.index_data.values_by_type if values_index else {}

        nodes_by_type_counts  = {self._type_to_str(k): len(v) for k, v in nodes_by_type.items()}
        edges_by_type_counts  = {self._type_to_str(k): len(v) for k, v in edges_by_type.items()}
        edges_by_pred_counts  = {str(k): len(v) for k, v in edges_by_pred.items()}
        values_by_type_counts = {self._type_to_str(k): len(v) for k, v in values_by_type.items()}

        index_cached = self._is_index_cached(resolved_ref)

        return Schema__Graph__Index__Stats__Response(
            graph_ref                 = resolved_ref                                 ,
            total_nodes               = Safe_UInt(sum(nodes_by_type_counts.values())),
            node_types_count          = Safe_UInt(len(nodes_by_type_counts))         ,
            nodes_by_type_counts      = nodes_by_type_counts                         ,
            total_edges               = Safe_UInt(sum(edges_by_type_counts.values())),
            edge_types_count          = Safe_UInt(len(edges_by_type_counts))         ,
            edges_by_type_counts      = edges_by_type_counts                         ,
            total_predicates          = Safe_UInt(len(edges_by_pred_counts))         ,
            edges_by_predicate_counts = edges_by_pred_counts                         ,
            total_value_nodes         = Safe_UInt(sum(values_by_type_counts.values())),
            value_types_count         = Safe_UInt(len(values_by_type_counts))        ,
            values_by_type_counts     = values_by_type_counts                        ,
            index_cached              = index_cached                                 ,
            from_cache                = False                                        ,
            success                   = True                                         )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Re-Index
    # ═══════════════════════════════════════════════════════════════════════════════

    def re_index(self,                                                          # Force rebuild and cache index
                 request: Schema__Graph__Index__ReIndex__Request
                ) -> Schema__Graph__Index__ReIndex__Response:

        graph_ref            = request.graph_ref or Schema__Graph__Ref()
        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)

        # Force rebuild by creating fresh index from graph
        from mgraph_db.mgraph.actions.MGraph__Index import MGraph__Index
        mgraph_index = MGraph__Index.from_graph(mgraph.graph)

        values_index = mgraph_index.values_index

        nodes_indexed    = sum(len(v) for v in mgraph_index.nodes_by_type().values())
        edges_indexed    = sum(len(v) for v in mgraph_index.edges_by_type().values())
        values_indexed   = sum(len(v) for v in values_index.index_data.values_by_type.values()) if values_index else 0
        predicates_found = len(mgraph_index.index_data.edges_by_predicate)

        index_cached = False
        if request.cache_index and resolved_ref.cache_id:
            self._cache_index_data(mgraph_index, resolved_ref)
            index_cached = True

        return Schema__Graph__Index__ReIndex__Response(
            graph_ref        = resolved_ref                 ,
            nodes_indexed    = Safe_UInt(nodes_indexed)     ,
            edges_indexed    = Safe_UInt(edges_indexed)     ,
            values_indexed   = Safe_UInt(values_indexed)    ,
            predicates_found = Safe_UInt(predicates_found)  ,
            index_cached     = index_cached                 ,
            success          = True                         )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Cache Index Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    def cache_index(self,                                                       # Cache the current index for a graph
                    graph_ref: Schema__Graph__Ref
                   ) -> bool:

        mgraph, resolved_ref = self.graph_service.resolve_graph_ref(graph_ref)
        mgraph_index         = mgraph.index()
        return self._cache_index_data(mgraph_index, resolved_ref)

    # ═══════════════════════════════════════════════════════════════════════════════
    # Private Helper Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def _get_edges_matching_type(self,                                          # Match edges by type name (handles type→str conversion)
                                 edges_by_type: dict,
                                 type_name    : str
                                ) -> set:
        """Find edges where the type key matches the given type name string.

        The index uses Python type objects as keys, but REST passes string names.
        This method handles the matching by comparing __name__ or str() of type keys.
        """
        for type_key, edge_ids in edges_by_type.items():
            key_name = type_key.__name__ if isinstance(type_key, type) else str(type_key)
            if key_name == type_name or str(type_key) == type_name:
                return edge_ids
        return set()

    def _build_main_index_schema(self, mgraph_index) -> Schema__Graph__Index__Main:
        """Convert MGraph__Index to Schema__Graph__Index__Main"""

        def set_to_list(s):                                                     # Convert sets to lists for JSON serialization
            return list(str(x) for x in s) if s else []

        def dict_set_to_dict_list(d):
            return {self._type_to_str(k): set_to_list(v) for k, v in d.items()} if d else {}

        def dict_dict_set_to_nested(d):
            return {str(k): dict_set_to_dict_list(v) for k, v in d.items()} if d else {}

        def tuple_to_list(t):
            return [str(t[0]), str(t[1])] if t else []

        def dict_tuple_to_dict_list(d):
            return {str(k): tuple_to_list(v) for k, v in d.items()} if d else {}

        index_data = mgraph_index.index_data

        return Schema__Graph__Index__Main(
            nodes_by_type                   = dict_set_to_dict_list(mgraph_index.nodes_by_type())                    ,
            nodes_types                     = {str(k): self._type_to_str(v) for k, v in index_data.nodes_types.items()}   ,
            edges_by_type                   = dict_set_to_dict_list(mgraph_index.edges_by_type())                    ,
            edges_types                     = {str(k): self._type_to_str(v) for k, v in index_data.edges_types.items()}   ,
            edges_to_nodes                  = dict_tuple_to_dict_list(mgraph_index.edges_to_nodes())                 ,
            nodes_to_outgoing_edges         = dict_set_to_dict_list(mgraph_index.nodes_to_outgoing_edges())          ,
            nodes_to_incoming_edges         = dict_set_to_dict_list(mgraph_index.nodes_to_incoming_edges())          ,
            nodes_to_outgoing_edges_by_type = dict_dict_set_to_nested(mgraph_index.nodes_to_outgoing_edges_by_type()),
            nodes_to_incoming_edges_by_type = dict_dict_set_to_nested(mgraph_index.nodes_to_incoming_edges_by_type()),
            edges_predicates                = {str(k): str(v) for k, v in index_data.edges_predicates.items()}       ,
            edges_by_predicate              = dict_set_to_dict_list(index_data.edges_by_predicate)                   ,
            edges_by_incoming_label         = dict_set_to_dict_list(index_data.edges_by_incoming_label)              ,
            edges_by_outgoing_label         = dict_set_to_dict_list(index_data.edges_by_outgoing_label)              )

    def _build_values_index_schema(self, mgraph_index) -> Schema__Graph__Index__Values:
        """Convert MGraph__Index__Values to Schema__Graph__Index__Values"""

        values_index = mgraph_index.values_index
        if not values_index:
            return Schema__Graph__Index__Values()

        values_data = values_index.index_data

        return Schema__Graph__Index__Values(
            hash_to_node   = {str(k): str(v) for k, v in values_data.hash_to_node.items()}                  ,
            node_to_hash   = {str(k): str(v) for k, v in values_data.node_to_hash.items()}                  ,
            values_by_type = {self._type_to_str(k): set(v) for k, v in values_data.values_by_type.items()}  ,
            type_by_value  = {str(k): self._type_to_str(v) for k, v in values_data.type_by_value.items()}   )

    def _load_cached_index(self,                                                # Load index from cache data file
                           graph_ref    : Schema__Graph__Ref,
                           data_file_id : str
                          ) -> Optional[dict]:

        if not graph_ref.cache_id:
            return None

        cache_client = self.graph_service.graph_cache_client.cache_client
        return cache_client.data().retrieve().data__json__with__id(
            cache_id     = graph_ref.cache_id  ,
            namespace    = graph_ref.namespace ,
            data_file_id = data_file_id        )

    def _cache_index_data(self,                                                 # Cache index data (separate from graph)
                          mgraph_index,
                          graph_ref: Schema__Graph__Ref
                         ) -> bool:

        if not graph_ref.cache_id:
            return False

        cache_client = self.graph_service.graph_cache_client.cache_client

        main_index = self._build_main_index_schema(mgraph_index)                # Build and cache main index
        cache_client.data_store().data__store_json__with__id(
            cache_id     = graph_ref.cache_id       ,
            namespace    = graph_ref.namespace      ,
            data_file_id = INDEX_DATA_FILE_ID__MAIN ,
            body         = main_index.json()        )

        values_index = self._build_values_index_schema(mgraph_index)            # Build and cache values index
        cache_client.data_store().data__store_json__with__id(
            cache_id     = graph_ref.cache_id         ,
            namespace    = graph_ref.namespace        ,
            data_file_id = INDEX_DATA_FILE_ID__VALUES ,
            body         = values_index.json()        )

        return True

    def _is_index_cached(self, graph_ref: Schema__Graph__Ref) -> bool:
        """Check if index is cached for this graph"""
        return self._load_cached_index(graph_ref, INDEX_DATA_FILE_ID__MAIN) is not None

    def _resolve_value_type(self, type_name: str) -> type:
        """Resolve type name string to Python type for value index lookups"""
        type_map = { 'str'   : str   ,
                     'int'   : int   ,
                     'float' : float ,
                     'bool'  : bool  ,
                     'string': str   ,                                          # Alias
                     'integer': int  }                                          # Alias
        return type_map.get(type_name, str)

    def _convert_value(self, value: str, value_type: type):
        """Convert string value to typed value for index lookup"""
        if value_type == str:
            return value
        if value_type == int:
            return int(value)
        if value_type == float:
            return float(value)
        if value_type == bool:
            return value.lower() in ('true', '1', 'yes')
        return value

    def _type_to_str(self, t) -> str:
        """Convert a type to its string representation for REST serialization"""
        if t is None:
            return 'None'
        if isinstance(t, type):
            return t.__name__
        return str(t)