from osbot_utils.type_safe.Type_Safe                                     import Type_Safe
from mgraph_ai_service_graph.service.areas.edit.Graph__Edit__Add_Node    import Graph__Edit__Add_Node
from mgraph_ai_service_graph.service.areas.edit.Graph__Edit__Add_Value   import Graph__Edit__Add_Value
from mgraph_ai_service_graph.service.areas.edit.Graph__Edit__Add_Edge    import Graph__Edit__Add_Edge
from mgraph_ai_service_graph.service.areas.edit.Graph__Edit__Delete      import Graph__Edit__Delete
from mgraph_ai_service_graph.service.areas.edit.Graph__Edit__Builder     import Graph__Edit__Builder
from mgraph_ai_service_graph.service.graph.Graph__Service                import Graph__Service

# todo: move this class to the areas/edit folder
class Area__Graph__Edit(Type_Safe):                                     # Graph editing operations - thin orchestrator

    graph_service : Graph__Service                                      # Injected dependency

    add_node      : Graph__Edit__Add_Node   = None                      # Handlers - each focused on specific operation type
    add_value     : Graph__Edit__Add_Value  = None
    add_edge      : Graph__Edit__Add_Edge   = None
    delete        : Graph__Edit__Delete     = None
    builder       : Graph__Edit__Builder    = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_handlers()                                           # todo: see if we shouldn't be using the .setup() pattern here

    def _init_handlers(self):                                           # Initialize handlers with shared graph_service
        if self.graph_service:
            self.add_node  = Graph__Edit__Add_Node (graph_service = self.graph_service)
            self.add_value = Graph__Edit__Add_Value(graph_service = self.graph_service)
            self.add_edge  = Graph__Edit__Add_Edge (graph_service = self.graph_service)
            self.delete    = Graph__Edit__Delete   (graph_service = self.graph_service)
            self.builder   = Graph__Edit__Builder  (graph_service = self.graph_service)