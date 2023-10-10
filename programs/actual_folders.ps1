#This script is to automatize the generation of the plots from Furuno radar and post them in the website
#Author Eric Tellez, May 2022


#First, we need to copy the last files from the FTPRadar folder which is the folder receiving the data from Altzomoni
$Sourcefolder= "C:\FTP_Radar" #It must be FTPRadar
$Targetfolder= "D:\Medicion_actual"  #Any other folder
Get-ChildItem -Path $Sourcefolder -Recurse|
Where-Object {
  $_.LastWriteTime -gt [datetime]::Now.AddMinutes(-5)  #Minutes since the last radar routine. If you change the radar routine you must change this parameter too.
}| Copy-Item -Destination $Targetfolder


#Then we need to execute the converter of the SCN files to a netCDF format
$converter = 'C:\Convertidores\SCN2HDF5_Converter\SCN2HDF5_converter.exe'
Start-Process -Filepath $converter -WorkingDirectory C:\Users\radar1\Desktop\Convertidores\SCN2HDF5_Converter\


#Then we need to execute the python program inside wradlib environment
powershell -command "& 'C:\Users\radar1\anaconda3\shell\condabin\conda-hook.ps1' ; conda activate 'C:\Users\radar1\anaconda3'; conda activate 'C:\Users\radar1\anaconda3\envs\wradlib'; python 'c:\Users\radar1\Desktop\Furuno\plot_AllData_2D_H5.py' ;python 'c:\Users\radar1\Desktop\Programas_Furuno\vol-CAPPI_dBzh.py'"


#Then we need to send the output files to the Argos server
#This line is useful after using ssh-keygen to generate password
scp -r -P 8022 C:/Users/radar1/Desktop/Carpeta_Imag/ u.geofisica@132.248.8.177:

#Post a twitt in Twitter
Import-Module PSTwitterAPI
$OAuthSettings = @{
  ApiKey = $env:ApiKey
  ApiSecret = $env:ApiSecret
  AccessToken = $env:AccessToken
  AccessTokenSecret =$env:AccessTokenSecret
}
Set-TwitterOAuthSettings @OAuthSettings

# Send tweet to your timeline:
Send-TwitterStatuses_Update -status "Hello World!! @radarPopocatep #PSTwitterAPI"
