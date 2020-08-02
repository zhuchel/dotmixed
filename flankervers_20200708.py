#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Flanker experiment for little children.
   Response device: MilliKey device or keyboard
"""

# Author: Alyona Lainburg
# e-mail: Alyona.Lainburg[at]uni-ulm.de

from __future__ import absolute_import, division, print_function

import os
import random
import sys
import time

import serial
import win32api
from psychopy import core, visual, event

import c_device
import c_file
import c_inputscreen  # class TK to read data from PsychoPy Screen
import c_result
import c_visual
import constant

__author__ = 'Alyona Lainburg'
__version__ = 'v1.00 20200708'

# default port
mK_serial_port = 'COM8'

pathname = os.path.dirname(sys.argv[0])
RunPath = os.path.abspath(pathname)

# experiment parameters
parameters = {
    'DataPath': 'flanker_result_files',  # data directory
    'ScreenSize': [1024, 768],
    'FullScr': False,
    'NoMonitor': 0,  # 0 is windows 1, 1 is windows 2
    'ScreenUnits': 'height',  # range -0.5 ... 0.5 in height, -0.667 - 0.667 width
    'BackColor': -1.0,  # range -1 ... 1,

    'PicPath': 'Pict',  # pictures directory
    'DotFile': ('blue_congr.jpg', 'blue_incongr.jpg', 'red_congr.jpg', 'red_incongr.jpg'),
    'ArrowY': -0.3,  # relative distance of arrow from midline down
    'DotX': 0.0,  # relative distance of dot from midline to the left and right
    'WaitKey': 'space',
    'WaitKeyText': 'Leertaste',
    'TextUnit': 'height',  # ‘height’, ‘norm’, ‘cm’, ‘deg’ or ‘pix’
    'TextFont': 'Arial',
    'TextColor': (0.9, 0.9, 0.9),
    'TextBold': False,
    'FLeng': 9,  # half length of fixation cross in pix
    'FWi': 2,  # width of fixation cross in pix
    'Fcolor': 'white',  # fixation cross
    'DataFlag': True,  # maybe switched off - then no datafile is generated
    'MonitorFlag': False,  # experiment performance and results in output window
    'InstructText': u'bla',
    'InstructHeight': 0.04,
    'InstructPos': (0, 0),
    'FixDur': 3,  # timeout in sec
    'blank_duration': 0.5,  # waiting time between stimuli in seconds
    'wait_between_trails': 0.001,  # waiting time for keybox pressing events in seconds
    'NoRepetitions': 4,  # 12,   number of repetitions for mixed trails
    'NoRepetitionsTest': 8,   # 20,   number of repetitions for mixed test
    'SubjectID': '0',
    'NoCharInput': 6,
    'no_probe_repetitions': 4,   # 8,  number of repetitions for non mixed trails
    'too_fast_time': 200,  # threshold for too fast key pressing (overflow)
    'KeyCode': ('left', 'right'),  # key codes for keyboard - left and right arrows
    'toolbox_wait_time': 1.0  # key press wait time in seconds
}


def execute_shuffled_stimuli(number_repetitions, stimuli):
    """Executes shuffled stimuli using cross/image switching. If PSYCHO_TOOLBOX would
    be used, terminate connection before switching to cross and re-connect before
    switching to image

       :param number_repetitions: number of repetitions.
       :param stimuli: two dimensional array of stimuli
    """
    global mk_connection
    random.shuffle(stimuli)
    i = 0
    for trail in range(number_repetitions):
        if device == constant.PSYCHO_TOOLBOX:
            mk_connection.close()
        pressed_key = c_visual.instruct_cross_wait(ElementsCross, ElementsCrossPos, ExpWin, time,
                                                   parameters['blank_duration'], event)
        if pressed_key == 'q':
            end_experiment(False)
        if device == constant.PSYCHO_TOOLBOX:
            mk_connection = serial.Serial(mK_serial_port, baudrate=128000, timeout=0.1)
        instruct_pic_wait(stimuli[trail][0], stimuli[trail][1], InstructText, [], i)
        i += 1


def do_stimuli_execution(dialog_text, number_repetitions, colored_elements):
    """Carries out stimuli execution. Applied for mixed and non-mixed (colored) elements.
       :param dialog_text: text for info dialog.
       :param number_repetitions: number of repetitions
       :param colored_elements: elements for single colored execution or 'None' for mixed mode
    """
    if dialog_text is not None:
        show_dialog(dialog_text)
    random.seed()
    if colored_elements is not None:
        stimuli_probe = c_result.create_colored_stimuli(number_repetitions, colored_elements, ElementsPosRight,
                                                        ElementsPosLeft)
    else:
        stimuli_probe = c_result.create_mixed_stimuli1(number_repetitions, ElementsBlueCongr, ElementsRedCongr,
                                                       ElementsBlueUncongr, ElementsRedUncongr, ElementsPosLeft)
    execute_shuffled_stimuli(number_repetitions, stimuli_probe)


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


def get_answer_for_element(initial_answer, color, answ, pos):
    """Gets answer correctness from provided context.
     :param initial_answer: initial answer.
     :param color: stimuli element color
     :param answ: key pressed (left or right)
     :param pos: real stimuli element position (left or right)
     :return: '1' for correct answer and '0' for incorrect answer
     """
    answer = initial_answer
    if color == constant.CONGRUENT_COLOR:
        if answ == constant.KEY_PRESSED_RIGHT:
            answer = constant.ANSWER_CORRECT
            cumulativeResult.correct_count += 1
        else:
            cumulativeResult.incorrect_count += 1
    if color == constant.UNCONGRUENT_COLOR:
        if answ == constant.KEY_PRESSED_LEFT:
            answer = constant.ANSWER_CORRECT
            cumulativeResult.correct_count += 1
        else:
            cumulativeResult.incorrect_count += 1
    return answer


def process_key_pressed(kb_presses, elements_pos, stime, elements, count):
    """Carries out key pressed event processing.
    :param kb_presses: one dimensional array of key pressed event. Is empty, if no key was pressed
    :param elements_pos: two dimensional array of positional elements
    :param stime: start time before key was pressed
    :param elements: image elements containing congruent and non-congruent colors
    :param count: current stimuli index (beginning with 0)
    :return: 'True', if 'left' of 'right' device key was pressed
    """
    global cumulativeResult
    global results
    key_pressed = False
    if kb_presses:
        kpress, ktime = kb_presses[0]
        if kpress == 'q' or kpress == 'escape':
            end_experiment(False)
        if kpress is not None and (kpress == constant.LEFT_KEYCODE or kpress == constant.RIGHT_KEYCODE):
            answ, answer, pos = get_initial_values(kpress, elements_pos)
            answer = get_answer_for_element(answer, elements[1], answ, pos)
            if testMode:
                diff_time = ktime-stime
                # key pressing was done too quick. We don't consider such key overflow
                if diff_time*1000 < parameters['too_fast_time']:
                    cumulativeResult.timeout_too_fast_count += 1
                    if answer == constant.ANSWER_CORRECT:
                        cumulativeResult.correct_count -= 1
                    if answer == constant.ANSWER_INCORRECT:
                        cumulativeResult.incorrect_count -= 1
                    answ = constant.STIMULI_NO_ANSWER
                    answer = constant.ANSWER_INCORRECT
                    diff_time = 0.0
                if answer == constant.ANSWER_CORRECT:
                    results.append(diff_time)
                    cumulativeResult.cumulative_time += diff_time
                c_file.write_stimuli_row(data_file, count, elements[2], elements[1], answ, answer, diff_time,
                                         cumulativeResult.cumulative_time)
            key_pressed = True
    return key_pressed


def end_experiment(end_flag):
    """Ends current experiment.
    :param end_flag: experiment execution flag. 'False', if experiment was premature terminated
    """
    global mk_connection
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


def show_dialog(text):
    """Displays text dialog.
    :param text: text to display in the dialog
    """
    buffer = [text + ' \n\n\n\n', 'Weiter mit der ', parameters['WaitKeyText']]
    pressed_key = c_visual.instruct_wait(InstructText, ''.join(buffer), parameters['WaitKey'], ExpWin, event)
    if pressed_key == 'q':
        end_experiment(False)


def execute_test_step(dialog_text, step, elements):
    """Carries out test step.
    :param dialog_text: text to display in the dialog
    :param step: step number
    :param elements: elements for single colored execution or 'None' for mixed mode
    """
    show_dialog(dialog_text)
    cumulativeResult.reset()
    c_file.write_step_header1(step, data_file)
    do_stimuli_execution(None, parameters['NoRepetitionsTest'], elements)
    c_file.write_footer(data_file, cumulativeResult.correct_count, parameters['NoRepetitionsTest'])
    return c_result.build_result(cumulativeResult, parameters['NoRepetitionsTest'], results)


def instruct_pic_wait(elements, elements_pos, wait_text_element, wait_text, count):
    """Displays graphical stimuli and waits for key input.
    :param elements: graphical stimuli elements to display (e.g. flower and cross)
    :param elements_pos: graphical stimuli elements positions
    :param wait_text_element: wait text elements
    :param wait_text: wait text
    :param count: current stimuli index (beginning with 0)
    """
    global cumulativeResult
    c_visual.draw_elements(elements, elements_pos, wait_text_element, wait_text, ExpWin)
    flag_wait = True
    react_time_start = TrialClock.getTime()
    stime = c_device.get_start_time(device, core, TrialClock)
    while flag_wait:
        kb_presses = c_device.get_presses_from_device(device, event, parameters['toolbox_wait_time'], core, TrialClock,
                                                      parameters['KeyCode'])
        key_pressed = process_key_pressed(kb_presses, elements_pos, stime, elements, count)
        while not kb_presses or not key_pressed:
            kb_presses = c_device.get_presses_from_device(device, event, parameters['toolbox_wait_time'], core,
                                                          TrialClock, parameters['KeyCode'])
            key_pressed = process_key_pressed(kb_presses, elements_pos, stime, elements, count)
            # necessary for prevention of overflows, which can lead to lost key events
            time.sleep(parameters['wait_between_trails'])
            if not key_pressed:
                react_time_end = TrialClock.getTime()
                react_time = int(round(react_time_end - react_time_start, 3))
                if react_time > parameters['FixDur']:
                    # timeout waiting for key event
                    if testMode:
                        cumulativeResult.timeout_too_fast_count += 1
                        pos = constant.STIMULI_IMAGE_POSITION_LEFT
                        if elements_pos[0][0] > 0:
                            pos = constant.STIMULI_IMAGE_POSITION_RIGHT
                        c_file.write_stimuli_row(data_file, count, elements[2], elements[1], constant.STIMULI_NO_ANSWER,
                                                 constant.STIMULI_NO_ANSWER, react_time,
                                                 cumulativeResult.cumulative_time)
                    return
        flag_wait = False

###############################################################
GlobalClock = core.Clock()  # to keep track of time
TrialClock = core.Clock()  # to keep track of time
random.seed()

device = constant.KEYBOARD  # we have multi device implementation (default:  KEYBOARD)

serial_ports = c_device.get_millikey_serial_port()  # PSYCHO_TOOLBOX port
if serial_ports:
    mK_serial_port = serial_ports[0]
print('port=', serial_ports)

mk_connection = None
try:
    mk_connection = serial.Serial(mK_serial_port, baudrate=128000, timeout=0.1)
    device = constant.PSYCHO_TOOLBOX
except:
    print('MilliKey device not available')


results = []
ww = 1
wh = 1
FlagFull = False
try:
    ww = win32api.GetSystemMetrics(0)
    wh = win32api.GetSystemMetrics(1)
    FlagFull = True
except:
    print('Full screen mode not available')

if FlagFull:
    parameters['ScreenSize'] = (ww, wh)
    parameters['FullScr'] = True

# visual stimuli
ExpWin = c_visual.get_exp_win(parameters)

# fixation cross
FLine1 = c_visual.get_cross_line_1(ExpWin, parameters)
FLine2 = c_visual.get_cross_line_2(ExpWin, parameters)

InstructText = c_visual.get_instruct_text(ExpWin, parameters)
# stimuli images
CongrStimBlue = visual.ImageStim(ExpWin,
                                 image=os.path.join(RunPath, parameters['PicPath'], parameters['DotFile'][0])
                                 )
CongrStimRed = visual.ImageStim(ExpWin,
                                image=os.path.join(RunPath, parameters['PicPath'], parameters['DotFile'][2])
                                )
UncongrStimBlue = visual.ImageStim(ExpWin,
                                   image=os.path.join(RunPath, parameters['PicPath'], parameters['DotFile'][1])
                                   )
UncongrStimRed = visual.ImageStim(ExpWin,
                                  image=os.path.join(RunPath, parameters['PicPath'], parameters['DotFile'][3])
                                  )
while True:
    cumulativeResult = c_result.CumulativeResult()


    # Cross
    ElementsCross = [FLine1, FLine2]
    ElementsCrossPos = ((parameters['ArrowY']), (0, 0), (0, 0))
    # Images
    ElementsBlueCongr = [CongrStimBlue, 'blue', '1']
    ElementsRedCongr = [CongrStimRed, 'red', '1']
    ElementsBlueUncongr = [UncongrStimBlue, 'blue', '0']
    ElementsRedUncongr = [UncongrStimRed, 'red', '0']

    ElementsPosLeft = ((-1 * parameters['DotX'], 0), (-1 * parameters['DotX'], 0), (0, 0), (0, 0))
    ElementsPosRight = ((parameters['DotX'], 0), (parameters['DotX'], 0), (0, 0), (0, 0))

    show_dialog('Experiment mit ' + device)
    parameters['SubjectID'] = c_inputscreen.get_proband_id(parameters, ExpWin)

    testMode = True
    data_file = c_file.init_file(__version__, __author__, parameters['SubjectID'], parameters['DataPath'], device)
    mixed_results = execute_test_step('Test Flanker', 3, None)
    c_file.write_analysis(data_file, None, None, mixed_results, parameters['DataPath'],
                          parameters['SubjectID'], constant.REPORT_FILE_NAME)
    show_dialog('Experiment beendet. Vielen Dank!')

    if device == constant.PSYCHO_TOOLBOX:
        mk_connection.close()
    end_experiment(True)
