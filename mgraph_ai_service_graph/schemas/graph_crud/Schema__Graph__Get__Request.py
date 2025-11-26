from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Namespace      import Safe_Str__Namespace


class Schema__Graph__Get__Request(Type_Safe):
    graph_id  : Random_Guid                                                                 # Graph to retrieve
    namespace : Safe_Str__Namespace    = "default"                                          # Cache namespace
