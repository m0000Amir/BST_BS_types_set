""" DRAWING GRAPH"""
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
from binary_search.schedule import Schedule
from binary_search.tree import Tree
from networkx.drawing.nx_agraph import graphviz_layout


def plot(tree: Tree, stat: Schedule) -> None:
    """
    Parameters
    ----------
    tree obtained binary search tree
    stat statistics of problem solution

    Returns
    -------
    Plot of tree
    """
    labels = {}
    for n in tree.graph.nodes:
        if n in stat.close_nodes:
            if n in stat.record_node:
                label = f"$\\textit{{\\textbf{{R = }}}}$ $\\bf{{{int(stat.noncoverage[n])}}}$"
            else:
                label = r"$\varnothing$"

        else:
            label = fr"$W = {{{int(stat.noncoverage[n])}}}$"
        labels.update({stat.step[n]: label})

    color_map = []
    for node in tree.graph.nodes:
        if node in stat.close_nodes:
            color_map.append('orange')
        else:
            color_map.append('deepskyblue')

    draw(tree.graph, labels, color_map)


def draw(graph, labels: dict, node_color: list) -> None:
    matplotlib.rc('text', usetex=True)
    plt.rcParams['text.latex.preamble'] = \
        r"\usepackage{bm} \usepackage{amsmath} \usepackage{amssymb}"
    pos = graphviz_layout(graph, prog='dot',
                          args="-Gnodesep=200 -Granksep=-200")
    label_pos = {i: [pos[i][0] - pos[0][1] * 5, pos[i][1] +
                     pos[0][1] * .07] for i in pos.keys()}

    nx.draw(graph, pos, with_labels=True, arrows=False,
            node_size=400, node_color=node_color,
            node_shape="o", alpha=0.99, font_size=15,
            font_color="k", font_weight="bold", width=1.5,
            edge_color="k")

    nx.draw(graph, label_pos, with_labels=True, arrows=False,
            node_size=.1, edgelist=[], node_color='w',
            labels=labels, font_size=12, font_color="k")

    plt.savefig("bst.png")
    plt.show()


def _hierarchy_pos(graph, root, width=1., vert_gap=1, vert_loc=0, xcenter=.5,
                   pos=None):
    """
    If there is a cycle that is reachable from root, then this will see
    infinite recursion.
    :param root: the root node of current branch
    :param width: horizontal space allocated for this branch - avoids
        overlap with other branches
    :param vert_gap: gap between levels of hierarchy
    :param vert_loc: vertical location of root
    :param xcenter: horizontal location of root
    :param pos: a dict saying where all nodes go if they have been
        assigned
    :return: Node positions in plot
    """
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = list(graph.neighbors(root))

    if len(neighbors) != 0:
        dx = width / 1.9
        nextx = xcenter - width / 2 - dx / 2
        for neighbor in neighbors:
            nextx += dx
            pos = _hierarchy_pos(graph,
                                 neighbor,
                                 width=dx,
                                 vert_gap=vert_gap,
                                 vert_loc=(vert_loc - vert_gap),
                                 xcenter=nextx, pos=pos)
    return pos


if __name__ == "__main__":
    g = nx.DiGraph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)

    labels = {0: fr"$G_\nu$", 1: fr"$G^1_\nu$", 2: fr"$G^2_\nu$"}

    color_map = ['deepskyblue'] * len(g.nodes)

    matplotlib.rc('text', usetex=True)
    plt.rcParams['text.latex.preamble'] = \
        r"\usepackage{bm} \usepackage{amsmath}"

    plt.figure(figsize=(6, 4.8))

    pos = {0: (63.0, 20.0), 1: (27.0, 19.5), 2: (99.0, 19.5)}
    nx.draw(g, pos, node_size=2500, node_color=color_map)
    nx.draw_networkx_edges(g, pos, width=3)
    nx.draw_networkx_labels(g, pos, labels, font_size=25)
    nx.draw_networkx_edge_labels(g,
                                 pos,
                                 edge_labels={(0, 1): r'$\pi_{ij} = 1$',
                                              (0, 2): r'$\pi_{ij} = 0$'},
                                 font_size=35,
                                 verticalalignment="center")
    plt.axis("off")
    plt.savefig("bst_child_nodes.png")
    plt.show()

    """ NEW GRAPH """
    g = nx.MultiDiGraph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)

    g.add_edge(1, 0)
    g.add_edge(1, 3)
    g.add_edge(1, 4)
    g.add_edge(3, 1)
    g.add_edge(4, 1)

    labels = {0: fr"$G_0$", 1: fr"$G_1 = G^1_0$",
              2: fr"$G_2 = G^2_0$",  3: fr"$G_3 = G^1_1$",
              4: fr"$G_4 = G^2_1$"}

    color_map = ['deepskyblue',
                 'deepskyblue',
                 'deepskyblue',
                 'orange',
                 'orange']

    matplotlib.rc('text', usetex=True)
    plt.rcParams['text.latex.preamble'] = \
        r"\usepackage{bm} \usepackage{amsmath}"
    plt.figure(figsize=(6, 4.8))

    gg = nx.DiGraph()
    gg.add_node(0)
    nx.draw(gg, pos={0: (15, 20)}, node_color='w')
    pos = {0: (63.0, 30.0), 1: (51.0, 19.5), 2: (99.0, 19.5),
           3: (35.0, 10), 4: (75.0, 10)}
    nx.draw(g, pos, node_size=2000, node_color=color_map,
            arrows=True, connectionstyle='arc3, rad = 0.1', width=2.0)
    # nx.draw_networkx_edges(g, pos, width=3)
    label_pos = {0: (63.0, 30.0), 1: (44.0, 19.5), 2: (92.0, 19.5),
            3: (28.0, 10), 4: (68.0, 10)}
    nx.draw_networkx_labels(g, label_pos, labels, font_size=25)


    plt.savefig("tree_traversal.png")
    plt.show()
