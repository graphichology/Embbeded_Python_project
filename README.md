# installing python and QT
1. install python from official site
2. install QT from official site
3. install pyqt library by open cmd and write

`pip install PyQt5`

4. install pyqt tools to get qt designer by write in cmd

`pip install pyqt5-tools`

5. open python file location in c and go to /lib/site-packages/qt5_applicatioins/qt/bin/designer.exe

# applying style to python code
1. design gui with qt desinger
2. save ui file as name.ui
3. open powershell in same of ui file directory (shift and right click at the directory and select open powershell)
4. write this command

`pyuic5 .\name.ui -o newName.py`

5. open python file with vscode
6. create new python file at same direction and write those lines

`from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from newName import Ui_Form
class main(QWidget ,Ui_Form):
    def __init__(self) :
        QWidget.__init__(self)
        self.setupUi(self)
app =QApplication(sys.argv)
window=main()
window.show()
app.exec_()`

7. run last file


# build python app as exe
1. open shell in directory of python file and run this command

`pyinstaller --onefile filename.py` 
*note: this command work with linux*

2. or you can setup auto py to exe by write this command

`pip install auto-py-to-exe`


#packages installed
1-usb information
`pip install pyusb`

2-cpu information
`pip install py-cpuinfo`

3-mother board serial number
must add "Wbem" to system environment variables
at PATH add %SystemRoot%\System32\Wbem