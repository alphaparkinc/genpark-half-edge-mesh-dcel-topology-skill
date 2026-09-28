# genpark-half-edge-mesh-dcel-topology-skill

Agent Skill implementing the **Doubly Connected Edge List (DCEL)** Half-Edge topological mesh data structure for manifold mesh traversal, twin edge pairing, and Euler characteristic analysis.

## Architectural Overview
```mermaid
flowchart TD
    Vertices["Vertex Coordinates"] & Faces["Face Incidence Lists"] --> DCEL["Half-Edge DCEL Builder"]
    DCEL --> Twin["Twin Edge Pairing Map (u, v) <-> (v, u)"]
    DCEL --> Cycle["Next / Prev Half-Edge Cycle Links"]
    Twin & Cycle --> Topological["Compute Euler Characteristic Chi = V - E + F"]
```
