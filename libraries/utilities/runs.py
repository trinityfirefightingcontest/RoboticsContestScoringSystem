# -*- coding: utf-8; -*-

from libraries.utilities.utilities import Utilities


L3_SCORES = [
    600,
    550,
    450,
    400,
    350,
    325
]


class Runs(object):
    # form paramter name mappings
    NAME = 'name'
    RUN_DISQ = 'run_disqualified'
    SEC_JUDGE_1 = 'seconds_to_put_out_candle_1'
    SEC_JUDGE_2 = 'seconds_to_put_out_candle_2'
    NON_AIR = 'non_air'
    FURNITURE = 'furniture'
    ARBITRARY_START = 'arbitrary_start'
    RETURN_TRIP = 'return_trip'
    NO_CANDLE_CIRCLE = 'no_candle_circle'
    STOPPED_WITHIN_30 = 'stopped_within_30'
    CANDLE_DETECTED = 'candle_detected'
    NUM_ROOMS = 'number_of_rooms_searched'
    KICKED_DOG = 'kicked_dog'
    TOUCHED_CANDLE = 'touched_candle'
    WALL_CONTACT = 'wall_contact_cms'
    RAMP_USED = 'ramp_used'
    SECONDARY_SAFE_ZONE = 'secondary_safe_zone'
    ALL_CANDLES = 'all_candles'
    VERSA_VALVE_USED = 'versa_valve_used'
    L3_TRAVERSED_HALLWAY = 'l3_traversed_hallway'
    L3_FOUND_BABY = 'l3_found_baby'
    L3_RESCUED_BABY = 'l3_rescued_baby'
    L3_ALL_CANDLES = 'l3_all_candles'
    L3_ONE_CANDLE = 'l3_one_candle'
    L3_NONE = 'l3_none'

    # other parameters
    TIME_DIFF_ERROR = 'time_difference_error'

    # error strings
    NAME_ERR = 'Invalid name'
    SEC_JUDGE_1_ERR = 'Invalid value'
    SEC_JUDGE_2_ERR = 'Invalid value'
    NUM_ROOMS_ERR = 'Invalid value'
    TOUCHED_CANDLE_ERR = 'Invalid value'
    WALL_CONTACT_ERR = 'Invalid value'
    TIME_DIFF_ERR = (
        'If robot failed the trial, '
        'both judges should enter the same AT'
    )

    # name of all html form inputs
    ALL = [
        NAME,
        RUN_DISQ,
        SEC_JUDGE_1,
        SEC_JUDGE_2,
        NON_AIR,
        FURNITURE,
        ARBITRARY_START,
        RETURN_TRIP,
        NO_CANDLE_CIRCLE,
        STOPPED_WITHIN_30,
        CANDLE_DETECTED,
        NUM_ROOMS,
        KICKED_DOG,
        TOUCHED_CANDLE,
        WALL_CONTACT,
        RAMP_USED,
        SECONDARY_SAFE_ZONE,
        ALL_CANDLES,
        VERSA_VALVE_USED,
        L3_NONE,
        L3_ONE_CANDLE,
        L3_ALL_CANDLES,
        L3_FOUND_BABY,
        L3_RESCUED_BABY,
        L3_TRAVERSED_HALLWAY
    ]

    BOOLEANS = [
        RUN_DISQ,
        NON_AIR,
        FURNITURE,
        ARBITRARY_START,
        RETURN_TRIP,
        NO_CANDLE_CIRCLE,
        STOPPED_WITHIN_30,
        CANDLE_DETECTED,
        KICKED_DOG,
        RAMP_USED,
        SECONDARY_SAFE_ZONE,
        ALL_CANDLES,
        VERSA_VALVE_USED,
        L3_NONE,
        L3_ONE_CANDLE,
        L3_ALL_CANDLES,
        L3_FOUND_BABY,
        L3_RESCUED_BABY,
        L3_TRAVERSED_HALLWAY
    ]

    L3_MILESTONES = [
        L3_NONE,
        L3_ONE_CANDLE,
        L3_ALL_CANDLES,
        L3_FOUND_BABY,
        L3_RESCUED_BABY,
        L3_TRAVERSED_HALLWAY
    ]

    @staticmethod
    def validate_form(
        form,
        level,
        division,
        robot_name
    ):

        disqualified = form[Runs.RUN_DISQ]
        if disqualified:
            return Runs.validate_form_disqualified(
                form,
                level,
                division,
                robot_name
            )
        return Runs.validate_form_qualified(
            form,
            level,
            division,
            robot_name
        )

    @staticmethod
    def validate_form_disqualified(
        form,
        level,
        division,
        robot_name
    ):
        # if disqualified, need to verify name, time and # of rooms
        disqualified = True
        error = {}

        # validate name - sanity check
        valid = Runs.validate_name(form[Runs.NAME], robot_name)
        if not valid:
            error[Runs.NAME] = Runs.NAME_ERR
        # validate time recorded by first judge
        valid = Runs.validate_actual_time(
            form[Runs.SEC_JUDGE_1],
            level,
            disqualified
        )
        if not valid:
            error[Runs.SEC_JUDGE_1] = Runs.SEC_JUDGE_1_ERR
        # validate time recorded by second judge
        valid = Runs.validate_actual_time(
            form[Runs.SEC_JUDGE_2],
            level,
            disqualified
        )
        if not valid:
            error[Runs.SEC_JUDGE_2] = Runs.SEC_JUDGE_2_ERR
        # make sure they are equal (only if disqualified)
        valid = Runs.validate_actual_time_compare(
            form[Runs.SEC_JUDGE_1],
            form[Runs.SEC_JUDGE_2]
        )
        if not valid:
            error[Runs.TIME_DIFF_ERROR] = Runs.TIME_DIFF_ERR

        # check level and division
        if level == 1 and division in ['junior', 'walking']:
            # validate number of rooms
            valid = Runs.validate_num_rooms(
                form[Runs.NUM_ROOMS],
                level
            )
            if not valid:
                error[Runs.NUM_ROOMS] = Runs.NUM_ROOMS_ERR
        if level == 3:
            has_at_least_one_milestone = False
            for milestone in Runs.L3_MILESTONES:
                has_at_least_one_milestone = (
                    has_at_least_one_milestone or
                    form[milestone]
                )
            if not has_at_least_one_milestone:
                error['l3_sympathy'] = 'Please select at least one option'
        return error

    @staticmethod
    def validate_form_qualified(
        form,
        level,
        division,
        robot_name
    ):
        # if disqualified, need to verify name, time and # of rooms
        error = {}
        disqualified = False

        # validate name - sanity check
        valid = Runs.validate_name(form[Runs.NAME], robot_name)
        if not valid:
            error[Runs.NAME] = Runs.NAME_ERR
        # validate time recorded by first judge
        valid = Runs.validate_actual_time(
            form[Runs.SEC_JUDGE_1],
            level,
            disqualified
        )
        if not valid:
            error[Runs.SEC_JUDGE_1] = Runs.SEC_JUDGE_1_ERR
        # validate time recorded by second judge
        valid = Runs.validate_actual_time(
            form[Runs.SEC_JUDGE_2],
            level,
            disqualified
        )
        if not valid:
            error[Runs.SEC_JUDGE_2] = Runs.SEC_JUDGE_2_ERR
        # validate number of rooms
        valid = Runs.validate_num_rooms(
            form[Runs.NUM_ROOMS],
            level
        )
        if not valid:
            error[Runs.NUM_ROOMS] = Runs.NUM_ROOMS_ERR
        # validate wall contact centimeters
        valid = Runs.validate_wall_contact(
            form[Runs.WALL_CONTACT]
        )
        if not valid:
            error[Runs.WALL_CONTACT] = Runs.WALL_CONTACT_ERR
        # validate touched candle
        valid = Runs.validate_touched_candle(
            form[Runs.TOUCHED_CANDLE]
        )
        if not valid:
            error[Runs.TOUCHED_CANDLE] = Runs.TOUCHED_CANDLE_ERR

        return error

    @staticmethod
    def validate_name(name, robot_name):
        return name.lower() == robot_name.lower()

    @staticmethod
    def validate_actual_time_compare(time_j1, time_j2):

        time_j1 = time_j1.strip()
        time_j2 = time_j2.strip()

        if time_j1.isdigit() and time_j2.isdigit():
            return float(time_j1) == float(time_j2)
        return False

    @staticmethod
    def validate_actual_time(time_s, level, failed):
        # minimum and maximum time allowed for each level

        time_s = time_s.strip()

        # convet to a float
        try:
            time = float(time_s)
        except:
            return False

        print (time, failed, 0 < time <= 180)
        if failed:
            if level in [1, 2]:
                return time == 600
            else:
                return time in L3_SCORES

        # validation for level 1
        if level == 1:
            return 0 < time <= 180

        if level == 2:
            return 0 < time <= 240

        if level == 3:
            return 0 < time <= 300

    # validate number of rooms
    @staticmethod
    def validate_num_rooms(num_s, level):
        if level not in [1, 2]:
            return True

        num_s = num_s.strip()
        # minimum and maximum allowed values
        min_123 = 0
        max_123 = 4

        # check if input string is a number
        if level in [1, 2]:
            if not num_s.isdigit():
                return False

            return (int(num_s) >= min_123) and (int(num_s) <= max_123)

        return True

    # validate wall contact distance
    @staticmethod
    def validate_wall_contact(num_s):

        num_s = num_s.strip()
        # minimum and maximum allowed values
        min_123 = 0
        max_123 = 500  # length of arena

        # check if input string is a number
        if not num_s.isdigit():
            return False

        return (int(num_s) >= min_123) and (int(num_s) <= max_123)

    # validate touched_candle
    @staticmethod
    def validate_touched_candle(num_s):
        num_s = num_s.strip()
        # Just check if it's digit for now
        # minimum allowed value
        min_123 = 0

        # check if input string is a number
        if not num_s.isdigit():
            return False

        return int(num_s) >= min_123

    # converts html form to a python dictonary
    @staticmethod
    def convert_to_dict(form):
        dictionary = {}
        for p in Runs.ALL:
            if p in Runs.BOOLEANS:
                dictionary[p] = True if p in form else False
            else:
                dictionary[p] = form[p] if p in form else None
        return dictionary

    # gets score of current run based on from data
    @ staticmethod
    def get_score(robot, data):
        # calculate actual time
        judge1 = Utilities.safe_cast(
            data[Runs.SEC_JUDGE_1],
            float,
            0
        )
        judge2 = Utilities.safe_cast(
            data[Runs.SEC_JUDGE_2],
            float,
            0
        )
        actual_time = (judge1 + judge2) / 2.0
        # cast number of rooms to int
        num_rooms = Utilities.safe_cast(
            data[Runs.NUM_ROOMS],
            int,
            0
        )
        # cast number of candle touches to int
        candle_touch = Utilities.safe_cast(
            data[Runs.TOUCHED_CANDLE],
            int,
            0
        )
        # cast wall contact cms to int
        wall_conatct = Utilities.safe_cast(
            data[Runs.WALL_CONTACT],
            int,
            0
        )
        return actual_time, Runs.calculate_run_score(
            robot_div=robot['division'],
            level=robot['level'],
            failed_trial=data[Runs.RUN_DISQ],

            actual_time=actual_time,
            non_air=data[Runs.NON_AIR],
            furniture=data[Runs.FURNITURE],
            arbitrary_start=data[Runs.ARBITRARY_START],
            return_trip=data[Runs.RETURN_TRIP],

            candle_location_mode=data[Runs.NO_CANDLE_CIRCLE],
            stopped_within_circle=data[Runs.STOPPED_WITHIN_30],
            signaled_detection=data[Runs.CANDLE_DETECTED],
            num_rooms_detected=num_rooms,
            kicked_dog=data[Runs.KICKED_DOG],
            touched_candle=candle_touch,
            cont_wall_contact=wall_conatct or 0,
            ramp_hallway=data[Runs.RAMP_USED],
            alt_target=data[Runs.SECONDARY_SAFE_ZONE],
            all_candles=data[Runs.ALL_CANDLES],
            l3_traversed_hallway=data[Runs.L3_TRAVERSED_HALLWAY],
            l3_found_baby=data[Runs.L3_FOUND_BABY],
            l3_rescued_baby=data[Runs.L3_RESCUED_BABY],
            l3_all_candles=data[Runs.L3_ALL_CANDLES],
            l3_one_candle=data[Runs.L3_ONE_CANDLE],
            l3_none=data[Runs.L3_NONE]
        )

    # calculates score
    @staticmethod
    def calculate_run_score(
        robot_div,
        level,
        failed_trial,
        actual_time,
        non_air,
        furniture,
        arbitrary_start,
        return_trip,
        candle_location_mode,
        stopped_within_circle,
        signaled_detection,
        num_rooms_detected,
        kicked_dog,
        touched_candle,
        cont_wall_contact,
        ramp_hallway,
        alt_target,
        all_candles,
        l3_traversed_hallway,
        l3_found_baby,
        l3_rescued_baby,
        l3_all_candles,
        l3_one_candle,
        l3_none
    ):

        task_search = num_rooms_detected * (-30)
        task_detect = -30 if signaled_detection else 0
        task_position = -30 if stopped_within_circle else 0

        om_candle = 0.75 if candle_location_mode else 1

        om_start = 0.8 if arbitrary_start else 1
        om_return = 0.8 if return_trip else 1
        om_extinguisher = 0.75 if non_air else 1
        om_furniture = 0.75 if furniture else 1

        if num_rooms_detected == 0 or num_rooms_detected == 1:
            room_factor = 1
        elif num_rooms_detected == 2:
            room_factor = 0.85
        elif num_rooms_detected == 3:
            room_factor = 0.5
        elif num_rooms_detected == 4:
            room_factor = 0.35

        pp_candle = 50 * touched_candle
        pp_slide = cont_wall_contact / 2
        pp_dog = 50 if kicked_dog else 0

        om_alt_target = 0.6 if alt_target else 1
        om_ramp_hallway = 0.9 if ramp_hallway else 1
        om_all_candles = 0.6 if all_candles else 1

        l3_failure_reduction_factor = 0
        if ramp_hallway:
            l3_failure_reduction_factor = 25
        # Scores
        if failed_trial:
            if robot_div in ['junior', 'walking'] and level == 1:
                return 600 + task_detect + task_position + task_search
            # elif level == 3 and actual_time in L3_SCORES:
            if level == 3:
                if l3_none:
                    return 600
                if l3_traversed_hallway:
                    score = 550
                    if l3_found_baby:
                        score = 450
                    if l3_found_baby and l3_one_candle:
                        score = 400
                    if l3_found_baby and l3_all_candles:
                        score = 350
                    if l3_rescued_baby:
                        score = 350
                    if l3_one_candle and l3_rescued_baby:
                        score = 325
                    return score - l3_failure_reduction_factor
            else:
                return 600

        if level == 1:
            score = (
                (actual_time + pp_candle + pp_dog + pp_slide) *
                (om_candle * om_start * om_return * om_extinguisher * om_furniture) * room_factor)

        if level == 2:
            score = (
                (actual_time + pp_candle + pp_dog + pp_slide) *
                (om_start * om_return * om_extinguisher * om_furniture) * room_factor)

        if level == 3:
            score = (
                (actual_time + pp_candle + pp_dog + pp_slide) *
                om_alt_target * om_ramp_hallway * om_all_candles
            )

        if score > 600:
            return 600
        else:
            return score
