def resolve_dependencies(dependencies):
    if not isinstance(dependencies, dict):
        return []
    
    # Convert the dictionary to a list of tuples (package, dependencies)
    packages = list(dependencies.items())
    package_names = set()
    dependencies_graph = {package: [] for package, deps in packages}
    
    # Build the graph and count in-degrees
    for package, deps in packages:
        package_names.add(package)
        for dep in deps:
            if dep in package_names:
                dependencies_graph[package].append(dep)
    
    # Check for cycles
    def has_cycle(graph):
        in_degree = {node: 0 for node in graph}
        for node in graph:
            for neighbor in graph[node]:
                in_degree[neighbor] += 1
        queue = [node for node in graph if in_degree[node] == 0]
        while queue:
            node = queue.pop(0)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return any(in_degree[node] > 0 for node in in_degree)
    
    if has_cycle(dependencies_graph):
        return []
    
    # Perform Lexicographical Topological Sort
    sorted_packages = []
    while packages:
        package, deps = packages.pop(0)
        if all(dep in package_names for dep in deps):
            sorted_packages.append(package)
            for dep in deps:
                dependencies_graph[dep].remove(package)
                if not dependencies_graph[dep]:
                    packages.append((dep, dependencies_graph[dep]))
    return sorted_packages