#Function Send-Telegram {
#Param ([Parameter(Mandatory=$true)][String]$Message)
$Telegramtoken = "6156678877:AAEtwGzJSd3OqnXlScsYSfydQPMjgHDEXXY"
$Telegramchatid = "622176669"
$Message = "Falló la conexión"

[Net.ServicePointManager]::Expect100Continue = $true
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$irmParams = @{
  Uri = "https://api.telegram.org/bot$($Telegramtoken)/sendMessage?chat_id=$($Telegramchatid)&text=$($Message)"
}

$Response = Invoke-RestMethod @irmParams
#}
#$Response = Invoke-RestMethod -Uri "https://api.telegram.org/bot$($Telegramtoken)/sendMessage?chat_id=$($Telegramchatid)&text=$($Message)"}