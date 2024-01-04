import numpy as np
import floodlight.io.dfl as dfl
import floodlight.transforms.filter as filter
import matplotlib.pyplot as plt

# execute ALT+SHIFT+e
# CTRL+TAB
# ALT+8 go to console
# ESC-ESC go to editor
# :set visualbell
# :set noerrorbells

fpath = r"D:\sciebo\research_projects\DFL_position\data\raw\ObservedPositionalData\DFL-MAT-0002UK.xml"
fpath_info = r"D:\sciebo\research_projects\DFL_position\data\raw\MatchInformation\DFL-MAT-0002UK.xml"


(
    xy_objects,
    possession_objects,
    ballstatus_objects,
    teamsheets,
    pitch
) = dfl.read_position_data_xml(fpath, fpath_info)

ax = plt.subplots()[1]
pitch.plot(ax=ax)
plt.show()


xy1 = xy_objects["firstHalf"]["Home"]
np.shape(xy1)
xy1 = filter.butterworth_lowpass(xy1, Wn=0.25)

ax = plt.subplots()[1]
pitch.plot(ax=ax)
xy1.plot(t=(10, 10000), ax=ax, plot_type='trajectories')
plt.show()

p1 = xy1.player(1)
p2 = xy1.player(3)
ax = plt.subplots()[1]
pitch.plot(ax=ax)
ax.plot(p1[:, 0], p1[:, 1], color='blue')
ax.plot(p2[:, 0], p2[:, 1], color='red')
plt.show()
