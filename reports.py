import sys
from time import sleep
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from reportlab.lib.testutils import setOutDir
setOutDir(__name__)


def main():
    # import visa
    #
    # rm = visa.ResourceManager()
    # planar = rm.open_resource('TCPIP::192.168.0.3::INSTR')
    # print("inst=", planar.query("*IDN?"))
    #
    # fdate = planar.query("SYST:DATE?").replace(",", "_")
    # folder = r'C:\!meas\LPF_' + fdate
    # print("mkdir:", planar.write("MMEM:MDIR " + '"' + folder + '"'))
    # print(planar.write("DISP:WIND1:ACT"))
    #
    # for meas_num in range(1, 11):
    #     meas_file_name = folder + "\\" + "lpf_obr2_" + str(meas_num).zfill(4) + ".s2p"
    #     print(planar.write("INIT1"))
    #     sleep(0.5)
    #     # freqs = planar.query("SENS:FREQ:DATA?")
    #     # amps = planar.query("CALC1:DATA:FDAT?")
    #     # print("freqs:", freqs.count(",") + 1, freqs)
    #     # print("amp:", amps.count(",") + 1, amps)
    #     print(planar.write("MMEM:STOR:SNP:TYPE:S2P"))
    #     print(planar.write("MMEM:STOR:SNP " + '"' + meas_file_name + '"'))

    # import serial
    # def display_unicode(data):
    #     return "".join(["\\u%s" % hex(ord(l))[2:].zfill(4) for l in data])
    #
    # # msg = bytearray([0x00, 0x23, 0x00, 0x4e, 0x00, 0x41, 0x00, 0x4d, 0x00, 0x45, 0x13, 0x10])
    # # msg = b'\x00\x23\x00\x4e\x00\x41\x00\x4d\x00\x45\n'
    # # msg = b'\x23\x4e\x41\x4d\x45\n'
    # # msg = b'#NAME\n'
    # # msg = b'\xff\xfe\x00\x00#\x00\x00\x00N\x00\x00\x00A\x00\x00\x00M\x00\x00\x00E\x00\x00\x00'
    # # msg = b'\xff\xfe#\x00N\x00A\x00M\x00E\x00'
    # msg = bytes('#NAME', encoding="utf-16")
    #
    # port = serial.Serial("COM6", baudrate=115200, parity=serial.PARITY_NONE, bytesize=8, stopbits=serial.STOPBITS_ONE)
    # # port = serial.Serial(port='COM6', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0,
    # #                      rtscts=0)
    #
    # print("port name:", port.name)
    # print(port.is_open)
    # print("in data:", msg)
    #
    # port.writelines([msg])
    #
    # output = port.read_until(size=len(msg))
    # print("read data:", output)
    #
    # port.close()

    app = QApplication(sys.argv)
    # app.setStyle("macintosh")
    w = MainWindow()
    w.initApp()
    # w.showMaximized()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
