def resolve_dependencies(dependencies):
    if not isinstance(dependencies, dict):
        return []
    
    # Initialize in-degree for each package
    in_degree = {package: 0 for package in dependencies}
    
    # Count dependencies for each package
    for package, deps in dependencies.items():
        for dep in deps:
            if dep not in in_degree:
                in_degree[dep] = 0
            in_degree[dep] += 1
    
    # Collect all packages that have no dependencies
    queue = [package for package in in_degree if in_degree[package] == 0]
    
    # Result list to store the order of packages
    result = []
    
    while queue:
        # Pop the package with the smallest name
        package = min(queue)
        result.append(package)
        queue.remove(package)
        
        # Decrease the in-degree of all its dependencies
        for dep in dependencies.get(package, []):
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)
    
    # Check for cycles
    if len(result) != len(dependencies):
        return []
    
    return result