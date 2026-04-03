# -*- coding: utf-8 -*-

"""
Excel文件操作
"""

import os
import sys
import xlrd
import xlwt
from xlutils.copy import copy

sys.path.append(os.getcwd())
from public.log import LOG, logger


file_path = os.path.join(os.getcwd(), 'casefile/case.xls')


@logger('解析测试用例文件')
def datacel(case_select):
    """
    读取测试用例
    """
    try:
        case_info = xlrd.open_workbook(file_path)
        sheet_list = case_info.sheets()
        for sheet in sheet_list:
            if sheet.name == 'web'  and case_select in sheet.name:
                nrows = sheet.nrows
                caseid = []
                caseparms = []
                caseurl = []
                casemethod = []
                caseexpect = []
                casename = []
                for i in range(1, nrows):
                    caseid.append(sheet.cell(i, 0).value)
                    caseparms.append(sheet.cell(i, 2).value)
                    caseurl.append(sheet.cell(i, 3).value)
                    casename.append(sheet.cell(i, 1).value)
                    casemethod.append((sheet.cell(i, 4).value))
                    caseexpect.append((sheet.cell(i, 5).value))
                return caseid, caseparms, caseurl, casemethod, caseexpect, casename
            elif sheet.name == 'system' and case_select in sheet.name:
                nrows = sheet.nrows
                caseid = []
                caseparms = []
                caseexpect = []
                casename = []
                for i in range(1, nrows):
                    caseid.append(sheet.cell(i, 0).value)
                    caseparms.append(sheet.cell(i, 2).value)
                    casename.append(sheet.cell(i, 1).value)
                    caseexpect.append((sheet.cell(i, 3).value))
                return caseid, caseparms, caseexpect, casename
    except Exception as e:
        LOG.info('打开测试用例失败，原因是:%s' % e)
        return


def style(result):
    """
    用例测试结果单元样式
    """
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    if result == 'passed':
        pattern.pattern_fore_colour = 50
    elif result == 'failed':
        pattern.pattern_fore_colour = 2
    style = xlwt.XFStyle()
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style.pattern = pattern
    style.alignment = alignment
    fnt = xlwt.Font()
    fnt.name = u'微软雅黑'
    fnt.bold = True
    fnt.colour_index  = 1
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style.borders = borders
    style.font = fnt


    return style


@logger('回写测试结果到测试用例')
def writeCaseResult(case_select, casename, result):
    """
    回写测试结果到测试用例
    """
    try:
        rexcel = xlrd.open_workbook(file_path, formatting_info=True)
        rcell_list = rexcel.sheets()
        wexcel = copy(rexcel)
        for rcell in rcell_list:
            if rcell.name == 'web' and case_select in rcell.name:
                nrows = rcell.nrows
                table = wexcel.get_sheet(0)
                for i in range(1, nrows):
                    if casename == rcell.cell(i, 1).value:
                        table.write(i, 6, result, style=style(result))
            elif rcell.name == 'system' and case_select in rcell.name:
                nrows = rcell.nrows
                table = wexcel.get_sheet(1)
                for i in range(1, nrows):
                    if casename == rcell.cell(i, 1).value:
                        table.write(i, 4, result, style=style(result))
        wexcel.save(file_path)
    except Exception as e:
        LOG.info('打开测试用例失败，原因是:%s' % e)
        return
    
@logger('统计测试用例的结果信息')
def sum_test_results(case_select):
    data_dict = {'测试模块':'','用例总数':'','通过总数':'','失败总数':''}
    case_info = xlrd.open_workbook(file_path)
    sheet_list = case_info.sheets()
    module_name_list = []
    case_name_list = []
    pass_list = []
    fail_list = []
    for sheet in sheet_list:       
        nrows = sheet.nrows
        casenum = 0
        passnum = 0
        failnum = 0
        if sheet.name == 'web' and case_select == 'web':
            module_name_list.append(sheet.name)
            for row in range(1,nrows):
                casenum += 1
                if sheet.cell(row,6).value.strip() == 'passed':
                    passnum += 1
                elif sheet.cell(row,6).value.strip() == 'failed':
                    failnum += 1
            case_name_list.append(casenum)
            pass_list.append(passnum)
            fail_list.append(failnum)
            data_dict['测试模块'] =  module_name_list  
            data_dict['用例总数'] = case_name_list 
            data_dict['通过总数'] = pass_list
            data_dict['失败总数'] = fail_list
            return data_dict
        elif sheet.name == 'system' and case_select == 'system':
            module_name_list.append(sheet.name)
            for row in range(1,nrows):
                casenum += 1
                if sheet.cell(row,4).value.strip() == 'passed':
                    passnum += 1
                elif sheet.cell(row,4).value.strip() == 'failed':
                    failnum += 1
            case_name_list.append(casenum)
            pass_list.append(passnum)
            fail_list.append(failnum)
            data_dict['测试模块'] =  module_name_list  
            data_dict['用例总数'] = case_name_list 
            data_dict['通过总数'] = pass_list
            data_dict['失败总数'] = fail_list
            return data_dict


@logger('生成数据驱动所用数据')
def makedata(case_select):
    make_data = []
    if case_select == 'web':
        caseid, caseparms, caseurl, casemethod, caseexpect, casename = datacel(case_select)
        for i in range(len(caseid)):
            make_data.append({
                'caseid': int(caseid[i]),
                'url': caseurl[i],
                'parms': caseparms[i],
                'method': casemethod[i],
                'expect': caseexpect[i],
                'casename': casename[i]
            })
        return make_data
    elif case_select == 'system':
        caseid, caseparms, caseexpect, casename = datacel(case_select)
        for i in range(len(caseid)):
            make_data.append({
                'caseid': int(caseid[i]),
                'parms': caseparms[i],
                'expect': caseexpect[i],
                'casename': casename[i]
            })
        return make_data
        
   


if __name__ == "__main__":
    print(makedata('system')[-1])
