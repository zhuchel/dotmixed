#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""GUI related functions"""

from __future__ import absolute_import, division, print_function

from psychopy import visual


# gets main window
def get_exp_win(parameters):
    return visual.Window(parameters['ScreenSize'], units=parameters['ScreenUnits'], fullscr=parameters['FullScr'],
                         screen=parameters['NoMonitor'], color=parameters['BackColor'],
                         allowGUI=not parameters['FullScr'])


# creates cross line 1
def get_cross_line_1(exp_win, parameters):
    return visual.Line(exp_win, units='pix', start=(- parameters['FLeng'], 0), end=(parameters['FLeng'], 0),
                       lineWidth=parameters['FWi'], lineColor=parameters['Fcolor'])


# creates cross line 2
def get_cross_line_2(exp_win, parameters):
    return visual.Line(exp_win, units='pix', start=(0, - parameters['FLeng']), end=(0, parameters['FLeng']),
                       lineWidth=parameters['FWi'], lineColor=parameters['Fcolor'])


# creates instructional text
def get_instruct_text(exp_win, parameters):
    return visual.TextStim(exp_win, units=parameters['TextUnit'], height=parameters['InstructHeight'],
                           pos=parameters['InstructPos'], font=parameters['TextFont'], bold=parameters['TextBold'],
                           text=parameters['InstructText'])


def draw_elements_without_text(elements, elements_pos, exp_win):
    """Draw elements without text.
    :param elements: elements to draw
    :param elements_pos: positions of the elements to draw
    :param exp_win: visual.Window
    """
    i = 0
    for Element in elements:
        if i < 3 and type(Element) != str:
            Element.setPos(elements_pos[i])
            Element.draw()
        i += 1
    exp_win.flip()


def draw_elements(elements, elements_pos, wait_text_element, wait_text, exp_win):
    """Draw elements.
    :param elements: elements to draw
    :param elements_pos: positions of the elements to draw
    :param wait_text_element: wait text element
    :param wait_text: wait text
    :param exp_win: visual.Window
    """
    if wait_text:
        wait_text_element.setText(wait_text)
        wait_text_element.draw()
    draw_elements_without_text(elements, elements_pos, exp_win)


def instruct_cross_wait(elements, elements_pos, exp_win, time, blank_duration, event):
    """Draw cross and wait shortly for key input.
    :param elements: cross elements to draw
    :param elements_pos: positions of the cross elements to draw
    :param exp_win: visual.Window
    :param time: import time
    :param blank_duration: waiting time between stimuli in seconds
    :param event: from psychoPy import event
    :return: 'q', is 'escape' keyboard key was pressed, otherwise empty
    """
    pressed_key = ''
    draw_elements_without_text(elements, elements_pos, exp_win)
    time.sleep(blank_duration)
    for keys in event.getKeys():
        if keys in ['q', 'escape']:
            pressed_key = 'q'
        if keys in ['escape', 'q']:
            pressed_key = 'q'
    return pressed_key


def instruct_wait(wait_text_element, wait_text, wait_key, exp_win, event):
    """Draw text element and wait for key input.
    :param wait_text_element: text elements to draw
    :param wait_text: wait text
    :param wait_key: 'Leertaste'
    :param exp_win: visual.Window
    :param event: from psychoPy import event
    :return: 'q', is 'escape' keyboard key was pressed, otherwise empty
    """
    pressed_key = ''
    if wait_text:
        wait_text_element.setText(wait_text)
    wait_text_element.draw()
    exp_win.flip()
    flag_wait = True
    while flag_wait:
        for keys in event.getKeys():
            if keys in ['q', 'escape']:
                pressed_key = 'q'
            if keys in ['escape', 'q']:
                pressed_key = 'q'
            if keys in wait_key:
                flag_wait = False
    return pressed_key
