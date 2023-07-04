import networkx as nx


class HashMultiGraph(nx.MultiGraph):
    def __eq__(self, other):
        return self.nodes == other.nodes and self.edges == other.edges

    def __hash__(self):
        """
        This hash function assumes that the MDG has no isolated vertices.
        :return:
        """
        t = (frozenset(self.nodes), frozenset(self.edges))
        return hash(t)

    def __repr__(self):
        return f"MultiDiGraph with {self.number_of_edges()} edges and {self.number_of_nodes()} nodes (so EC = {self.number_of_edges() - self.number_of_nodes() + 1})"



class HashMultiDiGraph(nx.MultiDiGraph):
    def __eq__(self, other):
        return self.nodes == other.nodes and self.edges == other.edges

    def __hash__(self):
        """
        This hash function assumes that the MDG has no isolated vertices.
        :return:
        """
        t = (frozenset(self.nodes), frozenset(self.edges))
        return hash(t)

    def __repr__(self):
        return f"MultiDiGraph with {self.number_of_edges()} edges and {self.number_of_nodes()} nodes (so EC = {self.number_of_edges() - self.number_of_nodes() + 1})"

