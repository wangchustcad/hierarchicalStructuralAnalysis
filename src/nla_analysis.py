"""Functions to find the under-constrained part of a component.

Implemented following the algorithms in the paper "A fast structural
analysis algorithms for reuse-oriented models" by Wang Chao
using numpy and networkx modules of python.

NOTICE: optimization needed.
"""
# --------Import modules-------------------------
import networkx as nx
from networkx import bipartite
from plot_graph import *
from read_graph import *
from constant_def import *


def get_subgraph(graph, match):
    """construct dummy equations in an undirected bipartite graph.

    <g>: undirected bipartite graph. Nodes are separated by their
         'bipartite' attribute.

    Return <dummy_eqs>: list, each is a set of edges from a dummy equation to its variables.

    Author: Chao Wang (wangc@hust.edu.cn)
    Update time: 2021-03-21 20:04:51.
    """

    # ---------------Find exposed variables
    var_nodes = {n for n, v in graph.nodes(data=True) if v[NTYPE] == VAR};
    exposed_var_set = var_nodes - {ii for ii in match} - {match[ii] for ii in match}

    # ---------------Search under-constrained variables on feasible paths
    under_constrained_vars = exposed_var_set.copy();
    for exposed_var in exposed_var_set:
        if exposed_var in nx.isolates(graph):
            under_constrained_vars.add(exposed_var);
            continue;
        else:
            # -----------------Find feasible path----------------
            # -----------------Enter recursion-----------------
            feasible_paths = find_feasible_paths_rec(graph, match, exposed_var);

            # -------------add under-constrained variables in feasible path ------
            alternating_vars = {kk for kk, vv in feasible_paths.items()};
            under_constrained_vars = under_constrained_vars.union(alternating_vars);

    # -------- MARK well-constrained part -----------
    well_constrained_vars = var_nodes - under_constrained_vars;
    for m in match:
        if m in well_constrained_vars or match[m] in well_constrained_vars:
            graph.nodes[m][CTYPE]=WELL_CONSTRAINED;
            graph.nodes[match[m]][CTYPE]=WELL_CONSTRAINED;

    return graph, well_constrained_vars;

def find_feasible_paths_rec(graph, match, alternating_var, feasible_paths=None):
    """Recursively search feasible paths.

    <graph>: bipartite graph. Nodes are separated by their
         'bipartite' attribute.
    <feasible_paths>: set of feasible paths.
    <alternating_var>: the source of the feasible paths.

    Return <feasible_paths>: set of feasible_paths, including feasible paths from the alternating_var.

    Author: Chao Wang (wangc@hust.edu.cn)
    Update time: 2021-03-21 20:09:01.
    """

    # -----------------if no unconstrained variable specified, terminate------------
    if not graph or not alternating_var:
        return feasible_paths;

    if not feasible_paths or len(feasible_paths)==0:
        feasible_paths={alternating_var:[alternating_var]};

    for eq in graph.neighbors(alternating_var):
        if alternating_var in match and eq== match[alternating_var]:
            continue;
        if eq not in match:
            raise Exception("error maximum match");
        target_var = match[eq];
        # --------- filter duplicated feasible paths ------------
        if target_var in feasible_paths:
            continue;
        feasible_paths[target_var]=(alternating_var,eq,target_var);
        # ----- find feasible paths recursively
        feasible_paths = find_feasible_paths_rec(graph, match, target_var, feasible_paths);

    return feasible_paths;


def decompose(graph):
    # # ----------------Find one matching M----------------
    match = bipartite.hopcroft_karp_matching(graph)

    g_marked, w_part = get_subgraph(graph, match);

    g=paint_match(g_marked,match);
    g=paint_decomposition(g);
    plot_graph(g);

    return g_marked, w_part;


