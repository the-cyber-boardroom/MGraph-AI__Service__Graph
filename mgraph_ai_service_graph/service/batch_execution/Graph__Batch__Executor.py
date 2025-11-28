import inspect
from typing                                                                                 import Dict
from mgraph_ai_service_graph.service.areas.Area__Graph__Export                              import Area__Graph__Export
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Request          import Schema__Graph__Batch__Request
from mgraph_ai_service_graph.schemas.batch_execution.Schema__Graph__Batch__Response         import Schema__Graph__Batch__Response
from mgraph_ai_service_graph.schemas.enums.Enum__Graph__Area                                import Enum__Graph__Area
from mgraph_ai_service_graph.service.areas.Area__Graph__CRUD                                import Area__Graph__CRUD
from mgraph_ai_service_graph.service.areas.Area__Graph__Edit                                import Area__Graph__Edit
from mgraph_ai_service_graph.service.areas.Area__Graph__Query                               import Area__Graph__Query



class Graph__Batch__Executor(Type_Safe):                                  # Executes batch commands using enum-based method registry
    area_registry: Dict[Enum__Graph__Area, Type_Safe]                     # Registry mapping area enum → class instance

    def __init__(self, **kwargs):                                                   # Initialize registry with empty entries
        super().__init__(**kwargs)
        self.set_area_instances()


    # todo: see if we can refactor this engine logic into another class
    def set_area_instances(self,                                          # Inject area instances with their dependencies
                           # crud : Area__Graph__CRUD ,                   # todo: see if we need this mode of injection Area__Graph__* instances, or what we do below is enough
                           # edit : Area__Graph__Edit ,
                           # query: Area__Graph__Query
                          ) -> 'Graph__Batch__Executor':                  # Self for chaining
        self.area_registry[Enum__Graph__Area.GRAPH_CRUD  ] = Area__Graph__CRUD  ()
        self.area_registry[Enum__Graph__Area.GRAPH_EDIT  ] = Area__Graph__Edit  ()
        self.area_registry[Enum__Graph__Area.GRAPH_QUERY ] = Area__Graph__Query ()
        self.area_registry[Enum__Graph__Area.GRAPH_EXPORT] = Area__Graph__Export()
        return self

    # todo: refactor this method into smaller components
    #       add feature to validate commands before execution (which will return a nice Type_Safe object with any mapping or validation errors)
    def execute(self,                                                    # Execute a batch of commands in sequence
                request: Schema__Graph__Batch__Request                   # Batch request with commands list and options
           ) -> Schema__Graph__Batch__Response:                          # Response with results, success/failure counts, errors

        results        = []         # todo this should be a Type_Safe class
        errors         = []         # todo this should be a Type_Safe class
        success        = False
        successful     = 0
        failed         = 0
        total_commands = len(request.commands)

        for idx, command in enumerate(request.commands):
            try:
                area_instance = self.area_registry.get(command.area)                        # Validate area exists
                if area_instance is None:
                    raise ValueError(f"Unknown or uninitialized area: {command.area}")      # todo: move this validation to a previous step

                method_func = getattr(area_instance, str(command.method), None)             # Validate method exists
                if not method_func or not callable(method_func):
                    raise ValueError(f"Unknown method: {command.area}.{command.method}")

                sig    = inspect.signature(method_func)                                     # Get method's expected request type from signature
                params = list(sig.parameters.values())                                      # todo: move this 'target method resolution' into a previous step

                if len(params) != 1:
                    raise ValueError(f"Method {command.method} must take exactly 1 parameter (got {len(params)})")

                request_type = params[0].annotation
                if request_type == inspect.Parameter.empty:
                    raise ValueError(f"Method {command.method} parameter must have type annotation")        # todo: refactor validation

                # todo: see if we need this
                payload_dict = {str(k): str(v) for k, v in command.payload.items()}                         # Convert payload dict → typed request object
                try:
                    request_obj = request_type(**payload_dict)
                except Exception as e:
                    raise ValueError(f"Failed to convert payload to {request_type.__name__}: {e}")          # todo: move this error and validation to a different step

                # add error handling here, since the error here will be very specific to this particular step execution
                response = method_func(request_obj)                                                         # Execute method with typed request

                # todo: we shouldn't need this as long as every method executed returns a Type_Safe object
                # todo: add the check (if the return value of a method is Type_Safe) to the batch validation steps (separate methods)
                if hasattr(response, 'json'):                                                               # Serialize response to dict
                    result_dict = response.json()
                elif hasattr(response, '__dict__'):
                    result_dict = response.__dict__
                else:
                    result_dict = {"result": str(response)}

                # todo: see if we need this
                result_safe = {  Safe_Str__Text(str(k)): Safe_Str__Text(str(v))                 # Convert to Safe_Str__Text format
                                 for k, v in result_dict.items()                }

                results.append(result_safe)
                successful += 1

            except Exception as e:
                failed    += 1
                error_msg  = f"Command {idx} ({command.area}.{command.method}): {str(e)}"
                errors.append(Safe_Str__Text(error_msg))
                if request.stop_on_error:
                    break

        if total_commands > 0 and failed == 0:                                            # if there were commands, and there we not failures
            success = True

        return Schema__Graph__Batch__Response(results        = results                  ,
                                              total_commands = total_commands           ,
                                              stop_on_error  = request.stop_on_error    ,
                                              success        = success                  ,
                                              successful     = Safe_UInt(successful)    ,
                                              failed         = Safe_UInt(failed)        ,
                                              errors         = errors                   )

    # todo expand this usage as per the todos above (and wire this in, since at the moment this method is only used by the tests)
    def validate_command(self,                          # Validate that a command can be executed
                         area : Enum__Graph__Area ,     # Area enum value
                         method: str                    # Method name
                    ) -> bool:                          # True if command is valid

        area_instance = self.area_registry.get(area)
        if area_instance is None:
            raise ValueError(f"Unknown area: {area}")

        method_func = getattr(area_instance, method, None)
        if not method_func or not callable(method_func):
            raise ValueError(f"Unknown method: {area}.{method}")

        return True
