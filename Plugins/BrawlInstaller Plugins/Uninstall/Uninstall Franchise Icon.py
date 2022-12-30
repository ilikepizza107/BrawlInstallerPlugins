__author__ = "Squidgy"

from BrawlInstallerLib import *
from InstallLib import *
from BrawlInstallerForms import *

def main():
		try: 
			if str(BrawlAPI.RootNode) != "None":
				BrawlAPI.CloseFile()
			if not MainForm.BuildPath:
				BrawlAPI.ShowMessage("Build path must be set. This can be done by navigating to Tools > Settings > General and setting the 'Default Build Path' to the path to your build's root folder.", "Build Path Not Set")
				return
			if not Directory.Exists(MainForm.BuildPath + '/pf/'):
				BrawlAPI.ShowMessage("Build path does not appear to be valid. Please change your build path by going to 'Tools > Settings' and modifying the 'Default Build Path' field.\n\nYour build path should contain a folder named 'pf' within it.", "Invalid Build Path")
				return
			# Get user settings
			if File.Exists(MainForm.BuildPath + '/settings.ini'):
				settings = getSettings()
			else:
				settings = initialSetup()
			if not settings:
				return
			createLogFile()

			# If temporary directory already exists, delete it to prevent duplicate files
			if Directory.Exists(AppPath + '/temp'):
				Directory.Delete(AppPath + '/temp', 1)

			# Franchise Icon ID prompt
			franchiseIconId = showIdForm("Uninstall Franchise Icon", "Uninstall", "franchiseImage", "Franchise Icon ID:")
			if franchiseIconId:
				franchiseIconId = int(franchiseIconId, 16)
			else:
				return

			# Set up progressbar
			progressCounter = 0
			progressBar = ProgressWindow(MainForm.Instance, "Uninstalling Franchise Icon...", "Uninstalling Franchise Icon", False)
			progressBar.Begin(0, 5, progressCounter)

			# Uninstall from sc_selcharacter
			removeFranchiseIcon(franchiseIconId, '/pf/menu2/sc_selcharacter.pac')
			fileOpened = checkOpenFile("sc_selcharacter")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			# info.pac
			removeFranchiseIcon(franchiseIconId, '/pf/info2/info.pac')
			fileOpened = checkOpenFile("info")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			# single player cosmetics
			if settings.installSingleplayerCosmetics == "true":
				for file in Directory.GetFiles(MainForm.BuildPath + '/pf/info2/', "*.pac"):
					fileName = getFileInfo(file).Name
					if fileName != "info.pac":
						# Franchise icons first
						removeFranchiseIcon(franchiseIconId, '/pf/info2/' + fileName)
						fileOpened = checkOpenFile(fileName.split('.pac')[0])
						if fileOpened:
							BrawlAPI.SaveFile()
							BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			# STGRESULT
			removeFranchiseIconResult(franchiseIconId)
			fileOpened = checkOpenFile("STGRESULT")
			if fileOpened:
				BrawlAPI.SaveFile()
				BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)

			# SSE
			if settings.installToSse == "true":
				removeFranchiseIcon(franchiseIconId, '/pf/menu2/if_adv_mngr.pac')
				fileOpened = checkOpenFile("if_adv_mngr")
				if fileOpened:
					BrawlAPI.SaveFile()
					BrawlAPI.ForceCloseFile()

			progressCounter += 1
			progressBar.Update(progressCounter)
			progressBar.Finish()

			# Delete temporary directory
			if Directory.Exists(AppPath + '/temp'):
				Directory.Delete(AppPath + '/temp', 1)
			archiveBackup()
			BrawlAPI.ShowMessage("Franchise icon uninstalled successfully.", "Success")

		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()


main()