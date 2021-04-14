import networkx as nx
from networkx import bipartite
from constant_def import *
from read_graph import *
from plot_graph import *


# plot graph of each loop
DEBUG=False;

def SSMatching(graph):
    mat={};
    while True:
        diffed=False;

        eqs = {n for n,v in graph.nodes(data=True) if v[NTYPE]==EQ};
        for eq in eqs:
            # filter matched or singular eqs
            if eq in mat or FLAG_OVER in graph.nodes[eq]:
                continue;
            # augment match
            ret=augment(graph, eq, mat);

            if ret:
                clear_flag(graph, None, FLAG_AUG);
                continue;
            replace_flag(graph, FLAG_AUG, FLAG_DIFF, None);

            ret2 = augment(graph, eq, mat, False);
            if ret2:
                differentiate(graph)
                diffed = True;
            else:
                mark_flag(graph, eq, FLAG_OVER);
            clear_flag(graph, None, FLAG_AUG, FLAG_DIFF);

        if DEBUG:
            paint_match(graph,mat);
            plot_graph(graph);
        if not diffed:
            break;

    return mat;

def augment(graph, cur_node, mat={}, in_diff=True):
    eq = cur_node;
    # try a direct match
    mark_flag(graph, eq, FLAG_AUG);
    for nv in graph.neighbors(eq):
        # filter algebraic variables in diff mode, from algebraic set and no der exist.
        # if in_diff and (FLAG_INDEX not in nv or ORIGIN in graph.nodes[nv]) and has_der(graph, nv):
        if in_diff and (FLAG_INDEX not in nv or has_diff(graph, nv)):
            continue;
        if nv not in mat:
            match(eq, nv, mat);
            return True;

    # try an alternating path
    for nv in graph.neighbors(eq):
        if in_diff and (FLAG_INDEX not in nv or has_diff(graph, nv)):
            continue;
        tar_node = mat[nv];
        if FLAG_AUG in graph.nodes[tar_node]:
            continue;
        if augment(graph, tar_node, mat, in_diff):
            # clear_flag(graph, eq, FLAG_AUG);
            match(eq, nv, mat);
            return True;

    return False;

def has_diff(graph, var):
    vvs = [n for n,v in graph.nodes(data=True)
           if v[NTYPE]==VAR and str(n).startswith(var+FLAG_INDEX)];
    return len(vvs)>0;

def match(n1, n2, m={}):
    m[n1]=n2;
    m[n2]=n1;
    return m;

def alter_flag(graph, node=None, *flags):
    if len(flags)==0:
        return False;
    nodes = [];
    if node is not None:
        nodes.append(node);
    else:
        nodes = [n for n in graph.nodes()];
    for n in nodes:
        data = graph.nodes[n];
        for flag in flags:
            if flag in data:
                data.pop(flag);
            else:
                data[flag]=None;
    return True;

def clear_flag(graph, node=None, *flags):
    if len(flags)==0:
        return False;
    nodes=[];
    if node is not None:
        nodes.append(node);
    else:
        nodes=[n for n in graph.nodes()];
    for n in nodes:
        data = graph.nodes[n];
        for flag in flags:
            if flag in data:
                data.pop(flag);
    return True;


def mark_flag(graph, node, *flags):
    if len(flags)==0:
        return False;
    node_data = graph.nodes[node];
    for k in flags:
        node_data[k]=None;
    return True;

def replace_flag(graph, flag1, flag2, node=None):
    if not flag1 or not flag2:
        return False;
    nodes = [];
    if node is not None:
        nodes.append(node);
    else:
        nodes = [n for n in graph.nodes()];
    for n in nodes:
        data = graph.nodes[n];
        if flag1 in data:
            data.pop(flag1);
            data[flag2]=None;
    return True;

def differentiate(graph):
    diff_edges=[];
    eqs = {eq:ed for eq, ed in graph.nodes(data=True) if ed[NTYPE]==EQ}
    e_index=len(eqs);
    v_index=len(graph.nodes())-e_index;
    for eq in eqs:
        ed = eqs[eq];
        if FLAG_DIFF in ed:
            diff_eq = eq+FLAG_INDEX;
            diff_times=1;
            # while graph.has_node(diff_eq):
            #     diff_eq=diff_eq+FLAG_INDEX;
            #     diff_times+=1;

            if not graph.has_node(diff_eq):
                graph.add_node(diff_eq, node=EQ, pos=e_index, constrained=UNDER_CONSTRAINED, origin=eq);
                e_index += 1;

            for var in graph.neighbors(eq):
                diff_var=var+FLAG_INDEX*diff_times;
                if not graph.has_node(diff_var):
                    graph.add_node(diff_var, node=VAR, pos=v_index, constrained=UNDER_CONSTRAINED, origin=var);
                    v_index += 1;
                graph.add_edge(diff_eq, diff_var);
    return True;


if __name__=="__main__":
    # test = [("e1", "T"),
    #         ("e1", "x"),
    #         ("e1", "x''"),
    #         ("e2", "T"),
    #         ("e2", "y"),
    #         ("e2", "y''"),
    #         ("e3", "x"),
    #         ("e3", "y")
    #         ]

    test = [("e1", "P"),
            ("e1", "U'"),
            ("e1", "V'"),
            ("e2", "V"),
            ("e3", "P"),
            ("e3", "V"),
            ("e3", "T"),
            ("e4", "U"),
            ("e4", "T"),
            ];


    graph=extend_graph_from_edges(test);
    plot_graph(graph)

    match=SSMatching(graph);
    paint_match(graph,match);
    plot_graph(graph);

    print "success";
