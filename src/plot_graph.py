# --------Import modules-------------------------
import networkx as nx
from networkx import bipartite
from constant_def import *


def plot_graph(graph, fit_width=True, fig_height=3, location=111, match={}):
    """Plot graph using nodes as position number.
    """
    import matplotlib.pyplot as plt

    fig_width=8;
    if fit_width:
        fig_width=0.3*len(graph.nodes())

    fig = plt.figure(figsize=[fig_width,fig_height]);
    ax = fig.add_subplot(location);

    node_pos = {};
    node_color=[];
    border_width=[];
    for n, v in graph.nodes(data=True):
        if POSITION in v:
            node_pos[n]=(v[POSITION],v[NTYPE]);
        else:
            raise Exception("The position of current node is not specified");
        if COLOR in v:
            node_color.append(v[COLOR]);
        else:
            node_color.append(DEF_NODE_COLOR);
        if WIDTH in v:
            border_width.append(v[WIDTH]);
        else:
            border_width.append(DEF_BORDER_WIDTH);

    edge_color=[];
    edge_width=[];
    for n1, n2, v in graph.edges(data=True):
        if COLOR in v:
            edge_color.append(v[COLOR]);
        else:
            edge_color.append(DEF_EDGE_COLOR);
        if WIDTH in v:
            edge_width.append(v[WIDTH]);
        else:
            edge_width.append(DEF_EDGE_WIDTH);

    nx.draw(graph, node_pos, ax=ax, with_labels=True,
            node_shape=DEF_NODE_SHAPE,
            node_color=node_color,
            node_size=DEF_NODE_SIZE,
            linewidths=border_width,
            edgecolors=DEF_BORDER_COLOR,
            edge_color=edge_color,
            width=edge_width,
            WIDTH=DEF_EDGE_WIDTH,
            font_color=DEF_FONT_COLOR,
            font_size=DEF_FONT_SIZE,
            font_family=DEF_FONT_FAMILY);
    plt.show(block=False);
    return;

def paint_match(graph, match):
    for nk in match:
        edge_data = graph.edges[nk,match[nk]];
        edge_data[COLOR]=MATCHED_EDGE_COLOR;
        edge_data[WIDTH]=MATCHED_EDGE_WIDTH;
    return graph;

def paint_decomposition(graph):
    nodes=graph.nodes(data=True);
    for n,d in nodes:
        if d[CTYPE]==WELL_CONSTRAINED:
            d[COLOR]=WELL_CONSTRAINED_COLOR;
        elif d[CTYPE]==UNDER_CONSTRAINED:
            d[COLOR] = UNDER_CONSTRAINED_COLOR;
        elif d[CTYPE]==OVER_CONSTRAINED:
            d[COLOR] = OVER_CONSTRAINED_COLOR;
        else:
            d[COLOR] = DEF_NODE_COLOR;
    return graph;

def paint_diff(graph):
    nodes=graph.nodes(data=True);
    for n,d in nodes:
        if d[ORIGIN] is not None:
            d[WIDTH]=DIFFERENTIATED_NODE_WIDTH;
            d[COLOR]=DIFFERENTIATED_NODE_COLOR;
    return graph;
