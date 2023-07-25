################################
# >>      _Sense_Your_Life_
#
# >> Program created by PreIntelligentCoders
# >> Marcin Truszczynski && Grzegorz Stark
#
#
################################
from sense_hat import SenseHat
import math
import time
from threading import Thread


#----------------------------SENSE-CALIBRATION----------------------------------

sense = SenseHat()
sense.clear()

def LETSGETITSTARTED():
    for i in range(30, 0, -1):
        print i
        sense.show_message(str(i), scroll_speed = 0.05,text_colour = [255,0,0])
        time.sleep(0.9)
        C_X, C_Y, C_Z = sense.get_compass_raw().values()  #SETS LOCAL VARIABLES TO MAKE SENSE WORK AS IT SHOULD
        calibration = (sense.get_temperature_from_humidity() + sense.get_temperature_from_pressure()) + sense.get_humidity() #SETS LOCAL VARIABLES TO MAKE SENSE WORK AS IT SHOULD



LETSGETITSTARTED()
sense.set_rotation(r=180)

#================================================================================


#-----------------CONST-,-GLOBALS-AND-CLASS-INSTANCE-DEFINITIONS-AND-INITIALIZATIONS-----------------------------------


CONST_t = (sense.get_temperature_from_humidity() + sense.get_temperature_from_pressure())/2
CONST_h = sense.get_humidity()
CONST_p = sense.get_pressure()
C_X, C_Y, C_Z = sense.get_compass_raw().values()
CONST_m = math.fabs(C_X)+math.fabs(C_Y)+math.fabs(C_Z)


Wait_For_Stable = False

Scale_T = 1
Scale_H = 1
Scale_P = 1
Scale_M = 1

CONSTS = [CONST_t, CONST_h, CONST_p, CONST_m]
Scale = [Scale_T, Scale_H, Scale_P, Scale_M] #A NUMBER OF UNITS CORRESPONDING TO ONE PIXEL

Jump = 1

Cooldown = 0

timer = 0
mode = 0

b = [0,0,255]
g = [0,255,0]
y = [255,255,0]
r = [255,0,0]
e = [0,0,0]
w = [255, 255, 255]

calc = 0
solarFlareDetected = False

Matrix = [
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e]


#=====================================================================================


#----------------BUFOR-CLASS-FOR-MULTITHREADING--------------------------------------------------------------

class Bufor:

    global Matrix
        
    def set_pixel(j, x, y, c):
         for i in range(8):
            if x == i:      
                Matrix[8*y + x] = c
                break
        
        
    def Print(k):
        sense.set_pixels(Matrix)


Sense = Bufor()
#==============================================================================================================

        
#--------------------SENSOR-READER--------------------------------------

def GetSensorsValues():
    t = (sense.get_temperature_from_humidity() + sense.get_temperature_from_pressure())/2 #GETS AVARAGE FOR BETTER ACCURACY
    h = sense.get_humidity()
    p = sense.get_pressure()
    C_x, C_y, C_z = sense.get_compass_raw().values()
    m = math.fabs(C_x)+math.fabs(C_y)+math.fabs(C_z)
    w = [t,h,p,m]
    return w

#=======================================================================



def Printer(arg):    
    c = [y, b, g, r]

    i = 7
    k = 0
    while i > 3:
       
        for s in range(8):
            Sense.set_pixel(i,s,e)
           
            
        
        for s in range(arg[k]+1):
            Sense.set_pixel(i,s,c[k])
            
            
        k = k+1            
        i = i - 1



#-------------DYNAMIC-SCALE-FOR-CHART----------------------------------

def DynamicScale(value):
    
    W = 0

    global Scale
    
    for i in range(4):
    
        if value[i] > CONSTS[i]:
            W = math.fabs(value[i] - CONSTS[i])
        else:
            W = math.fabs(CONSTS[i] - value[i])
        
        W = round(W,0)
    
        if W > (Scale[i] * 4):
            while W > (Scale[i] * 4):
                Scale[i] += Jump
            
        elif W < (Scale[i]):
            while W < (Scale[i]):
                Scale[i] -= Jump
                
      
    for i in range(4):
        
        if Scale[i] <= 0:
            Scale[i] = 1

    
#=========================================================================

#----------------------------CHART-PREPARATION---------------------------------------------------------------------------------------

