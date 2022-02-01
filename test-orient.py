import numpy as np
import SimpleITK as sitk
import os
import os.path as osp
import  matplotlib.pyplot as plt

def reverse_axes(image):
    return np.transpose(image, tuple(reversed(range(image.ndim))))

def read_image(imagefile):
    image = sitk.ReadImage(str(imagefile))
    data = reverse_axes(sitk.GetArrayFromImage(image))  # switch from zyx to xyz

    cosine = np.asarray(image.GetDirection()).reshape(3, 3)
    cosine_inv = np.linalg.inv(np.round(cosine))
    swap = np.argmax(abs(cosine_inv), axis=0)
    flip = np.sum(cosine_inv, axis=0)
    data = np.transpose(data, tuple(swap))
    print("after transpose")
    data = data[tuple(slice(None, None, int(f)) for f in flip)]
    data = np.rot90(data, -1)
    data = np.transpose(data, (2,0,1))


    return data

def normalize_slice_orientation(image, header):
    header['original'] = header.copy()

    # Compute inverse of cosine (round first because we assume 0/1 values only)
    # to determine how the image has to be transposed and flipped for cosine = identity
    cosine = np.asarray(header['direction']).reshape(3, 3)
    cosine_inv = np.linalg.inv(np.round(cosine))

    swap = np.argmax(abs(cosine_inv), axis=0)
    flip = np.sum(cosine_inv, axis=0)
    image = np.transpose(image, tuple(swap))
    image = image[tuple(slice(None, None, int(f)) for f in flip)]
    image = np.rot90(image, -1)
    image = reverse_axes(image)


    return swap_flip_dimensions(cosine_inv, image, header)



def swap_flip_dimensions(cosine_matrix, image, header=None):
    # Compute swaps and flips
    swap = np.argmax(abs(cosine_matrix), axis=0)
    flip = np.sum(cosine_matrix, axis=0)
    # Apply transformation to image volume
    image = np.transpose(image, tuple(swap))
    image = image[tuple(slice(None, None, int(f)) for f in flip)]

    if header is None:
        return image

    # Apply transformation to header
    header['spacing'] = tuple(header['spacing'][s] for s in swap)
    header['direction'] = np.eye(3)
    image = np.rot90(image, -1)
    return image, header


def restore_original_slice_orientation(mask, header):
    # Use original orientation for transformation because we assume the image to be in
    # normalized orientation, i.e., identity cosine)
    cosine = np.asarray(header['original']['direction']).reshape(3, 3)
    cosine_rnd = np.round(cosine)

    # Apply transformations to both the image and the mask
    return swap_flip_dimensions(cosine_rnd, mask), header['original']

base_dir = "/home/lin/Desktop/msd/Task08_HepaticVessel/imagesTr/"
for f in os.listdir(base_dir):
    data = read_image(osp.join(base_dir, f))
    # data, _ = normalize_slice_orientation(data, header)
    plt.imshow(data[10,:,:])
    plt.show()

# https://gist.github.com/nlessmann/24d405eaa82abba6676deb6be839266civ
