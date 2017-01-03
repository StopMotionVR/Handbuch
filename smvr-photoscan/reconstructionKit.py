import urllib.request
import PhotoScan
import pseudoGlobals
from stateMachine import *
import sys
import os
import shutil
import time


##########################################################
# config variables (declaration and default fallback)
##########################################################
qualityLevels_MatchingAccuracy = [PhotoScan.LowestAccuracy, PhotoScan.LowAccuracy, PhotoScan.MediumAccuracy, PhotoScan.HighAccuracy, PhotoScan.HighestAccuracy]
configQuality_MatchingAccuracy = PhotoScan.MediumAccuracy

qualityLevels_MatchingPreselection = [PhotoScan.NoPreselection, PhotoScan.ReferencePreselection, PhotoScan.GenericPreselection]
configQuality_MatchingPreselection = PhotoScan.GenericPreselection

qualityLevels_DenseCloudQuality = [PhotoScan.LowestQuality, PhotoScan.LowQuality, PhotoScan.MediumQuality, PhotoScan.HighQuality, PhotoScan.UltraQuality]
configQuality_DenseCloudQuality = PhotoScan.LowQuality

qualityLevels_Interpolation = [PhotoScan.DisabledInterpolation, PhotoScan.EnabledInterpolation, PhotoScan.Extrapolated]
configQuality_Interpolation = PhotoScan.EnabledInterpolation

configQuality_FaceCount = 10000

qualityLevels_UVMappingMode = [PhotoScan.GenericMapping, PhotoScan.OrthophotoMapping, PhotoScan.AdaptiveOrthophotoMapping, PhotoScan.SphericalMapping, PhotoScan.CameraMapping]
configQuality_UVMappingMode = PhotoScan.SphericalMapping

configQuality_DiffuseTextureSize = 256

qualityLevels_DiffuseBlendingMode = [PhotoScan.DisabledBlending, PhotoScan.AverageBlending, PhotoScan.MosaicBlending, PhotoScan.MinBlending, PhotoScan.MaxBlending]
configQuality_DiffuseBlendingMode = PhotoScan.MosaicBlending

processFolderPath = "/"
photoList = []
exportFolderPath = "/"


def checkForStop():
	if pseudoGlobals.shouldInterruptReconstruction:
		print("Cleaning project...")
		PhotoScan.app.document.clear() 
		return True
	return False
	
def progressCallback(progress):
	pseudoGlobals.currentRelativeProgress = progress / 100.0
	setStep(pseudoGlobals.currentAbsoluteStep) # force absolute progress update
	
def setStep(current, totalSteps = 8):
	pseudoGlobals.currentAbsoluteStep = current
	pseudoGlobals.currentAbsoluteProgress = (float(current) / float(totalSteps)) + (pseudoGlobals.currentRelativeProgress / float(totalSteps))
	
def startReconstruction(arguments = ['']): # = ['-ProcessFolder=\\\\berry\\ray\\schuh']):
	
	global configQuality_MatchingAccuracy
	global configQuality_MatchingPreselection
	global configQuality_DenseCloudQuality
	global configQuality_Interpolation
	global configQuality_FaceCount
	global configQuality_UVMappingMode
	global configQuality_DiffuseTextureSize
	global configQuality_DiffuseBlendingMode
	global processFolderPath
	global photoList
	global exportFolderPath
	
	# basic stuff
	cmdArgumentAnnouncementString = "-"
	cmdArgumentDefinitionString = "="
	cmdArgumentPathSpaceEscapeString = "§§"
	scriptStartTimestamp = time.time()
	scriptDuration = 0.0

	
	
	##########################################################
	# crawl photo directory and download files
	##########################################################
	setStep(1)
	thisDir = os.path.dirname(__file__)
	tmpList = []
	fileCounter = 0
	for url in photoList:
		fileCounter += 1
		relPath = 'tmp\\' + str(fileCounter) + '.jpg'
		fullpath = os.path.join(thisDir, relPath)
		print('Downloading "'+url+'" to "'+fullpath+'"')
		try:
			tmpList.append(fullpath)
			progressCallback(fileCounter / len(photoList) * 100.0)
			with urllib.request.urlopen(url) as response, open(fullpath, 'wb') as out_file:
				shutil.copyfileobj(response, out_file)
		except Exception as e:
			print('Could not download file!')
			print(type(e))
			print(e)
			return False
			
	print('Fetching completed!')
	photoList = tmpList
	"""	
	print("Crawling temporarily processing directory...")
	for file in os.listdir(processFolderPath):
		if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".jpeg") or file.endswith(".JPEG"):
			photoList += [str(file)]
	print(str(len(photoList)) + " photos found.")

	print("Reading absolute base paths...")
	for i in range(len(photoList)):
		photoList[i] = os.path.join(processFolderPath, '') + photoList[i]
	"""
		
	##########################################################
	# start calculation process
	##########################################################
	print(str(len(photoList)) + " photos in queue!")

	doc = PhotoScan.app.document

	print("Creating chunk...")
	chunk = doc.addChunk()
	print(photoList)
	chunk.addPhotos(photoList)

	print(str(len(chunk.cameras)) + " cameras created!")
	
	if checkForStop():return
	setStep(2)
	print("Matching photos...")
	if not chunk.matchPhotos(progress = progressCallback, accuracy = configQuality_MatchingAccuracy, preselection = configQuality_MatchingPreselection):
		return False

	if checkForStop():return
	setStep(3)
	print("Align cameras...")
	if not chunk.alignCameras(progress = progressCallback):
		return False

	if checkForStop():return
	setStep(4)
	print("Building dense cloud...")
	if not chunk.buildDenseCloud(progress = progressCallback, quality = configQuality_DenseCloudQuality):
		return False

	if checkForStop():return
	setStep(5)
	print("Generating model...")
	if not chunk.buildModel(progress = progressCallback, surface = PhotoScan.Arbitrary, interpolation = configQuality_Interpolation, face_count = configQuality_FaceCount):
		return False

	if checkForStop():return
	setStep(6)
	print("Generating UV map...")
	if not chunk.buildUV(progress = progressCallback, mapping = configQuality_UVMappingMode):
		return False

	if checkForStop():return
	setStep(7)
	print("Generate diffuse map...")
	if not chunk.buildTexture(progress = progressCallback, blending = configQuality_DiffuseBlendingMode, size = configQuality_DiffuseTextureSize):
		return False

	if checkForStop():return
	setStep(8)
	print("Exporting model...")
	if not chunk.exportModel(progress = progressCallback, path = os.path.join(exportFolderPath, "") + "export.obj", format = "obj", cameras = False, binary = False):
		return False
	print("Saving project file...")
	if not doc.save(path = os.path.join(exportFolderPath, "") + "projectFile.psx"):
		return False
	
	print("Cleaning project...")
	doc.clear() 

	scriptDuration = time.time() - scriptStartTimestamp
	print("Reconstruction ended. ("+str(scriptDuration)+" seconds processing time)")
	setStep(0)
	return True
	
