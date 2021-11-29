""""
topic_name, device_name, rs_485_id, port_num
"""

map_table = {
    # bedroom
    "home/bedroom/recuperator_periodic_mode": ["bed room recuperator periodic mode", 0x1, 0x1],
    "home/bedroom/recuperator_low_speed": ["bed room recuperator low speed", 0x4, 0x2],
    "home/bedroom/recuperator_hi_speed": ["bed room recuperator hi speed", 0x4, 0x8],
    "home/bedroom/main_lamp": ["bed room main lamp", 0x4, 0x4],
    "home/bedroom/bed_lamp": ["bed room bed light", 0x3, 0x7],

    # kitchen
    "home/kitchen/background_lamp": ["kitchen furniture background lamp", 0x4, 0x6],
    "home/kitchen/main_lamp": ["kitchen main lamp", 0x4, 0x3],
    "home/kitchen/table_lamp": ["kitchen table lamp", 0x4, 0x9],

    # corridor
    "home/corridor/lamp": ["corridor lamp", 0x4, 0x7],

    # living room
    "home/livingroom/recuperator_hi_speed": ["living room recuperator hi speed", 0x4, 0x1],
    "home/livingroom/recuperator_low_speed": ["living room recuperator low speed", 0x4, 0xD],
    "home/livingroom/bacground_main_lamp": ["living room bacground LED lamp", 0x3, 0x6],
    "home/livingroom/bacground_serhiis_table_lamp": ["living room serhii's table lamp", 0x3, 0x5],

    # bathroom
    "home/bathroom_1": ["kitchen main lamp", 0x3, 0x3],
    "home/bathroom_2": ["kitchen main lamp", 0x3, 0x3]
}