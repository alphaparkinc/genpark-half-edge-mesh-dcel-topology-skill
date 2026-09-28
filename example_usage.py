from client import HalfEdgeMesh

mesh = HalfEdgeMesh()
v0 = mesh.add_vertex((0, 0, 0))
v1 = mesh.add_vertex((1, 0, 0))
v2 = mesh.add_vertex((1, 1, 0))
v3 = mesh.add_vertex((0, 1, 0))

mesh.add_polygon([0, 1, 2])
mesh.add_polygon([0, 2, 3])

euler = mesh.euler_characteristic()
print("DCEL Mesh Topology Summary:")
print(f"Vertices: {euler['vertices']}, Edges: {euler['edges']}, Faces: {euler['faces']}")
print(f"Euler Characteristic: {euler['euler_characteristic']}")
