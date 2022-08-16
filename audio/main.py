# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 11:57:16 2022

@author: ph1g0
"""

"""This module provides Audio application"""

import sys

from PyQt5.QtWidgets import QApplication

from .views import AudioPlayer



def main():
    """Audio main function"""
    # Create the application
    app = QApplication(sys.argv)

    # Set style of the application
    app.setStyle('Fusion')

    # Create the main window
    win = AudioPlayer()
    win.show()
    
    # Run the event loop
    sys.exit(app.exec())