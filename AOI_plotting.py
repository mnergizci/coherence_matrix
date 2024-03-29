from LiCSBAS_meta import *
import getopt
import os
import sys
import time
import shutil
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import LiCSBAS_io_lib as io_lib
import LiCSBAS_tools_lib as tools_lib
import LiCSBAS_plot_lib as plot_lib
from scipy import stats
import matplotlib.patches as patches

if len(sys.argv) < 3:
    print('Please provide frame and pair which you like to illustrate : i.e python AOI_plotting.py  021D_05266_252525 20230129_20230210')
    sys.exit(1)
frame=sys.argv[1]
pair=sys.argv[2]
batchdir=os.environ['BATCH_CACHE_DIR']
framedir=os.path.join(batchdir, frame)
tr= int(frame[:3])
IFGdir=os.path.join(framedir, 'IFG')
SLC_dir=os.path.join(framedir, 'SLC')


####length, weight
a=os.listdir(SLC_dir)
for i in a:
    if i.startswith('2') and len(i) == 8:
        ref_epoc=i
mli_par=os.path.join(SLC_dir, ref_epoc, ref_epoc +'.slc.mli.par')
width=int(io_lib.get_param_par(mli_par, 'range_samples'))
length=int(io_lib.get_param_par(mli_par, 'azimuth_lines'))
print(width, length)
####

ccfile=os.path.join(IFGdir, pair, pair +f'.cc')
if os.path.exists(ccfile):
    if os.path.getsize(ccfile)==length*width:
        coh = io_lib.read_img(ccfile, length, width, np.uint8)
        coh = coh.astype(np.float32) / 255
        coh[coh == 0] = np.nan
       
    else:
        coh = io_lib.read_img(ccfile, length, width, endian='big')
        coh[coh == 0] = np.nan
        
else:
    print(f"The file doesn't exist in {IFGdir}, please check!")


rois = [
    {"start_row": 7200, "end_row": 8100, "start_col": 125, "end_col": 1125, "label": "C", "color": "green"},
    {"start_row": 2700, "end_row": 3800, "start_col": 1200, "end_col": 2300, "label": "B", "color": "red"},
    {"start_row": 1200, "end_row": 2200, "start_col": 1200, "end_col": 2400, "label": "A", "color": "orange"}
]


fig, ax = plt.subplots(figsize=(20, 30))

# Display the coherence image
ax.imshow(coh, cmap='gray', vmin=0, vmax=1)
# Remove the axis labels and ticks
ax.axis('off')  # This removes the axes including the frame

# Loop through each ROI, create a Rectangle patch, and add a label
for roi in rois:
    start_row, end_row = roi["start_row"], roi["end_row"]
    start_col, end_col = roi["start_col"], roi["end_col"]
    roi_rect = patches.Rectangle((start_col, start_row), end_col - start_col, end_row - start_row,
                                 linewidth=3, edgecolor=roi["color"], facecolor='none')
    ax.add_patch(roi_rect)
    
    # Add label
    #ax.text(start_col, start_row - 20, roi["label"], color=roi["color"], fontweight='bold', fontsize=25)

#plt.title('Coherence with Multiple ROIs and Labels')
# Eliminate white space
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)


plt.savefig('Coherence_Image_radar_coord.png', bbox_inches='tight', pad_inches=0)


