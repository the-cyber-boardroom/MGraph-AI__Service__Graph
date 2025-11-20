from mgraph_ai_service_graph import package_name

SERVICE_NAME                             = package_name
FAST_API__TITLE                          = "MGraph-AI Service Graph"
FAST_API__DESCRIPTION                    = "Base template for MGraph-AI microservices"
LAMBDA_DEPENDENCIES__GRAPH_SERVICE      = ['mgraph-db==v1.3.0'                 ,
                                           'osbot-fast-api-serverless==v1.29.0']