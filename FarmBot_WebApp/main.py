import Farmbot
import threading
import time
import datetime
from flask import Flask, render_template
    
sensor1 = "SENSOR 1";

class MainInterface:
    def __init__(self):
        
        self.sensor1 = "N.A.";
        self.sensor2 = "N.A.";
        self.sensor3 = "N.A.";
        self.sensor4 = "N.A.";
        
        #Varialbles del programa
        self.pararSensores = False
        self.comPort="COM2"
        self.baudRate=115200
        self.flag=0
        self.manualFlag=0
        self.autoFlag=0
        self.startFlag=0
        self.stopFlag=1
        
        #Crea un nuevo farmbot
        self.farmbot= Farmbot.Farmbot(self.comPort,self.baudRate)
        
        #incializa los threads de la interfaz
        self.threadAuto = threading.Thread(target= self.moveAutoFunc)
        self.threat_receive=threading.Thread(target= 
                                             self.farmbot.receiveMesagesContinuos)
        self.threadManual= threading.Thread(target= self.moveManualFunc)
        self.threadWaterPots= threading.Thread(target= self.farmbot.moveAuto)
        
    #Funciones para los botones

    def ClickStart(self):
        if self.startFlag ==0 and self.stopFlag==1:
            try:
                self.startFlag=1
                self.stopFlag=0
                superLog("Start")
                self.farmbot.initSerialPort()
                superLog("initiated serial port")
                self.pararSensores = True
                self.manualFlag =1
                self.autoFlag=0
                superLog("Reading")
                superLog("-----")
                # Empieza el thread de leer mensajes
                if not self.threat_receive.is_alive():
                    self.threat_receive = threading.Thread(target= 
                                             self.farmbot.receiveMesagesContinuos)
                if not self.threadManual.is_alive():
                    self.threadManual=threading.Thread(target=self.moveManualFunc)
                self.threat_receive.start()
                self.threadManual.start()
            except Exception as ex:
                self.startFlag=0
                self.stopFlag=1
                self.farmbot.closeSerialPort()
                superLog("Error Starting Farmbot")
        else:
            superLog("Farmbot Already Started")
            
    def read_writeSensores(self):
        #leer sensores

        #Espera 5 seg para que el FarmBot regrese las respuestas de los sensores

        #Actualiza el valor de los sensores
        
        changes = 0;
        
        s1 =  str(int(self.farmbot.ValPins[96]*100/1023))+' %'
        if self.sensor1 != s1:
            superLog("Sensor 1: " + self.sensor1 + " => " + s1)
            self.sensor1 =  s1
            changes = 1
            
        s2 =  str(int(self.farmbot.ValPins[95]*100/1023))+' %'
        if self.sensor2 != s2:
            superLog("Sensor 2: " + self.sensor2 + " => " + s2)
            self.sensor2 =  s2
            changes = 1
        
        s3 =  str(int(self.farmbot.ValPins[94]*100/1023))+' %'
        if self.sensor3 != s3:
            superLog("Sensor 3: " + self.sensor3 + " => " + s3)
            self.sensor3 =  s3
            changes = 1
        
        s4 =  str(int(self.farmbot.ValPins[93]*100/1023))+' %'
        if self.sensor4 != s4:
            superLog("Sensor 4: " + self.sensor4 + " => " + s4)
            self.sensor4 =  s4
            changes = 1
            
        if changes == 1:
            superLog( "-----" )
            
            
    #Espera 30 seg para volver a leer los sensores
    def moveManualFunc(self):
        while(self.manualFlag):
            
            file = open("farmbotLogs.txt","w")
            file.close()
            
            self.farmbot.updateHumiditySensors()
            self.read_writeSensores()
            for i in range(60):
                if not self.manualFlag:
                    return
                time.sleep(5/60)
    def moveAutoFunc(self):
        if not self.threadWaterPots.is_alive() :
                self.threadWaterPots= threading.Thread(target= self.farmbot.moveAuto)
        self.threadWaterPots.start()
        while(self.autoFlag):
            #Update the values of sensors in the interface
            if not self.farmbot.watering:
                self.farmbot.updateHumiditySensors()
                self.read_writeSensores()

            time.sleep(10)#5s sleep
    def ClickStop(self):
        if self.stopFlag==0 and self.startFlag==1:
            self.startFlag=0
            self.stopFlag=1
            self.farmbot.endCommunication()
            self.threat_receive.join()
            self.farmbot.closeSerialPort()
            # self.pararSensores = False
        
            # self.ledsFrame.cnvLedOff.create_oval(25,10,75,60, fill="#FF0000")
            # self.ledsFrame.cnvLedOn.create_oval(25,10,75,60, fill="#61605c")
            # self.ledsFrame.cnvLedAuto.create_oval(25,10,75,60, fill="#61605c")
            # self.ledsFrame.cnvLedManu.create_oval(25,10,75,60, fill="#61605c")
            # self.ledsFrame.cnvLedWater.create_oval(25,10,75,60, fill="#61605c") 

            print("Stop")
    def ClickAuto(self):
        if self.manualFlag==1 and self.autoFlag==0 and self.startFlag==1:
            self.manualFlag=0
            self.autoFlag=1
            self.threadManual.join()
            # self.ledsFrame.cnvLedAuto.create_oval(25,10,75,60, fill="#FFFD00")
            # self.ledsFrame.cnvLedManu.create_oval(25,10,75,60, fill="#61605c")
            if not self.threadAuto.isAlive():
                self.threadAuto=threading.Thread(target= self.moveAutoFunc)
            self.threadAuto.start()
        print("Auto")
    def ClickManual(self):
        if self.manualFlag==0 and self.autoFlag==1 and self.startFlag==1:
            self.autoFlag=0
            self.manualFlag=1
            self.farmbot.moveManual()
            if self.threadAuto.is_alive():   
                self.threadAuto.join()
            if self.threadWaterPots.is_alive():    
                self.threadWaterPots.join()
            # self.ledsFrame.cnvLedManu.create_oval(25,10,75,60, fill="#FFFD00")
            # self.ledsFrame.cnvLedAuto.create_oval(25,10,75,60, fill="#61605c")
            if not self.threadManual.is_alive():
                self.threadManual=threading.Thread(target=self.moveManualFunc)
            self.threadManual.start()
        print("Manual")
    def ClickHome(self):
        if self.manualFlag ==1:
            self.farmbot.move()
            print("Home")
        else:
            print("Farmbot is in autoMode please go to Manual")
    def ClickWater(self):
        if(self.flag==0 and self.manualFlag ==1):    
            # self.ledsFrame.cnvLedWater.create_oval(25,10,75,60, fill="#FFFD00")
            self.flag=1
            self.farmbot.water(1)
            print("Water")
        elif(self.flag==1 and self.manualFlag ==1):
            # self.ledsFrame.cnvLedWater.create_oval(25,10,75,60, fill="#61605c")
            self.flag=0
            self.farmbot.water(0)
            print("No Water")
        elif(self.autoFlag):
            superLog("Error Watering" + "Farmbot Must Be in manual mode")
    def ClickXup(self):
        superLog("xUp")
        if(self.autoFlag==1 and self.startFlag==1):
            superLog("Error " + "Farmbot Must Be in manual mode")
        elif(self.startFlag==0):
            superLog("Error " + "Farmbot Must Be started first")
        else:
            self.farmbot.move(x=self.farmbot.posX +100,
                              y=self.farmbot.posY,
                              z=self.farmbot.posZ)
    def ClickXdown(self):
        print("xDown")
        if(self.autoFlag==1 and self.startFlag==1):
            superLog("Error Farmbot Must Be in manual mode")
        elif(self.startFlag==0):
            superLog("Error Farmbot Must Be started first")
        else:
            self.farmbot.move(x=self.farmbot.posX -100,
                              y=self.farmbot.posY,
                              z=self.farmbot.posZ)
    def ClickYup(self):
        print("yUp")
        if(self.autoFlag==1 and self.startFlag==1):
            superLog("Error Farmbot Must Be in manual mode")
        elif(self.startFlag==0):
            superLog("Error Farmbot Must Be started first")
        else:
            self.farmbot.move(x=self.farmbot.posX,
                              y=self.farmbot.posY+100,
                              z=self.farmbot.posZ)
    def ClickYdown(self):
        print("yDown")
        if(self.autoFlag==1 and self.startFlag==1):
            superLog("Error Farmbot Must Be in manual mode")
        elif(self.startFlag==0):
            superLog("Error Farmbot Must Be started first")
        else:
            self.farmbot.move(x=self.farmbot.posX,
                              y=self.farmbot.posY-100,
                              z=self.farmbot.posZ)
    def ClickZup(self):
        print("zUp")
        if(self.autoFlag==1 and self.startFlag==1):
            superLog("Error Farmbot Must Be in manual mode")
        elif(self.startFlag==0):
            superLog("Error Farmbot Must Be started first")
        else:
            self.farmbot.move(x=self.farmbot.posX,
                              y=self.farmbot.posY,
                              z=self.farmbot.posZ+100)
    def ClickZdown(self):
        print("zDown")
        if(self.autoFlag==1 and self.startFlag==1):
            superLog("Error Farmbot Must Be in manual mode")
        elif(self.startFlag==0):
            superLog("Error Farmbot Must Be started first")
        else:
            self.farmbot.move(x=self.farmbot.posX ,
                              y=self.farmbot.posY,
                              z=self.farmbot.posZ-100)

