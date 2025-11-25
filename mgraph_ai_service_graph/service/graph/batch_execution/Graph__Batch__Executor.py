from typing                                                                         import Dict
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Request  import Schema__Graph__Batch__Request
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Response import Schema__Graph__Batch__Response
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Area                        import Enum__Graph__Area
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                        import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                        import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                       import Area__Graph__Query


class Graph__Batch__Executor(Type_Safe):                                 # Executes batch commands using enum-based method registry

    area_registry: Dict[Enum__Graph__Area, Type_Safe]                   # Registry mapping area → class

    def __init__(self):
        super().__init__()
        self.area_registry = {  Enum__Graph__Area.GRAPH_CRUD  : Area__Graph__CRUD  () ,              # Build static registry
                                Enum__Graph__Area.GRAPH_EDIT  : Area__Graph__Edit  () ,
                                Enum__Graph__Area.GRAPH_QUERY : Area__Graph__Query () }
                                #Enum__Graph__Area.GRAPH_CACHE : Area__Graph__Cache (),
                                #Enum__Graph__Area.GRAPH_EXPORT: Area__Graph__Export(),


    def execute(self, request: Schema__Graph__Batch__Request
                 ) -> Schema__Graph__Batch__Response:
        results = []
        errors = []
        successful = 0
        failed = 0

        for command in request.commands:
            try:
                # 1. Resolve area → class
                area_class = self.area_registry.get(command.area)
                if not area_class:
                    raise ValueError(f"Unknown area: {command.area}")

                # 2. Resolve method → static method
                method_func = getattr(area_class, command.method, None)
                if not method_func:
                    raise ValueError(f"Unknown method: {command.method}")

                # 3. Convert payload → request object
                # (Type_Safe handles JSON → typed object conversion)
                request_obj = None      # ... convert payload to appropriate Request type

                # 4. Execute method
                response = method_func(request_obj)

                # 5. Store result
                results.append(response.json())
                successful += 1

            except Exception as e:
                failed += 1
                errors.append(str(e))

                if request.stop_on_error:
                    break

        return Schema__Graph__Batch__Response(
            results        = results,
            total_commands = len(request.commands),
            successful     = successful,
            failed         = failed,
            errors         = errors
        )