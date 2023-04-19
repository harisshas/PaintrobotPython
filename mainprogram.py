from tkinter import *
import tkinter as tk
import logging
import datetime
import time
from time import strftime
import os
import subprocess
import socket
import threading
import serial
import glob

#North - Blue
#South - Green
#Top   - Orange
#Master - Black

ALARMONOFF=1
changeparcheck=0
Yaxisspeed=0
Xaxisspeed=0
CurrentMode=0

horizmovposoffset=20;

Pausemode=0;
Currprocess="";
PrevCurrprocess="";
Currprocesscommstring="";
Engagelimitsvar=1;
ICFbuttonenabled=1;

Inchenablestring="00000";
Inchenablenorth="0";
Inchenablesouth="0";
Inchenabletop="0";
Inchenableeast="0";
Inchenablewest="0";

datetimestring = strftime('%d/%m/%y %H:%M:%S %p')
screen_shot_cmd = 'scrot -e \'mv $f /home/pi/Desktop/PaintingRobot/screenshots/\''
logger = logging.getLogger('mylogger')
handler = logging.FileHandler('/home/pi/Desktop/PaintingRobot/logs/PR.log')
logger.addHandler(handler)
logger.warning(datetimestring + " :: " + "starting program run")


#GPIO.output(GPIO21, True);

Currprocess="";

#ICF Roof only
Type1windowstartposlist=[]
Type1windowlength=610
Type1windowheight=560
Type1coachlength=21337
Type1coachwidth=3245
Type1coachheight=4025
Type1sidewallheight=3336
Type1sidewalllength=2215
Type1baseheight=913
Type1windowbaseheight=1090;
Type1toppaintsouthsideclearance=400;
Type1toppaintnorthsideclearance=300;

#ICF NAC Sides only without windows
Type2windowstartposlist=[]
Type2windowlength=610
Type2windowheight=560
Type2coachlength=21337
Type2coachwidth=3245
Type2coachheight=4025
Type2sidewallheight=3336
Type2sidewalllength=2215
Type2baseheight=913
Type2windowbaseheight=1090;
Type2toppaintsouthsideclearance=400;
Type2toppaintnorthsideclearance=300;

#ICF NAC sitting sides only with windows
Type3windowstartposlist=[2695, 3546, 4397, 5248, 6099, 6950, 7801, 8652, 10515, 11366, 12217, 13068, 13919, 14770, 15621, 16472, 17323, 18174]
Type3windowlength=610
Type3windowheight=560
Type3coachlength=21337
Type3coachwidth=3245
Type3coachheight=4025
Type3sidewallheight=3336
Type3sidewalllength=2423
Type3baseheight=913
Type3windowbaseheight=1090;
Type3toppaintsouthsideclearance=400;
Type3toppaintnorthsideclearance=300;

#ICF AC sleeper sides only with windows
Type4windowstartposlist=[2695, 3546, 4397, 5248, 6099, 6950, 7801, 8652, 10515, 11366, 12217, 13068, 13919, 14770, 15621, 16472, 17323, 18174]
Type4windowlength=610
Type4windowheight=560
Type4coachlength=21337
Type4coachwidth=3245
Type4coachheight=4025
Type4sidewallheight=3336
Type4sidewalllength=2423
Type4baseheight=913
Type4windowbaseheight=1090;
Type4toppaintsouthsideclearance=400;
Type4toppaintnorthsideclearance=300;

#LHB Surfacer
Type5windowstartposlist=[]
Type5windowlength=610
Type5windowheight=560
Type5coachlength=23450
Type5coachwidth=3240
Type5coachheight=4039
Type5sidewallheight=3340
Type5sidewalllength=2242
Type5baseheight=1098
Type5windowbaseheight=914;
Type5toppaintsouthsideclearance=400;
Type5toppaintnorthsideclearance=300;

#LHB Fin Gray
Type6windowstartposlist=[]
Type6windowlength=610
Type6windowheight=560
Type6coachlength=23450
Type6coachwidth=3240
Type6coachheight=4039
Type6sidewallheight=1748
Type6sidewalllength=650
Type6baseheight=1098
Type6windowbaseheight=914;
Type6toppaintsouthsideclearance=400;
Type6toppaintnorthsideclearance=300;

#LHB Fin Non AC Sitting Red
Type7windowstartposlist=[2915, 3815, 4715, 5615, 6515, 7415, 8315, 9215, 10115, 11015, 11915, 12815, 13715, 14615, 15515, 16415, 17315, 18215, 19115, 20015]
Type7windowlength=610
Type7windowheight=560
Type7coachlength=23450
Type7coachwidth=3240
Type7coachheight=4039
Type7sidewallheight=3340;
Type7sidewalllength=1592;
Type7baseheight=1748;
Type7windowbaseheight=264;
Type7toppaintsouthsideclearance=400;
Type7toppaintnorthsideclearance=300;

#LHB Fin AC Sleeper Red
Type8windowstartposlist=[2915, 3815, 4715, 5615, 6515, 7415, 8315, 9215, 10115, 11015, 11915, 12815, 13715, 14615, 15515, 16415, 17315, 18215, 19115, 20015]
Type8windowlength=610
Type8windowheight=560
Type8coachlength=23450
Type8coachwidth=3240
Type8coachheight=4039
Type8sidewallheight=3340;
Type8sidewalllength=1592;
Type8baseheight=1748;
Type8windowbaseheight=264;
Type8toppaintsouthsideclearance=400;
Type8toppaintnorthsideclearance=300;

maingroupwidth=1600;

#field values
availablelength=27000; # in mm
widthresolution=300; #in mm
Yaxistravellength=2200; #in mm
Yaxisbottomclearance=1080; #in mm
Topaxistravellength=4200; #in mm 

#noofcolsrequired=round((availablelength/(eachcolwidth*widthresolution)));
noofcolsrequired=round(availablelength/widthresolution);
eachcolwidth=round(maingroupwidth/noofcolsrequired);

NSTXpos=0;
prevXpos=-1;
Currwindowpos=0
crossingwindow=0

whetherplotpointscalled=0;

def sprayandmovebuttonselect():
    global Currprocess;
    Currprocess="Spray & Move";
    sendsignal("12*100*2200*4200*300#3900*1#2199");

def ICFbuttonselect():
    global ICFbuttonenabled;
    print("ICF button selected")
    ICFbuttonenabled=1;
    LHBbutton["fg"]="gray"
    ICFbutton["fg"]="black"
    ICFbutton["bd"]=1
    LHBbutton["bd"]=0
    CoachtypeButton1["text"]="ICF Roof";
    CoachtypeButton2["text"]="ICF Non AC SL FC";
    CoachtypeButton3["text"]="ICF Non AC SL SC";
    CoachtypeButton4["text"]="ICF AC SL FC";
    
def LHBbuttonselect():
    global ICFbuttonenabled;
    print("LHB button selected")
    ICFbuttonenabled=0;
    ICFbutton["fg"]="gray"
    LHBbutton["fg"]="black"
    ICFbutton["bd"]=0
    LHBbutton["bd"]=1
    CoachtypeButton1["text"]="LHB Surfacer";
    CoachtypeButton2["text"]="LHB Gray SC";
    CoachtypeButton3["text"]="LHB Non AC Red SC";
    CoachtypeButton4["text"]="LHB AC Red SC";

def Engagelimitsselect():
    global Engagelimitsvar;
    if Engagelimitsvar==1:
        Engagelimitsvar=0;
        Engagelimitsbutton["image"]=limitsengageicon
        #print('limits bypassed');
        sendsignal("10*1*0")
    elif Engagelimitsvar==0:
        Engagelimitsvar=1;
        Engagelimitsbutton["image"]=limitsdisengageicon
        #print('limits engaged')
        sendsignal("10*0*0")

def initfieldvalues():
    global horizstartlength;
    global Inchdistanceset;
    global Spraytime;
    global Yaxisspeed;
    global Xaxisspeed;
    
    horizstartlength=500; # in mm
    Inchdistanceset=500; #inching distance in mm
    Spraytime=1000; # time in ms
    
    Yaxisspeed=50
    Xaxisspeed=50

def startbutton():
    global NSTXpos;
    global Pausemode;
    global Currprocess;
    Currprocess="BatchJobInchStart";
    Pausemode=0;
    NSTXpos=0;
    #sendsignal("1")
    runningmodebuttonstatus();
    NSTnextcommand();    

def pausebutton():
    global Pausemode;
    global PrevCurrprocess;
    global Currprocess;
    
    print('pause/resume button pressed');
    print("Currprocess inside pausebutton: "+Currprocess)    
    if Pausemode == 0:
        #print('pausing');
        #sendsignal("0")
        print('inside pause clause');
        Pausebutton["text"]="Resume";
        Pausemode=1;
        PrevCurrprocess=Currprocess
        #added now
        inchupbutton["state"] = NORMAL
        inchdownbutton["state"] = NORMAL
        inchleftbutton["state"] = NORMAL
        inchrightbutton["state"] = NORMAL
        sprayandmovebutton["state"] = NORMAL
        spraybutton["state"] = NORMAL
        Resetbutton["state"] = NORMAL
        Resetbutton["text"] = "Repeat"
        
        if Inchallcarraigevar.get() == 1:
            Inchallcarraige["state"] = NORMAL
            Inchcarraige1["state"] = DISABLED
            Inchcarraige2["state"] = DISABLED
            Inchcarraige3["state"] = DISABLED
            Inchcarraige4["state"] = DISABLED
            Inchcarraige5["state"] = DISABLED
        else:
            Inchallcarraige["state"] = NORMAL
            Inchcarraige1["state"] = NORMAL
            Inchcarraige2["state"] = NORMAL
            Inchcarraige3["state"] = NORMAL
            Inchcarraige4["state"] = NORMAL
            Inchcarraige5["state"] = NORMAL
        Statusbutton['text']="Pausing"
    else:
        #print('resuming');
        #sendsignal("10")
        print('inside pause clause');
        Pausebutton["text"]="Pause";
        Pausemode=0;
        print("Prevprocess inside pausebutton: "+PrevCurrprocess)
        if("BatchJobPaint" in PrevCurrprocess):
            Statusbutton['text']="Auto Painting"
            sendsignal("5*"+str(Xaxisspeed)+"*"+str(int(widthresolution)+int(horizmovposoffset)))
            Currprocess="BatchJobInchNext";            
        else:
            NSTnextcommand();    

def stopbutton():
    global Pausemode
    global Currprocess;
    #print('stop button pressed');
    Currprocess="Stopping";
    sendsignal("11*0*0")
    Pausemode=0;
    enableresetbuttongroup();
    #clearpoints();

def resetbutton():
    #sending reset signal
    global Currprocess;
    global CurrentMode;
    global Pausemode;
    
    if Pausemode==0:
        Currprocess="Resetting";
        sendsignal("2*"+str(Xaxisspeed)+"*"+str(Yaxisspeed))
        CurrentMode=0;
    elif Pausemode==1:
        Currprocess="Repeating";
        sendsignal(Currprocesscommstring);
    
def inchupbutton():
    global Currprocess;
    Currprocess="Inching Up";
    sendsignal("3*"+str(Yaxisspeed)+"*"+str(Inchdistanceset))
    
def inchdownbutton():
    global Currprocess;
    Currprocess="Inching Down";
    sendsignal("4*"+str(Yaxisspeed)+"*"+str(Inchdistanceset))    
    
def inchleftbutton():
    global Currprocess;
    Currprocess="Inching Backward";
    sendsignal("6*"+str(Xaxisspeed)+"*"+str(Inchdistanceset))      
    
def inchrightbutton():
    global Currprocess;
    Currprocess="Inching Forward";
    sendsignal("5*"+str(Xaxisspeed)+"*"+str(Inchdistanceset))
    
def spraybutton():
    global Currprocess;
    Currprocess="Spraying";
    sendsignal("7*"+str(Spraytime)+"*0")

def disableallitemsexceptstop():
#     Engageallcarraige["state"] = DISABLED
#     Engagecarraige1["state"] = DISABLED
#     Engagecarraige2["state"] = DISABLED
#     Engagecarraige3["state"] = DISABLED
#     Engagecarraige4["state"] = DISABLED
#     Engagecarraige5["state"] = DISABLED
    
    Inchallcarraige["state"] = DISABLED    
    Inchcarraige1["state"] = DISABLED
    Inchcarraige2["state"] = DISABLED
    Inchcarraige3["state"] = DISABLED
    Inchcarraige4["state"] = DISABLED
    Inchcarraige5["state"] = DISABLED
    
    CoachtypeButton1["state"] = DISABLED
    CoachtypeButton2["state"] = DISABLED
    CoachtypeButton3["state"] = DISABLED
    CoachtypeButton4["state"] = DISABLED
    
    ICFbutton["state"] = DISABLED
    LHBbutton["state"] = DISABLED
    
    ICFbutton["bd"]=0
    LHBbutton["bd"]=0
    
    HorizontalSpeedslider["state"] = DISABLED
    VerticalSpeedslider["state"] = DISABLED
    
    inchupbutton["state"] = DISABLED
    inchdownbutton["state"] = DISABLED
    inchleftbutton["state"] = DISABLED
    inchrightbutton["state"] = DISABLED
    spraybutton["state"] = DISABLED
    sprayandmovebutton["state"] = DISABLED
    
    Startbutton["state"] = DISABLED
    Stopbutton["state"] = NORMAL
    Pausebutton["state"] = DISABLED
    Resetbutton["state"] = DISABLED
    
    Engagelimitsbutton["state"] = DISABLED

def disableallitems():
#     Engageallcarraige["state"] = DISABLED
#     Engagecarraige1["state"] = DISABLED
#     Engagecarraige2["state"] = DISABLED
#     Engagecarraige3["state"] = DISABLED
#     Engagecarraige4["state"] = DISABLED
#     Engagecarraige5["state"] = DISABLED
    
    Inchallcarraige["state"] = DISABLED    
    Inchcarraige1["state"] = DISABLED
    Inchcarraige2["state"] = DISABLED
    Inchcarraige3["state"] = DISABLED
    Inchcarraige4["state"] = DISABLED
    Inchcarraige5["state"] = DISABLED
    
    CoachtypeButton1["state"] = DISABLED
    CoachtypeButton2["state"] = DISABLED
    CoachtypeButton3["state"] = DISABLED
    CoachtypeButton4["state"] = DISABLED
    
    ICFbutton["state"] = DISABLED
    LHBbutton["state"] = DISABLED
    
    ICFbutton["bd"]=0
    LHBbutton["bd"]=0
    
    HorizontalSpeedslider["state"] = DISABLED
    VerticalSpeedslider["state"] = DISABLED
    
    inchupbutton["state"] = DISABLED
    inchdownbutton["state"] = DISABLED
    inchleftbutton["state"] = DISABLED
    inchrightbutton["state"] = DISABLED
    spraybutton["state"] = DISABLED
    sprayandmovebutton["state"] = DISABLED
    
    Startbutton["state"] = DISABLED
    Stopbutton["state"] = DISABLED
    Pausebutton["state"] = DISABLED
    Resetbutton["state"] = DISABLED
    
    Engagelimitsbutton["state"] = DISABLED
    
def enableallitems():
    global ICFbuttonenabled;
    print('inside enable all items');
    # Engageallcarraige["state"] = NORMAL
    # Engagecarraige1["state"] = NORMAL
    # Engagecarraige2["state"] = NORMAL
    # Engagecarraige3["state"] = NORMAL
    # Engagecarraige4["state"] = NORMAL
    # Engagecarraige5["state"] = NORMAL
    
