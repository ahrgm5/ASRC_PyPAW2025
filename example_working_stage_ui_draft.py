"""
@author: Romain Tirole
         The Advanced Science Research Center, City University of New York
         rtirole1@gc.cuny.edu
         
An example on how to load a stage and connect buttons and functions in an UI made in Qt Designer.
"""

# your own stage class to load
from my_Linear import LinearStage as Stage
import time

# import the required PyQt5 functions
from PyQt5.QtWidgets import QMainWindow, QWidget,  QApplication
from PyQt5.QtGui import QValidator, QDoubleValidator
from PyQt5 import uic


class StageWidget(QWidget):
    
    def __init__(self):
        
        # create a stage object
        self.stage = Stage()
        self.step_size = 2.5
        
        # just get the Qt out of it
        super().__init__()
        
        # load the UI and assign it to the widget itself
        uic.loadUi('PyPAW.ui', self)
        
        # when we create the widget, we want to look for available stages and list them as options
        self.stage.find_devices()
        for stage in self.stage.ports:
            self.Stage_List.addItem(stage)
            
        
    

        
        
        # Validation of Double input type for the Step_Size variable in GUI
        self.step_size = 0.5
        self.Step_Size_input.setText(str(self.step_size))
        validator1 = QDoubleValidator(0.0, 100.0, 2, self)
        self.Step_Size_input.setValidator(validator1)
        state1 = validator1.validate(self.Step_Size_input.text(), 0)[0]

        if state1 == QValidator.Acceptable:
            self.step_size = float(self.Step_Size_input.text())

        # Validation of Double input type for the Move_To variable in GUI
        self.setpoint = 0.0
        self.Move_To_input.setText(str(self.setpoint))   
        validator2 = QDoubleValidator(0.0, 14, 2, self)
        self.Move_To_input.setValidator(validator2)
        state2 = validator2.validate(self.Move_To_input.text(), 0)[0]

        if  state2 == QValidator.Acceptable:
            self.setpoint = float(self.Move_To_input.text())
       


        self.Go_button.clicked.connect(self.move_stage)
        self.Home_button.clicked.connect(self.move_home)
        self.Forward_button.clicked.connect(self.move_forward)
        self.Connect_button.clicked.connect(self.connect_stage)
        self.Backward_button.clicked.connect(self.move_backward)
        
    def connect_stage(self):
        self.stage.connect(self.Stage_List.currentText())
        self.Current_Position.setText(str(self.stage.check_position))


    def move_stage(self):
        self.stage.move(self.setpoint)
        x = self.stage.check_position()
        self.Current_Position.setText(str(x))


    def move_home(self):
        self.setpoint = 14.0
        self.stage.move(self.setpoint)
        self.Current_Position.setText(str(self.setpoint))
   

    def move_forward(self):
        pos = self.stage.check_position() + self.step_size
        self.stage.move(pos)
        self.Current_Position.setText(str(pos))


    def move_backward(self): 
        pos = self.stage.check_position() - self.step_size
        self.stage.move(pos)
        self.Current_Position.setText(str(pos))
  
    
    def closeEvent(self, *args, **kwargs):
        # this makes sure the affiliated stage instrument control disconnects properly when closing
        self.stage.on_closing()
        super(QWidget, self).closeEvent(*args, **kwargs)
        

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
        
    def closeEvent(self, *args, **kwargs):
        # this makes sure the widgets within the Main Window are closing properly
        self.stage_widget.close()
        super(QMainWindow, self).closeEvent(*args, **kwargs)




if __name__ == '__main__':

    app = QApplication([])
    myStage = StageGui()

    app.exec()
