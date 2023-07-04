from pprint import pprint

import networkx as nx
from typing import List
from collections import defaultdict

from graph_types import HashMultiGraph, HashMultiDiGraph


def get_word_graph(word: List[int]):
    G = HashMultiDiGraph()
    for i, let in enumerate(word):
        e = (i, (i + 1) % len(word))
        edge = e[::-1] if let < 0 else e
        G.add_edge(edge[0], edge[1], label=abs(let))
    return G


def get_word_fringe(word: List[int], fold=True, verbose=False):
    G_word = get_word_graph(word)
    distances = defaultdict(lambda: 999)
    distances[G_word] = 0
    get_downward_fringe(G_word, distances, fold=fold)
    min_ec = 1000
    for G, dist in distances.items():
        EC = G.number_of_edges() - G.number_of_nodes()
        if EC < dist:
            min_ec = min(min_ec, EC)
    print(f"Minimum Euler characteristic = {min_ec}")
    if verbose:
        pprint(distances)


def identify_edges(G: HashMultiDiGraph, e, d):
    """

    :param G: graph to identify edges e, d
    :param e: edge 1
    :param d: edge 2
    :return: graph with e,d identified
    """
    if d[0] < e[0] or d[0] == e[0] and d[1] < e[1]:
        d, e = e, d

    _u = d[0]
    _v = d[1]

    u = e[0]
    v = e[1] if _v != u and _u != e[1] else u

    H = G.copy()
    H.remove_node(_u)

    if _u != _v:
        H.remove_node(_v)

    edges = set((e[0], e[1], e[2]['label']) for e in H.edges(data=True))
    for x in G.out_edges(_u, data=True):
        q = v if x[1] == _v else u if x[1] == _u else x[1]
        edges.add((u, q, x[2]['label']))
    for y in G.in_edges(_u, data=True):
        q = v if y[0] == _v else u if y[0] == _u else y[0]
        edges.add((q, u, y[2]['label']))
    for z in G.out_edges(_v, data=True):
        q = v if z[1] == _v else u if z[1] == _u else z[1]
        edges.add((v, q, z[2]['label']))
    for w in G.in_edges(_v, data=True):
        q = v if w[0] == _v else u if w[0] == _u else w[0]
        edges.add((q, v, w[2]['label']))
    K = HashMultiDiGraph()
    K.add_edges_from(ebunch_to_add=[(e[0], e[1], {"label": e[2], "number": e[3]}) for e in edges])
    return K


def fold(H: HashMultiDiGraph):
    folded = False
    while not folded:
        folded = True
        for node in H.nodes:
            # Check out edges
            for e in H.out_edges(node, data=True):
                label = e[2]['label']
                for d in H.out_edges(node, data=True):
                    if d == e:
                        continue
                    if label == d[2]['label']:
                        folded = False
                        H = identify_edges(H, e, d)
                    if not folded:
                        break
                if not folded:
                    break
            if not folded:
                break
            # Check in edges
            for e in H.in_edges(node, data=True):
                label = e[2]['label']
                for d in H.in_edges(node, data=True):
                    if d == e:
                        continue
                    if label == d[2]['label']:
                        folded = False
                        H = identify_edges(H, e, d)
                    if not folded:
                        break
                if not folded:
                    break
            if not folded:
                break
    return H

def identify_edges_and_fold(G: HashMultiDiGraph, e, d):
    H = identify_edges(G, e, d)
    H = fold(H)
    return H


def get_downward_fringe(G, distances: dict, fold=True, verbose=False):
    next_level = set()
    for e in G.edges(data=True):
        for d in G.edges(data=True):
            if e != d and e[2]['label'] == d[2]['label']:
                next_level.add(identify_edges_and_fold(G, e, d) if fold else identify_edges(G, e, d))
    for H in next_level:
        distances[H] = min(distances[H], distances[G] + 1)
        ### TODO: FIX THIS MIN TO BE UP TO ISOMORPHISM!!!
        get_downward_fringe(H, distances, verbose=verbose)
    # When next_level is empty, this ends.


get_word_fringe([1,2,-1], fold=True, verbose=True)