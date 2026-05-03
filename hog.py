"""The Game of Hog."""

from cs61a.homework.hog.dice import six_sided, make_test_dice
from cs61a.homework.hog.ucb import main, trace, interact

GOAL = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome. Defaults to the six sided dice.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, "num_rolls must be an integer."
    assert num_rolls > 0, "Must roll at least once."
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    total = 0
    had_one = False
    for i in range(num_rolls):
        outcome = dice()
        if outcome == 1:
            had_one = True
        else:total += outcome
    
    if had_one == 1 :
        return 1
    return total


    # END PROBLEM 1

                                                   
def boar_brawl(player_score, opponent_score):
    """Return the points scored when the current player rolls 0 dice according to Boar Brawl.

    player_score:     The total score of the current player.
    opponent_score:   The total score of the other player.

    """
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    if player_score < 0 or opponent_score < 0 :
        print("请输入非负数")
    score_1 = (opponent_score // 10) % 10
    
    score_2 = player_score % 10
    result = abs(score_1 - score_2) * 3
    return max(result, 1)
    # END PROBLEM 2


def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the points scored on a turn rolling NUM_ROLLS dice when the
    current player has PLAYER_SCORE points and the opponent has OPPONENT_SCORE points.

    num_rolls:       The number of dice rolls that will be made.
    player_score:    The total score of the current player.
    opponent_score:  The total score of the other player.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, "num_rolls must be an integer."
    assert num_rolls >= 0, "Cannot roll a negative number of dice in take_turn."
    assert num_rolls <= 10, "Cannot roll more than 10 dice."
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if num_rolls == 0:
        # 如果投掷 0 个骰子，计算 Boar Brawl 的得分
        score = boar_brawl(player_score, opponent_score)
    else:
        # 如果投掷 > 0 个骰子，计算掷骰子的得分
        score = roll_dice(num_rolls, dice)
    
    # 关键！必须返回这回合拿到的分数
    return score

    # END PROBLEM 3


def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Sus Fuss.
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score


def is_prime(n):
    """Return whether N is prime."""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True


def num_factors(n):
    total = 0
    # 循环从 1 到 n（包括 n 本身，所以是 n + 1）
    for i in range(1, n + 1):
        if n % i == 0:
            total += 1
    return total
    "*** YOUR CODE HERE ***"
    # END PROBLEM 4


def sus_points(score):
    # BEGIN PROBLEM 4
    count = num_factors(score)
    if count == 3 or count == 4:
        # 只要还没找到质数（因子数不等于2），就一直往后找
        new_score = score + 1
        while num_factors(new_score) != 2:
            new_score += 1
        return new_score
    return score
    # END PROBLEM 4


def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, *including* Sus Fuss.
    """
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    player_score += take_turn(num_rolls, player_score, opponent_score, dice)
    player_score = sus_points(player_score)
    return player_score
    # END PROBLEM 4


def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the opponent's score.
    """
    return 5


def play(strategy0, strategy1, update, score0=0, score1=0, dice=six_sided, goal=GOAL):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.

    E.g., play(always_roll_5, always_roll_5, sus_update) simulates a game in
    which both players always choose to roll 5 dice on every turn and the Sus
    Fuss rule is in effect.

    A strategy function, such as always_roll_5, takes the current player's
    score and their opponent's score and returns the number of dice the current
    player chooses to roll.

    An update function, such as sus_update or simple_update, takes the number
    of dice to roll, the current player's score, the opponent's score, and the
    dice function used to simulate rolling dice. It returns the updated score
    of the current player after they take their turn.

    strategy0: The strategy for player0.
    strategy1: The strategy for player1.
    update:    The update function (used for both players).
    score0:    Starting score for Player 0
    score1:    Starting score for Player 1
    dice:      A function of zero arguments that simulates a dice roll.
    goal:      The game ends and someone wins when this score is reached.
    """
    # BEGIN PROBLEM 5
    who = 0
    while score0 < goal and score1 < goal:
        if who == 0:
            # 1. 调用 strategy 获取投掷次数
            num_rolls = strategy0(score0, score1)
            # 2. 调用 update 获取更新后的分数并赋值
            score0 = update(num_rolls, score0, score1, dice)
        else:
            # Player 1 的回合，注意参数顺序（当前玩家分数在前，对手在后）
            num_rolls = strategy1(score1, score0)
            score1 = update(num_rolls, score1, score0, dice)
        
        # 3. 切换玩家：0 变成 1，1 变成 0
        who = 1 - who 
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a player strategy that always rolls N dice.

    A player strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10

    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    def strategy(score, opponent_score):
        return n
    return strategy
    # END PROBLEM 6


def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # Roll one more to catch up
    else:
        return 5


def is_always_roll(strategy, goal=GOAL):
    """Return whether STRATEGY always chooses the same number of dice to roll
    for every possible combination of score and opponent_score
    given a game that goes to GOAL points.

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    first_roll = strategy(0,0)

    for i in range(goal):
        for j in range(goal):
            if strategy(i, j) != first_roll:
                return False
    return True

    # END PROBLEM 7


def make_averaged(original_function, times_called=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TIMES_CALLED times.

    To implement this function, you will have to use *args syntax.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    3.0
    """

    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def fn(*args):
        result = 0
        for i in range(times_called):
            result += original_function(*args)
        total = result / times_called
        return total
    return fn
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, times_called=1000):
    """Return the number of dice (1 to 10) that gives the maximum average score for a turn.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # roll_dice(num_rolls, dice=six_sided)
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    average = make_averaged(roll_dice, times_called)
    count = 1
    max_num = 1
    pre_point = average(count, dice)
    for i in range(9):
        curr_point = average(count + 1, dice)
        if curr_point > pre_point :
            max_num = count + 1
            pre_point = curr_point
        count += 1
    return max_num
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print("Max scoring num rolls for six-sided dice:", six_sided_max)

    print("always_roll(6) win rate:", average_win_rate(always_roll(6)))  # near 0.5
    print("catch_up win rate:", average_win_rate(catch_up))
    print("always_roll(3) win rate:", average_win_rate(always_roll(3)))
    print("always_roll(8) win rate:", average_win_rate(always_roll(8)))

    print("boar_strategy win rate:", average_win_rate(boar_strategy))
    print("sus_strategy win rate:", average_win_rate(sus_strategy))
    print("final_strategy win rate:", average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"




def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice if Boar Brawl gives at least THRESHOLD
    points, and returns NUM_ROLLS otherwise. Ignore the Sus Fuss rule.
    """
    # BEGIN PROBLEM 10
    point = boar_brawl(score, opponent_score)
    if point >= threshold :
        return 0
    return num_rolls  # Remove this line once implemented.
    # END PROBLEM 10


def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice when rolling 0 increases the score by at least
    THRESHOLD points, and returns NUM_ROLLS otherwise. Consider both the Boar Brawl and
    Suss Fuss rules."""
    # BEGIN PROBLEM 11
    point_zero = boar_brawl(score,opponent_score)
    total = score + point_zero
    point_sus = sus_points(total)
    if point_sus - score >= threshold:
        return 0
    else:
        return num_rolls  # Remove this line once implemented.
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # 1. 先看投 0 个骰子能不能直接赢，或者收益是否巨大
    bb_score = boar_brawl(score, opponent_score)
    new_score_if_0 = sus_points(score + bb_score)
    if new_score_if_0 >= GOAL:
        return 0
    
    # 2. 如果投 0 个收益非常诱人（比如大于某个阈值）
    if new_score_if_0 - score >= 9:
        return 0

    # 3. 如果落后较多，可以稍微激进一点
    if opponent_score - score > 20:
        return 6
        
    # 4. 默认策略：通常 6 是一个比较稳健的平均最高分
    return 6
    # BEGIN PROBLEM 12 # Remove this line once implemented.
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: The function in this section does not need to be changed. It uses
# features of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse

    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument(
        "--run_experiments", "-r", action="store_true", help="Runs strategy experiments"
    )

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()