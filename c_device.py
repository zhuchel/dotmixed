#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Device related functionality. Currently supported: MilliKey and Keyboard"""

from __future__ import absolute_import, division, print_function

import os
import serial
import constant


def get_millikey_serial_port():
    """
    Return list of serial port addresses that have been opened.
    See http://blog.labhackers.com/
    """
    if os.name == 'nt':  # Windows
        available = []
        for i in range(1, 512):
            try:
                sport = 'COM%d' % i
                s = serial.Serial(sport, baudrate=128000)
                available.append(sport)
                s.close()
            except (serial.SerialException, ValueError):
                pass
        return available
    else:  # macOS and Linux
        from serial.tools import list_ports
        return [port[0] for port in list_ports.comports()]


def get_start_time(device, core, trial_clock):
    """Gets start time for provided device context.
    :param device: current device.
    :param core: psychoPy import core
    :param trial_clock: core.Clock()
    :return: start time
    """
    start_time = 0
    if device == constant.PSYCHO_TOOLBOX:
        # See http://blog.labhackers.com/?cat=29
        evt_delay_sec = constant.MILLI_KEY_DELAY / 1000.0 / 1000.0
        start_time = core.getTime() + evt_delay_sec
    if device == constant.KEYBOARD:
        start_time = trial_clock.getTime()
    return start_time


def get_presses_from_device(device, event, toolbox_wait_time, core, trial_clock, key_code):
    """Gets two dimensional array with one element, containing event key and key reaction time.
    :param device: current device
    :param event: psychoPy import event
    :param toolbox_wait_time: toolbox waiting time
    :param core: psychoPy import core
    :param trial_clock: core.Clock()
    :param key_code: keyboard observed key codes (e.g. 'left' and 'right')
    :return: two dimensional array with one element, containing event key and key reaction time
    """
    kb_presses = None
    if device == constant.PSYCHO_TOOLBOX:
        event_key = event.waitKeys(maxWait=toolbox_wait_time)
        if event_key:
            kb_presses = [[event_key[0], core.getTime()]]
    if device == constant.KEYBOARD:
        kb_presses = get_keyboard_response(event, trial_clock, key_code)
    return kb_presses


def get_keyboard_response(event, trial_clock, key_code):
    """Gets two dimensional array with one element, containing event key and key reaction time from keyboard emulation.
    :param event: psychoPy import event
    :param trial_clock: core.Clock()
    :param key_code: keyboard observed keycodes (e.g. 'left' and 'right')
    :return: two dimensional array with one element, containing event key and key reaction time
    """
    act_key = -1
    kb_presses = None
    react_time_s = 0
    for key in event.getKeys(timeStamped=trial_clock):
        react_time_s = trial_clock.getTime()
        act_key = key[0]
    if act_key in ['q', 'escape']:
        kb_presses = [['q', react_time_s]]
    if act_key in key_code:
        arrow = constant.LEFT_KEYCODE
        if act_key == 'right':
            arrow = constant.RIGHT_KEYCODE
        kb_presses = [[arrow, react_time_s]]
    return kb_presses
