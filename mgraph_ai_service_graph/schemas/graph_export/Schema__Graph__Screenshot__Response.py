from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Content_Type import Safe_Str__Http__Content_Type
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id          import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                        import Schema__Graph__Ref


class Schema__Graph__Screenshot__Response(Type_Safe):                           # Response for screenshot generation
    graph_ref    : Schema__Graph__Ref            = None                         # Resolved reference
    format       : Safe_Str__Id                  = None                         # Output format used
    image_base64 : str                           = None                         # Base64 encoded image data
    content_type : Safe_Str__Http__Content_Type  = None                         # MIME type (image/png, image/svg+xml, etc)
    success      : bool                          = False                        # Whether rendering succeeded