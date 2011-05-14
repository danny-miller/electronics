"""
J.C. Woltz's Portal Script. 
setRFTime function written by me.

get_temp_logger written by Synapse Wireless
F4Swu7Aruphewume

at this point, many other synapse example functions added
"""
"""
    logSupport.py - one method of supporting "log to file" functionality

    Makes use of the standard logging capabilities of Python
"""

import logging, logging.handlers, datetime, time, codecs, os


import binascii
import time

#import thermistor
import wx
buttonCount = 0
frame = None

CSV_FILENAME = "tempDataLog.csv"

def setRFTime(nodeAddr):
    """Call with nodeAddr to set the time on that node"""
    Year = int(time.strftime('%y'))
    Month = int(time.strftime('%m'))
    Date = int(time.strftime('%d'))
    Hour = int(time.strftime('%H'))
    Minute = int(time.strftime('%M'))
    Second = int(time.strftime('%S'))
    DOW = int(time.strftime('%w'))
    
    rpc(nodeAddr, "writeClockTime", Year, Month, Date, DOW, Hour, Minute, Second)
    
def setRFPCF2129Time():
    """Call with nodeAddr to set the time on that node"""
    Year = int(time.strftime('%y'))
    Month = int(time.strftime('%m'))
    Date = int(time.strftime('%d'))
    Hour = int(time.strftime('%H'))
    Minute = int(time.strftime('%M'))
    Second = int(time.strftime('%S'))
    DOW = int(time.strftime('%w'))
    
    mcastrpc(1, 3, "writeClockTime", Year, Month, Date, DOW, Hour, Minute, Second)
    
def pingESCO():
    rpc("\x00\x31\x56", "vmStat", 10)

def dispayLastWriteAddress(tt):
    remoteNode.setColumn("Next EEPROM Address", tt)
    
def WakeAlert(Minutes, Seconds):
    eventString = str(Minutes) + " " + str(Seconds)
    remoteNode.setColumn("Wake At",eventString)
    #rpc(remoteAddr, "portalcmdsleep")

def WakeDisplay(Years, Months, Days, DOW, Hours, Minutes, Seconds):
    
    if (Months < 10):
        Months = str(0) + str(Months)
    if (Days < 10):
        Days = str(0) + str(Days)
    if (Hours < 10):
        Hours = str(0) + str(Hours)
    if (Minutes < 10):
        Minutes = str(0) + str(Minutes)    
    if (Seconds < 10):
        Seconds = str(0) + str(Seconds)
    eventString = str(displayDOW(DOW)) + " " + str(20) + str(Years) + "." + str(Months) + "." + str(Days) + " " + str(Hours) + ":" +  str(Minutes) + ":" + str(Seconds)
    #eventString = str(Minutes) + " " + str(Seconds)
    remoteNode.setColumn("Wake At",eventString)
    #rpc(remoteAddr, "portalcmdsleep")

def displayDOW(DOW):
    if (DOW == 0):
        Day = "Sun"
    if (DOW == 1):
        Day = "Mon"
    if (DOW == 2):
        Day = "Tues"
    if (DOW == 3):
        Day = "Wed"
    if (DOW == 4):
        Day = "Thu"
    if (DOW == 5):
        Day = "Fri"
    if (DOW == 6):
        Day = "Sat"
    if (DOW == 7):
        Day = "Sun"
    return Day
    
###############################################################################
## Below is from Synapse Wireless    ##########################################
## Some are modified  #########################################################
###############################################################################
def plotlq(who, lq, dts): 
    logData(who,lq,128)
    remoteNode.setColumn("Link", lq)
    remoteNode.setColumn("DT", dts)

def infoDT(dts):
    remoteNode.setColumn("DT", dts)
    
def infoLQ(who, lq):
    remoteNote.SetColumn("Link", dts)
    

def get_portal_logger():
    rpc(remoteAddr, "set_portal_addr", Portal.netAddr)

