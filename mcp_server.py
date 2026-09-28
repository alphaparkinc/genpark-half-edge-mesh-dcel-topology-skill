import sys
import json
from client import HalfEdgeMesh

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-half-edge-mesh-dcel-topology-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "analyze_mesh_topology",
                        "description": "Construct Half-Edge DCEL mesh and compute topological Euler characteristics",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "vertices": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}, "description": "3D coordinates"},
                                "faces": {"type": "array", "items": {"type": "array", "items": {"type": "integer"}}, "description": "Face vertex index lists"}
                            },
                            "required": ["vertices", "faces"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "analyze_mesh_topology":
            mesh = HalfEdgeMesh()
            for v in args.get("vertices", []):
                mesh.add_vertex(v)
            for f in args.get("faces", []):
                mesh.add_polygon(f)
            euler = mesh.euler_characteristic()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(euler)}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
