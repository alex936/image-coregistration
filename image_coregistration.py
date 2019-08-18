import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from nevergrad.optimization.optimizerlib import registry as optimizers
from skimage.transform import warp, AffineTransform

from make_gif import make_gif


def load_img(path):
    img = Image.open(path)
    img = np.array(img, dtype="float32")
    return img


def transform_image(img, scale=None, rotation=None, shear=None, translation=None):
    if rotation is not None:
        rotation = np.clip(rotation, -1.57, 1.57)
    if shear is not None:
        rotation = np.clip(rotation, -1.57, 1.57)
    if scale is not None:
        scale = np.clip(scale, -5, 5)

    tform = AffineTransform(scale=scale,
                            translation=translation, shear=shear, rotation=rotation)
    transformed = warp(img, tform, cval=255, mode='constant')
    return transformed


def calculate_error(wrap_img, target_img):
    # Intersection over Union
    img1 = wrap_img.copy()
    img2 = target_img.copy()
    aou = np.sum(img1 == 0) + np.sum(img2 == 0)
    img1[img1 == 0] = 1
    img1[img1 == 255] = 0
    img2[img2 == 0] = 1
    img2[img2 == 255] = -1
    aoo = np.sum(img1.flatten() == img2.flatten())
    return -(aoo / aou)



if __name__ == "__main__":
    target_img = load_img('data/target.png')
    input_img = load_img('data/input.png')

    optimizer_name = "CMA"
    optimizer = optimizers[optimizer_name](instrumentation=6, budget=3000)
    errors = []
    for i in range(optimizer.budget):
        parameters = optimizer.ask()
        transformed_img = transform_image(input_img, translation=(parameters.data[0], parameters.data[1]),
                                               scale=(parameters.data[2], parameters.data[3]),
                                               shear=parameters.data[4] / 100,
                                               rotation=parameters.data[5] / 100)
        error = calculate_error(transformed_img, target_img)
        errors.append(error)
        print(" Iteration {}".format(i))
        print("Error is {}".format(error))
        optimizer.tell(parameters, error)
        if i % 50 == 0:
            img = Image.fromarray(transformed_img.astype('uint8'))
            img.save('data/output/output_itr_{}.png'.format(i))

    plt.plot(errors)
    plt.xlabel('Iteration')
    plt.ylabel('Error')
    plt.savefig('data/output/errors.png')
    img = Image.fromarray(transformed_img.astype('uint8'))
    img.save('data/output/output.png')
    make_gif('data/output/')
