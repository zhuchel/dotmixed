#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""File related functionality. Currently supported: single report and general analysis report"""


import os

import platform
import sys
import time
import constant


def get_initial_values(kpress, elements_pos):
    """Gets initial values for single stimuli device response.
      :param kpress: pressed key code.
      :param elements_pos: two dimensional array of positional elements
      :return: 'L' or 'R' for pressed key, '0' or '1' for correctness and 'L' or 'R' for element positioning
    """
    answ = constant.KEY_PRESSED_LEFT
    answer = constant.ANSWER_INCORRECT
    pos = constant.STIMULI_IMAGE_POSITION_LEFT
    if kpress == constant.RIGHT_KEYCODE:
        answ = constant.KEY_PRESSED_RIGHT
    if elements_pos[0][0] > 0:
        pos = constant.STIMULI_IMAGE_POSITION_RIGHT
    return answ, answer, pos


def end_experiment(end_flag, parameters, testMode, data_file, device, core, mk_connection):
    """Ends current experiment.
    :param end_flag: experiment execution flag. 'False', if experiment was premature terminated
    """
    if end_flag:
        end_text = 'terminated at the end of the experiment'
    else:
        end_text = 'terminated by escape key'
    if parameters['MonitorFlag']:
        print(end_text)
    if parameters['DataFlag']:
        print(end_text)
    if testMode:
        data_file.close()
    if device == constant.PSYCHO_TOOLBOX:
        mk_connection.close()
    core.quit()