from ast import Try
from asyncio.windows_events import NULL
from Task7_UIIIIIII import Ui_MainWindow , MplWidget
import sys
from IPython.display import display, Math, Latex
from PIL import Image
import cv2
import os
import numpy as np
from numpy import asarray
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
import pydicom
import math 
import PIL
import random
from pydicom.data import get_testdata_files
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageQt, ImageEnhance
from matplotlib.widgets import RectangleSelector
from phantominator import shepp_logan
import smear
import piradon
from skimage.transform import radon, rescale, rotate,iradon

import qdarkstyle

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self): 
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Draw_T()
        self.shear_image(-45)
        self.Original_ROI()
        self.ROI_Noise()
        
        self.ui.actionBrowse.triggered.connect(self.Load)
        self.ui.Show_Hist_pushButton.clicked.connect(self.histogram)
        self.ui.actionBrowse.triggered.connect(self.Original_View)
        self.ui.actionBrowse.triggered.connect(self.OriginalDE)
        self.ui.Noise_pushButton.clicked.connect(self.Salt_and_papper)
        self.ui.Filter_pushButton.clicked.connect(self.median_filter)
        self.ui.Sharp_pushButton.clicked.connect(self.boxFilter)
        self.ui.Show_Original_Magnitiude_pushButton.clicked.connect(self.Original_Mag)
        self.ui.Show_Original_Phase_pushButton.clicked.connect(self.Original_Phase)
        self.ui.Show_Logged_Magnitiude_pushButton.clicked.connect(self.Logged_Mag)
        self.ui.Show_Logged_Phase_pushButton.clicked.connect(self.Logged_Phase)
        self.ui.Blur_pushButton.clicked.connect(self.Blurring)
        self.ui.Fourier_pushButton.clicked.connect(self.Fourier_Filtering)
        self.ui.Difference_pushButton.clicked.connect(self.Difference)
        self.ui.Show_ROI_Hist_pushButton.clicked.connect(self.ROI_Histogram)
        self.ui.Moire_Filter_pushButton.clicked.connect(self.Moire_Pattern)
        self.ui.ROI_Noise_pushButton.clicked.connect(self.ROI_Noise)
        self.ui.ZoomFactor_lineEdit.returnPressed.connect(self.Nearest_Interpolation)
        self.ui.ZoomFactor_lineEdit.returnPressed.connect(self.Bilinear_Interpolation)
        self.ui.Shear_pushButton.clicked.connect(lambda: self.shear_image(45))
        self.ui.Show_Phantom_pushButton.clicked.connect(self.Phantom) 
        self.ui.Show_Sinogram_pushButton.clicked.connect(self.Sinogram) 
        self.ui.Show_Laminogram_pushButton.clicked.connect(self.Laminogram) 
        self.ui.Show_Laminogram_NoFilter_pushButton.clicked.connect(self.LaminogramNoFilter) 
        self.ui.Show_Laminogram_Hamming_pushButton.clicked.connect(self.LaminogramHamming) 
        self.ui.Show_Laminogram_RamLak_pushButton.clicked.connect(self.LaminogramRamlak) 
        self.ui.Erosion_pushButton.clicked.connect(self.DrawErosin) 
        self.ui.Dilation_pushButton.clicked.connect(self.DrawDilation) 
        self.ui.Rotation_Angle_lineEdit.returnPressed.connect(self.rotation)
        self.Select_ROI()

    def shear_image(self, sheared_angle):
        sheared_angle = -sheared_angle

        #  convert rotation amount to radian
        sheared_amount_rad = math.radians(sheared_angle)

        #  get dimension info
        height, width= 128 ,128

        
        sheared_image = np.zeros((128,128))

        sheared_height, sheared_width = 128,128
        mid_row = int( (sheared_height+1)/2 )
        mid_col = int( (sheared_width+1)/2 )

        for i in range(width):
            for j in range(height):

                x = (i-mid_col)
                y = (j-mid_row)
                
                new_x = round(x-y*math.tan(sheared_amount_rad/2))
                new_y = y

                new_x = new_x + mid_row
                new_y = new_y + mid_col

                if (new_x >= 0 and new_y >= 0 and new_x < width and new_y < height):
                    sheared_image[j][i] = self.Timage[new_y,new_x]

        ImageSheared=PIL.Image.fromarray(sheared_image)
        ImageSheared = ImageSheared.convert('L')            
        self.imgQ = ImageQt.ImageQt(ImageSheared)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneShearedImage.addPixmap(pixMap)        
        # self.ui.NearestNeighbor_Rotation_graphicsView.fitInView(QRectF(0, 0,128,128),Qt.KeepAspectRatio)
        self.ui.sceneShearedImage.update()
       
    def rotation(self):
        try:
            float(self.ui.Rotation_Angle_lineEdit.text())
        except:
            QMessageBox.critical(self, "Error", "Please, Enter valid number")
            return

        if self.ui.radioButton_Nearest.isChecked():
            self.Rotation_Nearest()
        elif self.ui.radioButton_Linear.isChecked():
            self.Rotation_Linear()
        else:
            QMessageBox.critical(self, "Error", "Please, choose type of interpolation")

    def Load(self):
        self.path = filedialog.askopenfilename(filetypes=[("Images" ,".dcm .jpg .bmp .png .jpeg" )])
        ext = os.path.splitext(self.path)[-1].lower()
        self.ui.scene.clear()
        if ext == ".dcm":
                try:
                    Dicomraw = pydicom.dcmread(self.path)
                    fileinfo= pydicom.read_file(self.path)                  
                    image=Dicomraw.pixel_array.astype(float)
                except :
                    self.ui.textBrowser.clear() 
                    self.ui.textBrowser.append('Not Working')  
                    return
                rescaled_image = (np.maximum(image,0)/image.max())*255 # float pixels
                final_image = np.uint8(rescaled_image) # integers pixels
                final_image = Image.fromarray(final_image)
                final_image.save('now_image.jpg')  
                self.path ='now_image.jpg'
                self.img = Image.open('now_image.jpg')
                self.imgGray = self.img.convert('L') #Convert into grayscale 
                # print(fileinfo) #dicom info
                try:
                    self.img = Image.open(self.path)
                except:
                    self.ui.textBrowser.append('Not Working') 
                    return
                w, h = self.img.size
                self.imgQ = ImageQt.ImageQt(self.img)  # we need to hold reference to imgQ, or it will crash
                pixMap = QPixmap.fromImage(self.imgQ)
                self.ui.scene.addPixmap(pixMap)
                print(fileinfo)
                self.ui.Image_graphicsView.fitInView(QRectF(0, 0, w, h))
                self.ui.textBrowser.append("Patient Name: "+str(fileinfo.get("PatientName")))
                self.ui.textBrowser.append("Patient Age: "+str(fileinfo.get("PatientAge")))
                self.ui.textBrowser.append("Modality: "+str(fileinfo.get("Modality")))
                self.ui.textBrowser.append("Body Part Examined: "+str(fileinfo.get("BodyPartExamined")))
                self.ui.textBrowser.append("Width: "+str(w))
                self.ui.textBrowser.append("height "+str(h))
                self.bitdepth=fileinfo.get("BitsAllocated")
                self.ui.textBrowser.append('Rows X Columns = '+ str(h) +" x "+ str(w))
                self.ui.textBrowser.append("Bit Depth:  "+ str(fileinfo.get("BitsAllocated")))
                self.SizeInBits=(int(w*h*self.bitdepth))
                self.ui.textBrowser.append("Size (Bits) "+str(self.SizeInBits))
                self.bit=os.stat(self.path).st_size
                self.ui.Image_graphicsView.fitInView(QRectF(0, 0, w, h) , Qt.KeepAspectRatio)

                self.ui.scene.update()
                
        else:   
                try:
                    self.img = Image.open(self.path)
                except:
                    self.ui.textBrowser.clear() 
                    self.ui.textBrowser.append('Not Working')  
                    return

                imaa=cv2.imread(self.path)
                self.imgGray = self.img.convert('L') #Convert into grayscale 
                w, h = self.img.size
                
                self.imgQ = ImageQt.ImageQt(self.img)  # we need to hold reference to imgQ, or it will crash
                pixMap = QPixmap.fromImage(self.imgQ)
                self.ui.scene.addPixmap(pixMap)

                self.ui.Image_graphicsView.fitInView(QRectF(0, 0, w, h) , Qt.KeepAspectRatio)
                self.ui.textBrowser.clear()
                self.ui.textBrowser.append("Width: "+str(w))
                self.ui.textBrowser.append("height "+str(h))
                self.ui.textBrowser.append("Image Color:  " + str(self.img.mode)) #RGB or Grayscale
                (self.Wedith,self.Height,self.Depth)=imaa.shape
                self.ui.textBrowser.append('Rows X Columns = '+ str(h) +" x "+ str(w))
                self.ui.textBrowser.append("Bit Depth:  "+ str(self.Depth*8))
                self.ui.textBrowser.append("Size (Bits)"+str(w*h*self.Depth*8))
                self.ui.scene.update()

    def Nearest_Interpolation(self):

        
        try:
            self.ui.sceneNearestNeighbor_Zoomed.clear()
            side1,side2 = self.imgGray.size
        except:
            QMessageBox.warning(self,"Error","Please Choose Image First !")
            return

        try:
            float(self.ui.ZoomFactor_lineEdit.text())           
        except:
            QMessageBox.critical(self,"Error","Please Enter a Number !")
            return

        if float(self.ui.ZoomFactor_lineEdit.text())<=0:
            QMessageBox.warning(self,"Error","Please Enter a postive Number !")
            return

        dimension1 = round(side1 * float(self.ui.ZoomFactor_lineEdit.text()))
        dimension2 = round(side2 * float(self.ui.ZoomFactor_lineEdit.text()))
        new_image = np.zeros((dimension2, dimension1))
        for i in range(dimension1):
            for j in range(dimension2):
                row = math.floor(i / float(self.ui.ZoomFactor_lineEdit.text()))
                column = math.floor(j / float(self.ui.ZoomFactor_lineEdit.text()))
                new_image[j, i] = self.imgGray.getpixel((row,column))
        ImageNearest = PIL.Image.fromarray(new_image)
        ImageNearest = ImageNearest.convert('L')
        imgQ = ImageQt.ImageQt(ImageNearest)
        pixMap = QPixmap.fromImage(imgQ)
        self.ui.sceneNearestNeighbor_Zoomed.addPixmap(pixMap)
        self.ui.textBrowser_Zoomed.clear()
        self.ui.textBrowser_Zoomed.append("Width: "+str(dimension1))
        self.ui.textBrowser_Zoomed.append("height "+str(dimension2))
        self.ui.textBrowser_Zoomed.append('Rows X Columns = '+ str(dimension1) +" x "+ str(dimension2))
        self.ui.sceneNearestNeighbor_Zoomed.update()
        
    def Bilinear_Interpolation(self):
        self.ui.sceneLinearInerpolation_Zoomed.clear()
        try:
            float(self.ui.ZoomFactor_lineEdit.text())           
        except:
            return
        if float(self.ui.ZoomFactor_lineEdit.text())<=0:
            return

        try:      
            width,height = self.imgGray.size
        except:
            return
        dimension0= round(width* float(self.ui.ZoomFactor_lineEdit.text()))
        dimension1=round(height * float(self.ui.ZoomFactor_lineEdit.text()))
        new_image = np.zeros((dimension1, dimension0))
        y_ratio = float(width - 1) / (dimension0 - 1) if dimension0 > 1 else 0
        x_ratio = float(height - 1) / (dimension1 - 1) if dimension1 > 1 else 0
        for i in range(dimension0):
            for j in range(dimension1):
                x_l, y_l = math.floor(x_ratio * j), math.floor(y_ratio * i)
                x_h, y_h = math.ceil(x_ratio * j), math.ceil(y_ratio * i)

                x_weight = (x_ratio * j) - x_l
                y_weight = (y_ratio * i) - y_l
                try:
                    a = self.imgGray.getpixel((y_l, x_l))
                    b = self.imgGray.getpixel((y_l, x_h))
                    c = self.imgGray.getpixel((y_h, x_l))
                    d = self.imgGray.getpixel((y_h, x_h))
                    
                    pixel = a * (1 - x_weight) * (1 - y_weight) + b * x_weight * (1 - y_weight) + c * y_weight * (1 - x_weight) + d * x_weight * y_weight
                    new_image[j][i] = pixel
                except:
                    pass    
        # Interpolate over layers
        Imagebiliniar = PIL.Image.fromarray(new_image)
        Imagebiliniar = Imagebiliniar.convert('L')
        imgQ = ImageQt.ImageQt(Imagebiliniar)  
        pixMap = QPixmap.fromImage(imgQ)
        self.ui.sceneLinearInerpolation_Zoomed.addPixmap(pixMap)
        self.ui.sceneLinearInerpolation_Zoomed.update()

    def Draw_T(self):
        self.Timage=np.zeros((128,128))
        for i in range(29,99):
            for j in range(29,49):
                self.Timage[j][i]=255
        
        for i in range(54,74):
            for j in range(49,99):
                self.Timage[j][i]=255

        ImageRotated = PIL.Image.fromarray(self.Timage)
        ImageRotated=ImageRotated.convert('L')
        imgQ = ImageQt.ImageQt(ImageRotated)
        pixMap = QPixmap.fromImage(imgQ)
        
        self.ui.sceneNearestNeighbor_Rotation.addPixmap(pixMap)
        self.ui.sceneLinearInterpolation_Rotation.addPixmap(pixMap)
        self.ui.sceneShearedImage.addPixmap(pixMap)
        # self.ui.LinearInterpolation_Rotation_graphicsView.fitInView(QRectF(0, 0,8,8),Qt.KeepAspectRatio)
        # self.ui.NearestNeighbor_Rotation_graphicsView.fitInView(QRectF(0, 0,8,8),Qt.KeepAspectRatio)
        self.ui.sceneLinearInterpolation_Rotation.update()
        self.ui.sceneNearestNeighbor_Rotation.update()
        self.ui.sceneShearedImage.update()
    
    def Rotation_Nearest(self):
        Rotation_angle =float(self.ui.Rotation_Angle_lineEdit.text())

        #  convert rotation amount to radian
        rotation_amount_rad = math.radians(Rotation_angle)

        #  get dimension info
        height, width= 128 ,128

        # rotated_height, rotated_width, _ = rotated_image.shape
        rotated_image = np.zeros((128,128))

        rotated_height, rotated_width = 128,128
        mid_row = int( (rotated_height+1)/2 )
        mid_col = int( (rotated_width+1)/2 )

        #  for each pixel in output image, find which pixel it corresponds to in the input image
        for r in range(rotated_height):
            for c in range(rotated_width):
                #  apply rotation matrix, the other way
                y = (r-mid_col)*math.cos(rotation_amount_rad) + (c-mid_row)*math.sin(rotation_amount_rad)
                x = -(r-mid_col)*math.sin(rotation_amount_rad) + (c-mid_row)*math.cos(rotation_amount_rad)

                #  add offset
                y += mid_col
                x += mid_row

                #  get nearest index
                #a better way is linear interpolation
                x = round(x)
                y = round(y)


                #  check if x/y corresponds to a valid pixel in input image
                if (x >= 0 and y >= 0 and x < width and y < height):
                    rotated_image[r][c] = self.Timage[y][x]

            
        path_x=QtGui.QPainterPath()
        self.ui.sceneNearestNeighbor_Rotation.addPath(path_x)    
        ImageRotated=PIL.Image.fromarray(rotated_image)
        ImageRotated = ImageRotated.convert('L')            
        self.imgQ = ImageQt.ImageQt(ImageRotated)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneNearestNeighbor_Rotation.addPixmap(pixMap)        
        # self.ui.NearestNeighbor_Rotation_graphicsView.fitInView(QRectF(0, 0,128,128),Qt.KeepAspectRatio)
        self.ui.sceneNearestNeighbor_Rotation.update()
        self.ui.textBrowser_Rotated.clear()
        if float(self.ui.Rotation_Angle_lineEdit.text())>0:
            self.ui.textBrowser_Rotated.append("Rotation Angle = "+(self.ui.Rotation_Angle_lineEdit.text())+ " AntiClockWise ")
        else:
            self.ui.textBrowser_Rotated.append("Rotation Angle = "+str((-1)*float(self.ui.Rotation_Angle_lineEdit.text()))+ " ClockWise ")

        self.ui.textBrowser_Rotated.append(f"Width = {128}, Height = {128}")

    def Rotation_Linear(self):
        Rotation_angle =float(self.ui.Rotation_Angle_lineEdit.text())

        #  convert rotation amount to radian
        rotation_amount_rad = math.radians(Rotation_angle)

        #  get dimension info
        height, width= 128 ,128
        rotated_image = np.zeros((128,128))

        rotated_height, rotated_width = 128,128
        mid_row = int( (rotated_height+1)/2 )
        mid_col = int( (rotated_width+1)/2 )

        for c in range(rotated_height):
                for r in range(rotated_width):
                    #  apply rotation matrix, the other way
                    y = (r-mid_col)*math.cos(rotation_amount_rad) + (c-mid_row)*math.sin(rotation_amount_rad)
                    x = -(r-mid_col)*math.sin(rotation_amount_rad) + (c-mid_row)*math.cos(rotation_amount_rad)

                    #  add offset
                    y += mid_col
                    x += mid_row
            
                    # Linear Interpolation
                    x_l, y_l = math.floor(x), math.floor(y)
                    x_h, y_h = min(rotated_height-1, math.ceil(x)), min(rotated_width-1, math.ceil(y))
                    
                    if (x >= 0 and y >= 0 and x < rotated_width and y < rotated_height):
                        if (x_h == x_l) and (y_h == y_l):
                            q = self.Timage[int(y), int(x)]
                        elif (y_h == y_l):
                            q1 = self.Timage[int(y), int(x_l)]
                            q2 = self.Timage[int(y), int(x_h)]
                            q = q1 * (x_h - x) + q2 * (x - x_l)
                        elif (x_h == x_l):
                            q1 = self.Timage[int(y_l), int(x)]
                            q2 = self.Timage[int(y_h), int(x)]
                            q = (q1 * (y_h - y)) + (q2	 * (y - y_l))
                        else:
                            v1 = self.Timage[y_l, x_l]
                            v2 = self.Timage[y_h, x_l]
                            v3 = self.Timage[y_l, x_h]
                            v4 = self.Timage[y_h, x_h]

                            q1 = v1 * (y_h - y) + v2 * (y - y_l)
                            q2 = v3 * (y_h - y) + v4 * (y - y_l)
                            q = q1 * (x_h - x) + q2 * (x - x_l)

                        rotated_image[r,c] = q

        ImageRotated=PIL.Image.fromarray(rotated_image)
        ImageRotated = ImageRotated.convert('L')            
        self.imgQ = ImageQt.ImageQt(ImageRotated)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneLinearInterpolation_Rotation.addPixmap(pixMap)        
        self.ui.sceneLinearInterpolation_Rotation.update()
        self.ui.textBrowser_Rotated.clear()
        if float(self.ui.Rotation_Angle_lineEdit.text())>0:
            self.ui.textBrowser_Rotated.append("Rotation Angle = "+(self.ui.Rotation_Angle_lineEdit.text())+ " AntiClockWise ")
        else:
            self.ui.textBrowser_Rotated.append("Rotation Angle = "+str((-1)*float(self.ui.Rotation_Angle_lineEdit.text()))+ " ClockWise ")

    def Bi_scratch(self,Image ,rotation_amount_degree):
        rotation_amount_rad = rotation_amount_degree * np.pi / 180.0
        (width,height) = Image.shape
        width=int(width)
        height=int(height)
        rotated_image = np.zeros((width,height))

        rotated_height, rotated_width = Image.shape
        mid_row = math.floor( (rotated_height+1)/2 )
        mid_col = math.floor( (rotated_width+1)/2 )


        for r in range(rotated_height):
            for c in range(rotated_width):
                #  apply rotation matrix, the other way
                y = (r-mid_col)*math.cos(rotation_amount_rad) + (c-mid_row)*math.sin(rotation_amount_rad)
                x = -(r-mid_col)*math.sin(rotation_amount_rad) + (c-mid_row)*math.cos(rotation_amount_rad)

                #  add offset
                y += mid_col
                x += mid_row
                x = round(x)
                y = round(y)

                if (x >= 0 and y >= 0 and x < rotated_width and y < rotated_height):
                    rotated_image[r][c] = Image[y][x]
        return rotated_image

    def histogram(self):
        self.pixels=[]
        
        for x in range(256):
            self.pixels.append(x)

        #set width and height of image
        width,height=self.imgGray.size
        size=width*height
        self.counts=[]
        Equalized_image=np.zeros((height,width))
        Imagearray = np.array(self.imgGray)

        #for each intensity level
        for i in self.pixels:

        #set counter to 0
            temp=0

        #traverse through the pixels
            for x in range(width):
                for y in range(height):

                #if pixel intensity is equal to intensity level
                #increment counter
                    if (self.imgGray.getpixel((x,y))==i):
                        temp=temp+1
            
            #append frequency of intensity level
            self.counts.append(temp)

        #initialize list for frequency probabilities
        pdf=[]
        for i in self.counts:
            pdf.append(i/size)

        #initialize list for cumulative probability 
        cdf=[]
        total=0
        for i in pdf:
            total=total+i
            cdf.append(total)

        #intialize list for mapping cdf
        tr=[]
        for i in cdf:
            t=round(i*255)
            tr.append(t)

        for x in range(width):
            for y in range(height):
                Equalized_image[y,x]=tr[Imagearray[y,x]]
                   
        #initialize list containing new frequencies for equalized hist
        self.hs=[]
        for i in self.pixels:
            count=0
            tot=0
            for j in tr:
                if (j==i):
                    tot=tot+self.counts[count]
                count=count+1
            self.hs.append(tot)

        self.ui.EQ_Histogram.Plot(self.pixels,self.hs)    
        self.ui.Original_Histogram.Plot(self.pixels,self.counts)
        self.ui.Image_Brfore_EQ.Draw(Imagearray)
        self.ui.Image_After_EQ.Draw(Equalized_image)
        self.ui.Original_Histogram.update()
        self.ui.EQ_Histogram.update()
        
    def Original_View(self):
        self.ui.sceneUnsharpedImage.clear()
        self.ui.sceneUnsharpedFourierImage.clear()
        self.ui.sceneMoirePatternImage.clear()
        row , col = self.imgGray.size
        ImageUnsharped = ImageQt.ImageQt(self.imgGray)  
        pixMap = QPixmap.fromImage(ImageUnsharped)

        self.ui.sceneUnsharpedImage.addPixmap(pixMap)
        self.ui.Unsharped_image_graphicsView.fitInView(QRectF(0, 0,row,col),Qt.KeepAspectRatio)
        self.ui.sceneUnsharpedImage.update()
        
        self.ui.sceneUnsharpedFourierImage.addPixmap(pixMap)
        self.ui.Unsharped_image_graphicsView_1.fitInView(QRectF(0, 0,row,col),Qt.KeepAspectRatio)
        self.ui.sceneUnsharpedFourierImage.update()

        self.ui.sceneMoirePatternImage.addPixmap(pixMap)
        self.ui.Moire_pattern_image_graphicsView.fitInView(QRectF(0, 0,row,col),Qt.KeepAspectRatio)
        self.ui.sceneMoirePatternImage.update()
        
    def Salt_and_papper(self):
        try:
            self.row , self.col = self.imgGray.size
        except:
            QMessageBox.critical(self, "Error", "Please, Enter Image First!")
            return
        Size = self.row*self.col
        self.numpydata = asarray(self.imgGray)
        # Randomly pick some pixels in the
     
        number_of_pixels = random.randint(math.floor(0.05*Size), math.floor(0.15*Size))
        for i in range(number_of_pixels):
        
            # Pick a random y coordinate
            x_coord=random.randint(0, self.row - 1)
            
            # Pick a random x coordinate
            y_coord=random.randint(0, self.col - 1)
            
            # Color that pixel to white
            self.numpydata[y_coord][x_coord] = 255
            
        number_of_pixels = random.randint(math.floor(0.05*Size), math.floor(0.15*Size))
        for i in range(number_of_pixels):

            x_coord=random.randint(0, self.row - 1)
            y_coord=random.randint(0, self.col - 1)
            self.numpydata[y_coord][x_coord] = 0
            
        ImageNoised=PIL.Image.fromarray(self.numpydata)
        ImageNoised = ImageNoised.convert('L')            
        self.imgQ = ImageQt.ImageQt(ImageNoised)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneNoisedImage.addPixmap(pixMap)       
        self.ui.Noised_image_graphicsView.fitInView(QRectF(0, 0,self.row,self.col),Qt.KeepAspectRatio)

    def quicksort(self,array):
        if len(array)<=1: #base case
            return array
        else:
            # Choose pivot
            pivot=array[0]

            #Make Lists of less items than pivot 
            less = [item for item in array[1:] if item <= pivot]
            
            #Make Lists of great items than pivot 
            great = [item for item in array[1:] if item > pivot]
            # put items less than pivot in the left and put items great than pivot in the right
            # Recursion : repeat and sort the smaller lists
            return self.quicksort(less) + [pivot] + self.quicksort(great)

    def median_filter(self):
        try:
            data_final = np.zeros((len(self.numpydata),len(self.numpydata[0])))
        except:
             QMessageBox.critical(self, "Error", "Please, Add Noise to Image First ")
             return
        try:
            Filter_size=int(self.ui.Filter_Size_lineEdit.text())
        except:
             QMessageBox.critical(self, "Error", "Please, Enter Filter Size ")
             return

        temp = []
        n, m = self.imgGray.size
        # self.numpydata=asarray(self.imgGray)
        Filter_size=int(self.ui.Filter_Size_lineEdit.text())
        indexer = int(self.ui.Filter_Size_lineEdit.text()) // 2
        data_final = []
        
        data_final = np.zeros((len(self.numpydata),len(self.numpydata[0])))
        for i in range(len(self.numpydata)):

            for j in range(len(self.numpydata[0])):
                    
                for z in range(Filter_size):
                    
                    if i + z - indexer < 0 or i + z - indexer > len(self.numpydata) - 1:
                        # for c in range(Filter_size):
                            temp.append(0)
                    else:
                        if j + z - indexer < 0 or j + indexer > len(self.numpydata[0]) - 1:
                             temp.append(0)
                        else:
                            for k in range(Filter_size):
                                temp.append(self.numpydata[i + z - indexer][j + k - indexer])

                temp=self.quicksort(temp)
                data_final[i][j] = temp[len(temp) // 2]
                temp = []

        data_final = data_final.astype(np.uint8)
        ImageFiltered=PIL.Image.fromarray(data_final)
        ImageFiltered = ImageFiltered.convert('L')            
        self.imgQ = ImageQt.ImageQt(ImageFiltered)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneFilteredImage.addPixmap(pixMap)       
        self.ui.Filtered_image_graphicsView.fitInView(QRectF(0, 0,n,m),Qt.KeepAspectRatio)
        self.ui.sceneFilteredImage.update()

    def addPadding(self, val, image, paddSize):
        
        addedPadd = 2 * paddSize
        col, row = self.imgGray.size
        resultImage = np.zeros((row + addedPadd, col + addedPadd))
        size1,size2=resultImage.shape
        resultImage.fill(val)

        for i in range(paddSize, size1 - paddSize):
            for j in range(paddSize, size2 - paddSize):
                resultImage[i][j] = image[i-paddSize][j-paddSize]
        
        return resultImage

    def convolution(self, filter:np.ndarray,image:np.ndarray):
        
        filter = np.flip(filter)

        height, width = image.shape
        filterWidth = filter.shape[0]
        filterHeight = filter.shape[1]

        filterSize = max(filterWidth, filterHeight)
        paddingSize = filterSize // 2

        paddedImage =  self.addPadding(0,image,paddingSize)

        resultImage = []
        for i in range(height):
            endPointVertical = i + filterSize
            rowArray = []
            for j in range(width):
                endPointHorizontal = j + filterSize
                rowArray.append(np.sum(paddedImage[i:endPointVertical,j:endPointHorizontal] * filter))
            resultImage.append(rowArray)
        
        resultImage = np.array(resultImage)

        return resultImage

    def boxFilter(self):
        try:
            size=int(self.ui.Filter_Size_lineEdit.text())
        except:
             QMessageBox.critical(self, "Error", "Please, Enter Filter Size ")
             return

        if   int(self.ui.Filter_Size_lineEdit.text())%2==0  :
             QMessageBox.critical(self, "Error", "Please, Enter Odd Value")
             return
        
        # height,width = self.imgGray.size
        self.filter = np.zeros((size,size))
        self.filter.fill(1/(size*size))
        self.filterWidth= size
        self.filterHeight=size
        try:
            self.resImage = self.convolution(self.filter, asarray(self.imgGray) )
        except:
            QMessageBox.critical(self, "Error", "Please, Enter Image First")
            return
        self.Sharp()

    def Sharp(self):
        self.ui.sceneSharpedImage.clear()
        imgarr=asarray(self.imgGray)
        col,row=self.imgGray.size
        self.resImage=self.resImage[self.paddSize:self.resImage.shape[0]-self.paddSize,self.paddSize:self.resImage.shape[1]-self.paddSize]
        self.Mask=imgarr-self.resImage
        try:
            int(self.ui.Edge_Factor_lineEdit.text())
        except:
             QMessageBox.critical(self, "Error", "Please, Enter Edge Factor 'int'  ")
             return
        self.Mask=self.Mask*int(self.ui.Edge_Factor_lineEdit.text())
        imgarr=imgarr+self.Mask

        for i in range(row):
            for j in range(col):
                if imgarr[i,j]<0:
                    imgarr[i,j]=0
                elif imgarr[i,j]>255:
                    imgarr[i,j]=255

        # self.resImage = np.subtract(self.resImage, self.resImage.min())
        # self.resImage = 255*(self.resImage/self.resImage.max())
        # self.resImage = np.uint8(self.resImage)
       
        ImageSharped=PIL.Image.fromarray(imgarr)
        ImageSharped = ImageSharped.convert('L')            
        self.imgQ = ImageQt.ImageQt(ImageSharped)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneSharpedImage.addPixmap(pixMap)       
        self.ui.Sharped_image_graphicsView.fitInView(QRectF(0, 0,col,row),Qt.KeepAspectRatio)
        self.ui.sceneSharpedImage.update()

    def Original_Mag(self):
        self.ui.sceneoriginalMag.clear()
        Imagearray = asarray(self.imgGray)
        n,m=self.imgGray.size
        f = np.fft.fft2(Imagearray)
        fshift = np.fft.fftshift(f)
        self.magnitudeSpectrum = np.abs(fshift)

        Mag = np.subtract(self.magnitudeSpectrum, self.magnitudeSpectrum.min())
        Mag = 255*(Mag/Mag.max())
        Mag = np.uint8(Mag)

        img_magnitudeSpectrum = PIL.Image.fromarray(self.magnitudeSpectrum/255)
        img_magnitudeSpectrum = img_magnitudeSpectrum.convert('L')
        self.imgQ = ImageQt.ImageQt(img_magnitudeSpectrum)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneoriginalMag.addPixmap(pixMap)
        self.ui.Original_Magnitiude_graphicsView.fitInView(QRectF(0, 0,n,m),Qt.KeepAspectRatio)
        self.ui.sceneoriginalMag.update()

    def Logged_Mag(self):
        self.ui.sceneloggedMag.clear()
        n,m=self.imgGray.size
        try:
            maxPixelValue = np.max(self.magnitudeSpectrum)
        except:
            QMessageBox.critical(self, "Error", "Please show Original Magnitiude First !")
            return
        c = 255 / (np.log(1 + maxPixelValue))
        
        loggedMag = c*np.log(1+ self.magnitudeSpectrum)
        loggedMag = np.subtract(loggedMag, loggedMag.min())
        loggedMag = 255*(loggedMag/loggedMag.max())
        loggedMag = np.uint8(loggedMag)

        img_logged = PIL.Image.fromarray(loggedMag)
        img_logged = img_logged.convert('L')
        self.imgQ = ImageQt.ImageQt(img_logged)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.Logged_Magnitiude_graphicsView.fitInView(QRectF(0, 0,n,m),Qt.KeepAspectRatio)
        self.ui.sceneloggedMag.addPixmap(pixMap)
        self.ui.sceneloggedMag.update()

    def Original_Phase(self):
        self.ui.sceneoriginalPhase.clear()
        Imagearray = np.array(self.imgGray)
        n,m=self.imgGray.size
        f = np.fft.fft2(Imagearray)
        fshift = np.fft.fftshift(f)
        self.phaseSpectrum = np.angle(fshift) 
        
        self.phaseSpectrum = np.subtract(self.phaseSpectrum, self.phaseSpectrum.min())
        self.phaseSpectrum = 255*(self.phaseSpectrum/self.phaseSpectrum.max())

        img_phasespectrum = np.uint8(self.phaseSpectrum)
        img_phasespectrum = PIL.Image.fromarray(img_phasespectrum)
        img_phasespectrum = img_phasespectrum.convert('L')
        self.imgQ = ImageQt.ImageQt(img_phasespectrum)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.Original_Phase_graphicsView.fitInView(QRectF(0, 0,n,m),Qt.KeepAspectRatio)
        self.ui.sceneoriginalPhase.addPixmap(pixMap)
        self.ui.sceneoriginalPhase.update()

    def Logged_Phase(self):
        self.ui.sceneloggedPhase.clear()
        n,m=self.imgGray.size
        try:
            maxPValue = np.max(self.phaseSpectrum)
        except:
            QMessageBox.critical(self,"Error", "Please show Original Phase First !")
            return
        c = 255 / (np.log(1 + maxPValue))
        loggedPhase =c* np.log(1+ self.phaseSpectrum) 
        loggedPhase = np.subtract(loggedPhase, loggedPhase.min())
        loggedPhase = 255*(loggedPhase/loggedPhase.max())
        loggedPhase = np.uint8(loggedPhase)

        img_loggedPhase = PIL.Image.fromarray(loggedPhase)
        img_loggedPhase = img_loggedPhase.convert('L')
        self.imgQ = ImageQt.ImageQt(img_loggedPhase)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.Logged_Phase_graphicsView.fitInView(QRectF(0, 0,n,m),Qt.KeepAspectRatio)
        self.ui.sceneloggedPhase.addPixmap(pixMap)   
        self.ui.sceneloggedPhase.update()   

    def Blurring(self):

        try:
            size=int(self.ui.Filter_Size_Fourier_lineEdit.text())
        except:
             QMessageBox.critical(self, "Error", "Please, Enter Filter Size ")
             return

        if   int(self.ui.Filter_Size_Fourier_lineEdit.text())%2==0  :
             QMessageBox.critical(self, "Error", "Please, Enter Odd Value")
             return

        self.filter = np.zeros((size,size))
        self.filter.fill(1/(size*size))
        self.filterWidth= size
        self.filterHeight=size
        
        try:
          self.Blurred = self.convolution(self.filter, asarray(self.imgGray) )
        except:
            QMessageBox.critical(self, "Error", "Please, Enter Image First")
            return
        
        # x=(size//2)
        # self.Blurred=self.Blurred[self.Blurred.shape[0]-1,self.Blurred.shape[1]-1]
        self.ui.sceneBlurredImage.clear()
        ImageBlurred=PIL.Image.fromarray(self.Blurred)
        col,row=self.imgGray.size
        ImageBlurred = ImageBlurred.convert('L')            
        self.imgQ = ImageQt.ImageQt(ImageBlurred)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneBlurredImage.addPixmap(pixMap)       
        self.ui.Blurred_image_graphicsView.fitInView(QRectF(0, 0,col,row),Qt.KeepAspectRatio)
        self.ui.sceneBlurredImage.update()
        
    def Fourier_Filtering(self):
        self.ui.sceneBlurredFourierImage.clear()
        try:
            col,row=self.imgGray.size
        except:
            QMessageBox.critical(self,"Error", "Please choose image First !")
            return
        try:
            size=int(self.ui.Filter_Size_Fourier_lineEdit.text())
        except:
            QMessageBox.critical(self, "Error", "Please, Enter Filter Size ")
            return

        if   int(self.ui.Filter_Size_Fourier_lineEdit.text())%2==0  :
             QMessageBox.critical(self, "Error", "Please, Enter Odd Value")
             return
        
        startx=((row-size)//2)-1
        starty=((col-size)//2)-1

        filter = np.zeros((row,col))
        for i in range(startx, startx +size):
            for j in range(starty, starty + size):
                filter[i][j] = 1/(size*size)

        Imagearray = asarray(self.imgGray)        
        f = np.fft.fft2(Imagearray)
        fshift = np.fft.fftshift(f)
         
        FourierFilter=np.fft.fft2(filter)
        ff=np.fft.fftshift(FourierFilter)
        
        BlurredArray=ff*fshift
        BlurredArray=np.fft.ifftshift(BlurredArray)
        BlurredArray=np.fft.ifft2(BlurredArray)
        BlurredArray=np.fft.fftshift(BlurredArray)
        BlurredArray=np.abs(BlurredArray)

        ImageBlurred=PIL.Image.fromarray(BlurredArray)
        ImageBlurred = ImageBlurred.convert('L')            
        self.imgQ = ImageQt.ImageQt(ImageBlurred)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneBlurredFourierImage.addPixmap(pixMap)       
        self.ui.Blurred_Fourier_image_graphicsView.fitInView(QRectF(0, 0,col,row),Qt.KeepAspectRatio)
        self.ui.sceneBlurredFourierImage.update()
        return BlurredArray

    def Difference(self):
        self.ui.sceneDifferenceImage.clear()
        BlurredArray=self.Fourier_Filtering()
        DiffImage= BlurredArray-self.Blurred
        col,row=self.imgGray.size

        for i in range(row):
            for j in range(col):
                if DiffImage[i,j]<0:
                    DiffImage[i,j]=0
                elif DiffImage[i,j]>255:
                    DiffImage[i,j]=255

        ImageBlurred=PIL.Image.fromarray(DiffImage)
        ImageBlurred = ImageBlurred.convert('L')            
        self.imgQ = ImageQt.ImageQt(ImageBlurred)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneDifferenceImage.addPixmap(pixMap)       
        self.ui.Difference_image_graphicsView.fitInView(QRectF(0, 0,col,row),Qt.KeepAspectRatio)
        self.ui.sceneDifferenceImage.update()

    def notch_reject_filter(self, d0=9, u_k=0, v_k=0):
        X, Y = self.imgGray.size 
        # Initialize filter with zeros
        H = np.zeros((Y, X))

        # Traverse through filter
        for u in range(0, Y):
            for v in range(0, X):
                # Get euclidean distance from point D(u,v) to the center
                D_uv = np.sqrt((u - Y / 2 + u_k) ** 2 + (v - X / 2 + v_k) ** 2)
                D_muv = np.sqrt((u - Y / 2 - u_k) ** 2 + (v - X / 2 - v_k) ** 2)

                if D_uv <= d0 or D_muv <= d0:
                    H[u, v] = 0.0
                else:
                    H[u, v] = 1.0

        return H

    def Moire_Pattern(self):
        try:
            Imagearray =np.array(self.imgGray)
        except:
            QMessageBox.critical(self,"Error", "Please Select Image First !")
            return
        col, row = self.imgGray.size     
        f = np.fft.fft2(Imagearray)
        fshift = np.fft.fftshift(f)

        H1 = self.notch_reject_filter(8,38,30)
        H2 = self.notch_reject_filter(8,-42,27)
        H3 = self.notch_reject_filter(4,80,30)
        H4 = self.notch_reject_filter(4,-82,28)
        H5 = self.notch_reject_filter(2,-100,40)
        H6 = self.notch_reject_filter(2,40,100)
       
        NotchFilter = H1*H2*H3*H4*H5*H6
        NotchRejectCenter = fshift * NotchFilter 
        NotchReject = np.fft.ifftshift(NotchRejectCenter)
        inverse_NotchReject = np.fft.ifft2(NotchReject)  # Compute the inverse DFT of the result

        Result = np.abs(inverse_NotchReject)
        Result=PIL.Image.fromarray(Result)
        Result = Result.convert('L')            
        self.imgQ = ImageQt.ImageQt(Result)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneFilteredMoireImage.addPixmap(pixMap) 
        self.ui.Filtered_Moire_image_graphicsView.fitInView(QRectF(0, 0,col,row),Qt.KeepAspectRatio)      
        self.ui.sceneFilteredMoireImage.update()         

    def Original_ROI(self):
        self.circleArray=np.zeros((256,256))
        self.circleArray.fill(50)
        
        for i in range(30,224):
            for j in range(30,224):
                self.circleArray[i][j]=150

        for u in range(256):
            for v in range(256):
                # Get euclidean distance from point D(u,v) to the center
                D_uv = np.sqrt((u - 256 / 2 ) ** 2 + (v - 256 / 2 ) ** 2)
                D_muv = np.sqrt((u - 256 / 2 ) ** 2 + (v - 256 / 2 ) ** 2)

                if D_uv <= 65 or D_muv <=65:
                    self.circleArray[u, v] = 250
        
        self.ui.Original_ROI_Image.Draw(self.circleArray)
               
    def ROI_Noise(self):
        try:
            UniformNoise=np.random.uniform(float(self.ui.Uniform_Noise_Min_lineEdit.text()),float(self.ui.Uniform_Noise_Max_lineEdit.text()),(256,256))#Uniform noise
            Gaussian=np.random.normal(float(self.ui.Gaussian_Noise_Min_lineEdit.text()),float(self.ui.Gaussian_Noise_Max_lineEdit.text()),(256,256)) #gauessian
        except:
            QMessageBox.critical(self,"Error", "Please Enter Numerical Values !")
            return
        self.ROI_Noise_image=self.circleArray+UniformNoise+Gaussian
        for i in range(255):
            for j in range(255):
                if self.ROI_Noise_image[i,j]<0:
                    self.ROI_Noise_image[i,j]=0
                elif self.ROI_Noise_image[i,j]>255:
                    self.ROI_Noise_image[i,j]=255

        self.ui.Noisy_ROI_Image.Draw(self.ROI_Noise_image)

    def onselect_function(self,eclick, erelease):   
            self.extent = self.rect_selector.extents
            self.xmin,self.xmax,self.ymin,self.ymax=self.rect_selector.extents
            
    def Select_ROI(self):
        self.ui.Noisy_ROI_Image.Clear()
        self.ui.Noisy_ROI_Image.Draw(self.ROI_Noise_image)
        self.rect_selector = RectangleSelector(
            self.ui.Noisy_ROI_Image.canvas.axes, self.onselect_function, drawtype='box', button=[1], props = dict(facecolor='black', alpha=0.5),useblit=True, spancoords='pixels',interactive=True)
        
    def ROI_Histogram(self):
        counts=np.zeros(256)
        try:
            for i in range(int(self.xmin),int(self.xmax)):
                for j in range(int(self.ymin),int(self.ymax)):
                    x=int(self.ROI_Noise_image[i][j])
                    counts[x]+=1
        except:
            QMessageBox.critical(self,"Error", "Please select ROI first !")
            return

        # Normalize
        sumPixels = np.sum(counts)
        normalizedHistogram = counts/sumPixels

        mean = 0
        for i in range(256):
            mean += i * normalizedHistogram[i]

        variance = 0
        for i in range(256):
            variance += (i-mean)**2 *normalizedHistogram[i]

        std = np.sqrt(variance)

        self.ui.ROI_Hist.Plot(range(256),counts)
        
        self.ui.ROI_Hist.Settitle(f'Statistics  $\mu={mean:.5}$, $\sigma={std:.5}$')
    
    def Phantom(self):
        self.Phantomarr=np.zeros((256,256))
        self.Phantomarr=shepp_logan(256)
        self.Phantomarr=np.flip(self.Phantomarr) 
        self.ui.Phantom_Image.Draw(self.Phantomarr)
    
    def Sinogram(self):
        ################Bonus###################  
        #######################################
        # self.sinogram=np.zeros((256,180))
        # theta = np.linspace(0., 180.,180, endpoint=False)
        # numAngles=len(theta)
        # for n in range(numAngles):
        #     rotImgObj = self.Bi_scratch(self.Phantomarr,theta[n])
        #     self.sinogram[:,n] = sum(rotImgObj)
        # self.sinogram=np.rot90(self.sinogram,2)
        #########################################

        #################NotBonus####################
        #############################################
        theta = np.linspace(0., 180.,180, endpoint=False)
        self.sinogram = radon(self.Phantomarr, theta=theta)
        ############################################

        self.ui.Sinogram_Image.Draw(np.rot90(self.sinogram))

    def Laminogram(self):
        laminogram=np.zeros((256,256))
        for angle in range(0,160,20):

            strip=radon(self.Phantomarr,[angle])
            strip=np.tile(strip,(1,256))   
            strip=np.rot90(strip)
            strip=rotate(strip,angle=angle)
            laminogram+=strip

        self.ui.Laminogram_Image.Draw(laminogram)

    def LaminogramNoFilter(self):
        self.laminogramNoFilter=np.zeros((256,256))
        for angle in range(179):

            strip=radon(self.Phantomarr,[angle])
            strip=np.tile(strip,(1,256))
            strip=np.rot90(strip)
            strip=rotate(strip,angle=angle)
            self.laminogramNoFilter+=strip

        self.ui.Laminogram_NoFilter_Image.Draw(self.laminogramNoFilter)
    
    def LaminogramHamming(self):
        laminogramHamming=np.zeros((256,256))
        laminogramHamming=iradon(self.sinogram,filter_name="hamming")

        self.ui.Laminogram_Hamming_Image.Draw(laminogramHamming)

    def LaminogramRamlak(self):
        laminogramRamLak=np.zeros((256,256))
        laminogramRamLak=iradon(self.sinogram,filter_name="ramp")

        self.ui.Laminogram_RamLak_Image.Draw(laminogramRamLak)

    def OriginalDE(self):
        self.ui.sceneOriginalDE.clear()
        row , col = self.imgGray.size
        ImageOriginal = ImageQt.ImageQt(self.imgGray)  
        pixMap = QPixmap.fromImage(ImageOriginal)
        self.ui.sceneOriginalDE.addPixmap(pixMap)
        self.ui.OriginalDE_graphicsView.fitInView(QRectF(0, 0,row,col),Qt.KeepAspectRatio)
        self.ui.sceneOriginalDE.update()

    def MultBitWiseE(self,Mat1:np.ndarray,Mat2:np.ndarray):
        result=np.zeros(Mat1.shape)
        for i in range (Mat1.shape[0]):
            for j in range(Mat1.shape[1]):
                if Mat1[i][j] is None or Mat2[i][j] is None :
                    result[i][j]=255
                else:
                    result[i][j]=Mat1[i][j]*Mat2[i][j]
        return result
    
    def MultBitWiseD(self,Mat1:np.ndarray,Mat2:np.ndarray):
        result=np.zeros(Mat1.shape)
        for i in range (Mat1.shape[0]):
            for j in range(Mat1.shape[1]):
                if Mat1[i][j] is None or Mat2[i][j] is None :
                    result[i][j]=0
                else:
                    result[i][j]=Mat1[i][j]*Mat2[i][j]
        return result

    def Erosion(self):
        #Acquire size of the image
        col , row = self.imgGray.size 
        #Show the image
        image=asarray(self.imgGray)
        # Define the structuring element
        # k= 11,15,45 -Different sizes of the structuring element
        k=5
        SE= np.array([[None,1,1,1,None],
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [None,1,1,1,None]])
        
        constant= (k-1)//2
        #Define new image
        self.imgErode= np.zeros((row,col), dtype=np.uint8)
        #Erosion without using inbuilt cv2 function for morphology
        for i in range(constant, row-constant):
            for j in range(constant,col-constant):
                temp= image[i-constant:i+constant+1, j-constant:j+constant+1]
                product= self.MultBitWiseE(temp,SE)
                self.imgErode[i,j]= np.min(product)
        return self.imgErode

    
        
    def DrawErosin(self):
        self.Erosion()
        col , row = self.imgGray.size 
        self.ui.sceneErosion.clear()
        Erosion=PIL.Image.fromarray(self.imgErode)
        Erosion = Erosion.convert('L')            
        self.imgQ = ImageQt.ImageQt(Erosion)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneErosion.addPixmap(pixMap)       
        self.ui.Erosion_graphicsView.fitInView(QRectF(0, 0,col,row),Qt.KeepAspectRatio)
        self.ui.sceneErosion.update()

    def Dilation(self):
        #Acquire size of the image
        col , row = self.imgGray.size 
        #Show the image
        image=asarray(self.imgGray)
        #Define new image to store the pixels of dilated image
        self.imgDilate= np.zeros((row,col), dtype=np.uint8)
        #Define the structuring element 
        k=5
        SED= np.array([[None,1,1,1,None],
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [None,1,1,1,None]])
        constant= (k-1)//2
        #Dilation operation without using inbuilt CV2 function
        for i in range(constant, row-constant):
            for j in range(constant,col-constant):
                temp= image[i-constant:i+constant+1, j-constant:j+constant+1]
                product= self.MultBitWiseD(temp,SED)
                self.imgDilate[i,j]= np.max(product)
        return self.imgDilate

    def DrawDilation(self):
        self.Dilation()
        self.ui.sceneDilation.clear()
        col , row = self.imgGray.size 
        Dilation=PIL.Image.fromarray(self.imgDilate)
        Dilation = Dilation.convert('L')            
        self.imgQ = ImageQt.ImageQt(Dilation)  
        pixMap = QPixmap.fromImage(self.imgQ)
        self.ui.sceneDilation.addPixmap(pixMap)       
        self.ui.Dilation_graphicsView.fitInView(QRectF(0, 0,col,row),Qt.KeepAspectRatio)
        self.ui.sceneDilation.update()
    
    # def opening(self):

        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())