
import numpy as np
from scipy.ndimage import convolve
import matplotlib.pyplot as plt


def display_image(img, title):
    """ Show an image with matplotlib:

    Args:
        Image as numpy array (H,W,3)
    """
    # display the data img via function imshow() in matplotlib.pyplot
    plt.imshow(img)
    plt.title(title)
    plt.show() #load the image

def loaddata(path):
    """ Load bayerdata from file

    Args:
        Path of the .npy file
    Returns:
        Bayer data as numpy array (H,W)
    """
    temp=np.load(path)
    return temp


def separatechannels(bayerdata):
    """ Separate bayer data into RGB channels so that
    each color channel retains only the respective
    values given by the bayer pattern and missing values
    are filled with zero

    Args:
        Numpy array containing bayer data (H,W)
    Returns:
        red, green, and blue channel as numpy array (H,W)
    """
    r=np.zeros((512,448))     
    g=np.zeros((512,448)) 
    b=np.zeros((512,448)) 
    for i in range(512):
        for j in range(447):
            if i%2==0 and j%2==1: 
                r[i][j]=bayerdata[i][j]*255  #separate red pixels from bayer grid

            elif i%2==1 and j%2==0:
                b[i][j]=bayerdata[i][j]*255  #separate blue pixels from bayer grid
            else:
                g[i][j]=bayerdata[i][j]*255  #separate green pixels from bayer grid  
                
#     display_image(r, 'r')      
#     display_image(g, 'g')
#     display_image(b, 'b')

    return r,g,b
    


def assembleimage(r, g, b):
    """ Assemble separate channels into image

    Args:
        red, green, blue color channels as numpy array (H,W)
    Returns:
        Image as numpy array (H,W,3)
    """
    
    #rgbArray1 is 3 dimensional array with r,g and b colour planes 
    rgbArray1 = np.full((512,448,3),0, 'uint8')
    rgbArray1[..., 0] = r
    rgbArray1[..., 1] = g
    rgbArray1[..., 2] = b
   
    return(rgbArray1)


def interpolate(r, g, b):
    """ Interpolate missing values in the bayer pattern
    by using bilinear interpolation

    Args:
        red, green, blue color channels as numpy array (H,W)
    Returns:
        Interpolated image as numpy array (H,W,3)
    """

    k = np.array([[1,1,1], [1,1,1], [1,1,1]])
    
    #perform convolution of red, green and blue planes individually with k.
    r_new=convolve(r, k,mode='nearest') 
    g_new=convolve(g, k, mode='nearest')
    b_new=convolve(b, k, mode='nearest')
    
    for i in range(512):
        for j in range(448):
            if i%2==0 and j%2==1:
                g_new[i][j]=g_new[i][j]/4
                b_new[i][j]=b_new[i][j]/4
            elif i%2==1 and j%2==0:
                r_new[i][j]=r_new[i][j]/4
                g_new[i][j]=g_new[i][j]/4
            else:
                r_new[i][j]=r_new[i][j]/2
                b_new[i][j]=b_new[i][j]/2
                g_new[i][j]=g_new[i][j]/5
    
    #rgbArray2 is 3 dimensional array with interpolated r,g and b colour planes 
    rgbArray2 = np.full((512,448,3),0, 'uint8')
    rgbArray2[..., 0] = r_new
    rgbArray2[..., 1] = g_new
    rgbArray2[..., 2] = b_new
        
    return(rgbArray2)

def main():
    data = loaddata("bayerdata.npy")   
    r, g, b = separatechannels(data)

    img = assembleimage(r, g, b) 
    display_image(img,'Raw Bayer grid image')

    img_interpolated = interpolate(r, g, b)
    display_image(img_interpolated, 'Resonstructed RGB imgae')
    
if __name__ == "__main__":
    main()    

