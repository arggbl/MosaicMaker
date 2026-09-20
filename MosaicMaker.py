#SETUP
from PIL import Image
import os
from math import ceil

scale = 5 #How scaled up an image should be [larger val = larger image]

# define some functions

def AverageTileRGB(TileFile, Accuracy): #higher accuracy value = faster but less accurate
    TileWidth, TileHeight = TileFile.size[0], TileFile.size[1]
    count = 0
    TotalR,TotalG,TotalB = 0,0,0
    
    RGBtile = TileFile.convert('RGB')
    for x in range(0, TileWidth, Accuracy):
        for y in range(0, TileHeight, Accuracy):
            coords = (x,y)
            r, g, b = RGBtile.getpixel(coords)
            TotalR += r
            TotalG += g
            TotalB += b
            count += 1
            
    return TotalR/count,TotalG/count,TotalB/count

def FindClosest(TileNames, TileRGBS, targetRGB):
    ClosestName = "default.png"
    ClosestFactor = 765
    TargetR, TargetG, TargetB = targetRGB[0],targetRGB[1],targetRGB[2]
    #print(targetRGB)
    for RIndex in range(0, len(TileRGBS), 3):
        R,G,B = TileRGBS[RIndex], TileRGBS[RIndex+1], TileRGBS[RIndex+2]
        factor = abs(R-TargetR) + abs(G-TargetG) + abs(B-TargetB)
        if factor < ClosestFactor:
            ClosestName = TileNames[RIndex//3]
            ClosestFactor = factor
    return "Tiles\\" + ClosestName

# read input image for its dimensions
InputFiles = os.listdir("Input")
if (len(InputFiles) > 1):
    raise Exception("More than 1 image in \"Inputs\" folder.")
elif len(InputFiles) == 0:
    raise Exception("No files found in \"Inputs\" folder.")
FileName = InputFiles[0]
InputImage = Image.open("Input\\"+FileName)
InputWidth, InputHeight = InputImage.size[0], InputImage.size[1]

# ask for an input for image size (2 = 2x2 grid 3 = 3x3 grid)
GridSize = int(input("How large do you want the mosaic's grid to be?\nAn input of 2 makes a 2x2 grid and an input of 3 makes a 3x3 grid.\n"))
Accuracy = int(input("How accurate do you want the tiles to be?\nA larger accuracy value lowers runtime but also acccuracy. (MIN 1)\n"))

# output file name to user
print(f"Now creating a mosaic of: {FileName}")

# read tiles and average their RGBs
TileNames = os.listdir("Tiles")
TileRGBS = [] #format for TileRGBS is [R1, G1, B1, R2, G2, B2 ...]
for TileName in TileNames:
    TileFile = Image.open("Tiles\\" + TileName)
    R,G,B = AverageTileRGB(TileFile, Accuracy)
    TileRGBS.append(R)
    TileRGBS.append(G)
    TileRGBS.append(B)
    
# do some math for the tile parameters and create a grid
TileWidth, TileHeight = InputWidth/GridSize, InputHeight/GridSize
ProgressBar = ["[          ]", "[■         ]", "[■■        ]", "[■■■       ]", "[■■■■      ]", "[■■■■■     ]", "[■■■■■■    ]", "[■■■■■■■   ]", "[■■■■■■■■  ]", "[■■■■■■■■■ ]","[■■■■■■■■■■]"]

OUTPUT = Image.new(mode="RGB", size=(InputWidth * scale, InputHeight * scale))
# iterate through X and Y to find which image to place in each section of the grid
for CellX in range(0,GridSize):
    for CellY in range(0,GridSize):
        # crop out a section
        CroppedCell = InputImage.crop([CellX*TileWidth, CellY*TileHeight, (CellX+1)*TileWidth, (CellY+1)*TileHeight])
        # average the RGB of the section
        R,G,B = AverageTileRGB(CroppedCell, Accuracy)
        # find the closest image to paste in
        closest = FindClosest(TileNames,TileRGBS,[R,G,B])
        closestImg = Image.open(closest)
        resize = closestImg.resize((ceil(TileWidth * scale),ceil(TileHeight * scale)),Image.LANCZOS)
        # paste the image in
        Image.Image.paste(OUTPUT, resize, (ceil(CellX*TileWidth * scale), ceil(CellY*TileHeight * scale)))
        
    print(ProgressBar[ceil(CellX // (GridSize / 10))], end = " ")
    print(f"{int(CellX / GridSize * 100)}%")

number = len(os.listdir("Output"))
OUTPUT.save(f"Output\\{number}.png")
final = Image.open(f"Output\\{number}.png")
final.show()
print("FINISHED")
