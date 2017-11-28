###########################################################################################################
# Project: A plugin inspired by Shotgun and nextVersion by simon jokuschies

# Module:  testVersion.py - A plug-in in Nuke which saves files to a test location  

# Created: 11/21/2017

# Contact: Brian Wang (buyunwang@hotmail.com)
##########################################################################################################

# Imports
import nuke
import nukescripts
import os
import sys
import re
import time
import subprocess
import platform

# Add custom knobs to test panel
def addCustomKnobs():	
	node = nuke.thisNode()

	tab_test = nuke.Tab_Knob("test", "test")
	btn_createTestFolder = nuke.PyScript_Knob('create test folder', 'create test folder', '')
	btn_openInFinder = nuke.PyScript_Knob('open in explorer', 'open in explorer', '')
	btn_versionUp = nuke.PyScript_Knob('version up', 'version up', '')

	node.addKnob(tab_test)
	node.addKnob(btn_createTestFolder)
	node.addKnob(btn_openInFinder)
	node.addKnob(btn_versionUp)

# Select which write nodes to add to test folder		
def testVersionPanel():	
	p = nuke.Panel('test - Select write nodes to create test location')
	p.setWidth(500)
	for node in nuke.allNodes("Write"):
		p.addBooleanCheckBox("%s" % node.name() , 1)
	return p
	
# Set of corresponding custom functions	
def performCustomAction():	
	node = nuke.thisNode()
	knob = nuke.thisKnob()

	fileValue = node["file"].getValue()
	renderPath = os.path.dirname(fileValue)

	#open in finder
	if knob.name() == "open in explorer":
		if renderPath!="":
			try:
				if platform.system() == "Windows":
					os.startfile(renderPath)
				elif platform.system() == "Darwin":
					subprocess.Popen(["open", renderPath])
				else:
					subprocess.Popen(["xdg-open", renderPath])
			except:
				nuke.message("couldn't open render path. No such directory")
		else:
			nuke.message("Please make sure to set a render path")

	#create test folder		
	if knob.name() == "create test folder":
		if renderPath != "":	
			if not os.path.isdir(renderPath):
				# get topnode's value 
				# nuke.thisNode().input(0).name() 
				renderPath = os.path.join(renderPath ,"test_v1")
				os.makedirs(renderPath)
				nuke.message("successfully created test directory at: \n\n%s" % renderPath)
			else:
				nuke.message("please choose a new directory for test folders")	
		else:
			nuke.message("Please make sure to set a render path")		
	
	#create next version
	if knob.name() == "version up":	
		if renderPath != "":
			nukescripts.clear_selection_recursive()
			node.setSelected(True)
			nukescripts.version_up()
			node.setSelected(False)

			fileValue = node["file"].getValue()
			renderPath = os.path.dirname(fileValue)

			if not os.path.isdir(renderPath):
				os.makedirs(renderPath)
				nuke.message("Successfully versioned up")
			else:
				nuke.message("Please choose a test folder with version number or create a test folder")
		else:
			nuke.message("Please make sure to set a render path")
	

def testVersion():
	node = nuke.thisNode()
	fileValue = node["file"].getValue()
	renderPath = os.path.dirname(fileValue)
	p = testVersionPanel()
	if p.show():
		if renderPath != "":	
			if not os.path.isdir(renderPath):
				# get topnode's value 
				# nuke.thisNode().input(0).name() 
				renderPath = os.path.join(renderPath ,"test_v1")
				os.makedirs(renderPath)
				nuke.message("successfully created test directory at: \n\n%s" % renderPath)
			else:
				nuke.message("please choose a new directory for test folders")	
		else:
			nuke.message("Please make sure to set a render path")	