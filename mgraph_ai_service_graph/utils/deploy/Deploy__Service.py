from osbot_fast_api_serverless.deploy.Deploy__Serverless__Fast_API   import Deploy__Serverless__Fast_API
from osbot_utils.utils.Env                                           import get_env
from mgraph_ai_service_graph.config                                  import SERVICE_NAME, LAMBDA_DEPENDENCIES__GRAPH_SERVICE
from mgraph_ai_service_graph.fast_api.lambda_handler                 import run

class Deploy__Service(Deploy__Serverless__Fast_API):

    def deploy_lambda(self):
        with super().deploy_lambda() as _:
            # Add any service-specific environment variables here
            # Example: _.set_env_variable('BASE_API_KEY', get_env('BASE_API_KEY'))
            #FAST_API__AUTH__API_KEY__NAME
            #FAST_API__AUTH__API_KEY__VALUE
            _.set_env_variable("AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME" , get_env("AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME"  ))
            _.set_env_variable("AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE", get_env("AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE" ))
            _.set_env_variable("URL__TARGET_SERVER__CACHE_SERVICE"            , get_env("URL__TARGET_SERVER__CACHE_SERVICE"             ))
            return _

    def handler(self):
        return run

    def lambda_dependencies(self):
        return LAMBDA_DEPENDENCIES__GRAPH_SERVICE

    def lambda_name(self):
        return SERVICE_NAME