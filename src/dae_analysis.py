# --------Import modules-------------------------
import networkx as nx
from networkx import bipartite
from plot_graph import *
from read_graph import *
from constant_def import *
from SSMatching import SSMatching

IN_DEBUG=True

def get_subgraph(graph, match):

    # ---------------Find exposed variables
    var_nodes = {n for n, v in graph.nodes(data=True) if v[NTYPE] == VAR};
    exposed_var_set = var_nodes - {ii for ii in match} - {match[ii] for ii in match}

    if IN_DEBUG:
        print("exposed variables:%s"%exposed_var_set);

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
            if IN_DEBUG:
                print(feasible_paths);

            # -------------add under-constrained variables in feasible path ------
            alternating_vars = {kk for kk, vv in feasible_paths.items()};
            under_constrained_vars = under_constrained_vars.union(alternating_vars);

    if IN_DEBUG:
        print("under-constrained variables:%s" % under_constrained_vars);
    # -------- MARK well-constrained part -----------
    well_constrained_vars = var_nodes - under_constrained_vars;
    for m in match:
        if m in well_constrained_vars or match[m] in well_constrained_vars:
            graph.nodes[m][CTYPE]=WELL_CONSTRAINED;
            graph.nodes[match[m]][CTYPE]=WELL_CONSTRAINED;
    if IN_DEBUG:
        print("well-constrained variables:%s" % well_constrained_vars);
    return graph, well_constrained_vars;

def find_feasible_paths_rec(graph, match, alternating_var, feasible_paths=None):

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
    match = SSMatching(graph)

    g_marked, w_part = get_subgraph(graph, match);

    g=paint_match(g_marked,match);
    g=paint_decomposition(g);
    plot_graph(g);

    return g_marked, w_part;


