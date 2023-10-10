#This program is to test the connection every five minutes
#Eric Tellez, March 2023

#To test the connection with a ping
$uno= Test-Connection -ComputerName 192.168.10.50 -Quiet     #IP address of computer in Geophysics Institute
$dos= Test-Connection -ComputerName 192.168.10.52 -Quiet     #IP address of radio transmitter in UNAM
$tres= Test-Connection -ComputerName 192.168.10.56 -Quiet    #IP address of radio transmitter in Altzomoni
$cuatro= Test-Connection -ComputerName 192.168.10.60 -Quiet  #IP address of computer in Altzomoni

#Write-Output $uno
#Write-Output $dos
#Write-Output $tres
#Write-Output $cuatro

#If some part of the connection is broken, then a robotic voice warns about it
if ( ($uno="False") -or ($dos="False") -or ($tres="False") -or ($cuatro="False") ) 
    { 
    (New-Object -com SAPI.SpVoice).speak("Ya se fregó la conexión")

    #To make a beep instead of the robotic voice
    #[console]::beep(1000,500)
    }