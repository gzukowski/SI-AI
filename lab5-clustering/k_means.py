import numpy as np

def initialize_centroids_forgy(data, k):
    # TODO implement random initialization

    centroids = [None for _ in range(k)]

    for idx in range(k):
        random_index = np.random.randint(0, data.shape[0])
        centroids[idx] = data[random_index]
    centroids = np.vstack(centroids)
    return centroids

def initialize_centroids_kmeans_pp(data, k):
    # TODO implement kmeans++ initizalization

    n_samples = data.shape[0]

    centroids = [None for _ in range(k)]

    random_index = np.random.randint(0, data.shape[0])

    centroids[0] = data[random_index]


    distances = np.full(n_samples, np.inf)
    

    for i in range(1, k):
        for j in range(n_samples):

            new_dist = np.linalg.norm(data[j] - centroids[i-1])**2
            distances[j] = min(distances[j], new_dist)
        
        probabilities = distances / distances.sum()
        next_centroid_index = np.random.choice(n_samples, p=probabilities)
        centroids[i] = data[next_centroid_index]
    
    centroids = np.vstack(centroids)
    return centroids


def assign_to_cluster(data, centroids):
    # TODO find the closest cluster for each data point

    assignments = [None for _ in range(len(data))]

    for i, point in enumerate(data):

        distances = np.sqrt((centroids - point) ** 2)
        distances = np.sum(distances, axis=1)

        closest_centroid_index = np.argmin(distances)

        assignments[i] = closest_centroid_index

    return assignments

def update_centroids(data, assignments, k):
    # TODO find new centroids based on the assignments

    centroids_num = k

    matrix = [[] for _ in range(centroids_num)]


    for i, point in enumerate(data):
        assignment_value = assignments[i]

        matrix[assignment_value].append(point)

    centroids = [None for _ in range(centroids_num)]
    for idx, row in enumerate(matrix):
        mean = np.mean(row, axis=0)

        if np.any(np.isnan(mean)):
            mean = [0,0,0,0]

            
        centroids[idx] = mean

    try:
        centroids = np.vstack(centroids)
    except ValueError:
        print(centroids, assignments)
    
    return centroids

def mean_intra_distance(data, assignments, centroids):
    return np.sqrt(np.sum((data - centroids[assignments, :])**2))

def k_means(data, num_centroids, kmeansplusplus= False):
    # centroids initizalization
    if kmeansplusplus:
        centroids = initialize_centroids_kmeans_pp(data, num_centroids)
    else: 
        centroids = initialize_centroids_forgy(data, num_centroids)

    
    assignments  = assign_to_cluster(data, centroids)
    for i in range(100): # max number of iteration = 100
        print(f"Intra distance after {i} iterations: {mean_intra_distance(data, assignments, centroids)}")
        centroids = update_centroids(data, assignments, num_centroids)
        new_assignments = assign_to_cluster(data, centroids)
        if np.all(new_assignments == assignments): # stop if nothing changed
            break
        else:
            assignments = new_assignments

    return new_assignments, centroids, mean_intra_distance(data, new_assignments, centroids)         

