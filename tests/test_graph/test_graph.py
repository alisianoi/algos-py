from graph.graph import Graph, DiGraph


class TestGraph:
    def setup(self):
        self.g = Graph()

    def test_add_edge(self):
        self.g.add_edge(0, 1)
        for i in range(2): len(self.g.edges[i]) == 1

    def test_add_edge_loop(self):
        for i in range(10):
            self.g.add_edge(i, i + 1)

        for i in range(1, 9):
            assert len(self.g.edges[i]) == 2

        for i in [0, 10]:
            assert len(self.g.edges[i]) == 1

    def test_del_edge(self):
        self.g.add_edge(0, 1)
        for i in [0, 1]:
            assert len(self.g.edges[i]) == 1

        self.g.del_edge(0, 1)
        for i in [0, 1]:
            assert len(self.g.edges[i]) == 0

    def test_del_edge_nonexistent(self):
        self.g.del_edge(0, 1)
        assert True

    def test_del_edge_multiple(self):
        for i in range(3): self.g.add_edge(0, 1)
        self.g.del_edge(0, 1)
        for i in range(2): assert len(self.g.edges[i]) == 0


class TestDiGraph:
    def setup(self):
        self.g = DiGraph()

    def test_add_edge_0(self):
        self.g.add_edge(0, 1)

        assert self.g.edges[0] == [1]
        assert self.g.edges[1] == []

    def test_add_edge_1(self):
        self.g.add_edge(0, 1)
        self.g.add_edge(0, 1)

        assert self.g.edges[0] == [1, 1]
        assert self.g.edges[1] == []

    def test_add_edge_2(self):
        self.g.add_edge(0, 1)
        self.g.add_edge(1, 0)

        assert self.g.edges[0] == [1]
        assert self.g.edges[1] == [0]

    def test_del_edge_0(self):
        self.g.del_edge(0, 1)

        assert self.g.edges == {}

    def test_del_edge_1(self):
        self.g.add_edge(0, 1)
        self.g.del_edge(0, 1)

        assert self.g.edges[0] == []
        assert self.g.edges[1] == []

    def test_del_edge_2(self, N=10):
        for i in range(N):
            self.g.add_edge(0, 1)

        self.g.del_edge(0, 1)

        assert self.g.edges[0] == []
        assert self.g.edges[1] == []

    def test_del_edge_3(self):
        self.g.add_edge(0, 1)
        self.g.add_edge(0, 2)
        self.g.add_edge(1, 2)

        self.g.del_edge(0, 1)

        assert self.g.edges[0] == [2]
        assert self.g.edges[1] == [2]
        assert self.g.edges[2] == []

    def test_transpose_0(self):
        t = self.g.transpose()

        assert t.edges == {}

    def test_transpose_1(self):
        self.g.add_edge(0, 1)

        t = self.g.transpose()

        assert t.edges[0] == []
        assert t.edges[1] == [0]

    def test_transpose_2(self):
        self.g.add_edge(0, 1)
        self.g.add_edge(1, 0)

        t = self.g.transpose()

        assert t.edges[0] == []
        assert t.edges[1] == []

    def test_transpose_3(self, N=10):
        for i in range(N):
            self.g.add_edge(i, i + 1)

        self.g.add_edge(N, 0)

        t = self.g.transpose()

        for i in range(N + 1):
            for j in range(N + 1):
                if j == i or j == i + 1 or (j == 0 and i == N):
                    assert j not in t.edges[i]
                else:
                    assert j in t.edges[i], "{} {}".format(j, i)

    def test_has_cycle_0(self):
        assert self.g.has_cycle() is False

    def test_has_cycle_1(self):
        self.g.add_edge(0, 1)

        assert self.g.has_cycle() is False

    def test_has_cycle_2(self):
        self.g.add_edge(0, 1)
        self.g.add_edge(1, 0)

        assert self.g.has_cycle() is True

    def test_has_cycle_3(self, N=10):
        for i in range(N):
            self.g.add_edge(i, i + 1)

        self.g.add_edge(N, 0)

        assert self.g.has_cycle() is True

    def test_rpostdfs_0(self):
        assert list(self.g.rpostdfs()) == []

    def test_rpostdfs_1(self, N=10):
        for i in range(N):
            self.g.add_edge(i, i + 1)

        rorder = self.g.rpostdfs()

        assert list(rorder) == list(range(N + 1))

    def test_rpostdfs_2(self):
        self.g.add_edge(0, 1)
        self.g.add_edge(1, 0)

        rorder = list(self.g.rpostdfs())

        assert rorder == [0, 1] or rorder == [1, 0]

    def test_toposort_0(self):
        assert list(self.g.toposort()) == []

    def test_toposort_1(self):
        self.g.add_edge(0, 1)
        self.g.add_edge(1, 0)

        assert self.g.toposort() is None

    def test_toposort_2(self, N=10):
        for i in range(N):
            self.g.add_edge(i + 1, i)

        assert list(self.g.toposort()) == list(range(N, -1, -1))

    def test_sconcomp_0(self):
        scc = self.g.sconcomp()

        assert scc == {}

    def test_sconcomp_1(self):
        self.g.add_edge(0, 1)

        scc = self.g.sconcomp()

        assert scc[0] != scc[1], scc[1]

    def test_sconcomp_2(self):
        self.g.add_edge(0, 1)
        self.g.add_edge(1, 0)

        scc = self.g.sconcomp()

        assert scc[0] == scc[1]

    def test_sconcomp_3(self, N=10):
        for i in range(N):
            self.g.add_edge(i, i + 1)

        self.g.add_edge(N, 0)

        scc = self.g.sconcomp()

        for i in range(N):
            assert scc[i] == scc[i + 1]