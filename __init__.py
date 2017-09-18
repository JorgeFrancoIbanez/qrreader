# Author: Jorge Franco
# Based on the Jimmyromanticdevil project
# # QRbar-cv
# # Some of Good Refrensi stuff :
# #   https://github.com/jayrambhia/Install-OpenCV
# #   http://nwlinux.com/install-qtqr-in-ubuntu-10-04-lucid-using-apt-get/
# #   http://zbar.sourceforge.net/
#

######################################################
## Clean Capture qr function
######################################################
# set_width = 100.0 / 100
# set_height = 90.0 / 100
#
# a = False
#
# coord_x = int(frame.width * (1 - set_width) / 2)
# coord_y = int(frame.height * (1 - set_height) / 2)
# width = int(frame.width * set_width)
# height = int(frame.height * set_height)
#
# get_sub = cv.GetSubRect(frame, (coord_x + 1, coord_y + 1, width - 1, height - 1))
#
# cv.Rectangle(frame, (coord_x, coord_y), (coord_x + width, coord_y + height), (255, 0, 0))
#
# cm_im = cv.CreateImage((get_sub.width, get_sub.height), cv.IPL_DEPTH_8U, 1)
# cv.ConvertImage(get_sub, cm_im)
# image = zbar.Image(cm_im.width, cm_im.height, 'Y800', cm_im.tostring())
# set_zbar.scan(image)
#
# for symbol in image:
#     print '\033[1;32mResult : %s symbol "%s" \033[1;m' % (symbol.type, symbol.data), i
#     a = True
#     move()
# cv.ShowImage("webcame", frame)
# # cv.ShowImage("webcame2", get_sub)
# cv.WaitKey(10)
# return a



# #####################################################################
# Owe img drawer image                                                          #
# #####################################################################
#
# img = cv2.imread('qr.jpg',0)
# rows,cols = img.shape
#
# for i in range(0,290,2):
#     M = np.float32([[1,0,i],[0,1,i]])
#     dst = cv2.warpAffine(img,M,(cols,rows))
#
#     window = cv2.imshow('img',dst)
#     cv2.waitKey(1)
#     cv2.destroyAllWindows()




import cv2.cv as cv  # Use OpenCV-2.4.3
import cv2
import numpy as np
import os
import shutil
import zbar
import subprocess
import argparse

def createQRCodeVideoExampleLeftToRight(base_dir, img_dir, newImage=0):
    print base_dir, ' ', img_dir
    # create a video file from an image
    img = cv2.imread(img_dir, 0)
    # img = cv2.imread('sources/qrcode/qr.jpg', 0)
    rows, cols = img.shape
    # Delete old files images
    if newImage:
        if os.path.exists(base_dir+'sources/gif'):
            shutil.rmtree(base_dir+'sources/gif')
        os.makedirs(base_dir+'sources/gif')
        cont = 0

        # Move the qr.jpg from left to right
        for i in range(0, 1210, 1):
            M = np.float32([[1, 0, i], [0, 1, (rows+700)/2]])
            dst = cv2.warpAffine(img, M, (cols+1200, rows+700))


            # window = cv2.imshow('img', dst)
            cv2.waitKey(1)
            cv2.imwrite(base_dir+'sources/gif/img'+str(cont).zfill(3)+'.jpg', dst)
            # cv2.destroyAllWindows()
        cont+=1
    if not os.path.isfile(base_dir+'sources/output.mp4'):
        print 'output file not found:'
        bashCommand = 'ffmpeg -framerate 60 -i '+base_dir+'sources/gif/img%03d.jpg '+base_dir+'sources/output.mp4'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()


def scanner_procces(frame, set_zbar, i):
    set_width = 100.0 / 100
    set_height = 90.0 / 100

    a = False

    # size of the formated image, video file or cam source video recorded
    coord_x = int(frame.width * (1 - set_width) / 2)
    coord_y = int(frame.height * (1 - set_height) / 2)
    width = int(frame.width * set_width)
    height = int(frame.height * set_height)

    # describe the area to be cropped
    get_sub = cv.GetSubRect(frame, (coord_x + 1, coord_y + 1, width - 1, height - 1))

    # Function to draw the rectangle without fill
    cv.Rectangle(frame, (coord_x, coord_y), (coord_x + width, coord_y + height), (255, 0, 0))

    #this function take RGB image.Then convert it into grey image
    cm_im = cv.CreateImage((get_sub.width, get_sub.height), cv.IPL_DEPTH_8U, 1)
    cv.ConvertImage(get_sub, cm_im)

    #Create the scanner
    image = zbar.Image(cm_im.width, cm_im.height, 'Y800', cm_im.tostring())
    set_zbar.scan(image)

    for symbol in image:
        if i == 400:
            print '\033[1;32mResult : %s symbol "%s" \033[1;m' % (symbol.type, symbol.data), i
            # print 'AQUI SE LLAMARIA A LA OPCION DE RECONOCER EL VEHICULO CON ESTE FRAME'

            # Buscando el metodo de conversionde frame a img
            cv2.imwrite('frame.png', frame)

            a = True
            # move()
        a = True

    #display
    # cv.ShowImage("webcame", frame)
    # cv.ShowImage("webcame2", get_sub)
    cv.WaitKey(10)
    return a

def main(base_dir):
    # # set up our stuff
    i = 1
    # set Window Image
    # cv.NamedWindow("webcame", cv.CV_WINDOW_AUTOSIZE)
    capture = cv.CaptureFromFile(base_dir+'sources/output.mp4')  # Lectura de un video por frame

    # capture = cv.CaptureFromCAM(-1)    # Lectura de la camara


    # creation of the reader
    set_zbar = zbar.ImageScanner()

    while True:
        # Captura los frames de la fuente del video. Video o Captura de camara.
        frame = cv.QueryFrame(capture)
        # Si No Hay mas frames sale del programa
        if not frame:
            exit()
        if scanner_procces(frame, set_zbar, i):
            i += 1