def adc_to_resistance(adc_val):
    return PULLUP_RESISTOR * adc_val / (ADC_FULLSCALE - adc_val)

def doRollover(self):
    """
    do a rollover; in this case, a date/time stamp is appended to the filename
    when the rollover happens.  However, you want the file to be named for the
    start of the interval, not the current time.  If there is a backup count,
    then we have to get a list of matching filenames, sort them and remove
    the one with the oldest suffix.
    """
    self.stream.close()
    # get the time that this sequence started at and make it a TimeTuple
    t = self.rolloverAt - self.interval
    timeTuple = time.localtime(t)
    (path, filename) = os.path.split(self.baseFilename)
    (root, ext) = os.path.splitext(filename)
    dfn = path + os.path.sep + root + "_" + time.strftime(self.suffix, timeTuple) + ext
    if os.path.exists(dfn):
        os.remove(dfn)
    os.rename(self.baseFilename, dfn)
    if self.backupCount > 0:
        # find the oldest log file and delete it
        s = glob.glob(self.baseFilename + ".20*")
        if len(s) > self.backupCount:
            s.sort()
            os.remove(s[0])
    #print "%s -> %s" % (self.baseFilename , dfn)
    if self.encoding:
        self.stream = codecs.open(self.baseFilename, 'w', self.encoding)
    else:
        self.stream = open(self.baseFilename, 'w')
    self.rolloverAt = self.rolloverAt + self.interval

def logToFile(this, baseName, logInfo):
    """
    Writes an entry to the specified logfile. Caller provides the baseName,
    the logging facility will append timestamps to this baseName as needed.
    "this" must be the object considered to "own" the logfile (can be root)
    "logInfo" is the text to be logged, and it will automatically be preceeded
    by a timestamp.
    """
    log = logging.getLogger(baseName)

    try:
        this.logSetup == True
    except:
        #First time through this.logSetup won't exist
        logging.handlers.TimedRotatingFileHandler.doRollover = doRollover

        log.setLevel(logging.DEBUG)
        handler = logging.handlers.TimedRotatingFileHandler ("%s.log" % (baseName), 'midnight', 1)
        formatter = logging.Formatter ("%(asctime)s.%(msecs)d\t%(message)s", datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        this.logSetup = True
    log.info(logInfo)
    
def setButtonCount(newCount):
    """Called by multicastCounter nodes to set new count"""
    global frame
    
    if not frame:
        frame = McastFrame(root)

    frame.displayButtonCount(newCount)
    
    
class McastFrame(wx.Frame):
    """Main window frame"""
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Synapse Multicast Counter", style = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.panel = McastPanel(self)
        self.Show(True)

    def onClose(self, event):
        self.Destroy()

    def displayButtonCount(self, newCount):
        self.panel.sc.SetValue(newCount)
        self.panel.text.SetLabel('%d' % newCount)
        self.Refresh()
        
        
class McastPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.mcastFrame = parent
        box = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(box)
        
        self.text = wx.StaticText(self, -1, "0", (30, 40))
        font = wx.Font(72, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, "Courier New")
        self.text.SetFont(font)
        box.Add(self.text, 1, wx.ALIGN_CENTER)
        
        self.sc = wx.SpinCtrl(self, -1, "", (30, 40), style = wx.SP_ARROW_KEYS | wx.SP_WRAP)
        self.sc.SetRange(0,99)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpin, self.sc)
        box.Add(self.sc, 0, wx.ALIGN_CENTER)

    def OnSpin(self, event):
        global buttonCount
        buttonCount = event.Selection
        self.text.SetLabel('%d' % buttonCount)
        multicastRpc(1, 2, 'setButtonCount', buttonCount)
    

if __name__ == '__main__':
    """Mcast Test""" 
    class MyApp(wx.App):
        def OnInit(self):
            self.frame = McastFrame(None)
            self.SetTopWindow(self.frame)
            return True


    app = MyApp(0)
    app.MainLoop()

