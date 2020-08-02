#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Class c_inputscreen - to handle text input from psychoPy screen
Based on Thomas' initial implementation"""

from psychopy import visual, event

class InputScreenHandler:
    """Class to handle text input from psychopy screen """

    def __init__(self, screen_win, key_return=['return'], key_quit=['escape'], key_erase=['backspace'],
                 key_in=['lower', 'number'], key_specific=[], in_minimum=0, in_maximum=999999999,
                 input_info_str='', input_explain_min_str='', input_explain_max_str='', input_info_pos=(0, 0),
                 input_text_pos=(0, 0), input_explain_pos=(0, 0), units=None, height=None, color=(1.0, 1.0, 1.0),
                 font='', bold=False, italic=False):
        self._initParams = dir()
        self._initParams.remove('self')
        self._letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                         's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self._numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self._germanumlaut = [u'\xe4', u'\xf6', u'\xfc', u'\xc4', u'\xd6', u'\xdc', u'\xdf']  # äöü ÄÖÜ ß
        self._interpunction = [' ', ',', '.', ';', ':', '-', '_', '!', '?']
        self._shiftkeys = ['lshift', 'rshift']
        self._controlkeys = ['escape', 'return', 'backspace']
        self._ScreenWin = screen_win
        self.KeyReturn = key_return
        self.KeyQuit = key_quit
        self.KeyErase = key_erase
        self.KeyIn = key_in
        self.KeySpecific = key_specific
        self.InMinimum = in_minimum
        self.InMaximum = in_maximum
        self.InputInfoStr = input_info_str
        self.InputInfoPos = input_info_pos
        self.InputTextPos = input_text_pos
        self.InputExplainMinStr = input_explain_min_str
        self.InputExplainMaxStr = input_explain_max_str
        self.InputExplainPos = input_explain_pos
        self._onlyUpper = False
        self._InputKeyList = self.KeyReturn + self.KeyQuit + self.KeyErase + self.KeySpecific
        if 'upper' in key_in:
            if not 'lower' in key_in:
                self._InputKeyList += self._letters
                self._onlyUpper = True
            else:
                self._InputKeyList += self._shiftkeys
        if 'lower' in key_in:
            self._InputKeyList += self._letters
        if 'number' in key_in:
            self._InputKeyList += self._numbers
        self._TextInput = ''
        self.KeyTerminate = ''
        self.OK = False
        self._InputInfoText = visual.TextStim(screen_win, text=input_info_str, pos=input_info_pos, units=units,
                                              height=height, color=color, font=font, bold=bold, italic=italic)
        self._InputText = visual.TextStim(screen_win, text='', pos=input_text_pos, units=units, height=height,
                                          color=color, font=font, bold=bold, italic=italic)
        self._ExplainText = visual.TextStim(screen_win, text='', pos=input_explain_pos, units=units, height=height,
                                            color=color, font=font, bold=bold, italic=italic)

    def get_input(self):
        self._InputInfoText.draw()
        self._ScreenWin.flip()
        self.KeyTerminate = ''
        self._TextInput = ''
        wait_for_input = True
        shift_flag = False
        while wait_for_input:
            for keys in event.getKeys(keyList=None):
                if keys in self.KeyQuit:
                    self.KeyTerminate = keys
                    self._TextInput = ''
                    wait_for_input = False
                    self.OK = False
                elif keys in self.KeyReturn:
                    if len(self._TextInput) < self.InMinimum:
                        self._ExplainText.setText(self.InputExplainMinStr)
                        self._ExplainText.draw()
                        self._InputInfoText.draw()
                        self._InputText.draw()
                        self._ScreenWin.flip()
                    elif len(self._TextInput) > self.InMaximum:
                        self._ExplainText.setText(self.InputExplainMaxStr)
                        self._ExplainText.draw()
                        self._InputInfoText.draw()
                        self._InputText.draw()
                        self._ScreenWin.flip()
                    else:
                        self.KeyTerminate = keys
                        wait_for_input = False
                        self.OK = True
                elif keys in self._shiftkeys:
                    shift_flag = True
                elif keys in self.KeyErase:
                    self._TextInput = self._TextInput[:len(self._TextInput)-1]
                    self._InputInfoText.draw()
                    self._InputText.setText( self._TextInput )
                    self._InputText.draw()
                    self._ScreenWin.flip()
                else:
                    buffchar = keys[0]
                    if buffchar in self._InputKeyList:
                        if shift_flag or self._onlyUpper:
                            buffchar = buffchar.upper()
                            shift_flag = False
                        self._TextInput += buffchar
                        self._InputInfoText.draw()
                        self._InputText.setText(self._TextInput)
                        self._InputText.draw()
                        self._ScreenWin.flip()
        return self._TextInput


def get_proband_id(parameters, exp_win):
    """
    Gets proband id from provided parameters using visual input
    :param parameters: parameters for visual screen initialization
    :param exp_win: visual.Window
    :return: entered subject id (proband id)
    """
    get_input_text = InputScreenHandler(
        exp_win,
        units=parameters['TextUnit'],
        height=parameters['InstructHeight'],
        input_info_pos=(0, 0.1),
        color=parameters['TextColor'],
        font=parameters['TextFont'],
        bold=parameters['TextBold'],
        key_in=['lower', 'upper', 'number'],
        in_minimum=1,
        in_maximum=parameters['NoCharInput'],
        input_info_str='ID-Nummer eingeben (4 Ziffer) end press ENTER:'
    )
    return get_input_text.get_input()
