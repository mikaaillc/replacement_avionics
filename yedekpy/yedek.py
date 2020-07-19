import csv
import os
import sys  # we'll need this later to run our Qt application
import OpenGL.GL as gl  # python wrapping of OpenGL
import cv2
import numpy as np
import pyqtgraph as pg
import datetime
from OpenGL import GLU
from OpenGL.arrays import vbo
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtOpenGL
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox, QLabel, QFileDialog, QWidget
from PyQt5.uic import loadUi
import random
import pyqtgraph
import pyqtgraph.exporters
import numpy
import socket
import serial
ax=0
ay=0
az=0
ax_1=0
ay_1=0
az_1=0

pg.setConfigOption('background', QColor(240, 240, 240))
pg.setConfigOption('foreground', 'k')

basincmat=[]
yukseklikmat=[]
hizmat=[]
sicaklikmat=[]
pilgermat=[]
basincmat1=[]
yukseklikmat1=[]
hizmat1=[]
sicaklikmat1=[]
pilgermat1=[]


class ana1(QMainWindow):
    def __init__(self):
        super(ana1, self).__init__()
        uic.loadUi("arayüz_1.ui", self)
        self.setWindowIcon(QtGui.QIcon("gorseller\simge"))
        self.move(925, 0)
        self.paketnum1 = 0
        self.counter_ = 0
        self.counter_1 = 0
        self.counter_2 = 0
        self.counter_3 = 0
        self.counter_4 = 0
        self.glWidget1 = GLWidget1
        self.glWidget1 = GLWidget1(self)
        self.lineEdit_20.setStyleSheet("color: rgb(255, 0, 0);")
        self.dataplot5 = self.graphicsView_10.addPlot()
        self.dataplot5.showGrid(x=True, y=True, alpha=1)

        self.dataplot6 = self.graphicsView_8.addPlot()
        self.dataplot6.showGrid(x=True, y=True, alpha=1)

        self.dataplot7 = self.graphicsView_7.addPlot()
        self.dataplot7.showGrid(x=True, y=True, alpha=1)

        self.dataplot8 = self.graphicsView_9.addPlot()
        self.dataplot8.showGrid(x=True, y=True, alpha=1)

        self.dataplot9 = self.graphicsView_6.addPlot()
        self.dataplot9.showGrid(x=True, y=True, alpha=1)

        self.verigor1.clicked.connect(self.veri1)
        self.graf.clicked.connect(self.grafikg1)
        self.veribaslat1.clicked.connect(self.dongu1)
        self.timer5 = QTimer()
        self.timer5.setInterval(1000)
        self.timer5.timeout.connect(self.time)
        self.timer5.start()
        self.lineEdit_29.setText('PORT SEÇİNİZ:')
        self.gonder.clicked.connect(self.gonder1)
    def gonder1(self):
        yazilan=self.lineEdit_29.text().upper()
        com1 = yazilan.split(":")
        self.com_1=str(com1[1])
        self.lineEdit_29.setText('PORT SEÇİLDİ')


    def veri1(self):
       os.startfile(r'veri_kayit\yedekveri.csv')
    def grafikg1(self):
        os.startfile(r'yedekgrafikler')
    def time(self):
        self.tarih1.setText(str(datetime.datetime.strftime(datetime.datetime.now(), '%d %B %Y')))
        self.saat1.setText(str(datetime.datetime.strftime(datetime.datetime.now(), '%X')))


    def dongu1(self):
        global xbee
        try:
            self.lineEdit_29.setText('XBEE BAĞLI')
            xbee = serial.Serial('{}'.format(self.com_1), 9600)
            self.timer_2 = QTimer()
            self.timer_2.setInterval(1000)
            self.timer_2.timeout.connect(self.btn_clk1)
            self.timer_2.start()
        except:
            self.lineEdit_29.setText('XBEE BAĞLI DEĞİL')

    def btn_clk1(self):
        global datetime1, stat1, basincmat1, yukseklikmat1, hizmat1, pilgermat1, sicaklikmat1,xbee
        global takimno1, yukseklik1, basinc1, hiz1, sicaklik1, pilger1, paketno1, paketnum1, saat1, saniye1, dakika1, lat1, long1, alt1, statu1, ax_1, ay_1, az_1,ax_2, ay_2, az_2
        self.tarih1.setText(str(datetime.datetime.strftime(datetime.datetime.now(), '%d %B %Y')))
        self.saat1.setText(str(datetime.datetime.strftime(datetime.datetime.now(), '%X')))

        try:
            if xbee.inWaiting() > 0:

                an1 = datetime.datetime.now()
                paket = xbee.readline().decode().strip()
                f = paket.split(",")

                ax_1 =str(f[0])
                ay_1 = str(f[1])
                az_1 = str(f[2])
                sicaklik1 = str(f[3])
                basinc1 = str(f[4])
                yukseklik1 = str(f[5])
                pilger1 = str(f[6])
                stat1 = str(f[7])
                hiz1 =str(f[8])
                la1 = str(f[9])
                lo1 = str(f[10])
                al1 = str(f[11])


                saat1 = an1.hour
                dakika1 = an1.minute
                saniye1 = an1.second

                self.paketnum1 += 1

                basincmat1.append(float(basinc1))
                yukseklikmat1.append(float(yukseklik1))
                hizmat1.append(float(hiz1))
                sicaklikmat1.append(float(sicaklik1))
                pilgermat1.append(float(pilger1))

                self.dataplot5.plot(basincmat1, pen=pg.mkPen('r', width=2), clear=True)
                self.lineEdit_3.setText(str(basinc1) + ' ' + 'Pa')  # Son değer bastırma

                self.dataplot6.plot(yukseklikmat1, pen=pg.mkPen('b', width=2), clear=True)
                self.lineEdit_23.setText(str(yukseklik1) + ' ' + 'm')

                self.dataplot7.plot(hizmat1, pen=pg.mkPen('k', width=2), clear=True)
                self.lineEdit_22.setText(str(hiz1) + ' ' + 'm/s')

                self.dataplot8.plot(sicaklikmat1, pen=pg.mkPen('b', width=2), clear=True)
                self.lineEdit_24.setText(str(sicaklik1) + ' ' + '°c')

                self.dataplot9.plot(pilgermat1, pen=pg.mkPen('r', width=2), clear=True)
                self.lineEdit_14.setText(str(pilger1) + ' ' + 'V')

                self.lineEdit_18.setText(str(self.paketnum1) + ' sn')
                lat1 = float(la1)
                long1 = float(lo1)
                alt1 = float(al1)
                statu1 = int(stat1)
                ax_2 = float(ax_1)
                ay_2 = float(ay_1)
                az_2 = float(az_1)
                self.lineEdit_12.setText(str(lat1))
                self.lineEdit_26.setText(str(long1))
                self.lineEdit_27.setText(str(alt1) + ' m')
                if statu1 == 1:
                    self.lineEdit_20.setText('Bekleme')
                    statu1 = 'Bekleme'
                elif statu1 == 2:
                    self.lineEdit_20.setText('Yükseliş')
                    statu1 = 'Yükseliş'
                elif statu1 == 3:
                    self.lineEdit_20.setText('Düşüş')
                    statu1 = 'Düşüş'
                elif statu1 == 4:
                    self.lineEdit_20.setText('Ayrıldı')
                    statu1 = 'Ayrıldı'
                elif statu1 == 5:
                    self.lineEdit_20.setText('İndi')
                    statu1 = 'İndi'


                self.lineEdit_21.setText(str(ax_1) + ' ' + '°')
                self.lineEdit_28.setText(str(ay_1) + ' ' + '°')
                self.lineEdit_25.setText(str(az_1) + ' ' + '°')
                self.timer_1 = QTimer()
                self.timer_1.setInterval(10)
                self.timer_1.timeout.connect(self.glWidget1.updateGL)  # 3d simülasyon timerı
                self.timer_1.start()
                self.glWidget1.setRotX1(ax_2)
                self.glWidget1.setRotY1(ay_2)
                self.glWidget1.setRotZ1(az_2)

                if len(basincmat1) > 60:  # GRafik kayıt için
                    self.counter_ += 1
                    exporter = pg.exporters.ImageExporter(self.dataplot5)
                    exporter.params.param('width').setValue(965, blockSignal=exporter.widthChanged)
                    exporter.params.param('height').setValue(608, blockSignal=exporter.heightChanged)
                    exporter.export('yedekgrafikler\g_basinc\g_basinc' + str(self.counter_) + '.png')
                    basincmat1 = [float(basinc1)]
                if len(yukseklikmat1) > 60:  # GRafik kayıt için
                    self.counter_1 += 1
                    exporter = pg.exporters.ImageExporter(self.dataplot6)
                    exporter.params.param('width').setValue(965, blockSignal=exporter.widthChanged)
                    exporter.params.param('height').setValue(608, blockSignal=exporter.heightChanged)
                    exporter.export('yedekgrafikler\g_yukseklik\g_yukseklik' + str(self.counter_1) + '.png')
                    yukseklikmat1 = [float(yukseklik1)]
                if len(hizmat1) > 60:  # GRafik kayıt için
                    self.counter_2 += 1
                    exporter = pg.exporters.ImageExporter(self.dataplot7)
                    exporter.params.param('width').setValue(965, blockSignal=exporter.widthChanged)
                    exporter.params.param('height').setValue(608, blockSignal=exporter.heightChanged)
                    exporter.export('yedekgrafikler\g_hiz\g_hiz' + str(self.counter_2) + '.png')
                    hizmat1 = [float(hiz1)]
                if len(sicaklikmat1) > 60:  # GRafik kayıt için
                    self.counter_3 += 1
                    exporter = pg.exporters.ImageExporter(self.dataplot8)
                    exporter.params.param('width').setValue(965, blockSignal=exporter.widthChanged)
                    exporter.params.param('height').setValue(608, blockSignal=exporter.heightChanged)
                    exporter.export('yedekgrafikler\g_sicaklik\g_sicaklik' + str(self.counter_3) + '.png')
                    sicaklikmat1 = [float(sicaklik1)]
                if len(pilgermat1) > 60:  # GRafik kayıt için
                    self.counter_4 += 1
                    exporter = pg.exporters.ImageExporter(self.dataplot9)
                    exporter.params.param('width').setValue(965, blockSignal=exporter.widthChanged)
                    exporter.params.param('height').setValue(608, blockSignal=exporter.heightChanged)
                    exporter.export('yedekgrafikler\g_pilger\g_pilger' + str(self.counter_4) + '.png')
                    pilgermat1 = [float(pilger1)]
                with open(r'veri_kayit\yedekveri.csv', 'a') as outfile:
                    writer1 = csv.writer(outfile, delimiter='|')
                    writer1.writerow(
                        ['paketnumarası={pak:5}'.format(pak=self.paketnum1),
                         'saat={:3}'.format(saat1), 'dakika={:3}'.format(dakika1),
                         'saniye={:3}'.format(saniye1), 'basinc={bas:6}'.format(bas=basinc1),
                         'yukseklik={yuk:6}'.format(yuk=yukseklik1), 'hiz={hi:8}'.format(hi=hiz1),
                         'sicaklik={sic:8}'.format(sic=sicaklik1),
                         'pilgerilimi={pil:8}'.format(pil=pilger1), 'lat={l1:8}'.format(l1=lat1),
                         'long={l2:8}'.format(l2=long1),
                         'alt={l3:8}'.format(l3=alt1), 'statü={st:8}'.format(st=statu1), 'roll={xx:6}'.format(xx=ax_1),
                         'yaw={yy:6}'.format(yy=ay_1), 'z={zz:6}'.format(zz=az_1),
                         ])


        except:
            self.lineEdit_29.setText('XBEE BEKLENİYOR')


