__author__ = "Squidgy"

from BrawlInstallerLib import *

def main():
		# Check our backups
		createLogFile()
		backupCheck()
		backups = Directory.GetDirectories(BASE_BACKUP_PATH)
		if len(backups) <= 0:
			BrawlAPI.ShowMessage("No backups found!", "No Backups Found")
			return
		i = 1
		backupString = ""
		# Gather up backup options
		for backup in backups:
			backupString = backupString + str(i) + ' : ' + DirectoryInfo(backup).Name + '\n'
			i += 1
		BrawlAPI.ShowMessage("You will be prompted to enter an integer corresponding to one of your backups. Please enter a number corresponding to one of the below options, or enter 0 to cancel: \n" + backupString, "Backups")
		backupChoice = BrawlAPI.UserIntegerInput("Enter Backup Number", "Backup Number: ", 0, 0, i)
		if backupChoice > 0:
			restoreBackup(backups[backupChoice - 1])

main()