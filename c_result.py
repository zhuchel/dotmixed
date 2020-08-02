#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Experiment related classes and functions"""

import numpy


class Result:
    """Class containing single step results """
    def __init__(self, x_r, x_r_quote, x_r_rt_mean, xr_rt_median, x_w, x_err):
        self.x_r = x_r
        self.x_r_quote = x_r_quote
        self.x_r_rt_mean = x_r_rt_mean
        self.xr_rt_median = xr_rt_median
        self.x_w = x_w
        self.x_err = x_err


class CumulativeResult:
    """Class containing cumulative results """
    def __init__(self):
        self.cumulative_time = 0.0
        self.correct_count = 0
        self.incorrect_count = 0
        self.timeout_too_fast_count = 0

    def reset(self):
        """Reset values """
        self.cumulative_time = 0.0
        self.correct_count = 0
        self.incorrect_count = 0
        self.timeout_too_fast_count = 0


def build_result(cumulative_result, number_repetitions, results):
    """Creates Result class from single step execution.
    :param cumulative_result: CumulativeResult class instance
    :param number_repetitions: number of repetitions
    :param results: list filled with time values
    :return: created and populated Result class
    """
    np_array = numpy.array(results)

    mean = np_array.mean()
    if numpy.isnan(mean):
        mean = 0.0

    median = numpy.median(np_array)
    if numpy.isnan(median):
        median = 0.0

    x = Result(cumulative_result.correct_count, cumulative_result.correct_count / number_repetitions * 100,
               mean*1000, median*1000, cumulative_result.incorrect_count,
               cumulative_result.timeout_too_fast_count)
    results.clear()
    return x


def create_colored_stimuli(number_repetitions, colored_elements, elements_pos_right, elements_pos_left):
    """Creates colored (ocnly red or only blue) stimuli.
    :param number_repetitions: number of repetitions
    :param colored_elements: colored elements
    :param elements_pos_right: colored elements in right positions
    :param elements_pos_left: colored elements in left positions
    :return: created colored stimuli
    """
    normed_probe = round(number_repetitions / 2)
    stimuli_probe_colored = [[0 for x in range(2)] for y in range(number_repetitions)]
    for i in range(normed_probe):
        stimuli_probe_colored[i][0] = colored_elements
        stimuli_probe_colored[i][1] = elements_pos_right
        stimuli_probe_colored[i + normed_probe][0] = colored_elements
        stimuli_probe_colored[i + normed_probe][1] = elements_pos_left
    return stimuli_probe_colored


def create_mixed_stimuli(number_repetitions, elements_congruent, elements_pos_right, elements_pos_left,
                         elements_uncongruent):
    """Creates mixed stimuli.
    :param number_repetitions: number of repetitions
    :param elements_congruent: congruent elements
    :param elements_pos_right: colored elements in right positions
    :param elements_pos_left: colored elements in left positions
    :param elements_uncongruent: non congruent elements
    :return: created mixed stimuli
    """
    normed = round(number_repetitions / 4)
    stimuli = [[0 for x in range(2)] for y in range(number_repetitions)]
    for i in range(normed):
        stimuli[i][0] = elements_congruent
        stimuli[i][1] = elements_pos_right
        stimuli[i + normed][0] = elements_congruent
        stimuli[i + normed][1] = elements_pos_left
        stimuli[i + round(number_repetitions / 2)][0] = elements_uncongruent
        stimuli[i + round(number_repetitions / 2)][1] = elements_pos_left
        stimuli[i + 3 * normed][0] = elements_uncongruent
        stimuli[i + 3 * normed][1] = elements_pos_right
    return stimuli


def create_mixed_stimuli1(number_repetitions, elements_congruent_blue, elements_congruent_red,
                          elements_uncongruent_blue, elements_uncongruent_red, elements_pos_left):
    """Creates mixed stimuli.
    :param number_repetitions: number of repetitions
    :param elements_congruent: congruent elements
    :param elements_pos_right: colored elements in right positions
    :param elements_pos_left: colored elements in left positions
    :param elements_uncongruent: non congruent elements
    :return: created mixed stimuli
    """
    normed = round(number_repetitions / 4)
    stimuli = [[0 for x in range(2)] for y in range(number_repetitions)]
    for i in range(normed):
        stimuli[i][0] = elements_congruent_blue
        stimuli[i][1] = elements_pos_left
        stimuli[i + normed][0] = elements_congruent_red
        stimuli[i + normed][1] = elements_pos_left
        stimuli[i + round(number_repetitions / 2)][0] = elements_uncongruent_blue
        stimuli[i + round(number_repetitions / 2)][1] = elements_pos_left
        stimuli[i + 3 * normed][0] = elements_uncongruent_red
        stimuli[i + 3 * normed][1] = elements_pos_left
    return stimuli



