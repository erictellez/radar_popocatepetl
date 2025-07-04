#This program is to test the connection
#With help of Task Scheduler of Windows we can test the connection every some minutes
#Eric Tellez, March 2023

Write-Output "This program is testing the connection to Altzomoni"

#To test the connection with a ping
$uno= Test-Connection -ComputerName 192.168.10.50 -Quiet     #IP address of computer in Geophysics Institute
$dos= Test-Connection -ComputerName 192.168.10.52 -Quiet     #IP address of radio transmitter in UNAM
$tres= Test-Connection -ComputerName 192.168.10.56 -Quiet    #IP address of radio transmitter in Altzomoni
$cuatro= Test-Connection -ComputerName 192.168.10.60 -Quiet  #IP address of computer in Altzomoni

#Write-Output $uno
#Write-Output $dos
#Write-Output $tres
#Write-Output $cuatro


if ( ($uno -match "False") -or ($dos -match "False") -or ($tres -match "False") -or ($cuatro -match "False") ) 
    { 
    #If some part of the connection is broken, then a robotic voice warns about it
    (New-Object -com SAPI.SpVoice).speak("Falló la conexión")
    
    #This piece of code is to send a message to Telegram when the connection fails
    $Telegramtoken = ""
    $Telegramchatid = ""
    $Message = "Falló la conexión"

    [Net.ServicePointManager]::Expect100Continue = $true
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

    $irmParams = @{
        Uri = "https://api.telegram.org/bot$($Telegramtoken)/sendMessage?chat_id=$($Telegramchatid)&text=$($Message)"
    }

    $Response = Invoke-RestMethod @irmParams
    
    #To make a beep instead of the robotic voice
    #[console]::beep(1000,500)
    }
