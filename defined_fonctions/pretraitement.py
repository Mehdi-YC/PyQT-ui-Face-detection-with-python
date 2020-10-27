
import numpy as np
import cv2
import matplotlib.pyplot as plt


def normalisation(pic):
    img = cv2.imread(pic, 0)
    norm_img = np.zeros((600, 600))
    final_img = cv2.normalize(img,  norm_img, 0, 255, cv2.NORM_MINMAX)
    path = pic.split('/')
    path = path[:-2]
    path = '/'.join(path)
    path = path+'/pertraitement/normalisation.jpg'
    cv2.imwrite(path, final_img)
    return(path)


def egalisation_hist(pic):
    img = cv2.imread(pic, 0)
    img1 = cv2.equalizeHist(img)
    path = pic.split('/')
    path = path[:-2]
    path = '/'.join(path)
    path = path+'/pertraitement/egalisation.jpg'
    cv2.imwrite(path, img1)

    fig = plt.figure()
    plt.style.use("mehdi")
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.hist(img.ravel(), 256, [0, 256])

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.hist(img1.ravel(), 256, [0, 256])
    #extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

    plt.savefig('hist.dark.jpg')

    fig2 = plt.figure()
    plt.style.use('mehdilight')
    ax1 = fig2.add_subplot(1, 2, 1)
    ax1.hist(img.ravel(), 256, [0, 256])

    ax2 = fig2.add_subplot(1, 2, 2)
    ax2.hist(img1.ravel(), 256, [0, 256])

    plt.savefig('hist.jpg')

    # fig.savefig("/histogramme/hist.jpg")
    #plt.subplot(1, 2, 1)
    #plt.hist(img.ravel(), 256, [0, 256])
    #plt.subplot(1, 2, 2)
    #plt.hist(img1.ravel(), 256, [0, 256])
    # plt[0].savefig("/histogramme/hist.jpg")
    # plt.show()
    return(path)


def filtre_median(pic):
    img = cv2.imread(pic, 0)
    img_median = cv2.medianBlur(img, 5)
    path = pic.split('/')
    path = path[:-2]
    path = '/'.join(path)
    path = path+'/pertraitement/filtre_median.jpg'
    cv2.imwrite(path, img_median)
    return(path)


def debruit_img(pic):
    img = cv2.imread(pic, 0)
    cv2.fastNlMeansDenoising(img, img, 30.0, 7, 21)
    path = pic.split('/')
    path = path[:-2]
    path = '/'.join(path)
    path = path+'/pertraitement/debruit_img.jpg'
    cv2.imwrite(path, img)
    return(path)