app = Flask(__name__)

inte = MainInterface()

@app.route("/")
def conection():
    superLog("Somebody connected")
    return crearPagina()

@app.route("/home")
def home():
    return crearPagina()

@app.route('/start/', methods=['GET', 'POST'])
def clickStart():
    superLog("")
    superLog("Clicked Start");
    inte.ClickStart()
    return crearPagina()

@app.route('/stop/', methods=['GET', 'POST'])
def clickStop():
    superLog("Clicked Stop");
    inte.ClickStop()
    superLog("")
    return crearPagina()

@app.route('/homebtn/', methods=['GET', 'POST'])
def clickHome():
    superLog("")
    superLog("Clicked Home");
    inte.ClickHome()
    return crearPagina()

@app.route('/water/', methods=['GET', 'POST'])
def clickWater():
    superLog("Clicked Watering");
    inte.ClickWater()
    superLog("")
    return crearPagina()

@app.route('/auto/', methods=['GET', 'POST'])
def clickAuto():
    superLog("Clicked Auto");
    inte.ClickAuto()
    superLog("")
    return crearPagina()

@app.route('/manual/', methods=['GET', 'POST'])
def clickManual():
    superLog("Clicked Manual");
    inte.ClickManual()
    superLog("")
    return crearPagina()

@app.route('/moveXUp/', methods=['GET', 'POST'])
def moveXUp():
    superLog("Clicked x up");
    inte.ClickXup()
    return crearPagina()

