#This Program was made by Evan Witous between Oct. 9-15, 2016
#It was written using Jython (Java and Python)

def Copy(source, target, targX, targY):
  #This function copies a picture to the canvas at a certain X and Y coordinate
  targetX = targX
  for sourceX in range(0, getWidth(source)):
    targetY = targY
    for sourceY in range(0, getHeight(source)):
      px = getPixel(source,sourceX,sourceY)
      tx = getPixel(target, targetX, targetY)
      setColor(tx, getColor(px))
      targetY = targetY + 1
    targetX = targetX + 1

def HowRed(pic):
  #This function finds the average red value of the picture
  RedValue = 0
  length = 0
  
  for px in getPixels(pic):
    r = getRed(px)
    RedValue += r
    length += 1
  RedTotal = RedValue / length
  return RedTotal

def HowGreen(pic):
  #This function finds the average green value of the picture
  GreenValue = 0
  length = 0
  
  for px in getPixels(pic):
    g = getGreen(px)
    GreenValue += g
    length += 1
  GreenTotal = GreenValue / length
  return GreenTotal
  
def HowBlue(pic):
  #This function finds the average blue value of the picture
  BlueValue = 0
  length = 0
  
  for px in getPixels(pic):
    b = getBlue(px)
    BlueValue += b
    length += 1
  BlueTotal = BlueValue / length
  return BlueTotal
  
def ColorChange(pic,y,x,AvePicRed,AvePicGreen,AvePicBlue,canvas):
  #This finds the average Red, Green, and Blue values of a certain area of the canvas, then it modifies the main picture by the difference of the averages
  RedValue = 0
  GreenValue = 0
  BlueValue = 0
  length = 0
  
  for i in range(x,(x+getWidth(pic))):
    for j in range(y,(y+getHeight(pic))):
      px = getPixel(canvas,i,j)
      r = getRed(px)
      g = getGreen(px)
      b = getBlue(px)
      RedValue += r
      GreenValue += g
      BlueValue += b
      length += 1
      
  Redtotal = RedValue / length
  Greentotal = GreenValue / length
  Bluetotal = BlueValue / length
  RedDif = Redtotal - AvePicRed
  GreenDif = Greentotal - AvePicGreen
  BlueDif = Bluetotal - AvePicBlue
  
  for px in getPixels(pic):
    r = getRed(px) + RedDif
    g = getGreen(px) + GreenDif
    b = getBlue(px) + BlueDif
    setColor(px, makeColor(r,g,b))
  return pic
  
def RedChromaKey(pic, canvas):
  #It adds red to the signature, and then gets rid of everything that isn't above the red threshhold
  for px in getPixels(pic):
    r = 255 - getRed(px)
    g = getGreen(px)
    b = getBlue(px)
    setColor(px, makeColor(r,g,b))
  
  for y in range(getHeight(pic)):
    for x in range(getWidth(pic)):
      px = getPixel(pic,x,y)
      r = getRed(px)
      g = getGreen(px)
      b = getBlue(px)
      
      if r < 175:
        nColor = getColor(getPixel(canvas,x,(getHeight(canvas)-getHeight(pic)+y)))
        setColor(px,nColor)
  return pic

def Collage():
  #This is the main function that calls all the other functions
  
  #This finds and sets the picture files to a variable
  setMediaPath()
  TedOne = makePicture(getMediaPath("Ted1Small.jpeg"))
  canvas = makePicture(getMediaPath("Ted3.jpeg"))
  Signature = makePicture(getMediaPath("EWSignature.jpg"))
  
  AvePicRed = HowRed(TedOne)
  AvePicGreen = HowGreen(TedOne)
  AvePicBlue = HowBlue(TedOne)
  
  #This runs a loop nested in a loop to edit/copy the pictures into a grid like formation
  for y in range(42):
    for x in range(32):
      TedOne = makePicture(getMediaPath("Ted1Small.jpeg"))
      Copy(ColorChange(TedOne,(y*getHeight(TedOne)),(1+(x*getWidth(TedOne))),AvePicRed,AvePicGreen,AvePicBlue,canvas),canvas,(1+(x*getWidth(TedOne))),(y*getHeight(TedOne)))
  
  #This takes the bottom of the picture and makes it black so I can put my signature there
  for i in range(672,700):
    for j in range(0,getWidth(canvas)):
      px = getPixel(canvas,j,i)
      setColor(px, makeColor(0,0,0))
          
  #Copies the signature
  Copy(RedChromaKey(Signature,canvas),canvas,0,(getHeight(canvas)-getHeight(Signature)))
  
  #Writes the picture to a file
  writePictureTo(canvas,getMediaPath("CollageEvanWitous.jpg"))
  
  show(canvas)
  return canvas