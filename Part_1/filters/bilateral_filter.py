from utils import *

def bilateral_filter(image, neighborhood_size, spatial_sigma, intensity_sigma):
    # Obtenir les dimensions de l'image
    height, width = image.shape
    # Initialiser l'image filtrée
    result = np.zeros((height, width))
    # Calculer la distance separant le pixel central et les bords du voisinage(pour savoir si le voisinage depasse)
    half_size = neighborhood_size // 2

    #parcourir chaque pixels
    for y in range(height):
        for x in range(width):
            #initialiser la somme des poids a zero
            weight_sum = 0
            filtered_value = 0
            #parcourir chaque voisin du pixel
            for i in my_range( half_size + 1, start = -half_size):
                for j in my_range(half_size + 1, start = -half_size):
                    #position du voisin
                    neighbor_y, neighbor_x = y + i, x + j
                    #si le voisin est a l'interieur de l'image (ne deborde pas)
                    if 0 <= neighbor_y < height and 0 <= neighbor_x < width:
                        #calculer la difference spatiale (distance) entre le pixel et son voisin
                        spatial_diff = (i**2 + j**2)**0.5
                        #calculer la difference d'intensite du pixel et de son voisin 
                        intensity_diff = abs(float(image[y, x]) - float(image[neighbor_y, neighbor_x]))

                        #fonction gaussienne avec hyperparametre sigma_s comme parametre (2.71828 = e) 
                        spatial_weight = 2.71828**(-(spatial_diff**2) / (2 * spatial_sigma**2))
                        #fonction gaussienne avec hyperparametre sigma_i comme parametre (2.71828 = e) 
                        intensity_weight = 2.71828**(-(intensity_diff**2) / (2 * intensity_sigma**2))
                        #calcule du poid(produis des fonctions gaussiennes)
                        weight = spatial_weight * intensity_weight
                        #somme des poids
                        weight_sum += weight
                        #somme du produit entre l'intensite du voisin et le poids calcule
                        filtered_value += weight * float(image[neighbor_y, neighbor_x])
            #normalisation par la somme des poids
            result[y, x] = filtered_value / weight_sum

    return np.array(result, dtype=np.uint8)
