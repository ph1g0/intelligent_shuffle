# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 12:01:09 2022

@author: ph1g0
"""

"""This module provides views to the audio player"""

import os, time, random, configparser

from PyQt5.QtCore import Qt, QUrl, QTimer

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from PyQt5.QtGui import QPalette, QColor

from PyQt5.QtWidgets import (
    QWidget, 
    QMessageBox, 
    QHBoxLayout, 
    QVBoxLayout, 
    QSlider, 
    QListWidget,
    QPushButton, 
    QLabel, 
    QComboBox,
    QFileDialog,
    QStyleFactory
    )



class AudioPlayer(QWidget):
    """Main Window"""
    def __init__(self, parent=None):       
        """Initializer"""
        super().__init__(parent)
        self.setWindowTitle("Audio Player")
        self.resize(800, 600)
        
        # Add QMediaPlayer class
        self.player = QMediaPlayer()
        
        # Add support for music formats and music list members
        self.song_formats = ['mp3', 'm4a', 'flac', 'wav', 'ogg']
        self.songs_list = [] # songs_list = [[song], [path], ...]
        self.cur_playing_song = ''
        self.is_pause = True
        self.is_switching = False
        
        # Initialize timer for music progress bar
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.execPlaybackMode)
        
        # Name of the config file to save the music folder path
        self.config_file = 'config.ini'
        
        # Setup UI
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI"""
        ##########################################################
        # Add elements to the GUI
        ##########################################################
        
        # Add slider as music progress bar
        self.slider = QSlider(Qt.Horizontal, self)
        self.startTimeLabel = QLabel('00:00')
        self.endTimeLabel = QLabel('00:00')
        
        # Add buttons for playback control
        self.playBtn = QPushButton('Play', self)
        self.playBtn.clicked.connect(self.playMusic)
        
        self.prevBtn = QPushButton('Previous song', self)
        self.prevBtn.clicked.connect(self.prevMusic)
        
        self.nextBtn = QPushButton('Next song', self)
        self.nextBtn.clicked.connect(self.nextMusic)
        
        self.openBtn = QPushButton('Open folder', self)
        self.openBtn.clicked.connect(self.openMusicFolder)
        
        # Add list that contains the music
        self.musicList = QListWidget()
        
        # Double click song to play
        self.musicList.itemDoubleClicked.connect(self.doubleClickToPlay)
        
        # Drag the slider to control the music playback progress
        self.slider.sliderMoved[int].connect(lambda: self.player.setPosition(self.slider.value()))
        
        # Add combo box button for selection of playback mode
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
        
        ##########################################################
        # Set color palette of the GUI
        ##########################################################
        
        palette = QPalette()
        
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(palette)
        
        ##########################################################
        # Other stuff
        ##########################################################
        
        # Load last music folder path
        self.loadMusicPath()
        
    def showTips(self, message):
        """Show tips"""
        QMessageBox.about(self, "showTips", message)
            
    def updateMusicPath(self):
        """Update current music path in config file"""
        # Read and parse config file
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        # Test if config file exists
        if not os.path.isfile(self.config_file):
            # Create a new section in the config file
            config.add_section('AudioPlayer')
        
        # Save path of the current music folder
        config.set('AudioPlayer', 'PATH', self.cur_path)
        
        # Write an .ini-format representation of the configuration state
        config.write(open(self.config_file, 'w'))
        
    def loadMusicPath(self):
        """Load last music path from config file"""
        # Read and parse config file
        config = configparser.ConfigParser()
        config.read(self.config_file)
            
        # Test if config file exists
        if not os.path.isfile(self.config_file):
            return
        
        # Get the last music path from config file
        self.cur_path = config.get('AudioPlayer', 'PATH')
        self.showMusicList()
        
    def openMusicFolder(self):
        """Open the music folder"""
        # Safe path of the music folder in the AudioPlayer class 
        self.cur_path = QFileDialog.getExistingDirectory(
            self, "Select your music folder ", './'
            )
        
        # Perform further tasks when music folder path is set
        if self.cur_path:
            self.showMusicList()
            self.cur_playing_song = ''
            self.startTimeLabel.setText('00:00')
            self.endTimeLabel.setText('00:00')
            self.slider.setSliderPosition(0)
            self.updateMusicPath()
            self.is_pause = True
            self.playBtn.setText(' Play ')
            
    def showMusicList(self):
        """Show the music list"""
        # Clear music list
        self.musicList.clear()
        
        # Identify playable files and add them to the songs list and music list
        for song in os.listdir(self.cur_path):
            if song.split('.')[-1] in self.song_formats:
                self.songs_list.append([song, os.path.join(self.cur_path, song).replace('\\', '/')])
                self.musicList.addItem(song)

        # Check if there is music in the music list
        if self.musicList.count() == 0:
            self.showTips('There are no playable music files in this directory')
            return
        
        # Set current playing song to first track in songs list
        self.musicList.setCurrentRow(0)
        self.cur_playing_song = self.songs_list[self.musicList.currentRow()][-1]
            
    def setCurPlaying(self):
        """Set the music currently playing"""
        # Set current playing song to selected row in music list
        self.cur_playing_song = self.songs_list[self.musicList.currentRow()][-1]
        self.player.setMedia(QMediaContent(QUrl(self.cur_playing_song)))

    def playMusic(self):
        """Start playing music"""
        # Check if there is music in the music list
        if self.musicList.count() == 0:
            self.showTips(' There is no music file to play in the current path ')
            return
        
        # Start playing music if it is not already playing        
        if not self.player.isAudioAvailable():
            self.setCurPlaying()
                
        # Start playing music if player is paused or song is switching
        if self.is_pause or self.is_switching:
            self.player.play()
            self.is_pause = False
            self.playBtn.setText('Pause')
                
        # Pause music if player is not paused or song is not switched
        elif (not self.is_pause) and (not self.is_switching):
            self.player.pause()
            self.is_pause = True
            self.playBtn.setText('Play')
            
    def prevMusic(self):
        """Play previous song"""  
        # Reset slider position
        self.slider.setValue(0)
        
        # Check if there is music in the music list
        if self.musicList.count() == 0:
            self.showTips(' There is no music file to play in the current path ')
            return
        
        # Select previous song in music list, if it is not the first song
        # When it is the first song, go to the end of the music list
        if self.musicList.currentRow() != 0:
            pre_row = self.musicList.currentRow()-1  
        else:
            pre_row = self.musicList.count()-1
            
        self.musicList.setCurrentRow(pre_row)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False

    def nextMusic(self):
        """Play next song"""
        # Reset slider position
        self.slider.setValue(0)
        
        # Check if there is music in the music list
        if self.musicList.count() == 0:
            self.showTips(' There is no music file to play in the current path ')
            return
        
        # Select next song in music list, if it is not the last song
        # When it is the last song, go to the start of the music list
        if self.musicList.currentRow() != self.musicList.count()-1:
            next_row = self.musicList.currentRow()+1
            
        else:
            next_row = 0
            
        self.musicList.setCurrentRow(next_row)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False
        
    def doubleClickToPlay(self):
        """Double click the name of the song to play"""
        # Reset slider position
        self.slider.setValue(0)
        self.is_switching = True
        
        # Set current playing song to selected row in music list
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False

    def execPlaybackMode(self):
        """Play music according to playback mode and refresh progress bar"""
        ##########################################################
        # Initialize slider
        ##########################################################
        
        # Set minimum, maximum and value of slider, if player is not paused or song is not switched
        if (not self.is_pause) and (not self.is_switching):
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.player.duration())
            self.slider.setValue(self.slider.value() + 1000)
        
        # Set start and end time label of slider 
        self.startTimeLabel.setText(time.strftime('%M:%S', time.localtime(self.player.position()/1000)))
        self.endTimeLabel.setText(time.strftime('%M:%S', time.localtime(self.player.duration()/1000)))
        
        ##########################################################
        # Set playback mode
        ##########################################################
        
        # Normal playback
        if (self.modeCom.currentIndex() == 0) and (not self.is_pause) and (not self.is_switching):
            # Do nothing if music list is empty
            if self.musicList.count() == 0:
                return
            
            # Play next song after the current one is finished 
            if self.player.position() == self.player.duration():
                self.nextMusic()
        
        # Single playback
        elif (self.modeCom.currentIndex() == 1) and (not self.is_pause) and (not self.is_switching):
            # Do nothing if music list is empty
            if self.musicList.count() == 0:
                return
            
            # Play the same song again after the current one is finished 
            if self.player.position() == self.player.duration():
                self.is_switching = True
                self.setCurPlaying()
                self.slider.setValue(0)
                self.playMusic()
                self.is_switching = False
        
        # Random playback
        elif (self.modeCom.currentIndex() == 2) and (not self.is_pause) and (not self.is_switching):
            # Do nothing if music list is empty
            if self.musicList.count() == 0:
                return
            
            # Play a random song after the current one is finished 
            if self.player.position() == self.player.duration():
                self.is_switching = True
                self.musicList.setCurrentRow(random.randint(0, self.musicList.count()-1))
                self.setCurPlaying()
                self.slider.setValue(0)
                self.playMusic()
                self.is_switching = False