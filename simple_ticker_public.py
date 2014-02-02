#!/usr/bin/env python
# set public_api_key and private_api_key to use :_) get these from cryptsy account settings
import curses, Cryptsy, time
public_api_key = 'public key goes here'
private_api_key = 'private key goes here'
data = [];
lasttradeprice = 0;
sellprices = [];
selltotals = [];
buyprices = [];
buytotals = [];
counter = 0;
height  = 0;

def drawEverything(window):
	window.addstr(1,1,"Puss's Ticker")
	window.addstr(1,onehalfw,"Last Trade Price: {d}".format(d=float(lasttradeprice)))
	window.addstr(3,onethirdw-11,"Sell Orders",curses.A_STANDOUT)
	window.addstr(3,2*onethirdw-11,"Buy Orders",curses.A_STANDOUT)
	window.addstr(height-2,1,"{a}".format(a=counter))
	printList("Price",4,2,sellprices,window)
	printList("Total",4,12,selltotals,window)
	printList("Price",4,2*onethirdw-10,buyprices,window)
	printList("Total",4,2*onethirdw,buytotals,window)
	window.border()

def printList(title,startY,startX,toPrint,window):
	global height
	window.addstr(startY,startX,"{t}".format(t=title),curses.A_BOLD)
	if(height - 7 > len(toPrint)):
		till = len(toPrint)
	else:
		till = height - 7
	for idx in range(1,till):
		add = float(toPrint[idx])
		window.addstr(startY+idx,startX,"{b}".format(b=add))

def pruneData(toPrune):
	global height
	if(len(toPrune) > height):
		for toPop in range(0,len(toPrune)-height):
			toPrune.pop(0)

def getData():
	global lasttradeprice
	global counter
	global sellprices
	global selltotals
	global buyprices
	global buytotals
	data = Exchange.getSingleMarketData(132)
	lasttradeprice = data['return']['markets']['DOGE']['lasttradeprice'];
	sellorders = data['return']['markets']['DOGE']['sellorders'];
	buyorders = data['return']['markets']['DOGE']['buyorders'];
	sellprices = [];	selltotals = [];	buyprices = [];	buytotals = [];
	for sale in sellorders:
		sellprices.append(sale['price']);
		selltotals.append(sale['total']);
	for sale in buyorders:
		buyprices.append(sale['price']);
		buytotals.append(sale['total']);
	sellprices = [float(x) for x in sellprices];
	selltotals = [float(x) for x in selltotals];
	buyprices = [float(x) for x in buyprices];
	buytotals = [float(x) for x in buytotals];
	#pruneData(sellprices)
	#pruneData(selltotals)
	#pruneData(buyprices)
	#pruneData(buytotals)

	counter+=1;

if __name__=='__main__':
	global height
	Exchange = Cryptsy.Cryptsy(public_api_key, private_api_key)
	getData();
	screen = curses.initscr()
	height,width = screen.getmaxyx()
	onehalfw = int(round(width / 2))
	onethirdw = int(round(width / 3))
	curses.noecho()
	curses.curs_set(0)
	screen.keypad(1)
	drawEverything(screen)

	while True:
	   #event = screen.getch()
	   #if event == ord("q"): break
	   #if event == ord("r"): getData(); counter+=1; drawEverything(screen); screen.refresh();
	   time.sleep(5)
	   getData(); drawEverything(screen); screen.refresh();
	curses.endwin()