# MCP Protocol Integration

import json
from typing import Any, Dict, List, Callable
from dataclasses import dataclass, field


@dataclass
class MCPTool:
    name: str
    description: str
    handler: Callable
    input_schema: Dict = field(default_factory=dict)


@dataclass
class MCPResource:
    uri: str
    name: str
    description: str
    mime_type: str = "text/plain"


class MCPServer:
    def __init__(self, name="opencode-server"):
        self.name = name
        self.tools = {}
        self.resources = {}
    
    def register_tool(self, tool):
        self.tools[tool.name] = tool
    
    def register_resource(self, resource):
        self.resources[resource.uri] = resource
    
    def list_tools(self):
        return [{"name": t.name, "description": t.description} for t in self.tools.values()]
    
    def list_resources(self):
        return [{"uri": r.uri, "name": r.name} for r in self.resources.values()]
    
    def call_tool(self, name, args):
        if name not in self.tools:
            return {"error": "Tool not found"}
        try:
            result = self.tools[name].handler(args)
            return {"content": [{"type": "text", "text": json.dumps(result)}]}
        except Exception as e:
            return {"error": str(e)}


class MCPClient:
    def __init__(self, server):
        self.server = server
    
    def get_tools(self):
        return self.server.list_tools()
    
    def execute_tool(self, name, args):
        return self.server.call_tool(name, args)


def create_default_server():
    server = MCPServer()
    
    def read_file(args):
        return {"content": "File contents here"}
    
    def write_file(args):
        return {"success": True}
    
    def run_command(args):
        return {"output": "Command executed"}
    
    server.register_tool(MCPTool(name="read_file", description="Read file", handler=read_file))
    server.register_tool(MCPTool(name="write_file", description="Write file", handler=write_file))
    server.register_tool(MCPTool(name="run_command", description="Run command", handler=run_command))
    
    server.register_resource(MCPResource(uri="file:///workspace", name="Workspace"))
    
    return server


if __name__ == "__main__":
    print("MCP Integration Ready!")
    server = create_default_server()
    client = MCPClient(server)
    print("Tools:", [t["name"] for t in client.get_tools()])
    print("Result:", client.execute_tool("read_file", {"path": "test.py"}))

