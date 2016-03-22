# -*- coding: utf-8; -*-


class ScoreCalculator(object):
    @staticmethod
    def get_best_scores(runs):
        l1_scores = [run['score'] for run in runs if run['level'] == 1]
        l2_scores = [run['score'] for run in runs if run['level'] == 2]
        l3_scores = [run['score'] for run in runs if run['level'] == 3]

        best_scores = {
            'LS1': min(l1_scores) if l1_scores else 600.0,
            'LS2': min(l2_scores) if l2_scores else 600.0,
            'LS3': min(l3_scores) if l3_scores else 600.0
        }
        attempted_levels = set([run['level'] for run in runs])
        return best_scores, attempted_levels, sum(best_scores.val())
