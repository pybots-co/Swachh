#0.0.1
#ClointFusion Cleaner Developed by Karthik Kallur

import os
import shutil
import subprocess
import time
import threading
import platform
import pyautogui as pg
import PySimpleGUI as sg
import safety
import site  
from glob import glob
from pathlib import Path
import click

os_name = str(platform.system()).lower()

site_packages_path = next(p for p in site.getsitepackages() if 'site-packages' in p)
site_packages_path = str(site_packages_path).strip() 

bat_script = r"""
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Active Setup Temp Folders" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\BranchCache" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Downloaded Program Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\GameNewsFiles" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\GameStatisticsFiles" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\GameUpdateFiles" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Internet Cache Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Memory Dump Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Offline Pages Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Old ChkDsk Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Previous Installations" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Recycle Bin" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Service Pack Cleanup" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Setup Log Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\System error memory dump files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\System error minidump files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Temporary Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Temporary Setup Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Temporary Sync Files" /V StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Thumbnail Cache" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Update Cleanup" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Upgrade Discarded Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\User file versions" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Defender" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Error Reporting Archive Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Error Reporting Queue Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Error Reporting System Archive Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Error Reporting System Queue Files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows ESD installation files" /v StateFlags0108 /d 2 /t REG_DWORD /f
REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows Upgrade Log Files" /v StateFlags0108 /d 2 /t REG_DWORD /f"""

cwd = os.path.dirname(os.path.realpath(__file__)) #get cwd

sg.theme('Dark') 
sg.SetOptions(text_justification='center')

sg.Print("Welcome to Swachh: ClointFusion's PC Cleaner", do_not_reroute_stdout=True,font='Helvetica 14',keep_on_top= True,grab_anywhere=True, no_titlebar=True)
current_user = os.environ['USERPROFILE']

def diskUsage():
    try:
        _, _, free = shutil.disk_usage(current_user[0:3])
        free = free // (1024*1024)
        return free
    except Exception as ex:
        print("Error in diskUsage="+str(ex))

def cleaned(bfs,afs):
    tfs = afs - bfs
    return tfs

def createBatScript():
    try:
        with open('bat.bat','w') as file:
            file.write(bat_script)
        subprocess.call("powershell.exe Start-Process bat.bat -Verb runAs")
        time.sleep(2)
        subprocess.call("cleanmgr.exe /sagerun:108")
        deleteBatScript()
    except Exception as ex:
        print("Error in createBatScript="+str(ex))

def deleteBatScript():
    try:
        os.remove("bat.bat")
    except Exception as ex:
        print("Error in deleteBatScript="+str(ex))

def clean_site_packages():
    folder_lst=glob(site_packages_path + "/*/")
    for fldr in folder_lst:
        fldr_path = Path(fldr)
        if "~" in str(fldr_path.stem) or str(fldr_path.stem).startswith("-"):
            # print("Deleting broken folder(s) : {}".format(fldr_path))
            sg.Print("Deleting broken folder(s) : {}".format(fldr_path))
            # os.system("rmdir /q /s {}".format(fldr_path))
            shutil.rmtree(fldr_path)
            
def cleanup():
    try:
        temp_folder = os.path.join(current_user,'AppData','Local','temp','')
        temp2_folder = os.path.join(current_user[0:3],'Windows','Temp','')
        temp3_folder = os.path.join(current_user,'Temp','')
        

        folders = [temp_folder,temp2_folder,temp3_folder]

        for folder in folders:
            if os.path.exists(folder):
                shutil.rmtree(folder, ignore_errors=True)
        subprocess.call('powershell.exe Clear-RecycleBin -Force -ErrorAction SilentlyContinue')
    except Exception as ex:
        print("Error in cleanup="+str(ex))

def checkSafetyOfPythonPackages():
    try:
        _ , list_of_unsafe_packages = subprocess.getstatusoutput('powershell.exe safety check --bare')
        
        if list_of_unsafe_packages:
            sg.Print("Found unsafe packages.. Please uninstall vulnerable package(s) {} ".format(list_of_unsafe_packages))        
            # cmd = "powershell.exe pip uninstall -y '{}' ".format(list_of_unsafe_packages)
            # subprocess.call(cmd) 
        else:
            sg.Print("All installed packages are safe")

        # return
    except Exception as ex:
        print("Error in checkSafetyOfPythonPackages="+str(ex))
    
def main():
    try:
        before_free_space = diskUsage()

        # sg.Print("\nDeveloped by ClointFusion")
        sg.Print("\nYour computer is being cleaned now..")
        sg.Print("\nPlease wait, while we Delete Junk, Cache files and Boost your PC")

        t1 = threading.Thread(target=cleanup)
        t2 = threading.Thread(target=createBatScript)

        t2.start()
        t1.start()

        t1.join()
        t2.join()

        cleanup()  

        after_free_space = diskUsage()

        total_cleaned_space = cleaned(before_free_space, after_free_space)
        total_cleaned_space = max(total_cleaned_space, 0)
        sg.Print("\nTotal Disk space cleaned {} MB ".format(total_cleaned_space))

        sg.Print("\nDeleting broken folders from Site-Packages")
        clean_site_packages()

        sg.Print("\nChecking for unsafe Python packages..")
        checkSafetyOfPythonPackages()

        sg.Print("\nExiting..")

        time.sleep(3)

    except Exception as ex:
        print("Error in main="+str(ex))

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
def cli_launch_swachh():
    try:
        if os_name == "windows":
            sg.Print("\nSwachh, version 0.0.3")
            main()
        else:
            pg.alert("This feature works only on Windows OS !")

    except Exception as ex:
        print("Error in cli_launch_swachh="+str(ex))