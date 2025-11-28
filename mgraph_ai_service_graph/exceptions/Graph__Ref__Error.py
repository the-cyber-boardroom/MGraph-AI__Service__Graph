from mgraph_ai_service_graph.exceptions.Graph__Service__Error import Graph__Service__Error


class Graph__Ref__Error(Graph__Service__Error):                                 # Base exception for Graph Ref errors
    status_code : int = 400
    error_type  : str = 'GRAPH_REF_ERROR'
    message     : str = 'Invalid graph reference'