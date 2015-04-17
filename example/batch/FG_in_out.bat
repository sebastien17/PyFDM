copy /Y simple_protocol.xml "D:\Programs\FlightGear 3.4.0\data\Protocol\"
cd "D:\Programs\FlightGear 3.4.0\bin"

fgfs.exe  --fg-root="D:\\Programs\\FlightGear 3.4.0\\"  --native-fdm=socket,in,30,127.0.0.1,5500,udp  --fdm=null --generic=socket,out,20,127.0.0.1,5501,udp,simple_protocol