def PrintResults():
    global Wait_For_Stable
    global Cooldown
    w = GetSensorsValues()
    t = w[0]
    h = w[1]
    p = w[2]
    m = w[3]
   
    t_w = 0
    h_w = 0
    p_w = 0
    m_w = 0

    DynamicScale(w)
    
    if (t - CONSTS[0]) >= (Scale[0]*4): 
        t_w = 7
    elif (t - CONSTS[0]) >= (Scale[0]*3):
        t_w = 6
    elif (t - CONSTS[0]) >= (Scale[0]*2):
        t_w = 5
    elif (t - CONSTS[0]) >= (Scale[0]*1):
        t_w = 4
    elif (t - CONSTS[0]) <= -(Scale[0]*4): 
        t_w = 0
    elif (t - CONSTS[0]) <= -(Scale[0]*3):
        t_w = 0
    elif (t - CONSTS[0]) <= -(Scale[0]*2):
        t_w = 1
    elif (t - CONSTS[0]) <= -(Scale[0]*1):
        t_w = 2
    elif (t - CONSTS[0]) > -(Scale[0]):
        t_w = 3



    if (h - CONSTS[1]) >= (Scale[1]*4): 
        h_w = 7
    elif (h - CONSTS[1]) >= (Scale[1]*3):
        h_w = 6
    elif (h - CONSTS[1]) >= (Scale[1]*2):
        h_w = 5
    elif (h - CONSTS[1]) >= (Scale[1]*1):
        h_w = 4
    elif (h - CONSTS[1]) <= -(Scale[1]*4): 
        h_w = 0
    elif (h - CONSTS[1]) <= -(Scale[1]*3):
        h_w = 0
    elif (h - CONSTS[1]) <= -(Scale[1]*2):
        h_w = 1
    elif (h - CONSTS[1]) <= -(Scale[1]*1):
        h_w = 2
    elif (h - CONSTS[1]) > -(Scale[1]):
        h_w = 3



    if (p - CONSTS[2]) >= (Scale[2]*4): 
        p_w = 7
    elif (p - CONSTS[2]) >= (Scale[2]*3):
        p_w = 6
    elif (p - CONSTS[2]) >= (Scale[2]*2):
        p_w = 5
    elif (p - CONSTS[2]) >= (Scale[2]*1):
        p_w = 4
    elif (p - CONSTS[2]) <= -(Scale[2]*4): 
        p_w = 0
    elif (p - CONSTS[2]) <= -(Scale[2]*3):
        p_w = 0
    elif (p - CONSTS[2]) <= -(Scale[2]*2):
        p_w = 1
    elif (p - CONSTS[2]) <= -(Scale[2]*1):
        p_w = 2
    elif (p - CONSTS[2]) > -(Scale[2]):
        p_w = 3

    
    
  

#--------------------WARNINGS-------------------------------------------------------------------------

    OnePercent = m / 100

    if Wait_For_Stable == False:
        

        if (m - CONSTS[3]) > 5 * OnePercent:
            sense.set_rotation(r=0)
            sense.show_message("WARNING!!!", text_colour=[255,0,0],scroll_speed = 0.07)
            sense.show_message("STRONG MAGNETIC STORM", text_colour=[255,0,0],scroll_speed = 0.07)
            solarFlareDetected = True
            sense.set_rotation(r=180)
            Wait_For_Stable = True
        elif (m - CONSTS[3]) > 4 * OnePercent:
            sense.set_rotation(r=0)
            sense.show_message("WARNING!!!", text_colour=[255,0,0],scroll_speed = 0.07)
            sense.show_message("Magnetic induction increased by 4 percent", text_colour=[255,0,0],scroll_speed = 0.07)
            sense.set_rotation(r=180)
            Wait_For_Stable = True
        elif (m - CONSTS[3]) > 3 * OnePercent:
            sense.set_rotation(r=0)
            sense.show_message("WARNING!!!", text_colour=[255,0,0],scroll_speed = 0.07)
            sense.show_message("Magnetic induction increased by 3 percent", text_colour=[255,0,0],scroll_speed = 0.07)
            sense.set_rotation(r=180)
            Wait_For_Stable = True
        elif (m - CONSTS[3]) > 2 * OnePercent:
            sense.set_rotation(r=0)
            sense.show_message("WARNING!!!", text_colour=[255,0,0],scroll_speed = 0.07)
            sense.show_message("Magnetic induction increased by 2 percent", text_colour=[255,0,0],scroll_speed = 0.07)
            sense.set_rotation(r=180)
            Wait_For_Stable = True
        elif (m - CONSTS[3]) > 1 * OnePercent:
            sense.set_rotation(r=0)
            sense.show_message("WARNING!!!", text_colour=[255,0,0],scroll_speed = 0.07)
            sense.show_message("Magnetic induction increased by 1 percent", text_colour=[255,0,0],scroll_speed = 0.07)
            sense.set_rotation(r=180)
            Wait_For_Stable = True
    else:
        Cooldown += 1
        if Cooldown >= 25:
            Wait_For_Stable = False
            Cooldown = 0
            
            


