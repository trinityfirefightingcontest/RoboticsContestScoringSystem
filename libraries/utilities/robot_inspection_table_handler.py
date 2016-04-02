# -*- coding: utf-8 -*-
import registry as r


class RobotInspectionTableHandler:
    HEIGHT = 'height'
    WIDTH = 'width'
    BREADTH = 'breadth'
    PASSES_INSPECTION = 'passes_inspection'
    PASSES_CHECK_BOX_ERR = 'PASSES_CHECK_BOX_ERR'
    HEIGHT_ERR = 'HEIGHT_ERR'
    WIDTH_ERR = 'WIDTH_ERR'
    BREADTH_ERR = 'BREADTH_ERR'

    REQUIRED_INPUTS = {
        HEIGHT: {
            'modifer': lambda x: int(x),
            'validator': lambda x: x > 0 and x <= 27,
            'error_key': HEIGHT_ERR
        },
        WIDTH: {
            'modifer': lambda x: int(x),
            'validator': lambda x: x > 0 and x <= 31,
            'error_key': WIDTH_ERR
        },
        BREADTH: {
            'modifer': lambda x: int(x),
            'validator': lambda x: x > 0 and x <= 31,
            'error_key': BREADTH_ERR
        },
        PASSES_INSPECTION: {
            'modifer': lambda x: bool(x),
            'validator': lambda x: x is True,
            'error_key': PASSES_CHECK_BOX_ERR
        }
    }

    @classmethod
    def validate_inputs(cls, inputs):
        valid = True
        vals = {}
        for i, j in cls.REQUIRED_INPUTS.iteritems():
            try:
                vals[i] = j['modifer'](inputs.get(i))
                vals[j['error_key']] = not j['validator'](vals[i])
            except:
                vals[j['error_key']] = True
            valid = valid and not vals[j['error_key']]
        return valid, vals

    @staticmethod
    def approve_and_store_volume(height, width, breadth, robot_id):
        r.get_registry()['ROBOTS'].approve_and_store_volume(
            robot_id=robot_id, volume=height * width * breadth
        )
