import sys

def read_image_data(filename):
    result = []
    with open(filename) as f:
        for line in f:
            result.extend([int(d) for d in line.strip('\n')])
        return result
def get_layers_from_image_data(image_data, width, height):
    total_image_pixels = (width * height)
    num_layers = len(image_data) // total_image_pixels
    pixels_per_layer = width * height
    print('digits={0} num_layers={1} pixels_per_layer={2}'.format(len(image_data), num_layers, pixels_per_layer))
    layers = []
    current_layer = []
    for i in range(len(image_data)):
        if (i + 1) % pixels_per_layer == 0:
            current_layer.append(image_data[i])
            layers.append(current_layer)
            current_layer = []
        else:
            current_layer.append(image_data[i])

    if len(current_layer) > 0:
        layers.append(current_layer)
    return layers

def solve(image_data, width, height):
    layers = get_layers_from_image_data(image_data, width, height)
    print('Total number of layers: {0}'.format(len(layers)))
    min_zeros = 0xFFFFFFFFFFFF
    result = 0
    for layer in layers:
        num_zeros = sum(pixel == 0 for pixel in layer)
        if num_zeros < min_zeros:
            min_zeros = num_zeros
            result = sum(pixel == 1 for pixel in layer) * sum(pixel == 2 for pixel in layer)
    return result

if __name__ == "__main__":
    image_data = read_image_data(sys.argv[1])
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    # for input width = 25 and height = 6
    print('Answer={0}'.format(solve(image_data, width, height)))