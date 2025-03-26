#This script is to automatize the generation of the plots from Furuno radar and post them in the website
#Author Eric Tellez, May 2022

Write-Output "This program is converting the raw data to images and sending those images to the web server"

#First, we need to copy the last files from the FTPRadar folder which is the folder receiving the data from Altzomoni
$Sourcefolder= "D:\RecData" #It must be the folder from the FTP
$Targetfolder= "D:\Medicion_actual"  #Any other folder
Get-ChildItem -Path $Sourcefolder -Recurse|
Where-Object {
  $_.LastWriteTime -gt [datetime]::Now.AddMinutes(-5)  #Minutes since the last radar routine. If you change the radar routine you must change this parameter too.
}| Copy-Item -Destination $Targetfolder


#Then we need to execute the converter of the SCN files to a netCDF format
$converter = 'D:\Convertidores\SCN2HDF5_Converter\SCN2HDF5_converter.exe'
Start-Process -Filepath $converter -WorkingDirectory D:\Convertidores\SCN2HDF5_Converter\


#Then we need to execute the python program inside wradlib environment
powershell -command "& 'C:\Users\radar1\anaconda3\shell\condabin\conda-hook.ps1' ; conda activate 'C:\Users\radar1\anaconda3'; conda activate 'C:\Users\radar1\anaconda3\envs\wradlib'; python 'c:\Users\radar1\Desktop\Furuno\plot_AllData_2D_H5.py'; python 'c:\Users\radar1\Desktop\Furuno\mosaic.py'; python 'c:\Users\radar1\Desktop\Furuno\vol-CAPPI_dbzh.py' "


#Then we need to send the output files to the Argos server
#This line is useful after using ssh-keygen already setup in both machines
scp -r -P 8022 D:/Carpeta_Imag/ u.geofisica@132.248.8.177:datos/


#Delete all the files but not the folders
Get-ChildItem -Path D:/Carpeta_Imag/ -Recurse -File | Remove-Item