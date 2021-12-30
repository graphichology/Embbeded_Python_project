from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psutil
import platform
from datetime import datetime
from gui_styling import Ui_Form
import uuid
import os
import wmi

#set size of bits
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


 
class main(QWidget ,Ui_Form):
    def __init__(self) :
        QWidget.__init__(self)
        super(main, self).__init__()
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.layout  = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addStretch(-1)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.pushButton.clicked.connect(sys.exit)
        self.smpl_Info_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.simple_page))
        self.smpl_Info_btn.clicked.connect(self.smpl)
        self.sys_info_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.system_page))
        self.sys_info_btn.clicked.connect(self.sysm)
        self.cpu_info_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.cpu_page))
        self.cpu_info_btn.clicked.connect(self.cpu)
        self.mem_info_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.memory_page))
        self.mem_info_btn.clicked.connect(self.mem)
        self.serials_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.serials_page))
        self.serials_btn.clicked.connect(self.serials)
        self.network_info_btn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.network_page))
        self.network_info_btn.clicked.connect(self.net)



    def smpl(self) :
        #battery
        if (psutil.sensors_battery() != 0):
            battery = psutil.sensors_battery()
            plugged = battery.power_plugged
            percent = battery.percent
            secondss =battery.secsleft
            self.plug_lbl.setText("Plugged : " +str(plugged))
            #self.time_left_lbl.setText("Time left : "+ str(round(secondss/3600,2))+" hours")
            self.btry_prog_bar.setProperty("value", percent)
        else:
            self.btry_lbl.setSize( 0, 0)
            self.btry_prog_bar.setSize(0,0)
        # Boot Time
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        self.boot_lbl.setText(f"Boot Time : {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
        ######################################
    def sysm(self) :
        uname = platform.uname()
        self.sys_lbl.setText(f"System : {uname.system}")
        self.node_lbl.setText(f"Node Name : {uname.node}")
        self.reles_lbl.setText(f"Release : {uname.release}")
        self.vrsion_lbl.setText(f"Version : {uname.version}")
        machine_core=(uname.machine)
        machine_core=machine_core[len(machine_core)-2:]
        self.mchin_lbl.setText(f"Machine : {machine_core}")
        self.proces_lbl.setText(f"Processor : {uname.processor}")
        ###################################
    def cpu(self):
        self.phys_core_lbl.setText("Physical cores:"+ str(psutil.cpu_count(logical=False)))
        self.tot_core_lbl.setText("Total cores :"+str(psutil.cpu_count(logical=True)))
        # CPU frequencies
        cpufreq = psutil.cpu_freq()
        self.max_freq_lbl.setText(f"Max Frequency : {cpufreq.max:.2f}Mhz")
        self.min_freq_lbl.setText(f"Min Frequency : {cpufreq.min:.2f}Mhz")
        self.crnt_freq_lbl.setText(f"Current Frequency: {cpufreq.current:.2f}Mhz")
        # CPU usage
        # print("CPU Usage Per Core:")
        # for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        #     print(f"Core {i}: {percentage}%")
        # print(f"Total CPU Usage: {psutil.cpu_percent()}%")
        # self.tot_cpu_use_lbl.setText(f"Total CPU Usage: {psutil.cpu_percent()}%")
        self.tot_cpu_bar.setProperty("value",psutil.cpu_percent())
        ###########################
    def mem(self):
        # Memory Information
        # get the memory details
        svmem = psutil.virtual_memory()
        self.tot_mem_lbl.setText(f"Total Memory: {get_size(svmem.total)}")
        self.avlb_mem_lbl.setText(f"Available Memory: {get_size(svmem.available)}")
        self.used_mem_lbl.setText(f"Used Memory: {get_size(svmem.used)}")
        self.mem_prog_bar.setProperty("value", svmem.percent)
        # get the swap memory details (if exists)
        swap = psutil.swap_memory()
        self.tot_swap_lbl.setText(f"Total Swap: {get_size(swap.total)}")
        self.free_swap_lbl.setText(f"Free Swap: {get_size(swap.free)}")
        self.used_swap_lbl.setText(f"Used Swap: {get_size(swap.used)}")
        self.swap_prog_bar.setProperty("value", swap.percent)
        ##########################
        
    def serials(self):    
        command = "wmic memorychip get serialnumber"
        ramValue=os.popen(command).read().replace("\n","").replace("SerialNumber", "RAM ID:")
        self.ram_serial_lbl.setText(ramValue)
        encrypt_str = ""
        c = wmi.WMI ()
        
        for cpu in c.Win32_Processor ():
                    encrypt_str = encrypt_str + cpu.ProcessorId.strip ()
                    cpuValue=('CPU ID:'+ cpu.ProcessorId.strip ())
        self.cpu_serial_lbl.setText(cpuValue)
        diskValue=[]
        for physical_disk in c.Win32_DiskDrive ():
                encrypt_str = encrypt_str + physical_disk.SerialNumber.strip ()            
                diskValue.append(physical_disk.SerialNumber.strip ())
        disk=str(diskValue).replace(","," \nDisk ID:").replace("'","").replace("[","").replace("]","")
        self.disk_serial_lbl.setText('Disk ID:'+disk)
        for board_id in c.Win32_BaseBoard ():
                        #Mainboard serial number encrypt_str = encrypt_str + board_id.SerialNumber.strip ()
                        motherboradValue=("Mother Board ID:"+ board_id.SerialNumber.strip ())
        self.board_serial_lbl.setText(motherboradValue)
        for bios_id in c.Win32_BIOS ():#bios serial number
                    encrypt_str = encrypt_str + bios_id.SerialNumber.strip ()
                    biosValue=("Bios ID:"+ bios_id.SerialNumber.strip ())
                    #print("encrypt_str:", encrypt_str)
        self.bios_serial_lbl.setText(biosValue)
        ######################################
    def net(self):
        # Network information
        # if_addrs = psutil.net_if_addrs()
        # for interface_name, interface_addresses in if_addrs.items():
        #     for address in interface_addresses:
        #         print(f"=== Interface: {interface_name} ===")
        #         if str(address.family) == 'AddressFamily.AF_INET':
        #             print(f"  IP Address: {address.address}")
        #             print(f"  Netmask: {address.netmask}")
        #             print(f"  Broadcast IP: {address.broadcast}")
        #             # self.tableWidget_3.insertRow(1)
        #             # self.tableWidget_3.setItem(0,3,QtWidgets.QTableWidgetItem(address.netmask))
        #         elif str(address.family) == 'AddressFamily.AF_PACKET':
        #             print(f"  MAC Address: {address.address}")
        #             print(f"  Netmask: {address.netmask}")
        #             print(f"  Broadcast MAC: {address.broadcast}")
        # get IO statistics since boot
        net_io = psutil.net_io_counters()
        self.byt_sent_lbl.setText(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
        self.byt_recev_lbl.setText(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")      
        mac_add= (':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1]))
        self.mac_lbl.setText(f"Your MAC address: "+ mac_add)


#####################################
class MyBar(QWidget):
    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        print(self.parent.width())
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(700,10,0,0)


        self.btn_min = QPushButton("-")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(21,21)

        self.btn_min.setStyleSheet("""font-size:15pt;font-weight:bold;color:#006801;background-color: #2aca42;border-radius:10;""")

        self.layout.addWidget(self.btn_min)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)


    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
    def btn_min_clicked(self):
        self.parent.showMinimized()
######################################

app =QApplication(sys.argv)
window=main()
window.show()
app.exec_()















