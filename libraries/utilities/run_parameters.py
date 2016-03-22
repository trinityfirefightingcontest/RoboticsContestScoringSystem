# -*- coding: utf-8; -*-


class RunParameters(object):
    NAME = 'name'
    RUN_DISQUALIFIED = 'run_disqualified'
    SECONDS_JUDGE_1 = 'seconds_to_put_out_candle_1'
    SECONDS_JUDGE_2 = 'seconds_to_put_out_candle_2'
    NON_AIR = 'non_air'
    FURNITURE = 'furniture'
    ARBITRARY_START = 'arbitrary_start'
    RETURN_TRIP = 'return_trip'
    NO_CANDLE_CIRCLE = 'no_candle_circle'
    STOPPED_WITHIN_30 = 'stopped_within_30'
    CANDLE_DETECTED = 'candle_detected'
    NUM_ROOMS_SEARCHED = 'number_of_rooms_searched'
    KICKED_DOG = 'kicked_dog'
    TOUCHED_CANDLE = 'touched_candle'
    WALL_CONTACT_CMS = 'wall_contact_cms'
    RAMP_USED = 'ramp_used'
    BABY_RELOCATED = 'baby_relocated'
    ALL_CANDLES = 'all_candles'
    VERSA_VALVE_USED = 'versa_valve_used'

    # name of all html form inputs, order matters
    ALL = [
        NAME,
        RUN_DISQUALIFIED,
        SECONDS_JUDGE_1,
        SECONDS_JUDGE_2,
        NON_AIR,
        FURNITURE,
        ARBITRARY_START,
        RETURN_TRIP,
        NO_CANDLE_CIRCLE,
        STOPPED_WITHIN_30,
        CANDLE_DETECTED,
        NUM_ROOMS_SEARCHED,
        KICKED_DOG,
        TOUCHED_CANDLE,
        WALL_CONTACT_CMS,
        RAMP_USED,
        BABY_RELOCATED,
        ALL_CANDLES,
        VERSA_VALVE_USED
    ]

    BOOLEANS = [
        RUN_DISQUALIFIED,
        NON_AIR,
        FURNITURE,
        ARBITRARY_START,
        RETURN_TRIP,
        NO_CANDLE_CIRCLE,
        STOPPED_WITHIN_30,
        CANDLE_DETECTED,
        KICKED_DOG,
        TOUCHED_CANDLE,
        RAMP_USED,
        BABY_RELOCATED,
        ALL_CANDLES,
        VERSA_VALVE_USED
    ]
