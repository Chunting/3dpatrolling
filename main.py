#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 
# This file is part of the framework 3dpatrolling. 
# 
# Copyright (C) 2016-present Luigi Freda <freda at diag dot uniroma1 dot it>
# For more information see <https://gitlab.com/luigifreda/3dpatrolling>
# 
# 3dpatrolling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# 3dpatrolling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with 3DPATROLLING. If not, see <http://www.gnu.org/licenses/>.

"""
Qt GUI for launching the patrolling system or the path planning system.
Author: Luigi Freda
"""

import os
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QDesktopWidget, QPushButton, QApplication)
from PyQt5.QtWidgets import (QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QFileDialog)
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QLabel) 
from PyQt5 import QtCore
from PyQt5.QtGui import QFont    
import subprocess

# get the location of this file!
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# --------------------------------------------  
# run-command utils 
        
def run_command(command, debug=False):
    """ runs command and returns the output."""
    if debug:
        print("$ {}".format(command))
    #p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, executable='/bin/bash')
    p = subprocess.Popen(command, shell=True, executable='/bin/bash')
    #return iter(p.stdout.readline, b'')
        
        
def executeCommand(command, stderr=None, stdout=None, debug=False):
    """ Raises an error when a command fails. """
    if debug:
        print("$ {}".format(command))
    subprocess.check_call(command, stderr=stderr, stdout=stdout, env=dict(os.environ), shell=True)

def executeCommands(commands, stderr=None, stdout=None, debug=False):
    for command in commands:
        executeCommand(command, stderr=stderr, stdout=stdout, debug=debug)
        
        
def executeCommandNoCheck(command, stderr=None, stdout=None, debug=False):
    """ Does not raise an error when a command fails. """
    if debug:
        print("$ {}".format(command))
    subprocess.call(command, stderr=stderr, stdout=stdout, env=dict(os.environ), shell=True)


def executeCommandsNoCheck(commands, stderr=None, stdout=None, debug=False):
    for command in commands:
        executeCommandNoCheck(command, stderr=stderr, stdout=stdout, debug=debug)         

# --------------------------------------------        
# Utils

def getBaseFileNameNoExt(filename):
    base = os.path.basename(filename)
    os.path.splitext(base)
    return os.path.splitext(base)[0]

# --------------------------------------------        
# Main Widget 

class MainWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.cmdDebug = False 

        self.mainWidgetWidth = 400
        self.mainWidgetHeight = 400

        self.patrollingWorldName = ''
        self.patrollingWorldsFolder=__location__+'/patrolling_ws/src/multirobot/patrolling3d_sim/maps'
        self.patrolling_enable = True     
        self.patrolling_interactive = False  
        self.vrep_mode = 1            

        self.sourceCmd='source source-all.bash; '

        self.initUI()
        self.center()
        
        
    def initUI(self):
        
        QToolTip.setFont(QFont('SansSerif', 10))
        
        self.setGeometry(0, 0, self.mainWidgetWidth, self.mainWidgetHeight)
        self.setWindowTitle('3dpatrolling')    

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)        

        #
        self.btn_patrolling = QPushButton('Launch patrolling', self)
        self.btn_patrolling.setToolTip('Launch the patrolling system.')     

        self.btn_patrolling_world = QPushButton('Select patrol world', self)
        self.btn_patrolling_world.setToolTip('Select your desired patrolling world. A default world is already set in the script sim_launcher_patrolling.')             

        self.checkbtn_patrolling_enable = QCheckBox('Enable patrolling',self)
        self.checkbtn_patrolling_enable.setToolTip('Enable/disable the patrolling agent. Disabling can be useful for building and saving a map in a selected world (please, read the documentation).')
        self.checkbtn_patrolling_enable.toggled.connect(self.slot_patrolling_enable)  
        self.checkbtn_patrolling_enable.setChecked(self.patrolling_enable)

        self.checkbtn_patrolling_interactive = QCheckBox('Build graph on start',self)
        self.checkbtn_patrolling_interactive.setToolTip('Interactively build the patrolling graph on start and save it, instead of loading a pre-built graph.')
        self.checkbtn_patrolling_interactive.toggled.connect(self.slot_patrolling_interactive)  
        self.checkbtn_patrolling_interactive.setChecked(self.patrolling_interactive)        

        #
        self.btn_path_planner = QPushButton('Launch navigation', self)
        self.btn_path_planner.setToolTip('Launch path planner system')     

        #
        hbox_vrep = QGroupBox()
        hboxlayout_vrep = QHBoxLayout()
        hbox_vrep.setLayout(hboxlayout_vrep)
        vrep_mode_help_string='normal:0 launch VREP in normal mode (you have to press the button play to start \nheadless:1 launch VREP in headless mode (hidden) and automatically start it \nnormal-autostart:2 launch VREP in normal mode and automatically start it (you will not be able to pause!)'
        self.label_vrep_mode = QLabel()
        self.label_vrep_mode.setText("V-REP mode")
        self.label_vrep_mode.setToolTip(vrep_mode_help_string)              
        self.cb_vrep_mode = QComboBox()
        self.cb_vrep_mode.setToolTip(vrep_mode_help_string)         
        self.cb_vrep_mode.addItems(["normal", "headless", "normal autostart"])
        self.cb_vrep_mode.setCurrentIndex(self.vrep_mode)
        self.cb_vrep_mode.currentIndexChanged.connect(self.slot_vrep_mode_change)
        hboxlayout_vrep.addWidget(self.label_vrep_mode)
        hboxlayout_vrep.addWidget(self.cb_vrep_mode)        

        #
        self.btn_save_map = QPushButton('Save map', self)
        self.btn_save_map.setToolTip('Save the built map')   

        #
        self.btn_load_map = QPushButton('Load map', self)
        self.btn_load_map.setToolTip('Load the built map')           

        #
        self.btn_kill = QPushButton('Kill', self)
        self.btn_kill.setToolTip('Kill all nodes of the system')              

        # set layouts
        self.createPatrollingLayout()   
        self.createPathPlanningLayout()   
        self.mainLayout.addWidget(hbox_vrep)          
        self.mainLayout.addWidget(self.btn_save_map)    
        self.mainLayout.addWidget(self.btn_load_map)                       
        self.mainLayout.addWidget(self.btn_kill)          
        
        # connections 
        self.btn_patrolling.clicked.connect(self.slot_patrolling)  
        self.btn_patrolling_world.clicked.connect(self.slot_patrolling_world)          

        self.btn_path_planner.clicked.connect(self.slot_path_planner)

        self.btn_save_map.clicked.connect(self.slot_save_map) 
        self.btn_load_map.clicked.connect(self.slot_load_map)         

        self.btn_kill.clicked.connect(self.slot_kill)                                

        # show the widget 
        self.show()
        
    def center(self):        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())   

    def createPatrollingLayout(self):
        self.horizontalGroupBox_patrolling = QGroupBox("Patrolling")
        self.gridLayout_patrolling = QGridLayout()
        #self.gridLayout_patrolling.setColumnStretch(1, 3)
        #self.gridLayout_patrolling.setColumnStretch(2, 3)
        
        self.gridLayout_patrolling.addWidget(self.btn_patrolling,0,0)
        self.gridLayout_patrolling.addWidget(self.btn_patrolling_world,0,1)
        self.gridLayout_patrolling.addWidget(self.checkbtn_patrolling_enable,1,1)   
        self.gridLayout_patrolling.addWidget(self.checkbtn_patrolling_interactive,2,1)                
        
        self.horizontalGroupBox_patrolling.setLayout(self.gridLayout_patrolling)      
        self.mainLayout.addWidget(self.horizontalGroupBox_patrolling)       

    def createPathPlanningLayout(self):
        self.horizontalGroupBox_pp = QGroupBox("Navigation")
        self.gridLayout_pp = QGridLayout()
        #self.gridLayout_pp.setColumnStretch(1, 3)
        #self.gridLayout_pp.setColumnStretch(2, 3)
        
        self.gridLayout_pp.addWidget(self.btn_path_planner,1,0)

        
        self.horizontalGroupBox_pp.setLayout(self.gridLayout_pp)      
        self.mainLayout.addWidget(self.horizontalGroupBox_pp)              