class GLWidget1(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.rotX1 = 0
        self.rotY1 = 0
        self.rotZ1 = 0
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.setMinimumSize(401,221)
        self.setGeometry(480, 620, 150, 150)

    def setRotX1(self, ax_2):
        self.rotX1 = ax_2

    def setRotY1(self, ay_2):
        self.rotY1 = ay_2

    def setRotZ1(self, az_2):
        self.rotZ1 = az_2

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 0))
        gl.glEnable(gl.GL_DEPTH_TEST)
        self.initGeometry()

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)
        GLU.gluPerspective(70, aspect, 2, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix()

        gl.glTranslate(0.0, 0.0, -50.0)
        gl.glScale(30.0, 20.0, 30.0)
        #gl.glRotated(30, 0.5, 0.0, 0.0)
        gl.glRotated(self.rotX1, 1.0, 0.0, 0.0)
        gl.glRotated(self.rotY1, 0.0, 1.0, 0.0)
        gl.glRotated(self.rotZ1, 0.0, 0.0, 1.0)
        gl.glTranslate(-0.5, -0.5, -0.5)  # first, translate cube center to origin


        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertVBO)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self.colorVBO)

        gl.glDrawElements(gl.GL_QUADS, len(self.cubeIdxArray), gl.GL_UNSIGNED_INT, self.cubeIdxArray)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPopMatrix()  # restore the previous modelview matrix

    def initGeometry(self):
        self.cubeVtxArray = np.array(
            [[0.0, 0.0, 0.0],
             [0.5, 0.0, 0.0],
             [0.5, 1.5, 0.0],
             [0.0, 1.5, 0.0],
             [0.0, 0.0, 0.5],
             [0.5, 0.0, 0.5],
             [0.5, 1.5, 0.5],
             [0.0, 1.5, 0.5]])
        self.vertVBO = vbo.VBO(np.reshape(self.cubeVtxArray,
                                          (1, -1)).astype(np.float32))
        self.vertVBO.bind()

        self.cubeClrArray = np.array(
            [[0.0, 0.0, 0.0],
             [0.5, 0.0, 0.0],
             [0.5, 1.5, 0.0],
             [0.0, 1.5, 0.0],
             [0.0, 0.0, 0.5],
             [0.5, 0.0, 0.5],
             [0.5, 1.5, 0.5],
             [0.0, 1.5, 0.5]])
        self.colorVBO = vbo.VBO(np.reshape(self.cubeClrArray,
                                           (1, -1)).astype(np.float32))
        self.colorVBO.bind()

        self.cubeIdxArray = np.array(
            [0, 1, 2, 3,
             3, 2, 6, 7,
             1, 0, 4, 5,
             2, 1, 5, 6,
             0, 3, 7, 4,
            7, 6, 5, 4])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ana1()
    window.show()
    sys.exit(app.exec_())