# -------------Main---------------------------------
if __name__ == '__main__':


    # test = [("e1", "P"),
    #         ("e1", "U'"),
    #         ("e1", "V'"),
    #         ("e2", "V"),
    #         ("e3", "P"),
    #         ("e3", "V"),
    #         ("e3", "T"),
    #         ("e4", "U"),
    #         ("e4", "T"),
    #         ];
    #
    # graph = extend_graph_from_edges(test);
    # decompose(graph);

    circuit = [("e1", "v1"),
               ("e1", "v2"),
               ("e2", "v1"),
               ("e2", "v3"),
               ("e2", "v4"),
               ("e3", "v3"),
               ("e3", "v4"),
               ("e3", "v9"),
               ("e4", "v3"),
               ("e4", "v5"),
               ("e4", "v7"),
               ("e5", "v6"),
               ("e5", "v8"),
               ("e6", "v4"),
               ("e6", "v6"),
               ("e7", "v2"),
               ("e7", "v10"),
               ("e8", "v9"),
               ("e8", "v11"),
               ("e9", "v12"),
               ("e10", "v12"),
               ("e10", "v14"),
               ("e10", "v16"),
               ("e11", "v15"),
               ("e11", "v17"),
               ("e12", "v13"),
               ("e12", "v15"),
               ("e13", "v18'"),
               ("e13", "v19"),
               ("e14", "v18"),
               ("e14", "v20"),
               ("e14", "v22"),
               ("e15", "v21"),
               ("e15", "v23"),
               ("e16", "v19"),
               ("e16", "v21"),
               ("e17", "v24"),
               ("e18", "v5"),
               ("e18", "v14"),
               ("e19", "v6"),
               ("e19", "v15"),
               ("e20", "v7"),
               ("e20", "v20"),
               ("e21", "v8"),
               ("e21", "v21"),
               ("e22", "v16"),
               ("e22", "v22"),
               ("e23", "v22"),
               ("e23", "v24")];
    drivers = [("e24", "v25"),
               ("e24", "v28"),
               ("e25", "v25"),
               ("e25", "v30"),
               ("e26", "v26"),
               ("e26", "v25'"),
               ("e27", "v27"),
               ("e27", "v26'"),
               ("e28", "v27"),
               ("e28", "v29"),
               ("e28", "v31"),

               ("e29", "v32"),
               ("e29", "v34"),
               ("e30", "v33"),
               ("e30", "v35"),
               ("e31", "v36"),
               ("e31", "v38"),
               ("e32", "v37"),
               ("e32", "v39"),
               ("e33", "v40"),
               ("e33", "v42"),
               ("e34", "v41"),
               ("e34", "v43"),
               ("e35", "v32"),
               ("e35", "v36"),
               ("e35", "v40"),
               ("e35", "v41"),
               ("e36", "v33"),
               ("e36", "v37"),

               ("e37", "v44"),
               ("e37", "v45"),
               ("e38", "v45"),
               ("e39", "v44"),
               ("e39", "v46"),
               ("e39", "v48"),
               # ("e40", "v48"),
               # ("e40", "v49"),

               ("e40", "v49"),
               ("e41", "v50"),

               ("e42", "v28"),
               ("e42", "v46"),
               ("e43", "v29"),
               ("e43", "v47"),
               ("e44", "v48"),
               ("e44", "v49"),

               ("e45", "v30"),
               ("e45", "v34"),
               ("e46", "v31"),
               ("e46", "v35"),

               ("e47", "v42"),
               ("e47", "v49"),
               ("e48", "v43"),
               ("e48", "v50")]

    systems = [("e49", "v51"),
               ("e49", "v52"),
               ("e50", "v51"),
               ("e50", "v53"),
               ("e50", "v55"),
               ("e51", "v54'"),
               ("e51", "v56"),
               ("e52", "v52'"),
               ("e52", "v54"),

               ("e53", "v57'"),
               ("e53", "v58"),
               ("e53", "v59'"),
               ("e53", "v61"),
               ("e54", "v57"),
               ("e54", "v58"),
               ("e54", "v60"),
               ("e55", "v59"),
               ("e55", "v60"),
               ("e56", "v57"),
               ("e56", "v62"),
               ("e57", "v58"),
               ("e57", "v63"),
               ("e58", "v61"),
               ("e58", "v65"),
               ("e59", "v60"),
               ("e59", "v64"),

               ("e60", "v55"),
               ("e60", "v64"),
               ("e61", "v56"),
               ("e61", "v65"),
               ("e62", "v38"),
               ("e62", "v62"),
               ("e63", "v39"),
               ("e63", "v63"),

               ("e64", "v10"),
               ("e64", "v53"),
               ("e65", "v11"),
               ("e65", "v54"),
               ]

    g_circuit = extend_graph_from_edges(circuit);
    g_circuit, w_circuit = decompose(g_circuit);

    g_drivers = extend_graph_from_edges(drivers);
    g_drivers, w_drivers = decompose(g_drivers);

    # compose equations in upper model with under-constrained parts of each component
    g_system = extend_graph_from_edges(circuit);
    g_system = extend_graph_from_edges(drivers, g_system);
    g_system = extend_graph_from_edges(systems, g_system);
    # flat structural analysis of upper level model
    g_system, w_system = decompose(g_system);
    # var_system = {n for n, d in g_system.nodes(data=True) if d[NTYPE]==VAR};
    # u1_system=var_system-w_system
    #
    # print(u1_system);
    # print(w_system);


    g_system = extend_graph_from_edges([(n1, n2, g_circuit.nodes[n1][NTYPE] == EQ) for n1, n2 in g_circuit.edges()
                                        if g_circuit.nodes[n1][CTYPE] == UNDER_CONSTRAINED
                                        and g_circuit.nodes[n2][CTYPE] == UNDER_CONSTRAINED]);
    g_system = extend_graph_from_edges([(n1, n2, g_drivers.nodes[n1][NTYPE] == EQ) for n1, n2 in g_drivers.edges()
                                        if g_drivers.nodes[n1][CTYPE] == UNDER_CONSTRAINED
                                        and g_drivers.nodes[n2][CTYPE] == UNDER_CONSTRAINED], g_system);
    g_system = extend_graph_from_edges(systems, g_system);
    w_vars = set(w_circuit).union(set(w_drivers));
    # remove well-constrained variables
    for wv in w_vars:
        # remove well-constrained variables
        if g_system.has_node(wv):
            g_system.remove_node(wv);
        # remove diff of well-constrained variables
        for node in g_system.nodes():
            if str(node).startswith(wv+FLAG_INDEX):
                g_system.remove_node(node);

    # structural analysis of upper level model
    g_system, w_system = decompose(g_system);
    # var_system = {n for n, d in g_system.nodes(data=True) if d[NTYPE]==VAR};
    # u2_system=var_system-w_system
    #
    # print(u2_system);
    # print(w_system);
    #
    # print(u1_system - u2_system);


    print ("succeed");
