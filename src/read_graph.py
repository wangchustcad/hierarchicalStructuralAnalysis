import networkx as nx;
from constant_def import *;

def extend_graph_from_edges(edges, graph=None):
    if not graph:
        graph = nx.Graph()
    e_index=len({n for n,v in graph.nodes(data=NTYPE) if v==EQ});
    v_index=len({n for n,v in graph.nodes(data=NTYPE) if v==VAR});
    for ii in edges:
        if len(ii)<2:
            raise Exception("error data in edge list")

        if len(ii) == 3 and not ii[2]:
            vi = 0;
            ei = 1;
        else:
            vi = 1;
            ei = 0;

        if not graph.has_node(ii[ei]):
            graph.add_node(ii[ei], node=EQ, pos=e_index, constrained=UNDER_CONSTRAINED);
            e_index += 1;
        if not graph.has_node(ii[vi]):
            graph.add_node(ii[vi], node=VAR, pos=v_index, constrained=UNDER_CONSTRAINED);
            v_index += 1;
    graph.add_edges_from([(e[0],e[1]) for e in edges]);
    return graph;