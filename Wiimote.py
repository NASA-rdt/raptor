import cwiid 
import time  
def connect():
	#connecting to the Wiimote. This allows several attempts 
	# as first few often fail. 
	print 'Press 1+2 on your Wiimote now...'  
	i=2 
	wm = None
	while not wm: 
	  try: 
	    wm=cwiid.Wiimote() 
	    print "wm is not none"
	  except RuntimeError: 
	    if (i>10): 
	      quit() 
	      break 
	    print "Error opening wiimote connection" 
	    print "attempt " + str(i) 
	    i +=1 
	
	#set Wiimote to report button presses and accelerometer state 
	wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC 
	 
	#turn on led to show connected 
	wm.led = 1
	
	return wm
if __name__ == '__main__':
	connect()

