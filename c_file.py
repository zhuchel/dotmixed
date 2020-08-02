#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""File related functionality. Currently supported: single report and general analysis report"""

from __future__ import absolute_import, division, print_function

import os

import platform
import sys
import time

from psychopy import __version__

pathname = os.path.dirname(sys.argv[0])
RunPath = os.path.abspath(pathname)


def init_file(version, author, subject_id, data_path, device, prefix, staff):
    """
    Creates and initializes single report file.
    :param version: application version
    :param author: experiment author
    :param subject_id: proband id
    :param data_path: data directory name, relative to current execution path
    :param device: current device
    :param prefix: report file prefix
    :param staff: header staff description
    """

    # create directory if it doesn't exist
    if not os.path.exists(get_file(data_path, '')):
        os.makedirs(get_file(data_path, ''))

    date_str = time.strftime("%Y%m%d_%H%M", time.localtime())  # add the current time
    file_name = prefix + '_' + subject_id + '_' + date_str + '_' + platform.node()
    file = open(os.path.join(RunPath, data_path, file_name + '.txt'), 'w')
    file.write('File: %s\n' % file_name)
    file.write('SourceCode: %s, %s, %s\n' % (__file__, version, author))
    file.write('Host: %s, OS: %s, Python: %s, PsychoPy: %s\n' % (platform.node(), platform.platform(terse=0),
                                                                 platform.python_version(), __version__))
    file.write('Response device:\t' + device + '\n')
    file.write('Staff:\t\t\t' + staff + '\n')
    return file


def write_step_header(step, data_file, tested_field_name):
    """
    Writes header for certain step execution report
    :param step: step number
    :param data_file: data file to write into
    :param tested_field_name: filed name varying between experiments, e.g. 'pos' for dotmixed
    """
    if step != 0:
        data_file.write("\n\n\t\t\tStep " + str(step) + "\n")
    data_file.write("\ntrial\t" + tested_field_name + "\tcolor\tansw\teval\tRT(ms)\t\tRT-right-cum(ms)")


def write_congruent_analysis(file, congruent, subject_id, formatting_tab):
    """
    Writes congruent analysis report row
    :param file: file to write the row into
    :param congruent: c_result.Result class filled with congruent test results
    :param subject_id: proband id
    :param formatting_tab: formatting tabs for single file result analysis formatting (e.g. additional '\t')
    This parameter is empty for general report
    """
    file.write("\n" + subject_id + "\t" + str(congruent.x_r) + "\t{:.0f}".format(congruent.x_r_quote))
    file.write(formatting_tab + "\t{:.0f}".format(congruent.x_r_rt_mean))
    file.write(formatting_tab + "\t{:.0f}".format(congruent.xr_rt_median))
    file.write(formatting_tab + "\t" + str(congruent.x_w) + "\t" + str(congruent.x_err))


def write_result_analysis(file, result_class, formatting_tab):
    """
    Writes analysis report row for non-congruent and general reports
    :param file: file to write the row into
    :param result_class: c_result.Result class filled with congruent or general test results
    :param formatting_tab: formatting tabs for single file result analysis formatting (e.g. additional '\t').
    This parameter empty for general report
    """
    file.write("\t" + str(result_class.x_r) + "\t{:.0f}".format(result_class.x_r_quote))
    file.write(formatting_tab + "\t{:.0f}".format(result_class.x_r_rt_mean))
    file.write(formatting_tab + "\t{:.0f}".format(result_class.xr_rt_median))
    file.write(formatting_tab + "\t" + str(result_class.x_w) + "\t" + str(result_class.x_err))


def write_analysis_header(file, prefix):
    """
    Writes analysis report header
    :param file: file to write the header into
    :param prefix: New lines prefix for single report. Prefix is empty for general reports
    """
    file.write(prefix + "prob_id\tc_r\tc_r_quote\tc_r_rt_mean\tc_r_rt_median\tc_w\tc_err")
    file.write("\tic_r\tic_r_quote\tic_r_rt_mean\tic_r_rt_median\tic_w\tic_err")
    file.write("\tm_r\tm_r_quote\tm_r_rt_mean\tm_r_rt_median\tm_w\tm_err")


def write_analysis_header_mixed(file, prefix):
    """
    Writes analysis report header for mixed experiments only
    :param file: file to write the header into
    :param prefix: New lines prefix for single report. Prefix is empty for general reports
    """
    file.write(prefix + "prob_id")
    file.write("\tm_r\tm_r_quote\tm_r_rt_mean\tm_r_rt_median\tm_w\tm_err")


def write_footer(data_file, correct_count, no_repetitions):
    """
    Writes footer for single report step
    :param data_file: file to write the footer into
    :param correct_count: number of correct answers for the step
    :param no_repetitions: number of stimuli in step
    """
    data_file.write("\n\n right answers: " + str(correct_count))
    data_file.write("\n wrong answers/no answer: " + str(no_repetitions - correct_count))


def get_file(data_path, report_fie_name):
    """
    Gets file by provided context
    :param data_path: data directory name, relative to current execution path
    :param report_fie_name: report file name
    :return: file by provided context
    """
    return os.path.join(RunPath, data_path, report_fie_name)


def write_analysis(data_file, congruent, incongruent, mixed, data_path, proband_id, report_fie_name):
    """
    Writes single report and general analysis report rows
    :param data_file: single report file to write row into
    :param congruent: c_result.Result class filled with congruent test results
    :param incongruent: c_result.Result class filled with non-congruent test results
    :param mixed: c_result.Result class filled with mixed test results
    :param data_path: data directory name, relative to current execution path
    :param proband_id: proband id
    :param report_fie_name: file name of the general analysis report
    """
    write_analysis_header_mixed(data_file, "\n\n")
    if not os.path.isfile(get_file(data_path, report_fie_name)):
        # create the general analysis report, if it doesn't exist
        data_file_all = open(get_file(data_path, report_fie_name), 'w')
        write_analysis_header_mixed(data_file_all, "")
    else:
        # open the general analysis report for appending, if it exists
        data_file_all = open(get_file(data_path, report_fie_name), 'a+')
    if congruent is not None:
        write_congruent_analysis(data_file, congruent, proband_id, '\t')
        write_congruent_analysis(data_file_all, congruent, proband_id, '')
    if incongruent is not None:
        write_result_analysis(data_file, incongruent, '\t')
        write_result_analysis(data_file_all, incongruent, '')
    if congruent is None and incongruent is None:
        data_file.write("\n" + proband_id)
    write_result_analysis(data_file, mixed, '\t')
    if congruent is None and incongruent is None:
        data_file_all.write("\n" + proband_id)
    write_result_analysis(data_file_all, mixed, '')
    data_file_all.close()


def write_stimuli_row(data_file, count, pos, color, answer, correctness, diff_time, cumulative_time):
    """
   Writes single step report row
   :param data_file: single report file to write row into
   :param count: current stimuli index, beginning with 0
   :param pos: element position
   :param color: currently 'red' or 'blue'
   :param answer: proband answer. ('L' or 'R')
   :param correctness: correctness of the answer. '0' for 'False' and '1' for 'True'
   :param diff_time: reaction time
   :param cumulative_time: cumulative time of correct answers for current step
   """
    data_file.write("\n" + str(count+1) + "\t" + pos + "\t" + color + "\t" +
                    answer + "\t" + correctness + "\t{:.0f}".format(diff_time * 1000) +
                    "\t\t{:.0f}".format(cumulative_time * 1000))