#=====================================================================================================

    
   
    if (m - CONSTS[3]) >= (Scale[3]*4): 
        m_w = 7
    elif (m - CONSTS[3]) >= (Scale[3]*3):
        m_w = 6
    elif (m - CONSTS[3]) >= (Scale[3]*2):
        m_w = 5
    elif (m - CONSTS[3]) >= (Scale[3]*1):
        m_w = 4
    elif (m - CONSTS[3]) <= -(Scale[3]*4): 
        m_w = 0
    elif (m - CONSTS[3]) <= -(Scale[3]*3):
        m_w = 0
    elif (m - CONSTS[3]) <= -(Scale[3]*2):
        m_w = 1
    elif (m - CONSTS[3]) <= -(Scale[3]*1):
        m_w = 2
    elif (m - CONSTS[3]) > -(Scale[3]):
        m_w = 3

    print "T: %s, Scale: %s" % (t, Scale[0])
    print "H: %s, Scale: %s" % (h, Scale[1])
    print "P: %s, Scale: %s" % (p, Scale[2])
    print "M: %s, Scale: %s\n" % (m, Scale[3])
    
    w=[t_w, h_w, p_w, m_w]
    Printer(w)

    return t, p, h, m

#===================================================================================================

#------------------------------------PRINT-NUMBERS-------------------------------------
def PrintValues(mo, time, t, p, h, m):
    
    t_str = str(round(t, 1))
    p_str = str(round(p, 1))
    h_str = str(round(h, 1))
    m_str = str(round(m, 1))
    
    print_number_clear()

    if mo == 0:
        if time >= len(t_str):
            print('STOP')
            time = -1
        
            mo += 1
        else:
            temperature_yellow()
            
            if t_str[time] == '0':
                print_zero()
            elif t_str[time] == '1':
                print_one()
            elif t_str[time] == '2':
                print_two()
            elif t_str[time] == '3':
                print_three()
            elif t_str[time] == '4':
                print_four()
            elif t_str[time] == '5':
                print_five()
            elif t_str[time] == '6':
                print_six()
            elif t_str[time] == '7':
                print_seven()
            elif t_str[time] == '8':
                print_eight()
            elif t_str[time] == '9':
                print_nine()
            elif t_str[time] == '.':
                print_dot()
    elif mo == 1:
        if time >= len(h_str):
            print('STOP')
            time = -1
        
            mo += 1
        else:
            humidity_blue()
            
            if h_str[time] == '0':
                print_zero()
            elif h_str[time] == '1':
                print_one()
            elif h_str[time] == '2':
                print_two()
            elif h_str[time] == '3':
                print_three()
            elif h_str[time] == '4':
                print_four()
            elif h_str[time] == '5':
                print_five()
            elif h_str[time] == '6':
                print_six()
            elif h_str[time] == '7':
                print_seven()
            elif h_str[time] == '8':
                print_eight()
            elif h_str[time] == '9':
                print_nine()
            elif h_str[time] == '.':
                print_dot()
    elif mo == 2:
        if time >= len(p_str):
            print('STOP')
            time = -1
        
            mo += 1
        else:
            pressure_green()
            
            if p_str[time] == '0':
                print_zero()
            elif p_str[time] == '1':
                print_one()
            elif p_str[time] == '2':
                print_two()
            elif p_str[time] == '3':
                print_three()
            elif p_str[time] == '4':
                print_four()
            elif p_str[time] == '5':
                print_five()
            elif p_str[time] == '6':
                print_six()
            elif p_str[time] == '7':
                print_seven()
            elif p_str[time] == '8':
                print_eight()
            elif p_str[time] == '9':
                print_nine()
            elif p_str[time] == '.':
                print_dot()
    elif mo == 3:
        if time >= len(m_str):
            print('STOP')
            time = -1
        
            mo = 0
        else:
            magnetic_red()
            
            if m_str[time] == '0':
                print_zero()
            elif m_str[time] == '1':
                print_one()
            elif m_str[time] == '2':
                print_two()
            elif m_str[time] == '3':
                print_three()
            elif m_str[time] == '4':
                print_four()
            elif m_str[time] == '5':
                print_five()
            elif m_str[time] == '6':
                print_six()
            elif m_str[time] == '7':
                print_seven()
            elif m_str[time] == '8':
                print_eight()
            elif m_str[time] == '9':
                print_nine()
            elif m_str[time] == '.':
                print_dot()
            
        
    time += 1
    return mo, time, t_str, h_str, p_str, m_str
