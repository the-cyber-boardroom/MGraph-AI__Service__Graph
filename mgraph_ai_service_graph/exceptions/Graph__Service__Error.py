from typing                                                                     import Dict

class Graph__Service__Error(Exception):                                         # Base exception for all Graph Service errors
    status_code : int           = 500                                           # HTTP status code
    error_type  : str           = 'GRAPH_SERVICE_ERROR'                         # Machine-readable error type
    message     : str           = 'An error occurred in the Graph Service'      # Human-readable message
    details     : Dict          = None                                          # Additional context

    def __init__(self,
                 message : str  = None,
                 details : Dict = None):
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)