#     if Engageallcarraigevar.get() == 1:
#         Engageallcarraige["state"] = NORMAL
#         Engagecarraige1["state"] = DISABLED
#         Engagecarraige2["state"] = DISABLED
#         Engagecarraige3["state"] = DISABLED
#         Engagecarraige4["state"] = DISABLED
#         Engagecarraige5["state"] = DISABLED
#     else:
#         Engageallcarraige["state"] = NORMAL
#         Engagecarraige1["state"] = NORMAL
#         Engagecarraige2["state"] = NORMAL
#         Engagecarraige3["state"] = NORMAL
#         Engagecarraige4["state"] = NORMAL
#         Engagecarraige5["state"] = NORMAL

    
    # Inchallcarraige["state"] = NORMAL
    # Inchcarraige1["state"] = NORMAL
    # Inchcarraige2["state"] = NORMAL
    # Inchcarraige3["state"] = NORMAL
    # Inchcarraige4["state"] = NORMAL
    # Inchcarraige5["state"] = NORMAL
    
    if Inchallcarraigevar.get() == 1:
        Inchallcarraige["state"] = NORMAL
        Inchcarraige1["state"] = DISABLED
        Inchcarraige2["state"] = DISABLED
        Inchcarraige3["state"] = DISABLED
        Inchcarraige4["state"] = DISABLED
        Inchcarraige5["state"] = DISABLED
    else:
        Inchallcarraige["state"] = NORMAL
        Inchcarraige1["state"] = NORMAL
        Inchcarraige2["state"] = NORMAL
        Inchcarraige3["state"] = NORMAL
        Inchcarraige4["state"] = NORMAL
        Inchcarraige5["state"] = NORMAL
    
    CoachtypeButton1["state"] = NORMAL
    CoachtypeButton2["state"] = NORMAL
    CoachtypeButton3["state"] = NORMAL
    CoachtypeButton4["state"] = NORMAL
    
    if ICFbuttonenabled == 1:
        ICFbutton["state"] = NORMAL
        LHBbutton["state"] = NORMAL
        LHBbutton["fg"]="gray"
        ICFbutton["fg"]="black"
        ICFbutton["bd"]=1
        LHBbutton["bd"]=0
    else :    
        ICFbutton["state"] = NORMAL
        LHBbutton["state"] = NORMAL
        LHBbutton["fg"]="black"
        ICFbutton["fg"]="gray"
        ICFbutton["bd"]=0
        LHBbutton["bd"]=1
        
    HorizontalSpeedslider["state"] = NORMAL
    VerticalSpeedslider["state"] = NORMAL
    
    inchupbutton["state"] = NORMAL
    inchdownbutton["state"] = NORMAL
    inchleftbutton["state"] = NORMAL
    inchrightbutton["state"] = NORMAL
    spraybutton["state"] = NORMAL
    sprayandmovebutton["state"] = NORMAL
    
    Startbutton["state"] = NORMAL
    Stopbutton["state"] = NORMAL
    Pausebutton["state"] = NORMAL
    Resetbutton["state"] = NORMAL
    
    Engagelimitsbutton["state"] = NORMAL
    
#    Engageallcarraigeselect()
#    Inchallcarraigeselect()

    
def disablestartbuttongroup():
    Startbutton["state"] = DISABLED
    Stopbutton["state"] = DISABLED
    Pausebutton["state"] = DISABLED
    Resetbutton["state"] = DISABLED
    
#     Engageallcarraige["state"] = DISABLED
#     Engagecarraige1["state"] = DISABLED
#     Engagecarraige2["state"] = DISABLED
#     Engagecarraige3["state"] = DISABLED
#     Engagecarraige4["state"] = DISABLED
#     Engagecarraige5["state"] = DISABLED
    
def enableresetbuttongroup():
    print('inside enable reset button group');
    Startbutton["state"] = DISABLED
    Stopbutton["state"] = DISABLED
    Pausebutton["state"] = DISABLED
    Resetbutton["state"] = NORMAL
    disablecoachtypeselect()
    
#     Engageallcarraige["state"] = DISABLED
#     Engagecarraige1["state"] = DISABLED
#     Engagecarraige2["state"] = DISABLED
#     Engagecarraige3["state"] = DISABLED
#     Engagecarraige4["state"] = DISABLED
#     Engagecarraige5["state"] = DISABLED
    
    Engagelimitsbutton["state"] = NORMAL
    
def enablestartbuttongroup():
    Startbutton["state"] = NORMAL
    Stopbutton["state"] = DISABLED
    Pausebutton["state"] = DISABLED
    Resetbutton["state"] = DISABLED
    
#     Engageallcarraige["state"] = NORMAL
#     Engagecarraige1["state"] = DISABLED
#     Engagecarraige2["state"] = DISABLED
#     Engagecarraige3["state"] = DISABLED
#     Engagecarraige4["state"] = DISABLED
#     Engagecarraige5["state"] = DISABLED
    
    Engagelimitsbutton["state"] = DISABLED

def enablecoachtypeselect() :
    global ICFbuttonenabled;
    CoachtypeButton1["state"] = NORMAL
    CoachtypeButton2["state"] = NORMAL
    CoachtypeButton3["state"] = NORMAL
    CoachtypeButton4["state"] = NORMAL
    
    if ICFbuttonenabled == 1:
        ICFbutton["state"] = NORMAL
        LHBbutton["state"] = NORMAL
        LHBbutton["fg"]="gray"
        ICFbutton["fg"]="black"
        ICFbutton["bd"]=1
        LHBbutton["bd"]=0
    else :    
        ICFbutton["state"] = NORMAL
        LHBbutton["state"] = NORMAL
        LHBbutton["fg"]="black"
        ICFbutton["fg"]="gray"
        ICFbutton["bd"]=0
        LHBbutton["bd"]=1
    
def disablecoachtypeselect() :
    CoachtypeButton1["state"] = DISABLED
    CoachtypeButton2["state"] = DISABLED
    CoachtypeButton3["state"] = DISABLED
    CoachtypeButton4["state"] = DISABLED
    
    ICFbutton["state"] = DISABLED
    LHBbutton["state"] = DISABLED
    ICFbutton["bd"]=0
    LHBbutton["bd"]=0
    
def runningmodebuttonstatus() :
    disableallitems()
    Stopbutton["state"] = NORMAL
    Pausebutton["state"] = NORMAL
    Resetbutton["state"] = DISABLED
    Resetbutton["text"] = "Reset"

def stoppingmodebuttonstatus() :
    disableallitems()
    Resetbutton["state"] = NORMAL
    
def selectcoachtype1():
    global changeparcheck
    global CurrentMode
    global whetherplotpointscalled
    global Inchenablenorth;
    global Inchenablesouth;
    global Inchenabletop;
    global Inchenableeast;
    global Inchenablewest;
    global Inchenablestring;

    changeparcheck=1
    global ICFbuttonenabled;
    if ICFbuttonenabled == 1 :
        CurrentMode=1
        print('selected coach type 1')
        whetherplotpointscalled=1;
        
        Inchallcarraigevar.set(0)
        Inchcarraige1var.set(0)
        Inchcarraige2var.set(0)
        Inchcarraige3var.set(0)
        Inchcarraige4var.set(0)
        Inchcarraige5var.set(1)
        Inchenablenorth="0";
        Inchenablesouth="0";
        Inchenabletop="1";
        Inchenableeast="0";
        Inchenablewest="0";
        setinchenablstring();
        sendsignal("8*7*1*"+str(Inchenablestring))

        addlsettingsbutton();
        #plotpoints()
    else :
        CurrentMode=5
        print('selected coach type 5')
        whetherplotpointscalled=1;
                
        Inchallcarraigevar.set(0)
        Inchcarraige1var.set(0)
        Inchcarraige2var.set(0)
        Inchcarraige3var.set(1)
        Inchcarraige4var.set(1)
        Inchcarraige5var.set(1)
        Inchenablenorth="1";
        Inchenablesouth="1";
        Inchenabletop="1";
        Inchenableeast="0";
        Inchenablewest="0";
        setinchenablstring();
        sendsignal("8*7*1*"+str(Inchenablestring))
        

        addlsettingsbutton();
        #plotpoints()
    
def selectcoachtype2():
    global changeparcheck
    global CurrentMode
    global whetherplotpointscalled
    global Inchenablenorth;
    global Inchenablesouth;
    global Inchenabletop;
    global Inchenableeast;
    global Inchenablewest;
    global Inchenablestring;
    
    changeparcheck=1
    #CurrentMode=2
    global ICFbuttonenabled;
    if ICFbuttonenabled == 1 :
        CurrentMode=2
        print('selected coach type 2')
        whetherplotpointscalled=1;
        
        Inchallcarraigevar.set(0)
        Inchcarraige1var.set(0)
        Inchcarraige2var.set(0)
        Inchcarraige3var.set(1)
        Inchcarraige4var.set(1)
        Inchcarraige5var.set(0)
        Inchenablenorth="1";
        Inchenablesouth="1";
        Inchenabletop="0";
        Inchenableeast="0";
        Inchenablewest="0";
        setinchenablstring();
        sendsignal("8*7*1*"+str(Inchenablestring))
        
        addlsettingsbutton();
        #plotpoints()
    else :
        CurrentMode=6
        print('selected coach type 6')
        whetherplotpointscalled=1;
                
        Inchallcarraigevar.set(0)
        Inchcarraige1var.set(0)
        Inchcarraige2var.set(0)
        Inchcarraige3var.set(1)
        Inchcarraige4var.set(1)
        Inchcarraige5var.set(0)
        Inchenablenorth="1";
        Inchenablesouth="1";
        Inchenabletop="0";
        Inchenableeast="0";
        Inchenablewest="0";
        setinchenablstring();
        sendsignal("8*7*1*"+str(Inchenablestring))
        
        addlsettingsbutton();
        #plotpoints()

def selectcoachtype3():
    global changeparcheck
    global CurrentMode
    global whetherplotpointscalled
    global Inchenablenorth;
    global Inchenablesouth;
    global Inchenabletop;
    global Inchenableeast;
    global Inchenablewest;
    global Inchenablestring;
    
    changeparcheck=1
    global ICFbuttonenabled;
    if ICFbuttonenabled == 1 :
        CurrentMode=3
        print('selected coach type 3')
        whetherplotpointscalled=1;
                
        Inchallcarraigevar.set(0)
        Inchcarraige1var.set(0)
        Inchcarraige2var.set(0)
        Inchcarraige3var.set(1)
        Inchcarraige4var.set(1)
        Inchcarraige5var.set(0)
        Inchenablenorth="1";
        Inchenablesouth="1";
        Inchenabletop="0";
        Inchenableeast="0";
        Inchenablewest="0";
        setinchenablstring();
        sendsignal("8*7*1*"+str(Inchenablestring))
        
        addlsettingsbutton();
        #plotpoints()
    else :
        CurrentMode=7
        print('selected coach type 7')
        whetherplotpointscalled=1;
                
        Inchallcarraigevar.set(0)
        Inchcarraige1var.set(0)
        Inchcarraige2var.set(0)
        Inchcarraige3var.set(1)
        Inchcarraige4var.set(1)
        Inchcarraige5var.set(0)
        Inchenablenorth="1";
        Inchenablesouth="1";
        Inchenabletop="0";
        Inchenableeast="0";
        Inchenablewest="0";
        setinchenablstring();
        sendsignal("8*7*1*"+str(Inchenablestring))
        
        addlsettingsbutton();
        #plotpoints()
    
def selectcoachtype4():
    global changeparcheck
    global CurrentMode
    global whetherplotpointscalled
    global Inchenablenorth;
    global Inchenablesouth;
    global Inchenabletop;
    global Inchenableeast;
    global Inchenablewest;
    global Inchenablestring;
    
    changeparcheck=1
    #CurrentMode=4
    global ICFbuttonenabled;
    if ICFbuttonenabled == 1 :
        CurrentMode=4
        print('selected coach type 4')
        whetherplotpointscalled=1;
        
        Inchallcarraigevar.set(0)
        Inchcarraige1var.set(0)
        Inchcarraige2var.set(0)
        Inchcarraige3var.set(1)
        Inchcarraige4var.set(1)
        Inchcarraige5var.set(0)
        Inchenablenorth="1";
        Inchenablesouth="1";
        Inchenabletop="0";
        Inchenableeast="0";
        Inchenablewest="0";
        setinchenablstring();
        sendsignal("8*7*1*"+str(Inchenablestring))
        
        addlsettingsbutton();
        #plotpoints()
    else :
        CurrentMode=8
        print('selected coach type 8')
        whetherplotpointscalled=1;
                
        Inchallcarraigevar.set(0)
        Inchcarraige1var.set(0)
        Inchcarraige2var.set(0)
        Inchcarraige3var.set(1)
        Inchcarraige4var.set(1)
        Inchcarraige5var.set(0)
        Inchenablenorth="1";
        Inchenablesouth="1";
        Inchenabletop="0";
        Inchenableeast="0";
        Inchenablewest="0";
        setinchenablstring();
        sendsignal("8*7*1*"+str(Inchenablestring))
        
        addlsettingsbutton();
        #plotpoints()

def NSTcellcolor(xpos, mode, currTypecoachlength):
    global noofcolsrequired;
    
    if mode == 1:
        #after completion window portion
        rowfind=0;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']="green";
        Southsidecellgrouplist[cellfind]['bg']="green";
        Topsidecellgrouplist[colfind]['bg']="green";
        
        rowfind=1;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']="white";
        Southsidecellgrouplist[cellfind]['bg']="white";
        
        rowfind=2;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']="green";
        Southsidecellgrouplist[cellfind]['bg']="green";
        
        Northsideprogress['text']=str(round(((xpos-int(horizstartlength))/currTypecoachlength)*100))+"%";
        Southsideprogress['text']=str(round(((xpos-int(horizstartlength))/currTypecoachlength)*100))+"%";
        Topsideprogress['text']=str(round(((xpos-int(horizstartlength))/currTypecoachlength)*100))+"%";
        
    if mode == 2:
        #after completion wall portion
        rowfind=0;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']="green";
        Southsidecellgrouplist[cellfind]['bg']="green";
        Topsidecellgrouplist[colfind]['bg']="green";
        
        rowfind=1;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']="green";
        Southsidecellgrouplist[cellfind]['bg']="green";
        
        rowfind=2;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']="green";
        Southsidecellgrouplist[cellfind]['bg']="green";
        
        Northsideprogress['text']=str(round(((xpos-int(horizstartlength))/currTypecoachlength)*100))+"%";
        Southsideprogress['text']=str(round(((xpos-int(horizstartlength))/currTypecoachlength)*100))+"%";
        Topsideprogress['text']=str(round(((xpos-int(horizstartlength))/currTypecoachlength)*100))+"%";
        
    if mode == 3:
        #current painting area for before coach start or after coach length area
        rowfind=0;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']="pink";
        Southsidecellgrouplist[cellfind]['bg']="pink";
        Topsidecellgrouplist[colfind]['bg']="pink";
        
        rowfind=1;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']="pink";
        Southsidecellgrouplist[cellfind]['bg']="pink";
        
        rowfind=2;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']="pink";
        Southsidecellgrouplist[cellfind]['bg']="pink";
               
        if xpos < int(horizstartlength) :
            Northsideprogress['text']="0%";
            Southsideprogress['text']="0%";
            Topsideprogress['text']="0%";
            
        if xpos > (int(currTypecoachlength)+int(horizstartlength)) :
            Northsideprogress['text']="100%";
            Southsideprogress['text']="100%";
            Topsideprogress['text']="100%";
     
    if mode == 4:
        #before coach start or after coach length area after passing through
        defcolor = '#F0F0F0'
        rowfind=0;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']=defcolor;
        Southsidecellgrouplist[cellfind]['bg']=defcolor;
        Topsidecellgrouplist[colfind]['bg']=defcolor;
        
        rowfind=1;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']=defcolor;
        Southsidecellgrouplist[cellfind]['bg']=defcolor;
        
        rowfind=2;
        colfind=round(xpos/int(widthresolution));
        cellfind=rowfind*noofcolsrequired+colfind;
        Northsidecellgrouplist[cellfind]['bg']=defcolor;
        Southsidecellgrouplist[cellfind]['bg']=defcolor;