@app.route('/moveXDown/', methods=['GET', 'POST'])
def moveXDown():
    superLog("Clicked x down");
    inte.ClickXdown()
    return crearPagina()

@app.route('/moveYUp/', methods=['GET', 'POST'])
def moveYUp():
    superLog("Clicked y up");
    inte.ClickYup()
    return crearPagina()

@app.route('/moveYDown/', methods=['GET', 'POST'])
def moveYDown():
    superLog("Clicked y down");
    inte.ClickYdown()
    return crearPagina()

@app.route('/moveZUp/', methods=['GET', 'POST'])
def moveZUp():
    superLog("Clicked z up");
    inte.ClickZup()
    return crearPagina()

@app.route('/moveZDown/', methods=['GET', 'POST'])
def moveZDown():
    superLog("Clicked z down");
    inte.ClickZdown()
    return crearPagina()
 


def crearPagina():
    sensor = {
    'p1': inte.sensor1,
    'p2': inte.sensor2,
    'p3': inte.sensor3,
    'p4': inte.sensor4
    }
    return render_template('page.html', sensor=sensor);
         
def superLog(mensaje):
    with open("logs.txt", 'r+') as f:
        log = datetime.datetime.now().strftime("%c") + " - " + mensaje
        content = f.read()
        f.seek(0, 0)
        f.write(log.rstrip('\r\n') + '\n' + content)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)