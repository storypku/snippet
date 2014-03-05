#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created:      Wed Mar  5 18:19:17 CST 2014
# Author:       Liu Jiaming <liujiaming@baicdata.com>
# Copyright:    Baicdata, Inc. All rights reserved
#
"""
本程序是供DPC项目使用的UDP发包工具，可以实时抓取指定网卡上的HTTP报文或者
离线的Pcap文件并解析砍掉链路层报文后，经由UDP Socket转发到目标机器的指定
端口上（目标机则在对应的网卡和端口上监听）。
"""

import sys
import socket
import pcapy
from impacket.ImpactDecoder import EthDecoder, LinuxSLLDecoder

class UdpSender:
    def __init__(self, pcapReader, dstIp, dstPort):
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = (dstIp, dstPort)
        # Query datalink type and instantiate the corresponding decoder
        datalink = pcapReader.datalink()
        if datalink == pcapy.DLT_EN10MB:
            self.decoder = EthDecoder()
        elif datalink == pcapy.DLT_LINUX_SLL:
            self.decoder = LinuxSLLDecoder()
        else:
            raise Exception("Datalink type not supported");
        self.pcapReader = pcapReader
        self.counter = 0

    def run(self):
        # Sniff ad infinitum
        # Packet handler will be invoked by pcap for every packet
        self.pcapReader.loop(0, self.packetHandler)

    def packetHandler(self, hdr, data):
        # Use the ImpactDecoder to turn the raw packet into a hierarchy of
        # ImpactPacket instances
        # Display the packet en human-readable form
        dl_header = self.decoder.decode(data)
        ip_header = dl_header.child()
        self.counter += 1
        data_to_send = ip_header.get_packet()
        self.socket_.sendto(data_to_send, self.dest)
        print "Transfered packet No. %d" % self.counter
        # tcp_header = ip_header.child()
        # http_header = tcp_header.child()
        # if http_packet.get_size() > 0:

def usageErr(prog):
    print "Usage:   %s --live    <interface> <dest-ip> <dest-port>     OR" % prog
    print "         %s --offline <pcapfile>  <dest-ip> <dest-port>"        % prog
    sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) != 5:
        usageErr(sys.argv[0])

    if sys.argv[1] == "--live":
        # interface, snaplen, promisc, to_ms
        pcapReader = pcapy.open_live(sys.argv[2], 2048, 1, 512)
    elif sys.argv[1] == "--offline":
        pcapReader = pcapy.open_offline(sys.argv[2])
    else:
        usageErr(sys.argv[0])

    dstIp = sys.argv[3];
    dstPort = int(sys.argv[4])

    pcapReader.setfilter("tcp port 80")

    worker = UdpSender(pcapReader, dstIp, dstPort)
    try:
        worker.run()
    except KeyboardInterrupt:
        print "Total packet received: %d, exiting..." % worker.counter
        sys.exit(0)