#================================================================================================

#----------------------------------PREDEFINED-NUMBERS----------------------------------
def print_one():
    Sense.set_pixel(0, 7, w)
    Sense.set_pixel(0, 6, w)
    Sense.set_pixel(0, 5, w)
    Sense.set_pixel(0, 4, w)
    Sense.set_pixel(0, 3, w)

def print_two():
    Sense.set_pixel(1, 7, w)
    Sense.set_pixel(2, 7, w)
    Sense.set_pixel(3, 6, w)
    Sense.set_pixel(0, 6, w)
    Sense.set_pixel(1, 5, w)
    Sense.set_pixel(2, 4, w)
    Sense.set_pixel(0, 3, w)
    Sense.set_pixel(1, 3, w)
    Sense.set_pixel(2, 3, w)
    Sense.set_pixel(3, 3, w)

def print_three():
    Sense.set_pixel(0, 7, w)
    Sense.set_pixel(1, 7, w)
    Sense.set_pixel(2, 7, w)
    Sense.set_pixel(0, 6, w)
    Sense.set_pixel(0, 5, w)
    Sense.set_pixel(1, 5, w)
    Sense.set_pixel(2, 5, w)
    Sense.set_pixel(0, 4, w)
    Sense.set_pixel(0, 3, w)
    Sense.set_pixel(1, 3, w)
    Sense.set_pixel(2, 3, w)

def print_four():
    Sense.set_pixel(3, 7, w)
    Sense.set_pixel(1, 6, w)
    Sense.set_pixel(3, 6, w)
    Sense.set_pixel(0, 5, w)
    Sense.set_pixel(1, 5, w)
    Sense.set_pixel(2, 5, w)
    Sense.set_pixel(3, 5, w)
    Sense.set_pixel(1, 4, w)
    Sense.set_pixel(1, 3, w)

def print_five():
    Sense.set_pixel(0, 7, w)
    Sense.set_pixel(1, 7, w)
    Sense.set_pixel(2, 7, w)
    Sense.set_pixel(3, 7, w)
    Sense.set_pixel(3, 6, w)
    Sense.set_pixel(0, 5, w)
    Sense.set_pixel(1, 5, w)
    Sense.set_pixel(2, 5, w)
    Sense.set_pixel(3, 5, w)
    Sense.set_pixel(0, 4, w)
    Sense.set_pixel(0, 3, w)
    Sense.set_pixel(1, 3, w)
    Sense.set_pixel(2, 3, w)
    Sense.set_pixel(3, 3, w)

def print_six():
    Sense.set_pixel(0, 7, w)
    Sense.set_pixel(1, 7, w)
    Sense.set_pixel(2, 7, w)
    Sense.set_pixel(3, 7, w)
    Sense.set_pixel(3, 6, w)
    Sense.set_pixel(0, 5, w)
    Sense.set_pixel(1, 5, w)
    Sense.set_pixel(2, 5, w)
    Sense.set_pixel(3, 5, w)
    Sense.set_pixel(0, 4, w)
    Sense.set_pixel(3, 4, w)
    Sense.set_pixel(0, 3, w)
    Sense.set_pixel(1, 3, w)
    Sense.set_pixel(2, 3, w)
    Sense.set_pixel(3, 3, w)

def print_seven():
    Sense.set_pixel(0, 7, w)
    Sense.set_pixel(1, 7, w)
    Sense.set_pixel(2, 7, w)
    Sense.set_pixel(3, 7, w)
    Sense.set_pixel(0, 6, w)
    Sense.set_pixel(1, 5, w)
    Sense.set_pixel(2, 4, w)
    Sense.set_pixel(3, 3, w)

def print_eight():
    Sense.set_pixel(0, 7, w)
    Sense.set_pixel(1, 7, w)
    Sense.set_pixel(2, 7, w)
    Sense.set_pixel(3, 7, w)
    Sense.set_pixel(0, 6, w)
    Sense.set_pixel(3, 6, w)
    Sense.set_pixel(0, 5, w)
    Sense.set_pixel(1, 5, w)
    Sense.set_pixel(2, 5, w)
    Sense.set_pixel(3, 5, w)
    Sense.set_pixel(0, 4, w)
    Sense.set_pixel(3, 4, w)
    Sense.set_pixel(0, 3, w)
    Sense.set_pixel(1, 3, w)
    Sense.set_pixel(2, 3, w)
    Sense.set_pixel(3, 3, w)