# slots         

    def slot_patrolling(self):
        print('launch patrolling')
        cmd_envs=''
        if  not self.patrolling_enable: 
            cmd_envs += 'export ENABLE_PATROLLING_ENV=false; '
        if  self.patrolling_interactive: 
            cmd_envs += 'export BUILD_PATROLLING_GRAPH_ON_START_ENV=true; '            
        cmd_envs += 'export LAUNCH_VREP_MODE_ENV=' + str(self.vrep_mode) + '; '            
        cmd = self.sourceCmd + cmd_envs + 'rosrun patrolling3d_sim sim_launcher_patrolling ' + self.patrollingWorldName
        print(cmd)
        run_command(cmd) 
         
    def slot_patrolling_world(self):
        print('select patrolling world')  
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select patrolling world", self.patrollingWorldsFolder,"V-REP scenes (*.ttt)", options=options)
        if fileName:
            self.patrollingWorldName = getBaseFileNameNoExt(fileName)
            print('world: ', self.patrollingWorldName)                         

    def slot_patrolling_enable(self):           
        self.patrolling_enable = self.checkbtn_patrolling_enable.isChecked()
        print('patrolling_enable: ', self.patrolling_enable)      

    def slot_patrolling_interactive(self):           
        self.patrolling_interactive = self.checkbtn_patrolling_interactive.isChecked()
        print('patrolling_interactive: ', self.patrolling_interactive)             

    def slot_path_planner(self):
        print('launch path planner system') 
        cmd_envs=''          
        cmd_envs += 'export LAUNCH_VREP_MODE_ENV=' + str(self.vrep_mode) + '; '           
        cmd = self.sourceCmd + cmd_envs + 'rosrun path_planner sim_launcher_navigation'
        print(cmd)
        run_command(cmd)  

    def slot_vrep_mode_change(self,i):
        print('change vrep mode')   
        self.vrep_mode = i
        print('Items in the list are :')
        for count in range(self.cb_vrep_mode.count()):
            print(self.cb_vrep_mode.itemText(count))
        print('Current index',self.vrep_mode,'selection changed ',self.cb_vrep_mode.currentText())

    def slot_save_map(self):
        print('save_map')   
        cmd = self.sourceCmd + 'rosrun patrolling3d_sim save_map'
        print(cmd)      
        run_command(cmd)  

    def slot_load_map(self):
        print('load_map')   
        cmd = self.sourceCmd + 'rosrun patrolling3d_sim load_map'
        print(cmd)      
        run_command(cmd)        

    def slot_kill(self):
        print('kill all nodes')   
        cmd = self.sourceCmd + 'rosrun patrolling3d_sim kill_vrep_sim'
        print(cmd)      
        run_command(cmd)  

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWidget()
    sys.exit(app.exec_())