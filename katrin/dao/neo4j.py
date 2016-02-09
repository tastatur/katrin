import py2neo


class Neo4jStore:
    def __init__(self, uri):
        self._graph = py2neo.Graph(uri)


class NormalHumanStore(Neo4jStore):
    def __init__(self, uri):
        super().__init__(uri)
        if "uid" not in self._graph.schema.get_uniqueness_constraints("Human"):
            self._graph.schema.create_uniqueness_constraint("Human", "uid")

    def update_human(self, human):
        human_node = self._graph.merge_one("Human", "uid", human.uid)
        for friend in human.friends:
            friend_node = self._graph.merge_one("Human", "uid", friend.uid)
            self._graph.create_unique(py2neo.Relationship(human_node, "FRIEND", friend_node))
