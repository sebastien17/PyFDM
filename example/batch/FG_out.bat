copy /Y simple_protocol.xml D:\Programs\FlightGear\data\Protocol\
cd D:\Programs\FlightGear\bin\Win64\
fgfs.exe --fg-root=D:\Programs\FlightGear\ --generic=socket,out,30,127.0.0.1,5501,udp,simple_protocol
