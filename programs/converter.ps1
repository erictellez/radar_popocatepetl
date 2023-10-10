#First, we need to copy the last files from the FTPRadar folder which is the folder receiving the data from Altzomoni
$Sourcefolder= "C:\Users\radar1\Desktop\Carpeta Inicial" #It must be FTPRadar
$Targetfolder= "C:\Users\radar1\Desktop\Carpeta_Intermedia"  #Any other folder
Get-ChildItem -Path $Sourcefolder -Recurse|
Where-Object {
  $_.LastWriteTime -gt [datetime]::Now.AddMinutes(-150000)  #Minutes since the last radar routine. If you change the radar routine you must change this parameter too.
}| Copy-Item -Destination $Targetfolder