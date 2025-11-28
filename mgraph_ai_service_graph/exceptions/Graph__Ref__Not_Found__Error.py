from mgraph_ai_service_graph.exceptions.Graph__Ref__Error import Graph__Ref__Error


class Graph__Ref__Not_Found__Error(Graph__Ref__Error):                          # Raised when referenced graph does not exist
    status_code : int = 404
    error_type  : str = 'GRAPH_REF_NOT_FOUND'
    message     : str = 'Graph not found'