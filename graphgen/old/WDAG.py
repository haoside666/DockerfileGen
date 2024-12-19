from collections import defaultdict
import heapq

class WDAG:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))

    def topo_sort(self):
        # 计算每个节点的入度
        indegree = defaultdict(int)
        for node in self.graph:
            for neighbor, weight in self.graph[node]:
                indegree[neighbor] += 1

                # 构建堆
        heap = [(0, node) for node in self.graph if indegree[node] == 0]
        heapq.heapify(heap)

        # 进行拓扑排序
        result = []
        while heap:
            _, node = heapq.heappop(heap)
            result.append(node)
            for neighbor, weight in self.graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    heapq.heappush(heap, (0, neighbor))
        return result
    def build(self):

        return

# 创建一个WDAG示例
dag = WDAG()
dag.add_edge('A', 'B', 1)
dag.add_edge('A', 'C', 2)
dag.add_edge('B', 'D', 3)
dag.add_edge('C', 'D', 2)
dag.add_edge('D', 'E', 1)

# 进行拓扑排序
topological_order = dag.topological_sort()
print("拓扑排序结果:", topological_order)
