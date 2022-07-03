# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 12:01:09 2022

@author: ph1g0
"""

"""This module provides views to the audio player"""
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import (
    QWidget, 
    QDesktopWidget,
    QMessageBox, 
    QHBoxLayout, 
    QVBoxLayout, 
    QSlider, 
    QListWidget,
    QPushButton, 
    QLabel, 
    QComboBox
    )



class Window(QWidget):
    """Main Window"""
    def __init__(self, parent=None):       
        """Initializer"""
        super().__init__(parent)
        self.setWindowTitle("Audio Player")
        self.resize(800, 600)
        
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI"""
        ##########################################################
        # Add elements to the GUI
        ##########################################################
        
        # Add labels
        self.startTimeLabel = QLabel('00:00')
        self.endTimeLabel = QLabel('00:00')
        
        # Add slider
        self.slider = QSlider(Qt.Horizontal, self)
        
        # Add buttons
        self.playBtn = QPushButton(' Play ', self)
        self.prevBtn = QPushButton(' Last song ', self)
        self.nextBtn = QPushButton(' Next song ', self)
        self.openBtn = QPushButton(' Open folder ', self)
        
        # Add list
        self.musicList = QListWidget()
        
        # Add combo box button
        self.modeCom = QComboBox()
        self.modeCom.addItem(' Normal Playback ')
        self.modeCom.addItem(' Single Playback ')
        self.modeCom.addItem(' Random Playback ')
        
        ##########################################################
        # Lay out the GUI
        ##########################################################
        
        # The QHBoxLayout class lines up widgets horizontally
        # Lay out the slider
        self.hBoxSlider = QHBoxLayout()
        self.hBoxSlider.addWidget(self.startTimeLabel)
        self.hBoxSlider.addWidget(self.slider)
        self.hBoxSlider.addWidget(self.endTimeLabel)
        
        # Lay out the buttons
        self.hBoxButton = QHBoxLayout()
        self.hBoxButton.addWidget(self.playBtn)
        self.hBoxButton.addWidget(self.nextBtn)
        self.hBoxButton.addWidget(self.prevBtn)
        self.hBoxButton.addWidget(self.modeCom)
        self.hBoxButton.addWidget(self.openBtn)
        
        # The QVBoxLayout class lines up widgets vertically
        # Combine slider and button layout to vBoxControl
        self.vBoxControl = QVBoxLayout()
        self.vBoxControl.addLayout(self.hBoxSlider)
        self.vBoxControl.addLayout(self.hBoxButton)
    
        # Combine vBoxControl layout and musicList to vboxMain layout
        self.vboxMain = QVBoxLayout()
        self.vboxMain.addWidget(self.musicList)
        self.vboxMain.addLayout(self.vBoxControl)
        
        # Create final layout
        self.setLayout(self.vboxMain)