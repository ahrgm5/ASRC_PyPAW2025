"""
@author: Romain Tirole
         The Advanced Science Research Center, City University of New York
         rtirole1@gc.cuny.edu
         
An example on how to load and display an UI made in Qt Designer.
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt5 import uic

class StageWidget(QWidget):
    
    def __init__(self):
        
        # just get the Qt out of it
        super().__init__()
        
        # load the UI and assign it to the widget itself
        uic.loadUi('PyPAW.ui', self)
                
class StageGui(QMainWindow):
    
    def __init__(self):
        
        # just get the Qt out of it
        super().__init__()
        
        # give a name to the window
        self.setWindowTitle('Stage')
        
        # create the affiliated stage widget
        self.stage_widget = StageWidget()
        
        # make the stage widget the main widget in the window
        self.setCentralWidget(self.stage_widget)
        
        # this runs the window once it is created
        self.show()

if __name__ == '__main__':

    app = QApplication([])

    myStage = StageGui()

    app.exec()