def extractNeighborhood(matrix, row, col, neighborhood_size):
    # Extract the neighborhood from the given matrix.
    # The center of the neighborhood is indexed by row/col.
    neighborhood = matrix[
                   row - (neighborhood_size // 2):row + (neighborhood_size // 2) + 1,
                   col - (neighborhood_size // 2):col + (neighborhood_size // 2) + 1]
    return neighborhood
