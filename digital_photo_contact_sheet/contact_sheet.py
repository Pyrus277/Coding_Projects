import PIL
from PIL import Image, ImageDraw, ImageFont, ImageStat

#make the list of different color schemes
images=[]  #initialize list
color_mod = .1 #initialize intensity multiplier
for i in range(9):
    #open a fresh copy of the image on each of the 9 loops
    image=Image.open("readonly/msi_recruitment.gif")
    image=image.convert('RGB')

    #loop thru the pixels
    for pix_x in range(image.size[0]):
        for pix_y in range(image.size[1]):
            r, g, b = image.getpixel((pix_x,pix_y))  #get the rgb values for each pixel

            #now we modify the pixel values accoring to the row and column of where
            #it will end up on the contact sheet
            if i <= 2:
                image.putpixel((pix_x,pix_y), ((int(r*color_mod)), g, b))

            elif i >= 3 and i <= 5:
                image.putpixel((pix_x,pix_y), (r, (int(g*color_mod)), b))

            else:
                image.putpixel((pix_x,pix_y), (r, g, (int(b*color_mod))))

    if i in [2,5]:
        color_mod = .1  #re-initialize the intensty multiplier for each new row
    else:
        color_mod += .4 #otherwise, adjust the intensity modifier according to the column
    images.append(image)


#color filtiers are done, now we just create the contact sheet and populate it with the
#   picures from the list above
first_image=images[0]
#adding 150 to the height of the contact sheet, to allow for 50 pixel high text banners
#   under each row
contact_sheet=PIL.Image.new(first_image.mode, (first_image.width*3,first_image.height*3+150))

#initialize x y coordinate variables for the placement of each of the 9 images
x=0
y=0
#initialize x y coordinates for the placement of the captions, and string.format variables
#   for the caption content
text_x = 0
text_y = 455
color_x = 0
color_y = 0.1

for img in images:
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y) )

    #make a font and construct the captions
    #   These next five lines establish the average rgb color numbers so we can
    #       adjust the font color accordingly
    avg_col = ImageStat.Stat(img)
    avg_col = avg_col.mean
    avg_r = avg_col[0]
    avg_g = avg_col[1]
    avg_b = avg_col[2]

    fnt = ImageFont.truetype("readonly/fanwood-webfont.ttf", 55) #font style and size
    text = "channel {} intensity {}".format(color_x, color_y) #caption text
    #place the captions
    image_textadd=ImageDraw.Draw(contact_sheet)
    image_textadd.text((text_x,text_y),text,(int(avg_r),int(avg_g),int(avg_b)), font = fnt)

    color_y += 0.4 #increment the intensity caption text

    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x+first_image.width == contact_sheet.width:
        x=0
        y=y+first_image.height+50 #and this 50 pasted the image on the canvas 50 pixels under the image above
        color_x += 1
        color_y = 0.1
    else:
        x=x+first_image.width

    #update the placement of the banner text
    if text_x == 1600:
        text_x = 0
        text_y += first_image.height+50
    else:
        text_x += 800

#resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
display(contact_sheet)
