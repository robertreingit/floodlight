import numpy as np
import pandas as pd
import floodlight.io.dfl as dfl
import floodlight.transforms.filter as filter
import matplotlib.pyplot as plt
from floodlight.models.kinematics import DistanceModel

# execute ALT+SHIFT+e
# CTRL+TAB
# ALT+8 go to console
# ESC-ESC go to editor
# :set visualbell
# :set noerrorbells

# home
root_path = r"D:\sciebo\research_projects\DFL_position\data"
fpath = root_path + r"\raw\ObservedPositionalData\DFL-MAT-0002UK.xml"
fpath_info = root_path + r"\raw\MatchInformation\DFL-MAT-0002UK.xml"

# office
root_path = r"D:\research_projects\DFG_soccer\DFL_Position"
fpath = root_path + r"\ObservedPositionalData\DFL-MAT-0002WQ.xml"
fpath_info = root_path + r"\MatchInformation\DFL-MAT-0002WQ.xml"
fpath_evt = root_path + r"\EventData\DFL-MAT-0002WQ.xml"


(
    xy_objects,
    possession_objects,
    ballstatus_objects,
    teamsheets,
    pitch,
) = dfl.read_position_data_xml(fpath, fpath_info)

ax = plt.subplots()[1]
pitch.plot(ax=ax)
plt.show()

xy1 = xy_objects["firstHalf"]["Home"]
np.shape(xy1)
xy1 = filter.butterworth_lowpass(xy1, Wn=0.25)

ax = plt.subplots()[1]
pitch.plot(ax=ax)
xy1.plot(t=(10, 10000), ax=ax, plot_type="trajectories")
plt.show()

p1 = xy1.player(1)
p2 = xy1.player(3)
ax = plt.subplots()[1]
pitch.plot(ax=ax)
ax.plot(p1[:, 0], p1[:, 1], color="blue")
ax.plot(p2[:, 0], p2[:, 1], color="red")
plt.show()


# event data
evts, _, _ = dfl.read_event_data_xml(
    fpath_evt, fpath_info, teamsheets["Home"], teamsheets["Away"]
)
evts["firstHalf"]["Home"].events.head()

# calculate distance
no_games = 10
result_df = pd.DataFrame(
    data={
        "team_1_id": np.full(no_games, np.NAN),
        "team_1_dist": np.full(no_games, np.NAN),
        "team_2_id": np.full(no_games, np.NAN),
        "team_2_dist": np.full(no_games, np.NAN),
    }
)

dm = DistanceModel()

current_game = 0
total_distance = {"Home": 0, "Away": 0}
for half in xy_objects:
    for team in total_distance:
        xy_tmp = xy_objects[half][team]
        dm.fit(xy_tmp)
        total_distance[team] += dm.cumulative_distance_covered()[-1, :].sum()
team_id = {
    "Home": teamsheets["Home"].teamsheet.team[0],
    "Away": teamsheets["Away"].teamsheet.team[0],
}
result_df.loc[current_game, "team_1_id"] = team_id["Home"]
result_df.loc[current_game, "team_1_dist"] = total_distance["Home"]
result_df.loc[current_game, "team_2_id"] = team_id["Away"]
result_df.loc[current_game, "team_2_dist"] = total_distance["Away"]
