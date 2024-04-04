import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load your image
image_path = '/home/zdeng/aeroplan/training_dataset/texture_ds.png'
img = mpimg.imread(image_path)

fig, ax = plt.subplots()
ax.imshow(img)

def onclick(event):
    ix, iy = event.xdata, event.ydata
    print(f'x = {int(ix)}, y = {int(iy)}')

# Connection to the click event
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
