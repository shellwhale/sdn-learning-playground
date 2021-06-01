REM USAGE : .\capture.cmd mn.r1 r1-eth0
"C:\Program Files\PuTTY\plink.exe" -ssh -no-antispoof -pw vagrant vagrant@192.168.0.71 "sudo docker exec %1 tcpdump -s0 -U -w - -i %2" | wireshark -i - -k
