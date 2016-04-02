from libraries.utilities.score_calculator import ScoreCalculator
import registry as r


class ScoreBoard():
    @staticmethod
    def add_scoreboard_params(robots):
        # adds necessary parameters to be displayed on the scoreboard
        for robot in robots:
            runs = r.get_registry()['RUNS'].get_runs(robot['id'])
            best_scores, attempted_levels, total_score, num_successful = (
                ScoreCalculator.get_best_scores(runs)
            )
            robot.update(best_scores)
            robot['TFS'] = total_score
            robot['completed'] = attempted_levels
            robot['num_successful'] = num_successful
        return robots
