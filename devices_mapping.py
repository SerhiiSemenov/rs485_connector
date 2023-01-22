""""
topic_name, device_name, rs_485_id, port_num
"""

map_table = {
    # master bedroom
    "home/bedroom/recuperator_low_speed": ["bed room recuperator low speed", 0x4, 0x2],
    "home/bedroom/recuperator_shutter_power": ["bed room recuperator hi speed", 0x4, 0x8],
    "home/bedroom/main_lamp": ["bed room main lamp", 0x4, 0x4],
    "home/bedroom/bed_lamp": ["bed room bed light", 0x3, 0x9],
    "home/bedroom/floor_lamp": ["bed room bed light", 0x3, 0x10],

    #kid area
    "home/kidroom/recuperator_low_speed": ["kidroom recuperator low speed", 0x5, 0x3],
    "home/kidroom/recuperator_hi_speed": ["kidroom room recuperator hi speed", 0x5, 0x1],
    "home/kidroom/main_lamp": ["bed room main lamp", 0x5, 0xB],
    "home/kidroom/bed_lamp": ["bed room bed light", 0x5, 0xD],
    "home/kidroom/floor_lamp": ["bed room bed light", 0x6, 0x5],

    # kitchen
    "home/kitchen/background_lamp": ["kitchen furniture background lamp", 0x4, 0x6],
    "home/kitchen/main_lamp": ["kitchen main lamp", 0x4, 0x3],
    "home/kitchen/table_lamp": ["kitchen table lamp", 0x4, 0x9],

    # corridor
    "home/corridor/lamp": ["corridor lamp", 0x4, 0x7],
    "home/corridor/server_fan": ["corridor fan", 0x4, 0x10],
    "home/corridor/flor_lamp": ["corridor fan", 0x6, 0x2],

    # living room
    "home/livingroom/recuperator_hi_speed": ["living room recuperator hi speed", 0x4, 0x1],
    "home/livingroom/recuperator_low_speed": ["living room recuperator low speed", 0x4, 0xD],
    "home/livingroom/bacground_main_lamp": ["living room bacground LED lamp", 0x3, 0x6],
    "home/livingroom/bacground_serhiis_table_lamp": ["living room serhii's table lamp", 0x3, 0x5],
    "home/livingroom/work_place_1_lamp": ["living room bacground LED lamp", 0x3, 0x7],
    "home/livingroom/launge_zone_lamp": ["launge zone lamp", 0x3, 0x4],

    # bathroom
    "home/bathroom_1/lamp": ["bathroom_1 lamp", 0x6, 0x3],
    "home/bathroom_1/vent": ["bathroom_1 main vent", 0x6, 0x1],
    "home/bathroom_1/heater": ["bathroom 1 water heater", 0x5, 0x6],
    "home/bathroom_2/vent": ["bathroom_2 main vent", 0x6, 0x5],
    "home/bathroom_2/lamp": ["bathroom 2 lamp", 0x5, 0x8],
    "home/bathroom_2/lamp_auto": ["bathroom 2 motion detected lamp", 0x5, 0x8],
    "home/bathroom_1/lamp_auto": ["bathroom 1 motion detected lamp", 0x6, 0x3],

    # heater valve
    "home/kitchen/heater_valve": ["kitchen heater valve", 0x3, 0xC],
    "home/livingroom/heater_valve": ["living room heater valve", 0x3, 0xD],
    "home/bedroom/heater_valve": ["bed room heater valve", 0x3, 0xE],
    "home/kidarea/heater_valve": ["bed room heater valve", 0x6, 0x6],
}
