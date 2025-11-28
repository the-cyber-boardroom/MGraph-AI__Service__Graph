from mgraph_ai_service_graph.exceptions.Graph__Ref__Error import Graph__Ref__Error


class Graph__Ref__Conflict__Error(Graph__Ref__Error):                           # Raised when both cache_id and graph_id are provided
    status_code : int = 400
    error_type  : str = 'GRAPH_REF_CONFLICT'
    message     : str = 'Cannot provide both cache_id and graph_id - use one or the other'