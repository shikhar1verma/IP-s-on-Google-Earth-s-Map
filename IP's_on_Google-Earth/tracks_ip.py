#!/usr/bin/env python
'''
this script get the source and destination ip
from the pcap file and show the ip's on Google
Eaerth through kml file.
'''
import dpkt         #to extract source and destination IP
import socket
import pygeoip      #to get the longitutde and latitude from the dat file of the ip's

gi = pygeoip.GeoIP('/home/shikhar/Documents/python-cdac/geoip-dat/GeoLiteCity.dat') #path of dat file

def retKML(ip):                                         #making of kml file
	rec = gi.record_by_name(ip)
	try:
		longitude = rec['longitude']
		latitude = rec['latitude']
		kml = ( '<Placemark>\n'                 #kml file foemat
			'<name>%s</name>\n'
			'<Point>\n'
			'<coordinates>%6f,%6f</coordinates>\n'
			'</Point>\n'    '</Placemark>\n')%(ip,longitude, latitude)
		return kml
	except:
		return ' '

def plotIPs(pcap):                                          #get the source and destination ip from pcap file through dpkt
	kmlPts = ''
	for (ts, buf) in pcap:
		try:
			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src = socket.inet_ntoa(ip.src)
			srcKML = retKML(src)
			dst = socket.inet_ntoa(ip.dst)
			dstKML = retKML(dst)
			kmlPts = kmlPts + srcKML + dstKML   #middle part of kml file
		except:
			pass
	return kmlPts

def main():
	pcapFile='/home/shikhar/Documents/python-cdac/Lecture4-3/assignment1/my_network_traffic.pcap'   #path  og pcap file
	f = open(pcapFile,'r')
	d = open('/home/shikhar/Documents/python-cdac/Lecture4-3/assignment1/GEarth.kml','w')           #path of kml file
	pcap = dpkt.pcap.Reader(f)
	kmlheader = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'    #header of kml
	kmlfooter = '</Document>\n</kml>\n'                                                                                 #footer of kml
	kmldoc=kmlheader+plotIPs(pcap)+kmlfooter            #whole kml file
	print kmldoc
	d.write(kmldoc)
	d.close()
if __name__ == '__main__': main()

