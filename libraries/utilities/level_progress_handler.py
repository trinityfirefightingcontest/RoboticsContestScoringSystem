# -*- coding: utf-8; -*-


class LevelProgressHandler(object):
    @staticmethod
    def get_eligibility_for_next_run(runs, current_level):
        # initial values
        # 3 failures in same run - > disqualified.
        # 3, 4, and 5 minutes each for L1, L2 and L3

        disqualified = False
        can_level_up = False
        if not runs:
            return {
                'disqualified': disqualified,
                'can_level_up': can_level_up
            }

        current_level_runs = 0
        cons_failed_count = 0
        successful_trial = False

        for run in runs:
            if current_level != run['level']:
                continue
                current_level_runs += 1
            if run['failed_trial']:
                cons_failed_count += 1
            else:
                successful_trial = True
                # reset consecutive failure counter
                cons_failed_count = 0
            # if three consecutive failures
            if cons_failed_count >= 5:
                return {
                    'disqualified': True,
                    'can_level_up': False
                }

        if successful_trial and current_level in [1, 2]:
            can_level_up = True

        return {
            'disqualified': disqualified,
            'can_level_up': can_level_up
        }
