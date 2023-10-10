#This program is to perform a routine check in the IP configuration in the Altzomoni computer once in a while
#We maybe even use it to perform some troubleshooting


#Need to check all the IP numbers
ipconfig
#Then ping to every connection number
Test-Connection

# If some ping is not responding then start the troubleshooting.
$condition = $true
if ( $condition )
{
    Write-Output "The Condition was true"
}

Start-Process IPconfig

