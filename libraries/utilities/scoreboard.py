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

    @staticmethod
    def get_gpmp_winners(robots):
        gpmp_winner = {}
        # only unique robots can win GPMP
        filtered = ScoreBoard.filter_robots_category(robots, 'unique')

        # check if number of successful runs is atleast 3
        filtered = ScoreBoard.filter_number_of_runs(filtered, 3)

        # sort robots
        score_name = 'TFS'
        sorted_robots = sorted(list(filtered), key=lambda k: k[score_name])

        # get winner
        for place in [1]:
            gpmp_winner[place] = sorted_robots[place-1] if place <= len(sorted_robots) else None

        return gpmp_winner

    @staticmethod
    def get_lisp_winners(robots):
        lisp_winners = {}

        for level in [1,2,3]:
            lisp_winners[level] = {}
            score_name = 'LS' + str(level)
            for category in ['unique','custom']:
                lisp_winners[level][category] = {}
                # filter based on level and category
                filtered = ScoreBoard.filter_robots_category(ScoreBoard.filter_robots_level(robots,level), category)
                # check if number of successful runs is atleast 3
                filtered = ScoreBoard.filter_number_of_runs(filtered, 3)
                # sort robots
                sorted_robots = sorted(list(filtered), key=lambda k: k[score_name])

                # get winners
                for place in [1]:
                    lisp_winners[level][category][place] = \
                        sorted_robots[place-1] if place <= len(sorted_robots) else None

        return lisp_winners

    @staticmethod
    def get_brd_winners(robots):
        brd_winners = {}

        for division in ['junior', 'high_school', 'walking', 'senior']:
            brd_winners[division] = {}
            score_name = 'TFS'
            for category in ['unique','custom']:
                brd_winners[division][category] = {}
                # filter based on division and category
                filtered = ScoreBoard.filter_robots_category(ScoreBoard.filter_robots_division(robots,division), category)
                # check if number of successful runs is atleast 3
                filtered = ScoreBoard.filter_number_of_runs(filtered,3)
                # sort robots
                sorted_robots = sorted(list(filtered), key=lambda k: k[score_name])

                # get winners
                for place in [1,2,3]:
                    brd_winners[division][category][place] = \
                        sorted_robots[place-1] if place <= len(sorted_robots) else None

        return brd_winners

    # filter robots based on level
    @staticmethod
    def filter_robots_level(robots, level):
        if level == 1:
            filtered = [robot for robot in robots if 1 in robot['completed'] and 2 not in robot['completed']]
        elif level == 2:
            filtered = [robot for robot in robots if 2 in robot['completed']]
        else:
            filtered = [robot for robot in robots if 3 in robot['completed']]

        return filtered

    # filter robots based on division
    @staticmethod
    def filter_robots_division(robots, division):
        return [robot for robot in robots if robot['division'] == division]

    # filter robots based on category(unique or customized)
    @staticmethod
    def filter_robots_category(robots, category):
        if category == 'unique':
            return [robot for robot in robots if robot['is_unique']]
        else:
            return [robot for robot in robots if not robot['is_unique']]

    # filter robots based number of sucessful runs
    @staticmethod
    def filter_number_of_runs(robots, minimum_runs):
        return [robot for robot in robots if robot['num_successful'] >= minimum_runs]
