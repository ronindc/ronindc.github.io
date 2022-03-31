from calendar import c
from dataclasses import dataclass
from logging import root
import os

# Code Generation String(s) for Gallery:modal-container template
mySlidesElement = """<div class="modal-my-slides"><div class="number-text">[IMAGE_INDEX]</div><img src="[IMAGE_SOURCE]" style="width: 100%;"></div>\n"""
modalGallerySlideshowColumn = """<div class="modal-gallery-slideshow-column"><img class="demo cursor" src="[IMAGE_SOURCE]" onclick="CurrentSlide([GALLERY_INDEX], [CURRENT_IMAGE_INDEX])" alt="[CURRENT_IMAGE_FILENAME]"></div>\n"""


# Code Generation String for Gallery:gallery-container-row-contents template'
galleryContainerRowColumn = """<div class="gallery-container-column" onclick="OpenModal([FOLDER_INDEX])"><p>[FOLDER_NAME]</p><img src="[IMAGE_SOURCE]"></div>\n"""

rootFolder = f'.{os.path.sep}images'

@dataclass
class ImageFolder():
    def __init__(self, folderName, filePaths) -> None:
        self.folderName = folderName
        self.contents = filePaths

def GenerateMySlidesArray(filePaths):
    fileCount = len(filePaths)
    mySlidesElements = []
    for i in range(fileCount):
        newSlideElement = mySlidesElement.replace("[IMAGE_INDEX]", f'{i + 1} / {fileCount}')
        newSlideElement = newSlideElement.replace("[IMAGE_SOURCE]", filePaths[i])
        mySlidesElements.append(str(newSlideElement))
    return mySlidesElements

def GenerateModalGallerySlideshowColumnArray(filePaths, currentGalleryIndex):
    fileCount = len(filePaths)
    elements = []
    for i in range(fileCount):
        newElement = modalGallerySlideshowColumn.replace("[IMAGE_SOURCE]", filePaths[i])
        newElement = newElement.replace("[GALLERY_INDEX]", str(currentGalleryIndex))
        newElement = newElement.replace("[IMAGE_SOURCE]", filePaths[i])
        newElement = newElement.replace("[CURRENT_IMAGE_INDEX]", str(i + 1))
        newElement = newElement.replace("[CURRENT_IMAGE_FILENAME]", filePaths[i])
        elements.append(newElement)
    return elements

def GenerateContainerRowColumnArray(folderName, filePaths, currentGalleryIndex):
    print(len(filePaths))
    newElement = galleryContainerRowColumn.replace("[IMAGE_SOURCE]", filePaths[1])
    newElement = newElement.replace("[FOLDER_INDEX]", str(currentGalleryIndex))
    newElement = newElement.replace("[FOLDER_NAME]", folderName)
    return newElement

# Generates all the required Modal Containers
def CreateModalContainers(imageFolders):
    modalContainerTemplate = open("./images/modal-container.html.template", "r").read()
    filledModalContainers = []
    currentGalleryIndex = 0

    # Creates the Modal Containers Section of the Gallery Webpage
    for imageFolder in imageFolders:
        emptyModalContainer = open("./images/modal-container.html.template", "r").read()
        emptyModalContainer = emptyModalContainer.replace("[FOLDER_INDEX]", str(currentGalleryIndex))
        filledModalContainer = emptyModalContainer.replace('[MODAL_CONTAINER_CONTENTS_HEADER]', imageFolder.folderName)
        mySlides = '\t\t'.join(slide for slide in GenerateMySlidesArray(imageFolder.contents))
        mySlideshowColumnContents = ''.join([element for element in GenerateModalGallerySlideshowColumnArray(imageFolder.contents, currentGalleryIndex)])
        currentGalleryIndex += 1
        filledModalContainer = filledModalContainer.replace("[MY_SLIDES_INSERTION_POINT]", mySlides)
        filledModalContainer = filledModalContainer.replace("[MODAL_GALLERY_SLIDESHOW_COLUMN_INSERTION_POINT]", mySlideshowColumnContents)
        filledModalContainers.append(filledModalContainer)
    return filledModalContainers

def CreateGalleryContainerRowColumns(imageFolders):
    filledGalleryContainerRowColums = []

    # Creates the Gallery:gallery-container-row-contents Section of the Gallery Webpage
    currentGalleryIndex = 0
    for imageFolder in imageFolders:
        containerRowColumns = GenerateContainerRowColumnArray(imageFolder.folderName, imageFolder.contents, currentGalleryIndex)
        currentGalleryIndex += 1
        filledGalleryContainerRowColums.append(containerRowColumns)
    return filledGalleryContainerRowColums

if __name__ == '__main__':
    imageFolders = []
    for f in os.listdir(rootFolder):
        path = os.path.join(rootFolder, f)
        if (os.path.isdir(path)):
            print(f)
            imagePaths = []
            for f1 in os.listdir(path):
                pathToImage = '.' + os.path.join(path, f1)
                imagePaths.append(pathToImage)
                print(pathToImage)
            imageFolders.append(ImageFolder(f, imagePaths))
            print("\n\n")
    modalContainers = CreateModalContainers(imageFolders)
    galleryContainerRowColumns = CreateGalleryContainerRowColumns(imageFolders)

    # Open the Gallery.html template
    emptyGalleryHtmlTemplate = open("./images/gallery.html.template", "r").read()
    filledGalleryHtml = emptyGalleryHtmlTemplate.replace("[MODAL_CONTAINER_INSERTION_POINT]", ''.join([modal for modal in modalContainers]))
    filledGalleryHtml = filledGalleryHtml.replace("[GALLERY_CONTAINER_ROW_CONTENTS_INSERTION_POINT]", ''.join([column for column in galleryContainerRowColumns]))

    completedGalleryHTMLFile = open("./pages/gallery-generated.html", "w")
    completedGalleryHTMLFile.writelines(filledGalleryHtml)
    completedGalleryHTMLFile.close()
