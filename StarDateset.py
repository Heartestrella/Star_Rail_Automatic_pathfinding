# 所有数据集都遵守0,1位为地图左侧选项，2,3位为选项所指定的转送锚点,TP为转送键所处坐标
TP = [1650, 975]
# 地图总数量
MAP_DIST = {
    "SPACE_STATION": [
        "Main_control_warehouse",
        "Base_cabin",
        "Containment_module",
        "Support_section",
    ],
    "Yalilo_VI": [
        "Administrative_District",
        "Suburban_Snowfield",
        "Edge_Road",
        "Iron_Guard_Noarea",
        "Reverberation_Corridor",
        "Yongdong_Ridge",
        "Panyan_Town",
        "Big_Miningarea",
        "Liuding_Town",
        "Mechanical_Equipment",
    ],
}
# 箱子所处位置坐标
BOX_SUMBER_ = {
    "SPACE_STATION": {
        "BASE_CABIN": [215, 151, 279, 171],
        "Containment_module": [221, 151, 303, 171],
        "Support_section": [219, 151, 275, 171],
    },
    "Yalilo_VI": {
        "Administrative_District": [220, 153, 305, 173],
        "Suburban_Snowfield": [220, 151, 275, 171],
        "Edge_Road": [216, 150, 277, 172],
        "Iron_Guard_Noarea": [218, 149, 309, 172],
        "Reverberation_Corridor": [215, 150, 305, 172],
        "Yongdong_Ridge": [219, 151, 276, 171],
        "Panyan_Town": [218, 151, 276, 171],
        "Big_Miningarea": [221, 151, 301, 171],
        "Liuding_Town": [219, 151, 275, 171],
        "Mechanical_Equipment": [218, 151, 277, 171],
    },
}
# 删除地图复杂元素所需
PHYSICAL_STRENGTH = [1440, 40, 1780, 85]
NAVIGATION_BAR = [1400, 120, 1900, 1030]
BOX_SUMBER = [140, 130, 410, 190]
UID = [30, 1040, 160, 1080]

# 空间站
BASE_CABIN = [1600, 420]
CONTAINMENT_MODULE = [1530, 520]
SUPPORT_SECTION = [1560, 640]

# 雅洛利-VI
ADMINISTRATIVE_DISTRICT = [1500, 340]
SUBURBAN_SNOWFIELD = [1500, 440]
EDGE_ROAD = [1500, 520]
IRON_GUARD_NOAREA = [1500, 610]
REVERBERATION_CORRIDOR = [1500, 720]
YONGDONG_RIDGE = [1500, 800]
PANYAN_TOWN = [1500, 900]
BIG_MININGAREA = [1500, 1000]
# 需滑动到底部
LIUDING_TOWN = [1500, 840]
MECHANICAL_EQUIPMENT = [1500, 940]

A_DRAGTO_B = [1500, 900, 1500, 520]

OBSERVATION_CAR = [1580, 250, 650, 805]
BODY_OF_SEA = [1580, 320, 570, 765]

ZOOM_ = [668, 985]


Week_task = [80, 120, 183, 754]

# 任务 : 键值

TASKS = {
    "Daily_tasks": 200,
    "Synthetic_consumables": 100,
    "Week_tasks": 200,
    "Gold": 100,
    "Breakthrough": 100,
    "Up_Relics": 100,
    "Weakness": 100,
    "Destroy": 100,
    "Decompose": 100,
    "Support": 200,
    "Red": 100,
    "Use_consumables": 100,
    "Photograph": 100,
    "Entrust": 100,
    "Pavilion": 200,
    "Weakpoint_break": 100,
    "Finishing_win": 200,
    "Secret_skills": 100,
    "Destroyer": 200,
    "Different_Weaknesses_Break": 100,
}

PRIORITY_TASK = {
    "Daily_tasks": 1,
    "Synthetic_consumables": 5,
    "Week_tasks": 5,
    "Gold": 5,
    "Breakthrough": 5,
    "Up_Relics": 5,
    "Weakness": 2,
    "Destroy": 2,
    "Decompose": 3,
    "Support": 5,
    "Red": 5,
    "Use_consumables": 3,
    "Photograph": 3,
    "Entrust": 2,
    "Pavilion": 1,
    "Weakpoint_break": 2,
    "Finishing_win": 2,
    "Secret_skills": 3,
    "Destroyer": 1,
    "Different_Weaknesses_Break": 1,
}

FIRST_TASK = [275, 410, 567, 883]
SECOND_TASK = [611, 410, 903, 883]
THIRD_TASK = [947, 410, 1239, 883]
FOURTH_TASK = [1283, 410, 1575, 883]
FIVETH_TASK = [1020, 410, 1312, 883]
SIXTH_TASK = [1356, 410, 1648, 883]
ACTIVITY = [308, 270, 377, 371]
GET_ACTIVITY = [329, 803, 515, 856]

FIGHT = [105, 55, 199, 78]
BREAKTHROUGH_OVER = [837, 250, 1081, 310]
