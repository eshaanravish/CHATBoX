from channels.routing import route, route_class
from mychannel.consumers import ws_connect, ws_message, ws_disconnect, Demultiplexer
from mychannel import consumers

from channels import route_class, route
from mychannel.models import IntegerValueBinding

channel_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
    # route_class(consumers.ChatServer, path=r"^/chat/"),
    route("websocket.connect", consumers.ws_connect, path=r"^/$"),
    route("websocket.connect", consumers.ws_connect, path=r"^/chat/$"),
    route_class(Demultiplexer, path="^/binding/"),
    # consumers.ChatServer.as_route(path=r"^/chat/"),
    # consumers.MyGenericConsumer.as_route(path=r"^/path/1/",
    #                                      attrs={'group': 'one', 'group_prefix': 'pre'}),
    # consumers.MyGenericConsumer.as_route(path=r"^/path/2/",
    #                                      attrs={'group': 'two', 'group_prefix': 'public'}),
]


