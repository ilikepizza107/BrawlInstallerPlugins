__author__ = "Squidgy"

from BrawlInstallerForms import *
from UninstallLib import *
from System.Drawing import Bitmap

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
			backupCheck()

			# User input
			form = CostumePrompt(uninstall=True)
			result = form.ShowDialog(MainForm.Instance)
			if result == DialogResult.OK:
				fighterId = hexId(form.fighterIdTextbox.Text).split('0x')[1].upper()
				cosmeticId = int(hexId(form.cosmeticIdTextbox.Text).replace('0x',''), 16)
				cssSlotConfigId = hexId(form.cssSlotConfigIdTextbox.Text).split('0x')[1].upper()
			else:
				return
			images = []
			positions = []
			newPositions = []
			skipPositions = []

			# Get costumes
			if File.Exists(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres'):
				BrawlAPI.OpenFile(MainForm.BuildPath + '/pf/menu/common/char_bust_tex/MenSelchrFaceB' + addLeadingZeros(str(cosmeticId), 2) + '0.brres')
				texFolder = getChildByName(BrawlAPI.RootNode, "Textures(NW4R)")
				costumeSet = True
				i = 0
				for node in texFolder.Children:
					if costumeSet:
						images.append(Bitmap(node.GetImage(0)))
						positions.append(i)
						costumeSet = True
					if node.SharesData:
						costumeSet = False
					else:
						costumeSet = True
					i += 1
						
				BrawlAPI.ForceCloseFile()

				# Get the costumes as indicated by stock icons
				stocksChecked = False
				if settings.installStocksToCSS == "true" and not stocksChecked:
					newPositions = checkStockIcons(cosmeticId, "Misc Data [90]", rootName="", filePath='/pf/menu2/sc_selcharacter.pac', fiftyCC=settings.fiftyCostumeCode)
					stocksChecked = True
				if settings.installStockIconsToResult == "true" and not stocksChecked:
					newPositions = checkStockIcons(cosmeticId, "Misc Data [120]", rootName="2", filePath='/pf/stage/melee/STGRESULT.pac', fiftyCC=settings.fiftyCostumeCode)
					stocksChecked = True
				if settings.installStocksToInfo == "true" and not stocksChecked:
					newPositions = checkStockIcons(cosmeticId, "Misc Data [30]", rootName="", filePath='/pf/info2/info.pac', fiftyCC=settings.fiftyCostumeCode)
					stocksChecked = True
				if settings.installStocksToStockFaceTex == "true" and not stocksChecked:
					newPositions = checkStockIcons(cosmeticId, "", rootName="", filePath='/pf/menu/common/StockFaceTex.brres', fiftyCC=settings.fiftyCostumeCode)
					stocksChecked = True
				if settings.installStocksToSSS == "true" and not stocksChecked:
					newPositions = checkStockIcons(cosmeticId, "Misc Data [40]", rootName="", filePath='/pf/menu2/sc_selmap.pac', fiftyCC=settings.fiftyCostumeCode)
					stocksChecked = True

				# Filter out costumes where stock and CSP color smash groups don't match			
				i = 0
				length = len(positions)
				while i < length:
					if positions[i] not in newPositions:
						skipPositions.append(i)
					i += 1

				# Show the form
				form = CostumeForm(images=images, skipPositions=skipPositions, remove=True)
				result = form.ShowDialog(MainForm.Instance)

				if result == DialogResult.OK:
					uninstallCostume(cosmeticId, fighterId, cssSlotConfigId, form.index, skipPositions)
			else:
				BrawlAPI.ShowMessage("Cosmetics for this fighter could not be found! Please try a different ID.", "Error")

		except Exception as e:
			writeLog("ERROR " + str(e))
			if 'progressBar' in locals():
				progressBar.Finish()
			BrawlAPI.ShowMessage(str(e), "An Error Has Occurred")
			BrawlAPI.ShowMessage("Error occured. Backups will be restored automatically. Any added files may still be present.", "An Error Has Occurred")
			restoreBackup()
			archiveBackup()



main()