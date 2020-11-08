""" DRAWING GRAPH"""
import networkx as nx
import matplotlib.pyplot as plt


def draw(graph):
    plt.close()
    nx.draw(graph,
            pos=_hierarchy_pos(graph, next(iter(graph.nodes))),
            with_labels=True)
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
        dx = width / len(neighbors)
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
