# 0.0.3
# ClointFusion Cleaner Developed by Karthik Kallur
# Contributor P.Murali Manohar Varma

import os
import shutil
import subprocess
import time
import platform
import site  
from glob import glob
from pathlib import Path
import click
import rich
from rich.console import JustifyMethod
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.columns import Columns
from rich import print
from rich.text import Text
import declutter_downloads


os_name = str(platform.system()).lower()

site_packages_path = site.getsitepackages()[1]

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

current_user = os.environ['USERPROFILE']

# UI 
summary = []

job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%",justify="center"),
)

job1 = job_progress.add_task("[magenta]Cleaning temp...", total=5)
job2 = job_progress.add_task("[cyan]Running scripts...", total=5)
job3 = job_progress.add_task("[red]Optimizing packages...", total=5)

total = sum(task.total for task in job_progress.tasks)
overall_progress = Progress(auto_refresh=True)
overall_task = overall_progress.add_task("Swachh", total=int(total))

text = Text(justify="center")
text.append("PC Cleaner / Tuner by ")
text.append("ClointFusion", style="bold magenta")

progress_table = Table.grid(pad_edge=True)
progress_table.add_row(Panel(text, border_style="magenta", padding=(1, 1)))
progress_table.add_row(
    Panel.fit(overall_progress, title="Overall Progress", border_style="green", padding=(2, 2)),
    Panel.fit(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
)

def update_over():
    completed = sum(task.completed for task in job_progress.tasks)
    overall_progress.update(overall_task, completed=completed)

# Logic

def diskUsage():
    try:
        _, _, free = shutil.disk_usage(current_user[0:3])
        free = free // (1024*1024)
        return free
    except Exception as ex:
        print("Error in diskUsage="+str(ex))

def cleaned(bfs,afs):
    return afs - bfs

def createBatScript(job_id):
    try:
        job_progress.advance(job_id, advance=1)
        update_over()
        with open('bat.bat','w') as file:
            file.write(bat_script)
            job_progress.advance(job_id, advance=1)
            update_over()
        subprocess.call("powershell.exe Start-Process bat.bat -Verb runAs")
        time.sleep(2)
        job_progress.advance(job_id, advance=1)
        update_over()
        subprocess.call("cleanmgr.exe /sagerun:108")
        job_progress.advance(job_id, advance=1)
        update_over()
        deleteBatScript(job_id)
    except Exception as ex:
        print("Error in createBatScript="+str(ex))

def deleteBatScript(job_id):
    try:
        os.remove("bat.bat")
        job_progress.advance(job_id, advance=1)
        update_over()
    except Exception as ex:
        print("Error in deleteBatScript="+str(ex))

def clean_site_packages(job_id):
    folder_lst=glob(site_packages_path + "/*/")
    points = len(folder_lst)/5
    deleted_folders = []
    for folder in folder_lst:
        folder_path = Path(folder)
        if "~" in str(folder_path.stem) or str(folder_path.stem).startswith("-"):
            shutil.rmtree(folder_path)
            deleted_folders.append(folder_path.stem)
        job_progress.advance(job_id, advance=points)
        update_over()
    if deleted_folders:
        printCommand(heading="Deleted Site Packages", description=deleted_folders)
    else:
        printCommand(heading="Your Site Packages are Good.", description="")
         
def cleanup(job_id):
    try:
        
        temp_folder = os.path.join(current_user,'AppData','Local','temp','')
        temp2_folder = os.path.join(current_user[0:3],'Windows','Temp','')
        temp3_folder = os.path.join(current_user,'Temp','')
        job_progress.advance(job_id, advance=1)
        update_over()
        

        folders = [temp_folder,temp2_folder,temp3_folder]

        for folder in folders:
            if os.path.exists(folder):
                shutil.rmtree(folder, ignore_errors=True)
                job_progress.advance(job_id, advance=1)
                update_over()
                

        subprocess.call('powershell.exe Clear-RecycleBin -Force -ErrorAction SilentlyContinue')
        job_progress.advance(job_id, advance=1)
        update_over()
        
    except Exception as ex:
        print("Error in cleanup="+str(ex))

def checkSafetyOfPythonPackages():
    try:
        _ , list_of_unsafe_packages = subprocess.getstatusoutput('powershell.exe safety check --bare')
        
        if list_of_unsafe_packages:
            printCommand(heading="Found unsafe packages.. Please uninstall vulnerable package(s):\n", description=list_of_unsafe_packages)       
            # cmd = "powershell.exe pip uninstall -y '{}' ".format(list_of_unsafe_packages)
            # subprocess.call(cmd) 
        else:
            printCommand("All installed packages are safe.", description="")

        # return
    except Exception as ex:
        print("Error in checkSafetyOfPythonPackages="+str(ex))

def printCommand(heading, description):
    global summary
    if type(description) == list:
        des = ["\n," + str(i) for i in description]
        description = "".join(des)
    command = f"[magenta][b]{heading}[/b][cyan][i]{'-' + description if  description else ''}[/i]"
    summary.append(command)

def main():
    try:
        global summary
        with Live(progress_table, refresh_per_second=10):
            
            perform_actions()
    except Exception as ex:
        print('Error in main=' + str(ex))

def perform_actions():   
    before_free_space = diskUsage()

    cleanup(job1)
    createBatScript(job2)
    cleanup(job1)

    after_free_space = diskUsage()

    total_cleaned_space = cleaned(before_free_space, after_free_space)
    total_cleaned_space = max(total_cleaned_space, 0)
    
    if total_cleaned_space == 0:
        printCommand(heading="Your Disk space is at Optimal level.", description="")
    else:
        printCommand(heading="Total Disk space cleaned", description=str(total_cleaned_space) + "MB")

    checkSafetyOfPythonPackages()
    clean_site_packages(job3)
    declutter_downloads.declutter_now()

    user_renderables = [Panel(i, expand=True) for i in summary]
    progress_table.add_row(Panel(Columns(user_renderables), title="Summary", border_style="cyan", padding=(1, 2)))

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
def cli_launch_swachh():
    try:
        if os_name == "windows":
            main()
        else:
            print("This feature works only on Windows OS !")

    except Exception as ex:
        print("Error in cli_launch_swachh="+str(ex))