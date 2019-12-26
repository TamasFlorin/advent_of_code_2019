import sys
from PIL import Image
from functools import reduce 
from operator import mul

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

def reshape(data, shape):
    if len(shape) == 1:
        return data
    n = reduce(mul, shape[1:])
    return [reshape(data[i*n:(i+1)*n], shape[1:]) for i in range(len(data)//n)]

def get_image_from_layers(layers, width, height):
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    pixels = image.load()

    for i in range(len(layers)):
        current_layer = reshape(layers[i], (height, width))
        for y in range(height):
            for x in range(width):
                # transparent 
                if pixels[x, y] == (255, 255, 255, 0):
                    # black color
                    if current_layer[y][x] == 0:
                        pixels[x, y] = (127, 128, 127, 255)
                    # white color
                    elif current_layer[y][x] == 1:
                        pixels[x, y] = (255, 255, 255, 255)
    return image

def solve(image_data, width, height):
    layers = get_layers_from_image_data(image_data, width, height)
    print('Total number of layers: {0}'.format(len(layers)))
    image = get_image_from_layers(layers, width, height)
    print('Genrated image size={0}'.format(image.size))
    image.save('result.png')

if __name__ == "__main__":
    image_data = read_image_data(sys.argv[1])
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    # for input width = 25 and height = 6
    solve(image_data, width, height)