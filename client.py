"""Doubly Connected Edge List (DCEL) Half-Edge Mesh Topology Engine.
100% Python Standard Library.
"""

class HalfEdgeMesh:
    """Doubly Connected Edge List (DCEL) Half-Edge topological mesh structure."""
    class Vertex:
        def __init__(self, idx, coords):
            self.idx = idx
            self.coords = tuple(coords)
            self.incident_edge = None

    class HalfEdge:
        def __init__(self, idx):
            self.idx = idx
            self.origin = None
            self.twin = None
            self.face = None
            self.next = None
            self.prev = None

    class Face:
        def __init__(self, idx):
            self.idx = idx
            self.half_edge = None

    def __init__(self):
        self.vertices = []
        self.half_edges = []
        self.faces = []
        self._edge_map = {}

    def add_vertex(self, coords):
        v = self.Vertex(len(self.vertices), coords)
        self.vertices.append(v)
        return v

    def add_polygon(self, vertex_indices):
        """Adds a polygon defined by an ordered list of vertex indices."""
        f = self.Face(len(self.faces))
        self.faces.append(f)
        n = len(vertex_indices)
        poly_half_edges = []

        for i in range(n):
            he = self.HalfEdge(len(self.half_edges))
            self.half_edges.append(he)
            poly_half_edges.append(he)

        for i in range(n):
            u_idx = vertex_indices[i]
            v_idx = vertex_indices[(i + 1) % n]
            he = poly_half_edges[i]
            he.origin = self.vertices[u_idx]
            he.face = f
            self.vertices[u_idx].incident_edge = he

            he.next = poly_half_edges[(i + 1) % n]
            he.prev = poly_half_edges[(i - 1 + n) % n]

            edge_key = (u_idx, v_idx)
            twin_key = (v_idx, u_idx)
            if twin_key in self._edge_map:
                twin_he = self._edge_map[twin_key]
                he.twin = twin_he
                twin_he.twin = he
            self._edge_map[edge_key] = he

        f.half_edge = poly_half_edges[0]
        return f

    def euler_characteristic(self):
        v = len(self.vertices)
        f = len(self.faces)
        edges = set()
        for he in self.half_edges:
            orig = he.origin.idx
            dest = he.next.origin.idx
            edges.add(tuple(sorted((orig, dest))))
        e = len(edges)
        chi = v - e + f
        return {"vertices": v, "edges": e, "faces": f, "euler_characteristic": chi}