def print_nine():
    Sense.set_pixel(0, 7, w)
    Sense.set_pixel(1, 7, w)
    Sense.set_pixel(2, 7, w)
    Sense.set_pixel(3, 7, w)
    Sense.set_pixel(0, 6, w)
    Sense.set_pixel(3, 6, w)
    Sense.set_pixel(0, 5, w)
    Sense.set_pixel(1, 5, w)
    Sense.set_pixel(2, 5, w)
    Sense.set_pixel(3, 5, w)
    Sense.set_pixel(0, 4, w)
    Sense.set_pixel(0, 3, w)
    Sense.set_pixel(1, 3, w)
    Sense.set_pixel(2, 3, w)
    Sense.set_pixel(3, 3, w)

def print_zero():
    Sense.set_pixel(0, 7, w)
    Sense.set_pixel(1, 7, w)
    Sense.set_pixel(2, 7, w)
    Sense.set_pixel(3, 7, w)
    Sense.set_pixel(0, 6, w)
    Sense.set_pixel(3, 6, w)
    Sense.set_pixel(0, 5, w)
    Sense.set_pixel(3, 5, w)
    Sense.set_pixel(0, 4, w)
    Sense.set_pixel(3, 4, w)
    Sense.set_pixel(0, 3, w)
    Sense.set_pixel(1, 3, w)
    Sense.set_pixel(2, 3, w)
    Sense.set_pixel(3, 3, w)

def print_dot():
    Sense.set_pixel(2, 3, w)

def print_number_clear():
    Sense.set_pixel(0, 7, e)
    Sense.set_pixel(1, 7, e)
    Sense.set_pixel(2, 7, e)
    Sense.set_pixel(3, 7, e)
    Sense.set_pixel(0, 6, e)
    Sense.set_pixel(1, 6, e)
    Sense.set_pixel(2, 6, e)
    Sense.set_pixel(3, 6, e)
    Sense.set_pixel(0, 5, e)
    Sense.set_pixel(1, 5, e)
    Sense.set_pixel(2, 5, e)
    Sense.set_pixel(3, 5, e)
    Sense.set_pixel(0, 4, e)
    Sense.set_pixel(1, 4, e)
    Sense.set_pixel(2, 4, e)
    Sense.set_pixel(3, 4, e)
    Sense.set_pixel(0, 3, e)
    Sense.set_pixel(1, 3, e)
    Sense.set_pixel(2, 3, e)
    Sense.set_pixel(3, 3, e)
    
def temperature_yellow():
    Sense.set_pixel(0, 0, y)
    Sense.set_pixel(1, 0, y)
    Sense.set_pixel(1, 1, y)
    Sense.set_pixel(0, 1, y)

def humidity_blue():
    Sense.set_pixel(0, 0, b)
    Sense.set_pixel(1, 0, b)
    Sense.set_pixel(1, 1, b)
    Sense.set_pixel(0, 1, b)

def pressure_green():
    Sense.set_pixel(0, 0, g)
    Sense.set_pixel(1, 0, g)
    Sense.set_pixel(1, 1, g)
    Sense.set_pixel(0, 1, g)

def magnetic_red():
    Sense.set_pixel(0, 0, r)
    Sense.set_pixel(1, 0, r)
    Sense.set_pixel(1, 1, r)
    Sense.set_pixel(0, 1, r)
#==============================================================================================
    

#-------------------------------------SAVE-DATA-TO-FILE-------------------------------------
def SaveToFile(t, p, h, m, cal):
    global solarFlareDetected
    if (cal % 30 == 0) or (solarFlareDetected == True):
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%d-%m-%Y')

        file = open(current_date + ' - SenseYourLife', 'a')
        file.write(current_time + ': T=' + t + ' H=' + h + ' P=' + p + ' M=' + m + '\n')
        solarFlareDetected = False
        file.close()
#==========================================================================================

print CONSTS
#-------------------------------------MAIN-LOOP-------------------------------------
while True:
    t, p, h, m = PrintResults()
    mode, timer, t_str, h_str, p_str, m_str = PrintValues(mode, timer, t, p, h, m)
    
    T = Thread(target=Sense.Print)
    T.start()
    T2 = Thread(target=SaveToFile,args=(t_str, p_str, h_str, m_str, calc))
    T2.start()
    time.sleep(1)
    calc += 1
#===================================================================================