# -------------Main---------------------------------
if __name__ == '__main__':

    # test =[("e4","v3"),
    #        ("e4","v4"),
    #        ("e5","v3"),
    #        ("e5","v4"),
    #        ("e6","v4"),
    #        ("e6","v5"),
    #        ("e6","v6"),
    #        ("e7","v5"),
    #        ("e7","v6"),
    #        ("e7","v7")]

    # test = [("e1", "v1"),
    #         ("e1", "v2"),
    #
    #         ("e2", "v1"),
    #         ("e2", "v2"),
    #         ("e2", "v3"),
    #
    #         ("e3", "v4"),
    #         ("e3", "v5"),
    #
    #         ("e4", "v2"),
    #         ("e4", "v4"),
    #
    #         ("e5", "v4"),
    #         ("e5", "v5"),
    #         ("e5", "v6")];
    
    #
    # g_test = extend_graph_from_edges(test);
    # g_test = decompose(g_test);
    # paint_match(g_test);
    # paint_constrained(g_test)
    # plot_graph(g_test)


    circuit=[("e1","v1"),
             ("e1","v2"),
             ("e2","v1"),
             ("e2","v3"),
             ("e2","v4"),
             ("e3","v3"),
             ("e3","v4"),
             ("e3","v9"),
             ("e4","v3"),
             ("e4","v5"),
             ("e4","v7"),
             ("e5","v6"),
             ("e5","v8"),
             ("e6","v4"),
             ("e6","v6"),
             ("e7","v2"),
             ("e7","v10"),
             ("e8","v9"),
             ("e8","v11"),
             ("e9","v12"),
             ("e10","v12"),
             ("e10","v14"),
             ("e10","v16"),
             ("e11","v15"),
             ("e11","v17"),
             ("e12","v13"),
             ("e12","v15"),
             ("e13","v18"),
             ("e14","v5"),
             ("e14","v14"),
             ("e15","v6"),
             ("e15","v15"),
             ("e16","v7"),
             ("e16","v16"),
             ("e17","v16"),
             ("e17","v18")]

    shell=[("e18","v19"),
           ("e18","v20"),
           ("e19","v19"),
           ("e19","v21"),
           ("e19","v23"),
           ("e20","v22"),
           ("e20","v24"),
           ("e21", "v20"),
           ("e21", "v22"),
           ("e22", "v25"),
           ("e22", "v26"),
           ("e23", "v25"),
           ("e24", "v21"),
           ("e24", "v26")]

    system=[("e25", "v23"),
            ("e25", "v10"),
            ("e26", "v24"),
            ("e26", "v11")]

    # decompose component circuit
    g_circuit=extend_graph_from_edges(circuit);
    g_circuit, w_circuit = decompose(g_circuit);

    # decompose component shell
    g_shell=extend_graph_from_edges(shell);
    g_shell, w_shell = decompose(g_shell);


    # compose equations in upper model with under-constrained parts of each component
    g_system = extend_graph_from_edges(circuit);
    g_system = extend_graph_from_edges(shell, g_system);
    g_system = extend_graph_from_edges(system, g_system);
    # flat structural analysis of upper level model
    g_system,wf_system = decompose(g_system);

    g_system = extend_graph_from_edges([(n1,n2,g_circuit.nodes[n1][NTYPE] == EQ) for n1,n2 in g_circuit.edges()
                                        if g_circuit.nodes[n1][CTYPE]==UNDER_CONSTRAINED
                                        and g_circuit.nodes[n2][CTYPE]==UNDER_CONSTRAINED]);
    g_system = extend_graph_from_edges([(n1,n2,g_shell.nodes[n1][NTYPE] == EQ) for n1,n2 in g_shell.edges()
                                        if g_shell.nodes[n1][CTYPE]==UNDER_CONSTRAINED
                                        and g_shell.nodes[n2][CTYPE]==UNDER_CONSTRAINED], g_system);
    g_system = extend_graph_from_edges(system, g_system);
    w_vars = set(w_circuit).union(set(w_shell));
    # remove well-constrained variables
    for wv in w_vars:
        if g_system.has_node(wv):
            g_system.remove_node(wv);
    # structural analysis of upper level model
    g_system, wh_system = decompose(g_system);


    print ("succeed");