def NSTnextcommand():
    global CurrentMode;
    global Currprocesscommstring;
    if CurrentMode == 1:
        CurrTypewindowstartposlist=Type1windowstartposlist
        CurrTypewindowlength=Type1windowlength
        CurrTypecoachlength=Type1coachlength
        CurrTypecoachwidth=Type1coachwidth
        CurrTypewindowheight=Type1windowheight;         #560
        CurrTypesidewallheight=Type1sidewallheight;     #3336
        CurrTypebaseheight=Type1baseheight;             #913
        CurrTypewindowbaseheight=Type1windowbaseheight; #553
        CurrTypetoppaintsouthsideclearance=Type1toppaintsouthsideclearance;
        CurrTypetoppaintnorthsideclearance=Type1toppaintnorthsideclearance;
        
    if CurrentMode == 2:
        CurrTypewindowstartposlist=Type2windowstartposlist
        CurrTypewindowlength=Type2windowlength
        CurrTypecoachlength=Type2coachlength
        CurrTypecoachwidth=Type2coachwidth
        CurrTypewindowheight=Type2windowheight;         
        CurrTypesidewallheight=Type2sidewallheight;     
        CurrTypebaseheight=Type2baseheight;             
        CurrTypewindowbaseheight=Type2windowbaseheight;
        CurrTypetoppaintsouthsideclearance=Type2toppaintsouthsideclearance;
        CurrTypetoppaintnorthsideclearance=Type2toppaintnorthsideclearance;
        
    if CurrentMode == 3:
        CurrTypewindowstartposlist=Type3windowstartposlist
        CurrTypewindowlength=Type3windowlength
        CurrTypecoachlength=Type3coachlength
        CurrTypecoachwidth=Type3coachwidth
        CurrTypewindowheight=Type3windowheight;         
        CurrTypesidewallheight=Type3sidewallheight;     
        CurrTypebaseheight=Type3baseheight;             
        CurrTypewindowbaseheight=Type3windowbaseheight;
        CurrTypetoppaintsouthsideclearance=Type3toppaintsouthsideclearance;
        CurrTypetoppaintnorthsideclearance=Type3toppaintnorthsideclearance;
        
    if CurrentMode == 4:
        CurrTypewindowstartposlist=Type4windowstartposlist
        CurrTypewindowlength=Type4windowlength
        CurrTypecoachlength=Type4coachlength
        CurrTypecoachwidth=Type4coachwidth
        CurrTypewindowheight=Type4windowheight;         
        CurrTypesidewallheight=Type4sidewallheight;     
        CurrTypebaseheight=Type4baseheight;             
        CurrTypewindowbaseheight=Type4windowbaseheight;
        CurrTypetoppaintsouthsideclearance=Type4toppaintsouthsideclearance;
        CurrTypetoppaintnorthsideclearance=Type4toppaintnorthsideclearance;
        
    if CurrentMode == 5:
        CurrTypewindowstartposlist=Type5windowstartposlist
        CurrTypewindowlength=Type5windowlength
        CurrTypecoachlength=Type5coachlength
        CurrTypecoachwidth=Type5coachwidth
        CurrTypewindowheight=Type5windowheight;         
        CurrTypesidewallheight=Type5sidewallheight;     
        CurrTypebaseheight=Type5baseheight;             
        CurrTypewindowbaseheight=Type5windowbaseheight; 
        CurrTypetoppaintsouthsideclearance=Type5toppaintsouthsideclearance;
        CurrTypetoppaintnorthsideclearance=Type5toppaintnorthsideclearance;
        
    if CurrentMode == 6:
        CurrTypewindowstartposlist=Type6windowstartposlist
        CurrTypewindowlength=Type6windowlength
        CurrTypecoachlength=Type6coachlength
        CurrTypecoachwidth=Type6coachwidth
        CurrTypewindowheight=Type6windowheight;         
        CurrTypesidewallheight=Type6sidewallheight;     
        CurrTypebaseheight=Type6baseheight;             
        CurrTypewindowbaseheight=Type6windowbaseheight;
        CurrTypetoppaintsouthsideclearance=Type6toppaintsouthsideclearance;
        CurrTypetoppaintnorthsideclearance=Type6toppaintnorthsideclearance;
        
    if CurrentMode == 7:
        CurrTypewindowstartposlist=Type7windowstartposlist
        CurrTypewindowlength=Type7windowlength
        CurrTypecoachlength=Type7coachlength
        CurrTypecoachwidth=Type7coachwidth
        CurrTypewindowheight=Type7windowheight;         
        CurrTypesidewallheight=Type7sidewallheight;     
        CurrTypebaseheight=Type7baseheight;             
        CurrTypewindowbaseheight=Type7windowbaseheight;
        CurrTypetoppaintsouthsideclearance=Type7toppaintsouthsideclearance;
        CurrTypetoppaintnorthsideclearance=Type7toppaintnorthsideclearance;
        
    if CurrentMode == 8:
        CurrTypewindowstartposlist=Type8windowstartposlist
        CurrTypewindowlength=Type8windowlength
        CurrTypecoachlength=Type8coachlength
        CurrTypecoachwidth=Type8coachwidth
        CurrTypewindowheight=Type8windowheight;         
        CurrTypesidewallheight=Type8sidewallheight;     
        CurrTypebaseheight=Type8baseheight;             
        CurrTypewindowbaseheight=Type8windowbaseheight;
        CurrTypetoppaintsouthsideclearance=Type8toppaintsouthsideclearance;
        CurrTypetoppaintnorthsideclearance=Type8toppaintnorthsideclearance;
    
    Commandstring="";
    Colsforcomplete=round(int(CurrTypecoachlength)/int(widthresolution));
    global Pausemode;
    
    global NSTXpos
    global prevXpos
    
    Xpos = NSTXpos
    global Currwindowpos
    global crossingwindow
    
    global Yaxistravellength
    global Currprocess
    global Yaxisbottomclearance
    global Topaxistravellength
    
    startpaintpos=1;
    #Currwindowpos=0
    #crossingwindow=0
    
    if int(CurrTypebaseheight) <= int(Yaxisbottomclearance) :
        startpaintpos=1;
    else :
        startpaintpos=int(CurrTypebaseheight)-int(Yaxisbottomclearance)
    
    if int(CurrTypesidewallheight) >= (int(Yaxistravellength)+int(Yaxisbottomclearance)) :
        CurrTypesidewallheight=int(Yaxistravellength)+int(Yaxisbottomclearance)-1;
    
    if Xpos <= (CurrTypecoachlength+int(horizstartlength)) and Xpos >= int(horizstartlength) and Pausemode == 0:
        #inside the portion where current coach is positioned
            
            if (Xpos-int(widthresolution)) == prevXpos:
                NSTcellcolor(prevXpos,4,CurrTypecoachlength);
        
            if Currwindowpos < len(CurrTypewindowstartposlist):
            #not completed all windows
                if (Xpos-int(horizstartlength)) >= CurrTypewindowstartposlist[Currwindowpos]:
                    if (Xpos-int(horizstartlength)) <= CurrTypewindowstartposlist[Currwindowpos]+CurrTypewindowlength :
                        if crossingwindow == 0:
                            crossingwindow = 1
                            #encountering window
                        Commandstring=""+str(startpaintpos)+"#"+str(int(CurrTypebaseheight)+int(CurrTypewindowbaseheight)-int(Yaxisbottomclearance))+"#"+str(int(CurrTypebaseheight)+int(CurrTypewindowbaseheight)+int(CurrTypewindowheight)-int(Yaxisbottomclearance))+"#"+str(int(CurrTypesidewallheight)-int(Yaxisbottomclearance));
                        #print(str(Xpos)+": win comd: "+Commandstring);
                        #print("Printing inside before : "+Currprocess)
                        Currprocess="BatchJobPaint";
                        NSTcellcolor(Xpos, 1,CurrTypecoachlength); # highlighting the current window area
                        Currprocesscommstring="12*"+str(Yaxisspeed)+"*"+str(Yaxistravellength)+"*"+str(Topaxistravellength)+"*"+str(CurrTypetoppaintsouthsideclearance)+"#"+str(int(Topaxistravellength)-int(CurrTypetoppaintnorthsideclearance))+"*"+Commandstring;
                        sendsignal(Currprocesscommstring);
                        
                    else:
                        if crossingwindow == 1:
                            crossingwindow = 0
                            Currwindowpos = Currwindowpos + 1
                            #completed passing window
                        Commandstring=""+str(startpaintpos)+"#"+str(int(CurrTypesidewallheight)-int(Yaxisbottomclearance));
                        #print(str(Xpos)+": wall cross wind comd: "+Commandstring);
                        #print("Printing inside before : "+Currprocess)
                        Currprocess="BatchJobPaint";
                        NSTcellcolor(Xpos, 2,CurrTypecoachlength); # highlighting the current wall area
                        Currprocesscommstring="12*"+str(Yaxisspeed)+"*"+str(Yaxistravellength)+"*"+str(Topaxistravellength)+"*"+str(CurrTypetoppaintsouthsideclearance)+"#"+str(int(Topaxistravellength)-int(CurrTypetoppaintnorthsideclearance))+"*"+Commandstring;
                        sendsignal(Currprocesscommstring);
                else:
                    Commandstring=""+str(startpaintpos)+"#"+str(int(CurrTypesidewallheight)-int(Yaxisbottomclearance));
                    #print(str(Xpos)+": wall comd: "+Commandstring);
                    #print("Printing inside before : "+Currprocess)
                    Currprocess="BatchJobPaint";
                    NSTcellcolor(Xpos, 2,CurrTypecoachlength); # highlighting the current wall area
                    Currprocesscommstring="12*"+str(Yaxisspeed)+"*"+str(Yaxistravellength)+"*"+str(Topaxistravellength)+"*"+str(CurrTypetoppaintsouthsideclearance)+"#"+str(int(Topaxistravellength)-int(CurrTypetoppaintnorthsideclearance))+"*"+Commandstring;
                    sendsignal(Currprocesscommstring);
                    #not encountering window, normal wall
            else:
                    Commandstring=""+str(startpaintpos)+"#"+str(int(CurrTypesidewallheight)-int(Yaxisbottomclearance));
                    #print(str(Xpos)+": wall allwindcomp comd: "+Commandstring);
                    #print("Printing inside before : "+Currprocess)
                    Currprocess="BatchJobPaint";
                    NSTcellcolor(Xpos, 2,CurrTypecoachlength); # highlighting the current wall area
                    Currprocesscommstring="12*"+str(Yaxisspeed)+"*"+str(Yaxistravellength)+"*"+str(Topaxistravellength)+"*"+str(CurrTypetoppaintsouthsideclearance)+"#"+str(int(Topaxistravellength)-int(CurrTypetoppaintnorthsideclearance))+"*"+Commandstring;
                    sendsignal(Currprocesscommstring);
                    #completed all windows only wall remaining
            NSTXpos=NSTXpos+int(widthresolution);
    elif Pausemode == 0 and Xpos <= (CurrTypecoachlength+int(horizstartlength)):
        Currprocess="BatchJobInchStart";
        NSTcellcolor(Xpos, 3,CurrTypecoachlength); # highlighting current painting area before coach start or after coach end
        #print(str(Xpos)+": portion before coach start or after coach end")
        Currprocesscommstring="5*"+str(Xaxisspeed)+"*"+str(int(widthresolution)+int(horizmovposoffset));
        sendsignal(Currprocesscommstring);
        #in the portion before coach start or after coach end

        if(prevXpos == -1) :
            print("starting only")
        else :
            NSTcellcolor(prevXpos,4,CurrTypecoachlength);
            
        prevXpos=Xpos;
        
        NSTXpos=NSTXpos+int(widthresolution);
    
    if Xpos > (CurrTypecoachlength+int(horizstartlength)):
        Currprocess="Resetting";
        #print("process complete. Resetting in 10secs");
        Statusbutton['text']="Resetting in 10 secs"
        time.sleep(10);
        sendsignal("2*"+str(Xaxisspeed)+"*"+str(Yaxisspeed))
        Pausemode=0;
        CurrentMode=0;
        
def clearpoints():
    global noofcolsrequired;
    global CurrentMode;
    CurrentMode=0;
    for j in range(noofcolsrequired):
            NSTcellcolor(j*widthresolution,4,0);
    
    Northsideprogress['text']="Progress - %";
    Southsideprogress['text']="Progress - %";
    Topsideprogress['text']="Progress - %"; 
    
def plotpoints():
    #print('herall')
    global CurrentMode
    global Xpos
    
    global availablelength
    global widthresolution
    global eachcolwidth
    global maingroupwidth
    global noofcolsrequired
    
    noofcolsrequired=round(int(availablelength)/int(widthresolution));
    eachcolwidth=round(int(maingroupwidth)/int(noofcolsrequired));
    
    #print(CurrentMode)
    global horizstartlength
    global Northsidecellgrouplist;
    global Southsidecellgrouplist;
    global Topsidecellgrouplist;
    global Eastsidecellgrouplist;
    global Westsidecellgrouplist;
    
    Northsidecellgrouplist = list()
    Southsidecellgrouplist = list()
    Topsidecellgrouplist = list()
    Eastsidecellgrouplist = list()
    Westsidecellgrouplist = list()
    #Type1windowstartposlist=[2530]
    #Type1windowlength=610
    #Type1coachlength=21337

    #Type1windowstartposlist=[2530]
    #Type1windowlength=610
    #Type1coachlength=21337
    if CurrentMode == 1:
        #print('selecting current mode 1');
        CurrTypewindowstartposlist=Type1windowstartposlist
        CurrTypewindowlength=Type1windowlength
        CurrTypecoachlength=Type1coachlength
        CurrTypecoachwidth=Type1coachwidth
        
    if CurrentMode == 2:
        #print('selecting current mode 2');
        CurrTypewindowstartposlist=Type2windowstartposlist
        CurrTypewindowlength=Type2windowlength
        CurrTypecoachlength=Type2coachlength
        CurrTypecoachwidth=Type2coachwidth
        
    if CurrentMode == 3:
        #print('selecting current mode 3');
        CurrTypewindowstartposlist=Type3windowstartposlist
        CurrTypewindowlength=Type3windowlength
        CurrTypecoachlength=Type3coachlength
        CurrTypecoachwidth=Type3coachwidth
        
    if CurrentMode == 4:
        #print('selecting current mode 4');
        CurrTypewindowstartposlist=Type4windowstartposlist
        CurrTypewindowlength=Type4windowlength
        CurrTypecoachlength=Type4coachlength
        CurrTypecoachwidth=Type4coachwidth
        
    if CurrentMode == 5:
        #print('selecting current mode 4');
        CurrTypewindowstartposlist=Type5windowstartposlist
        CurrTypewindowlength=Type5windowlength
        CurrTypecoachlength=Type5coachlength
        CurrTypecoachwidth=Type5coachwidth
        
    if CurrentMode == 6:
        #print('selecting current mode 4');
        CurrTypewindowstartposlist=Type6windowstartposlist
        CurrTypewindowlength=Type6windowlength
        CurrTypecoachlength=Type6coachlength
        CurrTypecoachwidth=Type6coachwidth
        
    if CurrentMode == 7:
        #print('selecting current mode 4');
        CurrTypewindowstartposlist=Type7windowstartposlist
        CurrTypewindowlength=Type7windowlength
        CurrTypecoachlength=Type7coachlength
        CurrTypecoachwidth=Type7coachwidth
        
    if CurrentMode == 8:
        #print('selecting current mode 4');
        CurrTypewindowstartposlist=Type8windowstartposlist
        CurrTypewindowlength=Type8windowlength
        CurrTypecoachlength=Type8coachlength
        CurrTypecoachwidth=Type8coachwidth

    #North side profile
    for i in range(Northsidecellgrouplistnoofrows):
        global Xpos;
        Xpos = 0
        Currwindowpos=0
        crossingwindow=0
        for j in range(noofcolsrequired):
                Xpos= j* int(widthresolution)
                #print("At Plotpoints start")
                #print("j val:"+str(j))
                #print("Width res:"+str(widthresolution))
                #print("Width res:"+str(widthresolution))
                #print("Xpos:"+str(Xpos))
                #print("CurrTypecoachlength:"+str(CurrTypecoachlength))
                #print("horizstartlength:"+str(horizstartlength))
                if int(Xpos) < (int(CurrTypecoachlength)+int(horizstartlength)) and int(Xpos) > int(horizstartlength):
                    if i == 2 :
                        Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=eachcolwidth, height=57, bd=1, bg="blue"))
                        Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)
                    if i == 1 :
                        if Currwindowpos < len(CurrTypewindowstartposlist) :
                            if (Xpos-int(horizstartlength)) >= CurrTypewindowstartposlist[Currwindowpos] :
                                if (Xpos-int(horizstartlength)) <= CurrTypewindowstartposlist[Currwindowpos]+CurrTypewindowlength :
                                    if crossingwindow == 0:
                                        crossingwindow = 1
                                    Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=eachcolwidth, height=37, bd=1, bg="white"))
                                    Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)
                                else:
                                    if crossingwindow == 1:
                                        crossingwindow = 0
                                        Currwindowpos = Currwindowpos + 1
                                    Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=eachcolwidth, height=37, bd=1, bg="blue"))
                                    Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)
                            else:
                                Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=eachcolwidth, height=37, bd=1, bg="blue"))
                                Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)
                        else:
                                Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=eachcolwidth, height=37, bd=1, bg="blue"))
                                Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)
                    if i == 0 :
                        Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=eachcolwidth, height=77, bd=1, bg="blue"))
                        Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)
                else :
                    if i == 2 :
                        Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=eachcolwidth, height=57, bd=1))
                        Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)
                    if i == 1 :
                        Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=eachcolwidth, height=37, bd=1))
                        Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)
                    if i == 0 :
                        Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=eachcolwidth, height=77, bd=1))
                        Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)
                        
    for i in range(Southsidecellgrouplistnoofrows):
        Xpos = 0
        Currwindowpos=0
        crossingwindow=0
        for j in range(noofcolsrequired):
                Xpos= j* int(widthresolution)
                #print(Xpos)
                if Xpos < (CurrTypecoachlength+int(horizstartlength)) and Xpos > int(horizstartlength):
                    if i == 2 :
                        Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=eachcolwidth, height=57, bd=1, bg="blue"))
                        Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)
                    if i == 1 :
                        if Currwindowpos < len(CurrTypewindowstartposlist) :
                            if (Xpos-int(horizstartlength)) >= CurrTypewindowstartposlist[Currwindowpos] :
                                if (Xpos-int(horizstartlength)) <= CurrTypewindowstartposlist[Currwindowpos]+CurrTypewindowlength :
                                    if crossingwindow == 0:
                                        crossingwindow = 1
                                    Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=eachcolwidth, height=37, bd=1, bg="white"))
                                    Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)
                                else:
                                    if crossingwindow == 1:
                                        crossingwindow = 0
                                        Currwindowpos = Currwindowpos + 1
                                    Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=eachcolwidth, height=37, bd=1, bg="blue"))
                                    Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)
                            else:
                                Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=eachcolwidth, height=37, bd=1, bg="blue"))
                                Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)
                        else:
                                Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=eachcolwidth, height=37, bd=1, bg="blue"))
                                Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)
                    if i == 0 :
                        Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=eachcolwidth, height=77, bd=1, bg="blue"))
                        Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)
                else :
                    if i == 2 :
                        Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=eachcolwidth, height=57, bd=1))
                        Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)
                    if i == 1 :
                        Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=eachcolwidth, height=37, bd=1))
                        Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)
                    if i == 0 :
                        Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=eachcolwidth, height=77, bd=1))
                        Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)
                        
    for i in range(noofcolsrequired):
        Xpos= i* int(widthresolution)
                #print(Xpos)
        if Xpos < (CurrTypecoachlength+int(horizstartlength)) and Xpos > int(horizstartlength):
            Topsidecellgrouplist.append(tk.LabelFrame(TopsidecoachliveStatus2, width=eachcolwidth, height=160, bd=1, bg="yellow"))
            Topsidecellgrouplist[-1].grid(row=0,column=i)
        else :
            Topsidecellgrouplist.append(tk.LabelFrame(TopsidecoachliveStatus2, width=eachcolwidth, height=160, bd=1))
            Topsidecellgrouplist[-1].grid(row=0,column=i)
            
    Statusbutton['text']="Ready to Start"
    enablestartbuttongroup()

                    
