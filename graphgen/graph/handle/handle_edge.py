def remove_redundant_edges(edge_list):
    # 创建一个图的邻接表
    graph = {}

    # 构建邻接表
    for source, target in edge_list:
        if source not in graph:
            graph[source] = set()
        graph[source].add(target)

    # 用于存储保留的边
    filtered_edges = []

    # 遍历边列表，检查并保留最近关系
    for source, target in edge_list:
        # 检查 target 是否有共同邻居
        common_neighbors = {neighbor for neighbor in graph.get(target, [])}

        # 如果没有共同邻居，则保留该边
        if not common_neighbors:
            filtered_edges.append((source, target))

    return filtered_edges


# 示例边关系
edge_list = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [2, 3], [4, 5], [4, 7], [4, 8], [5, 7], [5, 8], [5, 9], [6, 7], [6, 8], [7, 8], [7, 9], [8, 9]]

# 过滤多余的边
filtered_edges = remove_redundant_edges(edge_list)

print(filtered_edges)
