#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import serial


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()       

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createProgressBar()

        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.progressBar, 2, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 4)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 5)
        self.setLayout(mainLayout)

        self.setWindowTitle("Potentiostat Application")
        self.changeStyle('Fusion')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Insert Measurement Parameters:")

        # Select Measurement Method
        self.styleComboBox = QComboBox()
        methods = ["CV", "DPV", "EIS"]
        self.styleComboBox.addItems(methods)
        self.styleComboBox.setCurrentText("CV")

        self.styleLabel = QLabel("&Select measurement method:")
        self.styleLabel.setBuddy(self.styleComboBox)

        # Simpan metode pengukuran yang terpilih
        chosenMethod = self.styleComboBox.currentText()

        # Labels
        self.NbCycleLabel = QLabel(self)
        self.NbCycleLabel.setText("Number of cycles")
        self.VminLabel = QLabel(self)
        self.VminLabel.setText("Vmin (V)")
        self.VmaxLabel = QLabel(self)
        self.VmaxLabel.setText("Vmax (V)")
        self.SRLabel = QLabel(self)
        self.SRLabel.setText("Scan rate (V/s)")
        self.FminLabel = QLabel(self)
        self.FminLabel.setText("Min freq (Hz)")
        self.FmaxLabel = QLabel(self)
        self.FmaxLabel.setText("Max freq (Hz)")
        self.PWLabel = QLabel(self)
        self.PWLabel.setText("Pulse width (ms)")
        self.CurrRangeLabel = QLabel(self)
        self.CurrRangeLabel.setText("Curr range (uA)")

        # Text Fields
        self.NbCycle = QLineEdit(self)
        self.Vmin = QLineEdit(self)
        self.Vmax = QLineEdit(self)
        self.ScanRate = QLineEdit(self)
        self.Fmin = QLineEdit(self)
        self.Fmax = QLineEdit(self)
        self.PW = QLineEdit(self)
        self.CurrRange = QLineEdit(self)

        # Inisialisasi komunikasi serial
        esp_serial = serial.Serial('COM3', 115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None)

        # Kirim ke Serial dulu
        if esp_serial.is_open:
            esp_serial.write(("%.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f\r\n" % (self.NbCycle, self.Vmin, self.Vmax, self.ScanRate, self.Fmin, self.Fmax, self.PW, self.CurrRange)).encode("utf-8"))

        # Conditions
        #self.styleComboBox.update()
        #if chosenMethod == "CV":
        #    self.Fmin.setEnabled(False)
        #    self.Fmax.setEnabled(False)
        #    self.PW.setEnabled(False)
        #    self.CurrRange.setEnabled(False)
        #if chosenMethod == "DPV":
        #    self.NbCycle.setEnabled(False)
        #    self.Fmin.setEnabled(False)
        #    self.Fmax.setEnabled(False)
        #    self.CurrRange.setEnabled(False)
        #if chosenMethod == "EIS":
        #    self.NbCycle.setEnabled(False)
        #    self.Vmin.setEnabled(False)
        #    self.Vmax.setEnabled(False)
        #self.styleComboBox.update()

        # Push Buttons
        self.StartMeasurement = QPushButton("Start Measurement")
        self.StartMeasurement.setDefault(True)
        self.StartMeasurement.move(20, 320)
        self.StopMeasurement = QPushButton("Stop Measurement")
        self.StopMeasurement.setDefault(True)
        self.StopMeasurement.move(20, 350)

        # Notes field
        self.textEdit = QTextEdit()
        self.textEdit.setPlainText("Insert notes here")

        # Set positions in grid layout
        layout = QGridLayout()
        layout.addWidget(self.StartMeasurement,9,0)
        layout.addWidget(self.StopMeasurement,9,1)
        layout.addWidget(self.textEdit,10,0,10,2)
        layout.addWidget(self.styleComboBox,0,1)
        layout.addWidget(self.styleLabel,0,0)
        layout.addWidget(self.NbCycle,1,1)
        layout.addWidget(self.NbCycleLabel,1,0)
        layout.addWidget(self.Vmin,2,1)
        layout.addWidget(self.VminLabel,2,0)
        layout.addWidget(self.Vmax,3,1)
        layout.addWidget(self.VmaxLabel,3,0)
        layout.addWidget(self.ScanRate,4,1)
        layout.addWidget(self.SRLabel,4,0)
        layout.addWidget(self.Fmin,5,1)
        layout.addWidget(self.FminLabel,5,0)
        layout.addWidget(self.Fmax,6,1)
        layout.addWidget(self.FmaxLabel,6,0)
        layout.addWidget(self.PW,7,1)
        layout.addWidget(self.PWLabel,7,0)
        layout.addWidget(self.CurrRange,8,1)
        layout.addWidget(self.CurrRangeLabel,8,0)



        # layout.addWidget(radioButton1)
        # layout.addWidget(radioButton2)
        # layout.addWidget(radioButton3)
        # layout.addWidget(checkBox)
        

        #layout.addStretch()
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Measurement Results")

        defaultPushButton = QPushButton("Default Push Button")
        defaultPushButton.setDefault(True)

        

        flatPushButton = QPushButton("Flat Push Button")
        flatPushButton.setFlat(True)

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        #self.setCentralWidget(self.graphWidget)
        
        # Inisialisasi data yang ingin diplot
        voltage = []
        current = []
        voltage2 = []
        current2 = []

        # Inisialisasi ESP
        esp_serial = serial.Serial('COM3', 115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None)

        # Terima hasil dari ESP yg diposting ke serial setelah pengukuran dilakukan
        if esp_serial.is_open:
            while True:
                try:
                    len = esp_serial.in_waiting()
                    if len:
                        # Ambil data hasil pengukuran
                        [vin, vout, arus] = [float(v) for v in (esp_serial.readline().decode("utf-8").split("\t"))]
                        
                        voltage.append(vin)
                        current.append(arus)
                
                except Exception as e:
                    # plot data: x, y values
                    self.graphWidget.plot(voltage, current, pen=pg.mkPen('b', width=3))
                    self.graphWidget.plot(voltage2, current2, pen=pg.mkPen('r', width=3))
                    self.graphWidget.setLabel('bottom', 'Voltage (V)')
                    self.graphWidget.setLabel('left', 'Current (uA)')
                    self.graphWidget.showGrid(x=True, y=True)
                    break

        layout = QHBoxLayout()
        layout.addWidget(self.graphWidget)
        self.topRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())