def updateXaxisspeed(value):
    global changeparcheck
    changeparcheck=1
    global Xaxisspeed
    Xaxisspeed=value
    #print('X axis speed updated')
    #print(Xaxisspeed)
    
def updateYaxisspeed(value):
    global changeparcheck
    changeparcheck=1
    global Yaxisspeed
    Yaxisspeed=value
    #print('Y axis speed updated')
    #print(Yaxisspeed)
    
def Engageallcarraigeselect():
    #print('here')
    #print(Engageallcarraigevar.get())
    if Engageallcarraigevar.get() == 1:
        Engagecarraige1["state"] = DISABLED
        Engagecarraige2["state"] = DISABLED
        Engagecarraige3["state"] = DISABLED
        Engagecarraige4["state"] = DISABLED
        Engagecarraige5["state"] = DISABLED
        Engagecarraige1var.set(1)
        Engagecarraige2var.set(1)
        Engagecarraige3var.set(1)
        Engagecarraige4var.set(1)
        Engagecarraige5var.set(1)
        sendsignal("9*6*1")
    else:
        Engagecarraige1["state"] = NORMAL
        Engagecarraige2["state"] = NORMAL
        Engagecarraige3["state"] = NORMAL
        Engagecarraige4["state"] = NORMAL
        Engagecarraige5["state"] = NORMAL
        Engagecarraige1var.set(0)
        Engagecarraige2var.set(0)
        Engagecarraige3var.set(0)
        Engagecarraige4var.set(0)
        Engagecarraige5var.set(0)
        sendsignal("9*6*0")
        
def Engagecarraige1select():
    if Engagecarraige1var.get() == 1:
        sendsignal("9*1*1")
    else:
        sendsignal("9*1*0")
        
def Engagecarraige2select():
    if Engagecarraige2var.get() == 1:
        sendsignal("9*2*1")
    else:
        sendsignal("9*2*0")
        
def Engagecarraige3select():
    if Engagecarraige3var.get() == 1:
        sendsignal("9*3*1")
    else:
        sendsignal("9*3*0")
        
def Engagecarraige4select():
    if Engagecarraige4var.get() == 1:
        sendsignal("9*4*1")
    else:
        sendsignal("9*4*0")
        
def Engagecarraige5select():
    if Engagecarraige5var.get() == 1:
        sendsignal("9*5*1")
    else:
        sendsignal("9*5*0")
        
Inchenablestring="00000";
Inchenablenorth="0";
Inchenablesouth="0";
Inchenabletop="0";
Inchenableeast="0";
Inchenablewest="0";

def setinchenablstring():
    global Inchenablestring;
    global Inchenablenorth;
    global Inchenablesouth;
    global Inchenabletop;
    global Inchenableeast;
    global Inchenablewest;
    
    Inchenablestring=str(Inchenableeast)+str(Inchenablewest)+str(Inchenablenorth)+str(Inchenablesouth)+str(Inchenabletop);
    print("updated Inchenablestring: "+Inchenablestring);

def Inchallcarraigeselect():
    #print('here')
    #print(Engageallcarraigevar.get())
    global Inchenablenorth;
    global Inchenablesouth;
    global Inchenabletop;
    global Inchenableeast;
    global Inchenablewest;
    
    if Inchallcarraigevar.get() == 1:
        Inchcarraige1["state"] = DISABLED
        Inchcarraige2["state"] = DISABLED
        Inchcarraige3["state"] = DISABLED
        Inchcarraige4["state"] = DISABLED
        Inchcarraige5["state"] = DISABLED
        sendsignal("8*6*1")
        Inchcarraige1var.set(1)
        Inchcarraige2var.set(1)
        Inchcarraige3var.set(1)
        Inchcarraige4var.set(1)
        Inchcarraige5var.set(1)
        Inchenablenorth="1";
        Inchenablesouth="1";
        Inchenabletop="1";
        Inchenableeast="1";
        Inchenablewest="1";
        setinchenablstring();
    else:
        Inchcarraige1["state"] = NORMAL
        Inchcarraige2["state"] = NORMAL
        Inchcarraige3["state"] = NORMAL
        Inchcarraige4["state"] = NORMAL
        Inchcarraige5["state"] = NORMAL
        sendsignal("8*6*0")
        Inchcarraige1var.set(0)
        Inchcarraige2var.set(0)
        Inchcarraige3var.set(0)
        Inchcarraige4var.set(0)
        Inchcarraige5var.set(0)
        Inchenablenorth="0";
        Inchenablesouth="0";
        Inchenabletop="0";
        Inchenableeast="0";
        Inchenablewest="0";
        setinchenablstring();
        
def Inchcarraige1select():
    global Inchenableeast;
    if Inchcarraige1var.get() == 1:
        sendsignal("8*1*1")
        Inchenableeast="1";
        setinchenablstring();
    else:
        sendsignal("8*1*0")
        Inchenableeast="0";
        setinchenablstring();
        
def Inchcarraige2select():
    global Inchenablewest;
    if Inchcarraige2var.get() == 1:
        sendsignal("8*2*1")
        Inchenablewest="1";
        setinchenablstring();
    else:
        sendsignal("8*2*0")
        Inchenablewest="0";
        setinchenablstring();
        
def Inchcarraige3select():
    global Inchenablenorth;
    if Inchcarraige3var.get() == 1:
        sendsignal("8*3*1")
        Inchenablenorth=1;
        setinchenablstring();
    else:
        sendsignal("8*3*0")
        Inchenablenorth=0;
        setinchenablstring();
        
def Inchcarraige4select():
    global Inchenablesouth;
    if Inchcarraige4var.get() == 1:
        sendsignal("8*4*1")
        Inchenablesouth=1;
        setinchenablstring();
    else:
        sendsignal("8*4*0")
        Inchenablesouth=0;
        setinchenablstring();
        
def Inchcarraige5select():
    global Inchenabletop;
    if Inchcarraige5var.get() == 1:
        sendsignal("8*5*1")
        Inchenabletop=1;
        setinchenablstring();
    else:
        sendsignal("8*5*0")
        Inchenabletop=0;
        setinchenablstring();

        
def disptime():
    global datetimestring
    datetimestring = strftime('%d/%m/%y %H:%M:%S %p') 
    Datetimebutton.config(text = datetimestring) 
    Datetimebutton.after(1000, disptime)

def exitbutton():
    print("pressed close button")
    try:
       ser.flushInput()
       ser.flushOutput()
       ser.close()
       GPIO.output(GPIO21, False);
    except Exception as e:
        print("Serial close exception")
        logger.error(datetimestring + " :: " + "Serial close exception")
    try:
        thread.exit()
        print("Closing serial thread")
    except Exception as e:
        print("Closing serial thread exception")
        logger.error(datetimestring + " :: " + "Closing serial thread exception")
    try:
        #master.destroy()
        #print("Closing program")
        logger.error(datetimestring + " :: " + "Closing program")
        sys.exit()
#       print("Closing program after")
    except Exception as e:
        #print("Closing program exception")
        logger.error(datetimestring + " :: " + "Closing program exception")
        
def MCresetbutton():
    print('mc reset button pressed')
    # serialconnect()
    try:
        sendsignal("1*0*0")
    except Exception as e:
        print('send signal exception')
        print(e)

def snapshotbutton():
    try:
        os.system(screen_shot_cmd)
        #print("screen shot taken")
        logger.warning(datetimestring + " :: " + "screen shot taken")
    except Exception as e:
        #print("Screenshot exception")
        logger.error(datetimestring + " :: " + "Screenshot exception")
        return None
    
