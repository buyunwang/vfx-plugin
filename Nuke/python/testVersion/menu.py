import nuke
import testVersion

nuke.menu("Nuke").addCommand('Plugin/testVersion', 'testVersion.testVersion()')
nuke.addOnUserCreate(testVersion.addCustomKnobs, nodeClass = "Write")
nuke.addKnobChanged(testVersion.performCustomAction, nodeClass = "Write")