def addlsettingsbutton():
    addlsettingsWindow = Toplevel(master) 
    addlsettingsWindow.title("Additional Settings")
    addlsettingsWindowWidth=430
    addlsettingsWindowHeight=310
    addlsettingsWindow.geometry('{}x{}+{}+{}'.format(addlsettingsWindowWidth, addlsettingsWindowHeight, int(master.winfo_screenwidth()/2)-int(addlsettingsWindowWidth/2), int(master.winfo_screenheight()/2)-int(addlsettingsWindowHeight/2)))
    global CurrentMode
    global whetherplotpointscalled
    
    def updatesidewallheight(value):
        global Type1sidewallheight;
        global Type2sidewallheight;
        global Type3sidewallheight;
        global Type4sidewallheight;
        global Type5sidewallheight;
        global Type6sidewallheight;
        global Type7sidewallheight;
        global Type8sidewallheight;
        #print(value);
        if CurrentMode == 1:
            Type1sidewallheight=value;
        elif CurrentMode == 2:
            Type2sidewallheight=value;
        elif CurrentMode == 3:
            Type3sidewallheight=value;
        elif CurrentMode == 4:
            Type4sidewallheight=value;
        elif CurrentMode == 5:
            Type5sidewallheight=value;
        elif CurrentMode == 6:
            Type6sidewallheight=value;
        elif CurrentMode == 7:
            Type7sidewallheight=value;
        elif CurrentMode == 8:
            Type8sidewallheight=value;
        else:
            Type1sidewallheight=value;
            
    def updatebaseheight(value):
        global Type1baseheight;
        global Type2baseheight;
        global Type3baseheight;
        global Type4baseheight;
        global Type5baseheight;
        global Type6baseheight;
        global Type7baseheight;
        global Type8baseheight;
        #print(value);
        if CurrentMode == 1:
            Type1baseheight=value;
            updatesidewallheight(int(Type1baseheight)+int(Type1sidewalllength));
            sidewallheightslider.set(int(Type1baseheight)+int(Type1sidewalllength));
        elif CurrentMode == 2:
            Type2baseheight=value;
            updatesidewallheight(int(Type2baseheight)+int(Type2sidewalllength));
            sidewallheightslider.set(int(Type2baseheight)+int(Type2sidewalllength));
        elif CurrentMode == 3:
            Type3baseheight=value;
            updatesidewallheight(int(Type3baseheight)+int(Type3sidewalllength));
            sidewallheightslider.set(int(Type3baseheight)+int(Type3sidewalllength));
        elif CurrentMode == 4:
            Type4baseheight=value;
            updatesidewallheight(int(Type4baseheight)+int(Type4sidewalllength));
            sidewallheightslider.set(int(Type4baseheight)+int(Type4sidewalllength));
        elif CurrentMode == 5:
            Type5baseheight=value;
            updatesidewallheight(int(Type5baseheight)+int(Type5sidewalllength));
            sidewallheightslider.set(int(Type5baseheight)+int(Type5sidewalllength));
        elif CurrentMode == 6:
            Type6baseheight=value;
            updatesidewallheight(int(Type6baseheight)+int(Type6sidewalllength));
            sidewallheightslider.set(int(Type6baseheight)+int(Type6sidewalllength));
        elif CurrentMode == 7:
            Type7baseheight=value;
            updatesidewallheight(int(Type7baseheight)+int(Type7sidewalllength));
            sidewallheightslider.set(int(Type7baseheight)+int(Type7sidewalllength));
        elif CurrentMode == 8:
            Type8baseheight=value;
            updatesidewallheight(int(Type8baseheight)+int(Type8sidewalllength));
            sidewallheightslider.set(int(Type8baseheight)+int(Type8sidewalllength));
        else:
            Type1baseheight=value;
            
    def updateStartdistance(value):
        global horizstartlength;
        #print(value)
        horizstartlength=value;
        
    def updateVerticalclearance(value):
        global Yaxisbottomclearance;
        #print(value)
        Yaxisbottomclearance=value;
        #baseheightslider[from_]= Yaxisbottomclearance;
        
    def updateToppaintsouthsideclearance(value):
        global Type1toppaintsouthsideclearance;
        global Type2toppaintsouthsideclearance;
        global Type3toppaintsouthsideclearance;
        global Type4toppaintsouthsideclearance;
        global Type5toppaintsouthsideclearance;
        global Type6toppaintsouthsideclearance;
        global Type7toppaintsouthsideclearance;
        global Type8toppaintsouthsideclearance;
        
        if CurrentMode == 1:
            Type1toppaintsouthsideclearance=value;
        elif CurrentMode == 2:
            Type2toppaintsouthsideclearance=value;
        elif CurrentMode == 3:
            Type3toppaintsouthsideclearance=value;
        elif CurrentMode == 4:
            Type4toppaintsouthsideclearance=value;
        elif CurrentMode == 5:
            Type5toppaintsouthsideclearance=value;
        elif CurrentMode == 6:
            Type6toppaintsouthsideclearance=value;
        elif CurrentMode == 7:
            Type7toppaintsouthsideclearance=value;
        elif CurrentMode == 8:
            Type8toppaintsouthsideclearance=value;
        else:
            Type1toppaintsouthsideclearance=value;
            
    def updateToppaintnorthsideclearance(value):
        global Type1toppaintnorthsideclearance;
        global Type2toppaintnorthsideclearance;
        global Type3toppaintnorthsideclearance;
        global Type4toppaintnorthsideclearance;
        global Type5toppaintnorthsideclearance;
        global Type6toppaintnorthsideclearance;
        global Type7toppaintnorthsideclearance;
        global Type8toppaintnorthsideclearance;
        
        if CurrentMode == 1:
            Type1toppaintnorthsideclearance=value;
        elif CurrentMode == 2:
            Type2toppaintnorthsideclearance=value;
        elif CurrentMode == 3:
            Type3toppaintnorthsideclearance=value;
        elif CurrentMode == 4:
            Type4toppaintnorthsideclearance=value;
        elif CurrentMode == 5:
            Type5toppaintnorthsideclearance=value;
        elif CurrentMode == 6:
            Type6toppaintnorthsideclearance=value;
        elif CurrentMode == 7:
            Type7toppaintnorthsideclearance=value;
        elif CurrentMode == 8:
            Type8toppaintnorthsideclearance=value;
        else:
            Type1toppaintnorthsideclearance=value;
        
    def updatewidthresolution(value):
        global widthresolution;
        #print(value)
        widthresolution=value;
        
    def updateYaxistravellength(value):
        global Yaxistravellength;
        #print(value);
        Yaxistravellength=value;
        
    def updateTopaxistravellength(value):
        global Topaxistravellength;
        #print(value);
        Topaxistravellength=value;

    def proceedbuttonFunc():
        plotpoints();
        addlsettingsWindow.destroy()
        
    def cancelbuttonFunc():
        CurrentMode=0;
        enableallitems();
        enableresetbuttongroup();
        addlsettingsWindow.destroy()
    
    
    Currmodelabel = tk.Label(addlsettingsWindow, text="CurrentMode", font=('Helvetica', 11, 'bold'), width=20, height=2)
    Suggestionlabel = tk.Label(addlsettingsWindow, text="Suggested pressure & Nozzle", font=('Helvetica', 11, 'normal'), width=20, height=2)
    if CurrentMode == 1:
        Currmodelabel['text']="ICF Roof"
        Currmodelabel.grid(row=0, column=0, sticky=W)
        Suggestionlabel['text']="Nozzle:621&Pressure:12psi"
        Suggestionlabel.grid(row=0, column=1, sticky=W)
    elif CurrentMode == 2:
        Currmodelabel['text']="ICF Non AC SL FC"
        Currmodelabel.grid(row=0, column=0, sticky=W)
        Suggestionlabel['text']="Nozzle:519&Pressure:15psi"
        Suggestionlabel.grid(row=0, column=1, sticky=W)
    elif CurrentMode == 3:
        Currmodelabel['text']="ICF Non AC SL SC"
        Currmodelabel.grid(row=0, column=0, sticky=W)
        Suggestionlabel['text']="Nozzle:621&Pressure:12psi"
        Suggestionlabel.grid(row=0, column=1, sticky=W)
    elif CurrentMode == 4:
        Currmodelabel['text']="ICF AC SL FC"
        Currmodelabel.grid(row=0, column=0, sticky=W)
        Suggestionlabel['text']="Nozzle:519&Pressure:15psi"
        Suggestionlabel.grid(row=0, column=1, sticky=W)
    elif CurrentMode == 5:
        Currmodelabel['text']="LHB Surfacer"
        Currmodelabel.grid(row=0, column=0, sticky=W)
        Suggestionlabel['text']="Nozzle:621&Pressure:12psi"
        Suggestionlabel.grid(row=0, column=1, sticky=W)
    elif CurrentMode == 6:
        Currmodelabel['text']="LHB Gray SC"
        Currmodelabel.grid(row=0, column=0, sticky=W)
        Suggestionlabel['text']="Nozzle:519&Pressure:15psi"
        Suggestionlabel.grid(row=0, column=1, sticky=W)
    elif CurrentMode == 7:
        Currmodelabel['text']="LHB Non AC Red SC"
        Currmodelabel.grid(row=0, column=0, sticky=W)
        Suggestionlabel['text']="Nozzle:621&Pressure:12psi"
        Suggestionlabel.grid(row=0, column=1, sticky=W)
    elif CurrentMode == 8:
        Currmodelabel['text']="LHB AC Red SC"
        Currmodelabel.grid(row=0, column=0, sticky=W)
        Suggestionlabel['text']="Nozzle:519&Pressure:15psi"
        Suggestionlabel.grid(row=0, column=1, sticky=W)
    else:
        Currmodelabel['text']="Colour Scheme: Not Set"
        Currmodelabel.grid(row=0, column=0, sticky=W)
        Suggestionlabel['text']=""
        Suggestionlabel.grid(row=0, column=1, sticky=W)
    
    Horizdistancelider= tk.Scale(addlsettingsWindow, from_=200, to=5000, label="Set start distance:", resolution=100, width =18, length = 200, orient=HORIZONTAL, command=updateStartdistance, font=('Helvetica', 11, 'normal'))
    Horizdistancelider.set(horizstartlength)
    Horizdistancelider.grid(row=1, column=0)
    
    Verticalclearanceslider= tk.Scale(addlsettingsWindow, from_=900, to=1200, label="Set gun vertical clearance:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updateVerticalclearance, font=('Helvetica', 11, 'normal'))
    Verticalclearanceslider.set(Yaxisbottomclearance)
    Verticalclearanceslider.grid(row=1, column=1)
    
    Toppaintsouthsideclearanceslider= tk.Scale(addlsettingsWindow, from_=100, to=1000, resolution=50, label="Set top spray clearance south:", width =18, length = 200, orient=HORIZONTAL, command=updateToppaintsouthsideclearance, font=('Helvetica', 11, 'normal'))
    Toppaintsouthsideclearanceslider.grid(row=2, column=0)
    
    Toppaintnorthsideclearanceslider= tk.Scale(addlsettingsWindow, from_=100, to=1000, resolution=50, label="Set top spray clearance north:", width =18, length = 200, orient=HORIZONTAL, command=updateToppaintsouthsideclearance, font=('Helvetica', 11, 'normal'))
    Toppaintnorthsideclearanceslider.grid(row=2, column=1)
    
    if CurrentMode == 1:
        Toppaintsouthsideclearanceslider.set(Type1toppaintsouthsideclearance)
        Toppaintnorthsideclearanceslider.set(Type1toppaintnorthsideclearance)
    elif CurrentMode == 2:
        Toppaintsouthsideclearanceslider.set(Type2toppaintsouthsideclearance)
        Toppaintnorthsideclearanceslider.set(Type2toppaintnorthsideclearance)
    elif CurrentMode == 3:
        Toppaintsouthsideclearanceslider.set(Type3toppaintsouthsideclearance)
        Toppaintnorthsideclearanceslider.set(Type3toppaintnorthsideclearance)
    elif CurrentMode == 4:
        Toppaintsouthsideclearanceslider.set(Type4toppaintsouthsideclearance)
        Toppaintnorthsideclearanceslider.set(Type4toppaintnorthsideclearance)
    elif CurrentMode == 5:
        Toppaintsouthsideclearanceslider.set(Type5toppaintsouthsideclearance)
        Toppaintnorthsideclearanceslider.set(Type5toppaintnorthsideclearance)
    elif CurrentMode == 6:
        Toppaintsouthsideclearanceslider.set(Type6toppaintsouthsideclearance)
        Toppaintnorthsideclearanceslider.set(Type6toppaintnorthsideclearance)
    elif CurrentMode == 7:
        Toppaintsouthsideclearanceslider.set(Type7toppaintsouthsideclearance)
        Toppaintnorthsideclearanceslider.set(Type7toppaintnorthsideclearance)
    elif CurrentMode == 8:
        Toppaintsouthsideclearanceslider.set(Type8toppaintsouthsideclearance)
        Toppaintnorthsideclearanceslider.set(Type8toppaintnorthsideclearance)
    else:
        Toppaintsouthsideclearanceslider.set(200)
        Toppaintnorthsideclearanceslider.set(200)
    
    
    Yaxistravellengthslider= tk.Scale(addlsettingsWindow, from_=2000, to=3000, label="Set Y axis travel length:", resolution=50, width =18, length = 200, orient=HORIZONTAL, command=updateYaxistravellength, font=('Helvetica', 11, 'normal'))
    Yaxistravellengthslider.set(Yaxistravellength)
    Yaxistravellengthslider.grid(row=3, column=0)
    
    Topaxistravellengthslider= tk.Scale(addlsettingsWindow, from_=4000, to=6500, label="Set Top axis travel length:", resolution=50, width =18, length = 200, orient=HORIZONTAL, command=updateTopaxistravellength, font=('Helvetica', 11, 'normal'))
    Topaxistravellengthslider.set(Topaxistravellength)
    Topaxistravellengthslider.grid(row=3, column=1)
    
    if CurrentMode == 1:
        sidewallheightslider= tk.Scale(addlsettingsWindow, from_=int(Type1sidewallheight)-200, to=int(Type1sidewallheight)+200, label="Set side wall height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatesidewallheight, font=('Helvetica', 11, 'normal'))
        sidewallheightslider.set(Type1sidewallheight)
        sidewallheightslider["state"] = NORMAL
    elif CurrentMode == 2:
        sidewallheightslider= tk.Scale(addlsettingsWindow, from_=int(Type2sidewallheight)-200, to=int(Type2sidewallheight)+200, label="Set side wall height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatesidewallheight, font=('Helvetica', 11, 'normal'))
        sidewallheightslider.set(Type2sidewallheight)
        sidewallheightslider["state"] = NORMAL
    elif CurrentMode == 3:
        sidewallheightslider= tk.Scale(addlsettingsWindow, from_=Type3sidewallheight-200, to=Type3sidewallheight+200, label="Set side wall height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatesidewallheight, font=('Helvetica', 11, 'normal'))
        sidewallheightslider.set(Type3sidewallheight)
        sidewallheightslider["state"] = NORMAL
    elif CurrentMode == 4:
        sidewallheightslider= tk.Scale(addlsettingsWindow, from_=Type4sidewallheight-200, to=Type4sidewallheight+200, label="Set side wall height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatesidewallheight, font=('Helvetica', 11, 'normal'))
        sidewallheightslider.set(Type4sidewallheight)
        sidewallheightslider["state"] = NORMAL
    elif CurrentMode == 5:
        sidewallheightslider= tk.Scale(addlsettingsWindow, from_=Type5sidewallheight-200, to=Type5sidewallheight+200, label="Set side wall height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatesidewallheight, font=('Helvetica', 11, 'normal'))
        sidewallheightslider.set(Type5sidewallheight)
        sidewallheightslider["state"] = NORMAL
    elif CurrentMode == 6:
        sidewallheightslider= tk.Scale(addlsettingsWindow, from_=Type6sidewallheight-200, to=Type6sidewallheight+200, label="Set side wall height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatesidewallheight, font=('Helvetica', 11, 'normal'))
        sidewallheightslider.set(Type6sidewallheight)
        sidewallheightslider["state"] = NORMAL
    elif CurrentMode == 7:
        sidewallheightslider= tk.Scale(addlsettingsWindow, from_=Type7sidewallheight-200, to=Type7sidewallheight+200, label="Set side wall height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatesidewallheight, font=('Helvetica', 11, 'normal'))
        sidewallheightslider.set(Type7sidewallheight)
        sidewallheightslider["state"] = NORMAL
    elif CurrentMode == 8:
        sidewallheightslider= tk.Scale(addlsettingsWindow, from_=Type8sidewallheight-200, to=Type8sidewallheight+200, label="Set side wall height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatesidewallheight, font=('Helvetica', 11, 'normal'))
        sidewallheightslider.set(Type8sidewallheight)
        sidewallheightslider["state"] = NORMAL
    else:
        sidewallheightslider= tk.Scale(addlsettingsWindow, from_=Type2sidewallheight-200, to=Type2sidewallheight+200, label="Set side wall height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatesidewallheight, font=('Helvetica', 11, 'normal'))
        sidewallheightslider.set(0)
        sidewallheightslider["state"] = DISABLED
    if CurrentMode != 0:
        sidewallheightslider.grid(row=4, column=0)
        
    Horizontalfeedslider= tk.Scale(addlsettingsWindow, from_=100, to=1000, label="Set horizontal feed:", resolution=50, width =18, length = 200, orient=HORIZONTAL, command=updatewidthresolution, font=('Helvetica', 11, 'normal'))
    Horizontalfeedslider.set(widthresolution)
    
    if CurrentMode == 1:
        baseheightslider= tk.Scale(addlsettingsWindow, from_=int(Type1baseheight)-200, to=int(Type1baseheight)+200, label="Set side wall base height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatebaseheight, font=('Helvetica', 11, 'normal'))
        baseheightslider.set(Type1baseheight)
        baseheightslider["state"] = NORMAL
    elif CurrentMode == 2:
        baseheightslider= tk.Scale(addlsettingsWindow, from_=int(Type2baseheight)-200, to=int(Type2baseheight)+200, label="Set side wall base height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatebaseheight, font=('Helvetica', 11, 'normal'))
        baseheightslider.set(Type2baseheight)
        baseheightslider["state"] = NORMAL
    elif CurrentMode == 3:
        baseheightslider= tk.Scale(addlsettingsWindow, from_=Type3baseheight-200, to=Type3baseheight+200, label="Set side wall base height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatebaseheight, font=('Helvetica', 11, 'normal'))
        baseheightslider.set(Type3baseheight)
        baseheightslider["state"] = NORMAL
    elif CurrentMode == 4:
        baseheightslider= tk.Scale(addlsettingsWindow, from_=Type4baseheight-200, to=Type4baseheight+200, label="Set side wall base height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatebaseheight, font=('Helvetica', 11, 'normal'))
        baseheightslider.set(Type4baseheight)
        baseheightslider["state"] = NORMAL
    elif CurrentMode == 5:
        baseheightslider= tk.Scale(addlsettingsWindow, from_=Type5baseheight-200, to=Type5baseheight+200, label="Set side wall base height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatebaseheight, font=('Helvetica', 11, 'normal'))
        baseheightslider.set(Type5baseheight)
        baseheightslider["state"] = NORMAL
    elif CurrentMode == 6:
        baseheightslider= tk.Scale(addlsettingsWindow, from_=Type6baseheight-200, to=Type6baseheight+200, label="Set side wall base height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatebaseheight, font=('Helvetica', 11, 'normal'))
        baseheightslider.set(Type6baseheight)
        baseheightslider["state"] = NORMAL
    elif CurrentMode == 7:
        baseheightslider= tk.Scale(addlsettingsWindow, from_=Type7baseheight-200, to=Type7baseheight+200, label="Set side wall base height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatebaseheight, font=('Helvetica', 11, 'normal'))
        baseheightslider.set(Type7baseheight)
        baseheightslider["state"] = NORMAL
    elif CurrentMode == 8:
        baseheightslider= tk.Scale(addlsettingsWindow, from_=Type8baseheight-200, to=Type8baseheight+200, label="Set side wall base height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatebaseheight, font=('Helvetica', 11, 'normal'))
        baseheightslider.set(Type8baseheight)
        baseheightslider["state"] = NORMAL
    else:
        baseheightslider= tk.Scale(addlsettingsWindow, from_=Type8baseheight-200, to=Type8baseheight+200, label="Set side wall base height:", resolution=1, width =18, length = 200, orient=HORIZONTAL, command=updatebaseheight, font=('Helvetica', 11, 'normal'))
        baseheightslider.set(0)
        baseheightslider["state"] = DISABLED
    if CurrentMode != 0:
        baseheightslider.grid(row=4, column=1)
        Horizontalfeedslider.grid(row=5, column=1)
    else:
        addlsettingsWindow.geometry('{}x{}+{}+{}'.format(addlsettingsWindowWidth, 250, int(master.winfo_screenwidth()/2)-int(addlsettingsWindowWidth/2), int(master.winfo_screenheight()/2)-int(addlsettingsWindowHeight/2)))
        
    if whetherplotpointscalled == 1:
        whetherplotpointscalled=0;
        addlsettingsWindow.geometry('{}x{}+{}+{}'.format(addlsettingsWindowWidth, 410, int(master.winfo_screenwidth()/2)-int(addlsettingsWindowWidth/2), int(master.winfo_screenheight()/2)-int(addlsettingsWindowHeight/2)))
        Proceedbutton = tk.Button(addlsettingsWindow, text="Proceed to Start", justify=CENTER, command=proceedbuttonFunc, font=('Helvetica', 11, 'normal'))
        Proceedbutton['width']=18
        Proceedbutton.grid(row = 6, column = 0);
        
        Cancelbutton = tk.Button(addlsettingsWindow, text="Cancel", justify=CENTER, command=cancelbuttonFunc, font=('Helvetica', 11, 'normal'))
        Cancelbutton['width']=18
        Cancelbutton.grid(row = 6, column = 1);
    else:    
        Horizdistancelider["state"] = DISABLED
        Horizontalfeedslider["state"] = DISABLED
    #print(CurrentMode)

   
def AlarmOnOffbutton():
    global ALARMONOFF
    global changeparcheck
    changeparcheck=1
    if ALARMONOFF == 0:
        ALARMONOFF=1
        AlarmOnOffbutton['image']=alarmoffpic
    else:
        ALARMONOFF=0
        AlarmOnOffbutton['image']=alarmonpic
        
def MCresetbutton():
    print('mc reset button pressed')
    #serialconnect()
    try:
        sendsignal("1*0*0")
    except Exception as e:
        print('send signal exception')
        print(e)

def settingsbutton():
    global horizstartlength;
    global Inchdistanceset;
    #print("settings button clicked")
    settingsWindow = Toplevel(master) 
    settingsWindow.title("Settings")
    settingsWindowWidth=420
    settingsWindowHeight=420
    settingsWindow.geometry('{}x{}+{}+{}'.format(settingsWindowWidth, settingsWindowHeight, int(master.winfo_screenwidth()/2)-int(settingsWindowWidth/2), int(master.winfo_screenheight()/2)-int(settingsWindowHeight/2)))
    # Create a Tkinter variable
    res_choice_sel = StringVar(master)
    baud_rate_sel = StringVar(master)
    pwm_freq_sel = StringVar(master)
    # Dictionary with options
    res_choices = ["1ms","10ms","20ms","50ms"]
    baud_rate_choices = ["2400", "4800", "9600","19200","38400"]
    pwm_freq_choices = ["64kHz", "8kHz", "1kHz","500hz"]
    
    res_choice_sel.set(res_choices[0]) # set the default option
    baud_rate_sel.set(baud_rate_choices[2])
    pwm_freq_sel.set(pwm_freq_choices[1])

    res_choice_sel_popupMenu = tk.OptionMenu(settingsWindow, res_choice_sel, *res_choices)
    res_choice_sel_popupMenu['width']=5
    res_choice_sel_Label = tk.Label(settingsWindow, text="Set Resolution:", anchor='w', justify=LEFT)
    res_choice_sel_Label['width']=18
    res_choice_sel_Label.grid(row = 0, column = 0)
    res_choice_sel_popupMenu.grid(row = 0, column =1)
    
    
    baud_rate_sel_popupMenu = tk.OptionMenu(settingsWindow, baud_rate_sel, *baud_rate_choices)
    baud_rate_sel_popupMenu['width']=5
    baud_rate_sel_Label = tk.Label(settingsWindow, text="Set Baud Rate:", anchor='w', justify=LEFT)
    baud_rate_sel_Label['width']=18
    baud_rate_sel_Label.grid(row = 1, column = 0)
    baud_rate_sel_popupMenu.grid(row = 1, column =1)
    
    pwm_freq_sel_popupMenu = tk.OptionMenu(settingsWindow, pwm_freq_sel, *pwm_freq_choices)
    pwm_freq_sel_popupMenu['width']=5
    pwm_freq_sel_Label = tk.Label(settingsWindow, text="Set PWM freq:", anchor='w', justify=LEFT)
    pwm_freq_sel_Label['width']=18
    pwm_freq_sel_Label.grid(row = 2, column = 0)
    pwm_freq_sel_popupMenu.grid(row = 2, column =1)
    
    screenshot_folder_sel_Label = tk.Label(settingsWindow, text="Select folder for\nstoring screenshot:", anchor='w', justify=LEFT)
    screenshot_folder_sel_Label['width']=18
    screenshot_folder_sel_Label['height']=2
    screenshot_folder_sel_Label.grid(row = 3, column = 0)
        
    def screenshot_folder_sel_browse_button(*args):
        folder_path = StringVar()
        filename = filedialog.askdirectory()
        folder_path.set(filename)
        if str(filename) == "":
            screenshot_folder_sel_browse_button['text']="Browse"
        else:
            screenshot_folder_sel_browse_button['text']=str(filename)
        #print(filename)
        
    def check_ip_add(*args):
        #print("check ip address button clicked")
        # getting IP Address
        address = subprocess.check_output(['hostname', '-s', '-I']).decode('utf-8')[:-1]
        #print(address.split(" ")[0])
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            ipaddrstr=str(address.split(" ")[0])
            if ipaddrstr == "" or len(ipaddrstr) > 20:
                check_ip_address_Button['text']="NA Check"
                logger.error(datetimestring + " :: " + "No connections found")
                #print("No connections found")
            else:
                check_ip_address_Button['text']=ipaddrstr
        except Exception as e:
            check_ip_address_Button['text']="NA Check"
            logger.error(datetimestring + " :: " + "IP addr retrieval error")
            #print("IP addr retrieval error")
        try:
            ipaddrstr=str(address.split(" ")[1])
            if ipaddrstr == "" or len(ipaddrstr) > 20:
                check_ip_address2_Button['text']=""
                check_ip_address2_Button['width']=0
                check_ip_address2_Button['bd']=0
                logger.error(datetimestring + " :: " + "No additional connections found")
                #print("No connections found")
            else:
                check_ip_address2_Button['text']=ipaddrstr
                check_ip_address2_Button['bd']=1
        except Exception as e:
            check_ip_address2_Button['text']=""
            check_ip_address2_Button['width']=12
            check_ip_address2_Button['bd']=0
            logger.error(datetimestring + " :: " + "Secondary IP addr retrieval error")
            #print("Secondary IP addr retrieval error")
            
    def check_hostname(*args):
        hostname = socket.gethostname() 
        check_hostname_Button['text']=hostname
        
    def show_logs_button(*args):
        logsWindow = Toplevel(master) 
        logsWindow.title("Log Window")
        logsWindowWidth=800
        logsWindowHeight=850
        logsWindow.geometry('{}x{}+{}+{}'.format(logsWindowWidth, logsWindowHeight, int(master.winfo_screenwidth()/2)-int(logsWindowWidth/2), int(master.winfo_screenheight()/2)-int(logsWindowHeight/2)))
        horizontalscrollbar = tk.Scrollbar(logsWindow, orient = 'horizontal') 
        # attach Scrollbar to root window at the bootom 
        horizontalscrollbar.pack(side = BOTTOM, fill = X) 
        # create a vertical scrollbar-no need to write orient as it is by default vertical 
        verticalscrollbar = tk.Scrollbar(logsWindow) 
        # attach Scrollbar to root window on the side 
        verticalscrollbar.pack(side = RIGHT, fill = Y)
        rd = open ("/home/pi/Desktop/PaintingRobot/logs/PR.log", "r")
        texthold = tk.Text(logsWindow, wrap = NONE, xscrollcommand = horizontalscrollbar.set,  yscrollcommand = verticalscrollbar.set, state=NORMAL, width=80, height=50)
        while True:
            # Read next line
            line = rd.readline()
            # If line is blank, then you struck the EOF
            if not line :
                break;
            texthold.insert(END,line.strip())
            texthold.insert(END,"\n")
        # Close file 
        rd.close()
        texthold.pack(side=TOP, fill=X)
        texthold["state"] = DISABLED
        # here command represents the method to be executed xview is executed on object 't' Here t may represent any widget 
        horizontalscrollbar.config(command=texthold.xview) 
        # here command represents the method to be executed yview is executed on object 't' Here t may represent any widget 
        verticalscrollbar.config(command=texthold.yview)
        
    def clear_logs_button(*args):
        os.system("rm /home/pi/Desktop/PaintingRobot/logs/PR.log")
        os.system("touch /home/pi/Desktop/PaintingRobot/logs/PR.log")
        handler = logging.FileHandler('/home/pi/Desktop/PaintingRobot/logs/PR.log')
        logger.addHandler(handler)
        
    def start_prog_onboot_button(*args):
        rd = open ("/etc/profile", "r")
        chkboot = 0
        while True:
            # Read next line
            line = rd.readline()
            # If line is blank, then you struck the EOF
            if not line :
                break;
            #print(line.strip())
            if "python3 /home/pi/Desktop/PaintingRobot/mainprogram.py" in line:
                chkboot = 1
                break;
        # Close file 
        rd.close()
        if chkboot == 0:
            os.system("sudo sh -c \"echo python3 /home/pi/Desktop/PaintingRobot/mainprogram.py >> /etc/profile\"")
            start_prog_onboot_button['text']="Enabled"
        else:
            #start_prog_onboot_button['text']="Enabled"
            os.system("sudo sed -i.bak '$d' /etc/profile")
            start_prog_onboot_button['text']="Disabled"
            
    def reboot_button(*args):
        #sendstringtest=str(BPMSlider.get())+"*"+str(TiVSlider.get())+"*"+str(IERSlider.get()*10)+"*"+str(PIPLSlider.get())+"*"+str(PEEPLSlider.get())+"*"+str(FIOLSlider.get())+"*0*"+str(ALARMONOFF)
        #ser.write(sendstringtest.encode("utf-8"))
        os.system("sudo reboot")
        
    def shutdown_button(*args):
        #sendstringtest=str(BPMSlider.get())+"*"+str(TiVSlider.get())+"*"+str(IERSlider.get()*10)+"*"+str(PIPLSlider.get())+"*"+str(PEEPLSlider.get())+"*"+str(FIOLSlider.get())+"*0*"+str(ALARMONOFF)
        #ser.write(sendstringtest.encode("utf-8"))
        os.system("sudo shutdown now")
        
                    
    screenshot_folder_sel_browse_button = tk.Button(settingsWindow, text="Browse", command=screenshot_folder_sel_browse_button, width=10, height=2, wraplength=100)
    screenshot_folder_sel_browse_button.grid(row=3, column=1)
   
    check_ip_Label = tk.Label(settingsWindow, text="IP address:", width=18, height=1, anchor='w', justify=LEFT)
    check_ip_Label.grid(row=5, column=0)
    
    check_ip_address_Button = tk.Button(settingsWindow, text="Check", justify=CENTER, command=check_ip_add)
    check_ip_address_Button['width']=12
    check_ip_address_Button.grid(row = 5, column = 1)
    
    check_ip_address2_Button = tk.Button(settingsWindow, text="", justify=CENTER, bd=0)
    check_ip_address2_Button['width']=0
    check_ip_address2_Button.grid(row = 5, column = 2)
    
    check_hostname_Label = tk.Label(settingsWindow, text="Hostname:", width=18, height=1, anchor='w', justify=LEFT)
    check_hostname_Label.grid(row=6, column=0)
    
    check_hostname_Button = tk.Button(settingsWindow, text="Check", justify=CENTER, command=check_hostname)
    check_hostname_Button['width']=12
    check_hostname_Button.grid(row = 6, column = 1)
    
    check_cwd_Label = tk.Label(settingsWindow, text="Current working directory:", width=21, height=1, anchor='w', justify=CENTER)
    check_cwd_Label.grid(row=7, column=0)
        
    dirpath = os.getcwd()
    #print(dirpath)
    cwd_Label = tk.Label(settingsWindow, text=dirpath, width=30, height=1, anchor='center', justify=CENTER, font=('Helvetica', 10, 'normal'))
    cwd_Label.grid(row=7, column=1)
    
    check_USB_dev_Label = tk.Label(settingsWindow, text="Current MC unit addr:", width=21, height=1, anchor='w', justify=LEFT)
    check_USB_dev_Label.grid(row=8, column=0)
    
    try:
        ard_addr = glob.glob("/dev/ttyUSB*")[0]
        #print(ard_addr)
    except Exception as e:
        print(e)
        logger.error(datetimestring + " :: " + "arduino not sensed")
        ard_addr = "None"
            
    USB_dev_Label = tk.Label(settingsWindow, text=ard_addr, width=25, height=1, anchor='center', justify=RIGHT)
    USB_dev_Label.grid(row=8, column=1)
    #foldername = os.path.basename(dirpath)
    #print("Directory name is : " + foldername)
    
    show_logs_button = tk.Button(settingsWindow, text="Open logs", command=show_logs_button, width=18, height=1)
    show_logs_button.grid(row=9, column=0)
    
    clear_logs_button = tk.Button(settingsWindow, text="Clear logs", command=clear_logs_button, width=18, height=1)
    clear_logs_button.grid(row=9, column=1)
    
    start_prog_onboot_label = tk.Label(settingsWindow, text="Start program on boot:", width=20, height=1, anchor='w', justify=LEFT)
    start_prog_onboot_label.grid(row=10, column=0)
    
    start_prog_onboot_button = tk.Button(settingsWindow, command=start_prog_onboot_button, width=18, height=1)
    rd = open ("/etc/profile", "r")
    chkboot = 0
    while True:
        # Read next line
        line = rd.readline()
        # If line is blank, then you struck the EOF
        if not line :
            break;
        #print(line.strip())
        if "python3 /home/pi/Desktop/PaintingRobot/mainprogram.py" in line:
            chkboot = 1
            break;
    # Close file 
    rd.close()
    if chkboot == 0:
        start_prog_onboot_button['text']=DISABLED
    else:
        start_prog_onboot_button['text']="Enabled"
    start_prog_onboot_button.grid(row=10, column=1)
    
    reboot_button = tk.Button(settingsWindow, text="Reboot", command=reboot_button, width=18, height=1, font=('Helvetica', 11, 'bold'))
    reboot_button.grid(row=11, column=0)
    
    shutdown_button = tk.Button(settingsWindow, text="Shutdown", command=shutdown_button, width=18, height=1, font=('Helvetica', 11, 'bold'))
    shutdown_button.grid(row=11, column=1)
    
    def updateInchdistance(value):
        global Inchdistanceset;
        #print(value)
        Inchdistanceset=value;
        
    def updateSpraytime(value):
        global Spraytime;
        #print(value)
        Spraytime=value;
        
    Inchdistancelider= tk.Scale(settingsWindow, from_=100, to=20000, label="Set inch distance:", resolution=100, width =18, length = 200, orient=HORIZONTAL, command=updateInchdistance, font=('Helvetica', 11, 'normal'))
    Inchdistancelider.set(Inchdistanceset)
    Inchdistancelider.grid(row=12, column=0)
    
    Spraytimeslider= tk.Scale(settingsWindow, from_=500, to=60000, label="Set spray inch time:", resolution=10, width =18, length = 200, orient=HORIZONTAL, command=updateSpraytime, font=('Helvetica', 11, 'normal'))
    Spraytimeslider.set(Spraytime)
    Spraytimeslider.grid(row=12, column=1)
    
    # on change dropdown value
    def change_dropdown_res(*args):
        print( res_choice_sel.get() )
        
    def change_dropdown_bdr(*args):
        print( baud_rate_sel.get() )
        
    def change_dropdown_pwm(*args):
        print( pwm_freq_sel.get() )
        
    # link function to change dropdown
    res_choice_sel.trace('w', change_dropdown_res)
    baud_rate_sel.trace('w', change_dropdown_bdr)
    pwm_freq_sel.trace('w', change_dropdown_pwm)

def sendsignal(sendtext):
    global ser
    try:
       ser.write(sendtext.encode("utf-8"))
    #  print(sendscaninst)
    except Exception as e:
       print("Serial data write exception")
       print(e)
       logger.error(datetimestring + " :: " + "Serial data write exception-scan instruction")
       ComErrorAlarmlabel['text']="Serial Comm Error"
       
def serialconnect():
    global ser
    try:
        ard_addr = glob.glob("/dev/ttyUSB*")[0]
        logger.warning(datetimestring + " :: " + "connecting to " + ard_addr)
        ser = serial.Serial(port=str(ard_addr), baudrate = 115200)
        logger.warning(datetimestring + " :: " + "Serial variable created")
    except Exception as e:
        #print("Serial declare exception")
        logger.error(datetimestring + " :: " + "Serial declare exception")
        ComErrorAlarmlabel['text']="Serial Comm Error"
        
def read_from_port(serial_obj):
    global Currprocess;
    global PrevCurrprocess;
    global Currprocesscommstring;
    while True:
        try:
            readstring = serial_obj.readline().decode("utf-8")
            print(readstring)
            
            catcode=readstring.split("*")[0]
            #print(catcode)
            if catcode == "stat":
                message=readstring.split("*")[1]
                #print(message)
                if "commstart" in message :
                    #print("Currprocess during reset: "+Currprocess)
                    if "BatchJob" not in Currprocess :
                        ComErrorAlarmlabel['text']="MC COM OK"
                        enableallitems()
                        disablestartbuttongroup()
                if "noresettpos" in message :
                    #print("Currprocess during reset: "+Currprocess)
                    sendsignal("8*7*1*"+str(Inchenablestring))
                    if "BatchJob" not in Currprocess :
                        Statusbutton['text']="Not in Reset position"
                        enableresetbuttongroup()
                    else:
                        ComErrorAlarmlabel['text']="MC RESET"
                        if Inchallcarraigevar.get() == 1:
                            Inchallcarraige["state"] = NORMAL
                            Inchcarraige1["state"] = DISABLED
                            Inchcarraige2["state"] = DISABLED
                            Inchcarraige3["state"] = DISABLED
                            Inchcarraige4["state"] = DISABLED
                            Inchcarraige5["state"] = DISABLED
                        else:
                            Inchallcarraige["state"] = NORMAL
                            Inchcarraige1["state"] = NORMAL
                            Inchcarraige2["state"] = NORMAL
                            Inchcarraige3["state"] = NORMAL
                            Inchcarraige4["state"] = NORMAL
                            Inchcarraige5["state"] = NORMAL
                if "resetpos" in message :
                    print("Currprocess: "+Currprocess)
                    Statusbutton['text']="Select coach type"
                    enablecoachtypeselect()
                    disablestartbuttongroup()
                if "jobprog" in message :
                    if "BatchJobInchStart" in Currprocess :
                        Statusbutton['text']="Auto Painting"
                        runningmodebuttonstatus();
                    elif "BatchJobInchNext" in Currprocess :
                        Statusbutton['text']="Auto Painting"
                        runningmodebuttonstatus();
                    elif "BatchJobPaint" in Currprocess :
                        Statusbutton['text']="Auto Painting"
                        runningmodebuttonstatus();
                    else :
                        Statusbutton['text']=Currprocess;
                        disableallitemsexceptstop();
                if "jobcomp" in message :
                    print("Recjobcompafter: "+Currprocess)
                    if "Resetting" in Currprocess and Pausemode==0:
                        Statusbutton['text']="Select coach type"
                        #clearpoints();
                        enablecoachtypeselect()
                        disablestartbuttongroup()
                    elif "BatchJobInchStart" in Currprocess and Pausemode==0:
                        Statusbutton['text']="Auto Painting"
                        NSTnextcommand(); 
                    elif "BatchJobInchNext" in Currprocess and Pausemode==0:
                        Statusbutton['text']="Auto Painting"
                        NSTnextcommand(); 
                    elif "BatchJobPaint" in Currprocess and Pausemode==0:
                        Statusbutton['text']="Auto Painting"
                        Currprocesscommstring="5*"+str(Xaxisspeed)+"*"+str(int(widthresolution)+int(horizmovposoffset));
                        sendsignal(Currprocesscommstring);
                        Currprocess="BatchJobInchNext";
                    elif Pausemode==0 and "Batch" not in Currprocess and "Resetting" not in Currprocess: #added now
                        print('inside inch job comp elif');
                        Statusbutton['text']=Currprocess+" complete"
                        enableallitems()
                        enableresetbuttongroup()
                    elif Pausemode==1 and "Batch" not in Currprocess and "Resetting" not in Currprocess:
                        print('inside pausemode job comp elif');
                        Statusbutton['text']=Currprocess+" complete"
                        Pausebutton["text"]="Resume";
                        runningmodebuttonstatus();
                        Resetbutton["state"] = NORMAL
                        Resetbutton["text"] = "Repeat"
                        Currprocess=PrevCurrprocess;
                        #added now
                        inchupbutton["state"] = NORMAL
                        inchdownbutton["state"] = NORMAL
                        inchleftbutton["state"] = NORMAL
                        inchrightbutton["state"] = NORMAL
                        spraybutton["state"] = NORMAL
                        
                        if Inchallcarraigevar.get() == 1:
                            Inchallcarraige["state"] = NORMAL
                            Inchcarraige1["state"] = DISABLED
                            Inchcarraige2["state"] = DISABLED
                            Inchcarraige3["state"] = DISABLED
                            Inchcarraige4["state"] = DISABLED
                            Inchcarraige5["state"] = DISABLED
                        else:
                            Inchallcarraige["state"] = NORMAL
                            Inchcarraige1["state"] = NORMAL
                            Inchcarraige2["state"] = NORMAL
                            Inchcarraige3["state"] = NORMAL
                            Inchcarraige4["state"] = NORMAL
                            Inchcarraige5["state"] = NORMAL
                    elif Pausemode==1 and "Batch" in Currprocess:
                        Statusbutton['text']="Paused"
                       
                if "tskdspfail" in message :
                    if "BatchJob" not in Currprocess :
                        Statusbutton['text']="Sending failed"
                        enableallitems()
                        enableresetbuttongroup()
                    else :
                        Statusbutton['text']="Sending failed"
                        runningmodebuttonstatus();
                        
                
            if "inchenablestringset" in catcode:
                    inchenablestringsetarray=readstring.split(":")[1]
                    #print("inchenablestringsetarray:"+inchenablestringsetarray);
                    if(inchenablestringsetarray[0]=='0'):
                        East_IE_Label["bg"]="gray";
                    else:
                        East_IE_Label["bg"]="yellow";

                    if(inchenablestringsetarray[1]=='0'):
                        West_IE_Label["bg"]="gray";
                    else:
                        West_IE_Label["bg"]="yellow";
                        
                    if(inchenablestringsetarray[2]=="0"):
                        North_IE_Label["bg"]="gray";
                    else:
                        North_IE_Label["bg"]="yellow";
                        
                    if(inchenablestringsetarray[3]=="0"):
                        South_IE_Label["bg"]="gray";
                    else:
                        South_IE_Label["bg"]="yellow";
                        
                    if(inchenablestringsetarray[4]=="0"):
                        Top_IE_Label["bg"]="gray";
                    else:
                        Top_IE_Label["bg"]="yellow";
                        
            if "jobpendingatcmd" in catcode:
                    jobpendingatcmdarray=readstring.split(":")[1]
                    #print("jobpendingatcmdarray:"+jobpendingatcmdarray);
                    if(jobpendingatcmdarray[0]=='0'):
                        East_JC_Label["bg"]="gray";
                    else:
                        East_JC_Label["bg"]="yellow";

                    if(jobpendingatcmdarray[1]=='0'):
                        West_JC_Label["bg"]="gray";
                    else:
                        West_JC_Label["bg"]="yellow";
                        
                    if(jobpendingatcmdarray[2]=="0"):
                        North_JC_Label["bg"]="gray";
                    else:
                        North_JC_Label["bg"]="yellow";
                        
                    if(jobpendingatcmdarray[3]=="0"):
                        South_JC_Label["bg"]="gray";
                    else:
                        South_JC_Label["bg"]="yellow";
                        
                    if(jobpendingatcmdarray[4]=="0"):
                        Top_JC_Label["bg"]="gray";
                    else:
                        Top_JC_Label["bg"]="yellow";
                        
            if "jobpendingstatusupd" in catcode:
                    jobpendingstatusupdarray=readstring.split(":")[1]
                    print("jobpendingstatusupdarray:"+jobpendingstatusupdarray);
                    if(jobpendingstatusupdarray[0]=='0'):
                        East_FB_Label["bg"]="gray";
                    else:
                        East_FB_Label["bg"]="yellow";

                    if(jobpendingstatusupdarray[1]=='0'):
                        West_FB_Label["bg"]="gray";
                    else:
                        West_FB_Label["bg"]="yellow";
                        
                    if(jobpendingstatusupdarray[2]=="0"):
                        North_FB_Label["bg"]="gray";
                    else:
                        North_FB_Label["bg"]="yellow";
                        
                    if(jobpendingstatusupdarray[3]=="0"):
                        South_FB_Label["bg"]="gray";
                    else:
                        South_FB_Label["bg"]="yellow";
                        
                    if(jobpendingstatusupdarray[4]=="0"):
                        Top_FB_Label["bg"]="gray";
                    else:
                        Top_FB_Label["bg"]="yellow";
                        
                    
        except serial.SerialException as e:
            # There is no new data from serial port
            logger.error(datetimestring + " :: " + "Serial data read exception")
            ComErrorAlarmlabel['text']="Serial Comm Error"
            return None
        except TypeError as e:
            # Disconnect of USB->UART occured
            print("Serial data read exception")
            logger.error(datetimestring + " :: " + "Serial data read exception")
            ComErrorAlarmlabel['text']="Serial Comm Error"
            serial_obj.port.close()
            return None
        except Exception as e:
            print(e)
            
master = tk.Tk()
master.title("Painting Robot")
#windowWidth = master.winfo_reqwidth()
#windowHeight = master.winfo_reqheight()
master.attributes('-fullscreen', True)

# Creating a photoimage object to use image
mcresetpic = PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/icon_reset.png")
alarmoffpic = PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/alarmoff_icon.png")
alarmonpic = PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/alarmon_icon.png")
snapshotpic = PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/screen_shot.pgm")
settingsiconpic = PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/settings_icon.png")
addlsettingsiconpic = PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/addl_settings.png")
idleicon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/stop.png")
erroricon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/error.png")

inchupicon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/inch_up_icon.png")
inchdownicon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/inch_down_icon.png")
inchlefticon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/inch_left_icon.png")
inchrighticon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/inch_right_icon.png")
limitsengageicon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/limits_engaged_icon.png")
limitsdisengageicon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/limits_disengaged_icon.png")
sprayandmoveicon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/sprayandmove_icon.png")

inchtrayinicon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/inch_tray_in.png")
inchtrayouticon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/inch_tray_out.png")
sprayicon=PhotoImage(file = "/home/pi/Desktop/PaintingRobot/images/spray_icon.png")

TitleGroup = LabelFrame(master, text = "")
TitleGroup.grid(row=0, column=0)

AlarmDisplayGroup = LabelFrame(TitleGroup, text = "", width=400, height=2)
AlarmDisplayGroup.grid(row=0, column=0)

Datetimebutton = tk.Button(AlarmDisplayGroup, text="Date & Time", font=('Helvetica', 13, 'bold'), bd=0)
Datetimebutton.grid(row=0, column=0)

Statusbutton = tk.Button(AlarmDisplayGroup, text="Status label", font=('Helvetica', 13, 'bold'), bd=0, width=25, height=2, fg="red")
Statusbutton.grid(row=0, column=1)

Statusicon = tk.Label(AlarmDisplayGroup, bd=0, width=70, height=50, image=idleicon)
Statusicon.grid(row=0, column=2)

Titlelabel = tk.Label(AlarmDisplayGroup, text="Painting Robot - Goldenrock Workshops", font=('Helvetica', 22, 'bold'), width=45, height=2, bd=0)
Titlelabel.grid(row=0, column=3)

ComErrorAlarmlabel = tk.Label(AlarmDisplayGroup, text="Serialcomlabel", font=('Helvetica', 16, 'bold'), width=27, height=1, bd=0, fg="red")
ComErrorAlarmlabel.grid(row=0, column=4)

Snapshotbutton = tk.Button(AlarmDisplayGroup, text="", bd=0, image=snapshotpic, command=snapshotbutton, width=70, height=50)
Snapshotbutton.grid(row=0, column=5)

AddlSettingsbutton = tk.Button(AlarmDisplayGroup, text="", bd=0, image=addlsettingsiconpic, command=addlsettingsbutton, width=60, height=50)
AddlSettingsbutton.grid(row=0, column=6)

Settingsbutton = tk.Button(AlarmDisplayGroup, text="", bd=0, image=settingsiconpic, command=settingsbutton, width=70, height=50)
Settingsbutton.grid(row=0, column=7)

MCResetbutton = tk.Button(AlarmDisplayGroup, text="", bd=0, image=mcresetpic, command=MCresetbutton, width=60, height=50)
MCResetbutton.grid(row=0, column=8)

Exitbutton = tk.Button(AlarmDisplayGroup, text="X", font=('Helvetica', 20, 'bold'), bd=0, command=exitbutton)
Exitbutton.grid(row=0, column=9)

DisplayGroup = LabelFrame(master, text = "")
DisplayGroup.grid(row=1, column=0)

OptionsGroup = LabelFrame(DisplayGroup, text = "")
OptionsGroup.grid(row=0, column=0)

radioGroup = LabelFrame(OptionsGroup, text = "Select Coach type", font=('Helvetica', 15, 'bold'))
radioGroup.pack()

ICFLHBselectgroup = LabelFrame(radioGroup, text = "", bd=0)
ICFLHBselectgroup.pack()

ICFbutton = tk.Button(ICFLHBselectgroup, text="ICF", font=('Helvetica', 9, 'bold'), bd=0, width=10, height=1, command=ICFbuttonselect)
ICFbutton.grid(row=0, column=0)

LHBbutton = tk.Button(ICFLHBselectgroup, text="LHB", font=('Helvetica', 9, 'bold'), bd=0, width=10, height=1, command=LHBbuttonselect)
LHBbutton.grid(row=0, column=1)

CurrentMode=IntVar()

#command pending
CoachtypeButton1=tk.Radiobutton(radioGroup, text="ICF Roof", variable=CurrentMode, command=selectcoachtype1, value=1)
CoachtypeButton1.pack(anchor=W)

#command pending
CoachtypeButton2=tk.Radiobutton(radioGroup, text="ICF Non AC SL FC", variable=CurrentMode, command=selectcoachtype2, value=2)
CoachtypeButton2.pack(anchor=W)

#command pending
CoachtypeButton3=tk.Radiobutton(radioGroup, text="ICF Non AC SL SC", variable=CurrentMode, command=selectcoachtype3, value=3)
CoachtypeButton3.pack(anchor=W)

#command pending
CoachtypeButton4=tk.Radiobutton(radioGroup, text="ICF AC SL FC", variable=CurrentMode, command=selectcoachtype4, value=4)
CoachtypeButton4.pack(anchor=W)

CurrentMode.set(0)

#command pending
HorizontalSpeedslider= tk.Scale(OptionsGroup, from_=50, to=100, width =20, resolution=25, label = "X axis speed %",length = 200, orient=HORIZONTAL, command=updateXaxisspeed,font=('Helvetica', 12, 'bold'))
HorizontalSpeedslider.set(50)
HorizontalSpeedslider.pack()

#command pending
VerticalSpeedslider= tk.Scale(OptionsGroup, from_=50, to=100, width =20, resolution=25, label = "Y axis speed %",length = 200, orient=HORIZONTAL, command=updateYaxisspeed, font=('Helvetica', 12, 'bold'))
VerticalSpeedslider.set(50)
VerticalSpeedslider.pack()


FBdisplaygroup = LabelFrame(OptionsGroup, text = "", bd=1)
FBdisplaygroup.pack()

FBdisplaygroup_name_Label = tk.Label(FBdisplaygroup, text="Carrg", width=6, height=1, justify=CENTER)
FBdisplaygroup_name_Label.grid(row=0, column=0)

FBdisplaygroup_IE_Label = tk.Label(FBdisplaygroup, text="IE", width=5, height=1, justify=CENTER)
FBdisplaygroup_IE_Label.grid(row=0, column=1)

FBdisplaygroup_JC_Label = tk.Label(FBdisplaygroup, text="JC", width=5, height=1, justify=CENTER)
FBdisplaygroup_JC_Label.grid(row=0, column=2)

FBdisplaygroup_FB_Label = tk.Label(FBdisplaygroup, text="FB", width=5, height=1, justify=CENTER)
FBdisplaygroup_FB_Label.grid(row=0, column=3)

East_name_Label = tk.Label(FBdisplaygroup, text="East", width=6, height=1, anchor='w', justify=LEFT)
East_name_Label.grid(row=1, column=0)

East_IE_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
East_IE_Label.grid(row=1, column=1)

East_JC_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
East_JC_Label.grid(row=1, column=2)

East_FB_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
East_FB_Label.grid(row=1, column=3)

West_name_Label = tk.Label(FBdisplaygroup, text="West", width=6, height=1, anchor='w', justify=LEFT)
West_name_Label.grid(row=2, column=0)

West_IE_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
West_IE_Label.grid(row=2, column=1)

West_JC_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
West_JC_Label.grid(row=2, column=2)

West_FB_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
West_FB_Label.grid(row=2, column=3)

North_name_Label = tk.Label(FBdisplaygroup, text="North", width=6, height=1, anchor='w', justify=LEFT)
North_name_Label.grid(row=3, column=0)

North_IE_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
North_IE_Label.grid(row=3, column=1)

North_JC_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
North_JC_Label.grid(row=3, column=2)

North_FB_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
North_FB_Label.grid(row=3, column=3)

South_name_Label = tk.Label(FBdisplaygroup, text="South", width=6, height=1, anchor='w', justify=LEFT)
South_name_Label.grid(row=4, column=0)

South_IE_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
South_IE_Label.grid(row=4, column=1)

South_JC_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
South_JC_Label.grid(row=4, column=2)

South_FB_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
South_FB_Label.grid(row=4, column=3)

Top_name_Label = tk.Label(FBdisplaygroup, text="Top", width=6, height=1, anchor='w', justify=LEFT)
Top_name_Label.grid(row=5, column=0)

Top_IE_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
Top_IE_Label.grid(row=5, column=1)

Top_JC_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
Top_JC_Label.grid(row=5, column=2)

Top_FB_Label = tk.Label(FBdisplaygroup, width=5, height=1, bg="black",bd=1)
Top_FB_Label.grid(row=5, column=3)

Engageallcarraigevar=IntVar()
#command pending
Engageallcarraige = tk.Checkbutton(OptionsGroup, text='Engage All Carraiges', font=('Helvetica', 11, 'bold'),variable=Engageallcarraigevar, command=Engageallcarraigeselect)
#Engageallcarraige.pack(anchor=W)


Engagecarraige1var=IntVar()
#command pending
Engagecarraige1 = tk.Checkbutton(OptionsGroup, text='Engage East side Carraige', variable=Engagecarraige1var, command=Engagecarraige1select)
#Engagecarraige1.pack(anchor=W)

Engagecarraige2var=IntVar()
#command pending
Engagecarraige2 = tk.Checkbutton(OptionsGroup, text='Engage West side Carraige', variable=Engagecarraige2var, command=Engagecarraige2select)
#Engagecarraige2.pack(anchor=W)

Engagecarraige3var=IntVar()
#command pending
Engagecarraige3 = tk.Checkbutton(OptionsGroup, text='Engage North side Carraige', variable=Engagecarraige3var, command=Engagecarraige3select)
#Engagecarraige3.pack(anchor=W)

Engagecarraige4var=IntVar()
#command pending
Engagecarraige4 = tk.Checkbutton(OptionsGroup, text='Engage South Side Carraige', variable=Engagecarraige4var, command=Engagecarraige4select)
#Engagecarraige4.pack(anchor=W)

Engagecarraige5var=IntVar()
#command pending
Engagecarraige5 = tk.Checkbutton(OptionsGroup, text='Engage Top Side Carraige', variable=Engagecarraige5var, command=Engagecarraige5select)
#Engagecarraige5.pack(anchor=W)

Engageallcarraigevar.set(0)
Engageallcarraigeselect()

Inchallcarraigevar=IntVar()
#command pending
Inchallcarraige = tk.Checkbutton(OptionsGroup, text='Inch All Carraiges', font=('Helvetica', 11, 'bold'), command=Inchallcarraigeselect, variable=Inchallcarraigevar)
Inchallcarraige.pack(anchor=W)

Inchcarraige1var=IntVar()
#command pending
Inchcarraige1 = tk.Checkbutton(OptionsGroup, text='Inch East side Carraige', command=Inchcarraige1select, variable=Inchcarraige1var)
Inchcarraige1.pack(anchor=W)

Inchcarraige2var=IntVar()
#command pending
Inchcarraige2 = tk.Checkbutton(OptionsGroup, text='Inch West side Carraige', command=Inchcarraige2select, variable=Inchcarraige2var)
Inchcarraige2.pack(anchor=W)

Inchcarraige3var=IntVar()
#command pending
Inchcarraige3 = tk.Checkbutton(OptionsGroup, text='Inch North side Carraige', command=Inchcarraige3select, variable=Inchcarraige3var)
Inchcarraige3.pack(anchor=W)

Inchcarraige4var=IntVar()
#command pending
Inchcarraige4 = tk.Checkbutton(OptionsGroup, text='Inch South side Carraige', command=Inchcarraige4select, variable=Inchcarraige4var)
Inchcarraige4.pack(anchor=W)

Inchcarraige5var=IntVar()
#command pending
Inchcarraige5 = tk.Checkbutton(OptionsGroup, text='Inch Top side Carraige', command=Inchcarraige5select, variable=Inchcarraige5var)
Inchcarraige5.pack(anchor=W)

Inchallcarraigevar.set(0)
Inchallcarraigeselect()

keyiconwidth=65
keyiconheight=65

KeyGroup = LabelFrame(OptionsGroup, text = "", width=4*keyiconwidth, height=4)
KeyGroup.pack()

inchupbutton = tk.Button(KeyGroup, text="", bd=0, image=inchupicon, width=keyiconwidth, height=keyiconheight, command=inchupbutton)
inchupbutton.grid(row=0, column=1)

inchdownbutton = tk.Button(KeyGroup, text="", bd=0, image=inchdownicon, width=keyiconwidth, height=keyiconheight, command=inchdownbutton)
inchdownbutton.grid(row=2, column=1)

inchleftbutton = tk.Button(KeyGroup, text="", bd=0, image=inchlefticon, width=keyiconwidth, height=keyiconheight, command=inchleftbutton)
inchleftbutton.grid(row=1, column=0)

inchrightbutton = tk.Button(KeyGroup, text="", bd=0, image=inchrighticon, width=keyiconwidth, height=keyiconheight, command=inchrightbutton)
inchrightbutton.grid(row=1, column=2)

spraybutton = tk.Button(KeyGroup, text="", bd=0, image=sprayicon, width=keyiconwidth, height=keyiconheight, command=spraybutton)
spraybutton.grid(row=1, column=1)

Engagelimitsbutton = tk.Button(KeyGroup, text="", bd=0, image=limitsdisengageicon, width=keyiconwidth, height=keyiconheight, command=Engagelimitsselect)
Engagelimitsbutton.grid(row=0, column=2)

sprayandmovebutton = tk.Button(KeyGroup, text="", bd=0, image=sprayandmoveicon, width=keyiconwidth, height=keyiconheight, command=sprayandmovebuttonselect)
sprayandmovebutton.grid(row=0, column=0)

# Engagelimitsvar=IntVar()
# Engagelimits = tk.Checkbutton(OptionsGroup, text='Bypass limits', variable=Engagelimitsvar, command=Engagelimitsselect)
# Engagelimits.pack(anchor=W)

Startbutton = tk.Button(OptionsGroup, text="Start", width=15, height=1, bd=1, font=('Helvetica', 18, 'bold'), fg="green", command=startbutton)        
Startbutton.pack()

Pausebutton = tk.Button(OptionsGroup, text="Pause", width=15, height=1, bd=1, font=('Helvetica', 18, 'bold'), fg="blue", command=pausebutton)        
Pausebutton.pack()

Stopbutton = tk.Button(OptionsGroup, text="Stop", width=15, height=1, bd=1, font=('Helvetica', 18, 'bold'), fg="red", command=stopbutton)        
Stopbutton.pack()

Resetbutton = tk.Button(OptionsGroup, text="Reset", width=15, height=1, bd=1, font=('Helvetica', 18, 'bold'), command=resetbutton)        
Resetbutton.pack()

StatusGroup = LabelFrame(DisplayGroup, text = "",width=1700, height=995)
StatusGroup.grid(row=0, column=1)

NorthsideStatusGroup = LabelFrame(StatusGroup, text = "",width=1700, height=250)
NorthsideStatusGroup.pack()

NorthsideTitle= tk.Label(NorthsideStatusGroup, text="North Side", font=('Helvetica', 18, 'bold'), bd=0)
NorthsideTitle.pack()

NorthsideliveStatus = LabelFrame(NorthsideStatusGroup, text = "",width=1700, height=190)
NorthsideliveStatus.pack()

NorthsidecoachliveStatus1 = LabelFrame(NorthsideliveStatus, text = "",width=45, height=190)
NorthsidecoachliveStatus1.grid(row=0, column=0)

NorthsidecoachliveStatus2 = LabelFrame(NorthsideliveStatus, text = "",width=1600, height=190)
NorthsidecoachliveStatus2.grid(row=0, column=1)

Northsidecellgrouplistnoofrows=3
Northsidecellgrouplistnoofcolumns=800
Northsidecellgrouplist = list()
# Already declared as global

# 
# for i in range(Northsidecellgrouplistnoofrows):
#         for j in range(Northsidecellgrouplistnoofcolumns):
#             if i == 1 :
#                 Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=2, height=43, bd=1))
#                 Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)
#             if i == 2 :
#                 Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=2, height=63, bd=1))
#                 Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)
#             if i == 0 :
#                 Northsidecellgrouplist.append(tk.LabelFrame(NorthsidecoachliveStatus2, width=2, height=83, bd=1))
#                 Northsidecellgrouplist[-1].grid(row=Northsidecellgrouplistnoofrows-1-i,column=j)

NorthsidecoachliveStatus3 = LabelFrame(NorthsideliveStatus, text = "",width=45, height=190)
NorthsidecoachliveStatus3.grid(row=0, column=2)

Northsideprogress= tk.Label(NorthsideStatusGroup, text="Progress - %", font=('Helvetica', 15, 'bold'), bd=0)
Northsideprogress.pack()

SouthsideStatusGroup = LabelFrame(StatusGroup, text = "",width=1700, height=250)
SouthsideStatusGroup.pack()

SouthsideTitle= tk.Label(SouthsideStatusGroup, text="South Side", font=('Helvetica', 18, 'bold'), bd=0)
SouthsideTitle.pack()

SouthsideliveStatus = LabelFrame(SouthsideStatusGroup, text = "",width=1700, height=190)
SouthsideliveStatus.pack()

SouthsidecoachliveStatus1 = LabelFrame(SouthsideliveStatus, text = "",width=45, height=190)
SouthsidecoachliveStatus1.grid(row=0, column=0)

SouthsidecoachliveStatus2 = LabelFrame(SouthsideliveStatus, text = "",width=1600, height=190)
SouthsidecoachliveStatus2.grid(row=0, column=1)

Southsidecellgrouplistnoofrows=3
Southsidecellgrouplistnoofcolumns=800
Southsidecellgrouplist = list()
# for i in range(Southsidecellgrouplistnoofrows):
#         for j in range(Southsidecellgrouplistnoofcolumns):
#             if i == 1 :
#                 Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=2, height=43, bd=1))
#                 Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)
#             if i == 2 :
#                 Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=2, height=63, bd=1))
#                 Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)
#             if i == 0 :
#                 Southsidecellgrouplist.append(tk.LabelFrame(SouthsidecoachliveStatus2, width=2, height=83, bd=1))
#                 Southsidecellgrouplist[-1].grid(row=Southsidecellgrouplistnoofrows-1-i,column=j)

SouthsidecoachliveStatus3 = LabelFrame(SouthsideliveStatus, text = "",width=45, height=190)
SouthsidecoachliveStatus3.grid(row=0, column=2)

Southsideprogress= tk.Label(SouthsideStatusGroup, text="Progress - %", font=('Helvetica', 15, 'bold'), bd=0)
Southsideprogress.pack()

TopsideStatusGroup = LabelFrame(StatusGroup, text = "",width=1700, height=225)
TopsideStatusGroup.pack()

TopsideTitle= tk.Label(TopsideStatusGroup, text="Top Side", font=('Helvetica', 18, 'bold'), bd=0)
TopsideTitle.pack()

TopsideliveStatus = LabelFrame(TopsideStatusGroup, text = "",width=1700, height=160)
TopsideliveStatus.pack()

TopsidecoachliveStatus1 = LabelFrame(TopsideliveStatus, text = "",width=45, height=160)
TopsidecoachliveStatus1.grid(row=0, column=0)

TopsidecoachliveStatus2 = LabelFrame(TopsideliveStatus, text = "",width=1600, height=160)
TopsidecoachliveStatus2.grid(row=0, column=1)

Topsidecellgrouplistnoofcolumns=800
Topsidecellgrouplist = list()
# for i in range(Topsidecellgrouplistnoofcolumns):
#         Topsidecellgrouplist.append(tk.LabelFrame(TopsidecoachliveStatus2, width=2, height=160, bd=1))
#         Topsidecellgrouplist[-1].grid(row=0,column=i)

TopsidecoachliveStatus3 = LabelFrame(TopsideliveStatus, text = "",width=45, height=160)
TopsidecoachliveStatus3.grid(row=0, column=2)

Topsideprogress= tk.Label(TopsideStatusGroup, text="Progress - %", font=('Helvetica', 15, 'bold'), bd=0)
Topsideprogress.pack()

EastWestsideStatusGroup = LabelFrame(StatusGroup, text = "",width=1700, height=250)
EastWestsideStatusGroup.pack()

EastsideStatusGroup = LabelFrame(EastWestsideStatusGroup, text = "",width=848, height=250)
EastsideStatusGroup.grid(row=0, column=0)

EastsideTitle= tk.Label(EastsideStatusGroup, text="East Side", font=('Helvetica', 18, 'bold'), bd=0)
EastsideTitle.pack()

EastsideliveStatus = LabelFrame(EastsideStatusGroup, text = "",width=848, height=160)
EastsideliveStatus.pack()

EastsidecoachliveStatus1 = LabelFrame(EastsideliveStatus, text = "",width=45, height=160)
EastsidecoachliveStatus1.grid(row=0, column=0)

EastsidecoachliveStatus2 = LabelFrame(EastsideliveStatus, text = "",width=600, height=160)
EastsidecoachliveStatus2.grid(row=0, column=1)

Eastsidecellgrouplistnoofcolumns=300
Eastsidecellgrouplist = list()
# for i in range(Eastsidecellgrouplistnoofcolumns):
#         Eastsidecellgrouplist.append(tk.LabelFrame(EastsidecoachliveStatus2, width=2, height=160, bd=1))
#         Eastsidecellgrouplist[-1].grid(row=0,column=i)

EastsidecoachliveStatus3 = LabelFrame(EastsideliveStatus, text = "",width=45, height=160)
EastsidecoachliveStatus3.grid(row=0, column=2)

Eastsideprogress= tk.Label(EastsideStatusGroup, text="Progress - %", font=('Helvetica', 15, 'bold'), bd=0)
Eastsideprogress.pack()

WestsideStatusGroup = LabelFrame(EastWestsideStatusGroup, text = "",width=848, height=250)
WestsideStatusGroup.grid(row=0, column=1)

WestsideTitle= tk.Label(WestsideStatusGroup, text="West Side", font=('Helvetica', 18, 'bold'), bd=0)
WestsideTitle.pack()

WestsideliveStatus = LabelFrame(WestsideStatusGroup, text = "",width=848, height=160)
WestsideliveStatus.pack()

WestsidecoachliveStatus1 = LabelFrame(WestsideliveStatus, text = "",width=45, height=160)
WestsidecoachliveStatus1.grid(row=0, column=0)

WestsidecoachliveStatus2 = LabelFrame(WestsideliveStatus, text = "",width=600, height=160)
WestsidecoachliveStatus2.grid(row=0, column=1)

Westsidecellgrouplistnoofcolumns=300
Westsidecellgrouplist = list()
# for i in range(Westsidecellgrouplistnoofcolumns):
#         Westsidecellgrouplist.append(tk.LabelFrame(WestsidecoachliveStatus2, width=2, height=160, bd=1))
#         Westsidecellgrouplist[-1].grid(row=0,column=i)
        

WestsidecoachliveStatus3 = LabelFrame(WestsideliveStatus, text = "",width=45, height=160)
WestsidecoachliveStatus3.grid(row=0, column=2)

Westsideprogress= tk.Label(WestsideStatusGroup, text="Progress - %", font=('Helvetica', 15, 'bold'), bd=0)
Westsideprogress.pack()

#ActiveAppGroup = LabelFrame(master, text = "")
#ActiveAppGroup.grid(row=1, column=0)

disptime()

serialconnect()

try:
    thread = threading.Thread(target=read_from_port, args=(ser,))
    thread.daemon = True
    ComErrorAlarmlabel['text']="Waiting for MC response"
    Statusbutton['text']="Waiting for MC response"
#     print("serial thread declared")
except Exception as e:
    Statusbutton['text']="IDLE-STOP"
    print("Thread declaration exception")
    logger.error(datetimestring + " :: " + "Thread declaration exception")
    ComErrorAlarmlabel['text']="Serial Comm Error"
    
try:
    thread.start()
#     print("serial thread started")
    logger.error(datetimestring + " :: " + "serial thread started")
    
except Exception as e:
    #print("Thread start exception")
    logger.error(datetimestring + " :: " + "Thread start exception")
    ComErrorAlarmlabel['text']="Serial Comm Error"
    
#actual site parameters
horizstartlength=IntVar(); # in mm
Inchdistanceset=IntVar(); #inching distance in mm
Spraytime=IntVar(); # spray time in ms

disableallitems();
initfieldvalues();

#NSTnextcommand();    
master.mainloop()
