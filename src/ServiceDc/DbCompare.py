# -*- coding: utf-8 -*-
# Copyright (c) 2013 zyskm <zyskm@163.com>
#
"""
dbcompare structure compare
"""
import pdbc.metadata as meta
import time
import logging  
import sys


#结构不一致时用红色标注
errorTagStart="<font color=\"#FF0000\">"
errorTagEnd="</font>"
#多出来的部分
moreTagStart="<font color=\"#33CC00\">"
moreTagEnd="</font>"
def getHeadHtml():
    sb = "<head>"
    sb+="<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
    sb+="<title>dbcompare</title>"
    sb+="<style type=\"text/css\">"
    sb+="body{"
    sb+="text-align:center; "
    sb+="}"
    sb+="table{"
    sb+="    border-collapse:collapse;"
    sb+="    font-size:14px;"
    sb+="    margin-bottom:10px;"
    sb+="    overflow:hidden;"
    sb+="}"
    sb+=".tableColumn {"
    sb+="    margin-left:10px"
    sb+="}"
    sb+="}"
    sb+="/*浅蓝色的表格*/"
    sb+=".blue_tr{font-size:12px;background-color:#D9E8FE}"
    sb+="/* 表格第一行的表头样式*/"
    sb+=".navtittle {"
    sb+="    font-size: 12px;"
    sb+="    font-weight: bold;"
    sb+="    color: #FFFFFF;"
    sb+="    line-height:22px;"
    sb+="    background-color: #7EAAEB;"
    sb+="    padding-left:15px;"
    sb+="    }"
    sb+="</style>"
    sb+="<script>"
    sb+="function trun(divname){"
    sb+="if(document.getElementById(divname+'_left').style.display=='none'){"
    sb+="    document.getElementById(divname+'_left').style.display='block';"
    sb+="    document.getElementById(divname+'_right').style.display='block';"
    sb+="}else{"
    sb+="    document.getElementById(divname+'_left').style.display='none';"
    sb+="    document.getElementById(divname+'_right').style.display='none';"
    sb+="}"
    sb+="}"
    sb+="</script>"
    sb+="</head>"
    sb+="<body>"
    sb+="<div  align='center'>"
    sb+="<table border=\"1\">"
    sb+="<thead>"
    sb+="<tr class=\"navtittle\">"
    sb+="<th Colspan=\"3\">DbCompare &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;comparetime:"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"</th>"
    sb+="</tr>"
    sb+="<tr class=\"blue_tr\">"
    return sb
def getMiddletHtml():
    sb = "</tr>"
    sb+="  </thead>"
    sb+="  <tbody>"
    return sb

def getFootHtml():
    sb = "  </div>"
    sb = "  </tbody>"
    sb+="  </table>"
    sb+="  </body>"
    sb+="  </html>"
    return sb
def columnCompare(left,right):
    lefthtml=""
    rightHtml=""
    conflict="false"
    compare = [lefthtml,rightHtml,conflict]
    leftSb = ""
    rightSb = ""
    #1.比较是否自增长字段
    if cmp(left.isAutoIncrementStr(),right.isAutoIncrementStr())==0:
        leftSb+="<td>"+left.isAutoIncrementStr()+"</td>"
        rightSb+="<td>"+right.isAutoIncrementStr()+"</td>"
    else:
        conflict="true";
        leftSb+="<td>"+errorTagStart+left.isAutoIncrementStr()+errorTagEnd+"</td>"
        rightSb+="<td>"+errorTagStart+right.isAutoIncrementStr()+errorTagEnd+"</td>"

    #2.比较数据类型
    if cmp(left.getDataType(),right.getDataType())==0:
        leftSb+="<td>"+left.getDataType()+"</td>"
        rightSb+="<td>"+right.getDataType()+"</td>"
    else:
        conflict="true";
        leftSb+="<td>"+errorTagStart+left.isAutoIncrementStr()+errorTagEnd+"</td>"
        rightSb+="<td>"+errorTagStart+right.isAutoIncrementStr()+errorTagEnd+"</td>"
    #3.比较数据长度
    if cmp(left.getLengthStr(),right.getLengthStr())==0:
        leftSb+="<td>"+left.getLengthStr()+"</td>"
        rightSb+="<td>"+right.getLengthStr()+"</td>"
    else:
        conflict="true";
        leftSb+="<td>"+errorTagStart+left.getLengthStr()+errorTagEnd+"</td>"
        rightSb+="<td>"+errorTagStart+right.getLengthStr()+errorTagEnd+"</td>"
    #4.比较是否可以为空
    if cmp(left.isNullable(),right.isNullable())==0:
        leftSb+="<td>"+left.isNullable()+"</td>"
        rightSb+="<td>"+right.isNullable()+"</td>"
    else:
        conflict="true";
        leftSb+="<td>"+errorTagStart+left.isNullable()+errorTagEnd+"</td>"
        rightSb+="<td>"+errorTagStart+right.isNullable()+errorTagEnd+"</td>"
    lefthtml = leftSb
    compare[0] = lefthtml
    rightHtml = rightSb
    compare[1] = rightHtml
    compare[2] =conflict
    return compare;
def getTableHeadHtml(divname):
    sb ="<div id=\""+divname+"\" style=\"display:none;\">"
    sb+="<table class=\"tableColumn\">"
    sb+="<tr class=\"blue_tr\">"
    sb+="<td>code</td><td>primary</td><td>&nbsp;DateType&nbsp;</td><td>&nbsp;length&nbsp;</td><td>nullable</td>"
    sb+="<tr>"
    return sb
def getTableFootHtml():
    sb = "  </table>"
    sb+="</div>"
    return sb
#表结构比对
def tableCompare(leftTable,rightTable):
    lefthtml=""
    rightHtml=""
    conflict="false"
    compare = [lefthtml,rightHtml,conflict]
    leftList=leftTable.getColumnList()
    rightList=rightTable.getColumnList()
    leftSb = ""
    rightSb = ""
    if leftTable==None or rightTable==None: return compare;
    #1.表头设置
    leftSb+=getTableHeadHtml(leftTable.getName()+"_left")
    rightSb+=getTableHeadHtml(rightTable.getName()+"_right")
    #2.比对两个表列是否一致
    if(leftList==None or len(leftList)==0 or rightList==None or len(rightList)==0):
        return compare;
    
    
    leftindex=0;
    rightindex=0;
    for left in leftList:
        leftindex+=1
        if rightindex<len(rightList):
            right = rightList[rightindex]
            #left==right 
            if cmp(left.getName(),right.getName())==0:
                comArr = columnCompare(left,right)
                leftCompareStr=comArr[0];
                rightCompareStr=comArr[1];
                columnConflict=comArr[2];
                if cmp("true",columnConflict)==0:
                    #字段属性不一致
                    conflict = "true"
                rightindex+=1
                leftSb+="\n"
                leftSb+="<tr>"
                leftSb+="<td>"+left.getName()+"</td>"
                leftSb+=leftCompareStr
                leftSb+="</tr>"
                
                rightSb+="\n"
                rightSb+="<tr>"
                rightSb+="<td>"+right.getName()+"</td>"
                rightSb+=rightCompareStr
                rightSb+="</tr>"
            #left>right 
            if cmp(left.getName(),right.getName())>0:
                conflict="true"
                rightindex+=1
                leftSb+="\n"
                leftSb+="<tr>"
                leftSb+="<td>&nbsp;</td>"
                leftSb+="</tr>"
                
                rightSb+="\n"
                rightSb+="<tr>"
                rightSb+="<td>"+moreTagStart+right.getName()+"</font></td>"
                rightSb+="</tr>"
            #left<right
            if cmp(left.getName(),right.getName())<0:
                conflict="true";
                leftSb+="\n"
                leftSb+="<tr>"
                leftSb+="<td>"+moreTagStart+left.getName()+moreTagEnd+"</td>"
                leftSb+="</tr>"
                
                rightSb+="\n"
                rightSb+="<tr>"
                rightSb+="<td>&nbsp;</td>"
                rightSb+="</tr>"
        else:
            conflict="true";
            leftSb+="\n"
            leftSb+="<tr>"
            leftSb+="<td>"+moreTagStart+left.getName()+moreTagEnd+"</td>"
            leftSb+="</tr>"
            
            rightSb+="\n"
            rightSb+="<tr>"
            rightSb+="<td>&nbsp;</td>"
            rightSb+="</tr>"
    if len(rightList)>leftindex:
        for right in range(leftindex,len(rightList)):
            conflict="true"
            leftSb+="\n"
            leftSb+="<tr>"
            leftSb+="<td>&nbsp;</td>"
            leftSb+="</tr>"
            
            rightSb+="\n"
            rightSb+="<tr>"
            rightSb+="<td ><font color=\"#33CC00\">"+right.getName()+moreTagEnd+"</td>"
            rightSb+="</tr>"
    leftSb+=getTableFootHtml()
    lefthtml = leftSb
    rightSb+=getTableFootHtml()
    rightHtml = rightSb
    compare[0] = lefthtml;
    compare[1] = rightHtml;
    compare[2] =conflict;
    return compare;

def compare(left,right):
    '''compare two database structure left-->right'''
    #1.构造html框架
    sb = getHeadHtml()
    sb+="<th width=\"45%\">"+left.getHost()+"@"+left.getDbname()+"</th>"+'\n'
    sb+="<th width=\"10%\">&nbsp;</th>"+'\n'
    sb+="<th width=\"45%\">"+right.getHost()+"@"+right.getDbname()+"</th>"+'\n'
    sb+=getMiddletHtml()
    #2.比较表结构
    leftTableList = left.getTableList()
    rightTableList = right.getTableList()
    rightindex=0
    leftindex=0
    #for leftTable in leftTableList:
    while leftindex<len(leftTableList):
        leftTable = leftTableList[leftindex]
        if(rightindex<len(rightTableList)):
            rightTable = rightTableList[rightindex]
            #left==right 
            if cmp(leftTable.getName(),rightTable.getName())==0:
                comArr = tableCompare(leftTable,rightTable)
                leftCompareStr=comArr[0];
                rightCompareStr=comArr[1];
                conflict=comArr[2];
                #left & right go next
                rightindex+=1
                leftindex+=1
                sb+="<tr>"
                if cmp(leftCompareStr,"")!=0 and leftCompareStr!=None:
                    if cmp("true",conflict)==0:
                        sb+="<td ><span style=\"cursor:hand\" onclick=\"javascript:trun('"+leftTable.getName()+"')\">"+errorTagStart+leftTable.getName()+errorTagEnd+"</span>"+leftCompareStr+"</td>"+'\n'
                        sb+="<td>&nbsp;</td>"+'\n'
                    else:
                        sb+="<td ><span style=\"cursor:hand\" onclick=\"javascript:trun('"+leftTable.getName()+"')\">"+leftTable.getName()+"</span>"+leftCompareStr+"</td>"+'\n'
                        sb+="<td>=</td>"+'\n'
                else:
                    sb+="<td >"+leftTable.getName()+"</td>"+'\n'
                    sb+="<td>=</td>"+'\n'
                if cmp(rightCompareStr,"")!=0 and rightCompareStr!=None:
                    if cmp("true",conflict)==0:
                        sb+="<td ><span style=\"cursor:hand\" onclick=\"javascript:trun('"+rightTable.getName()+"')\">"+errorTagStart+rightTable.getName()+errorTagEnd+"</span>"+rightCompareStr+"</td>"+'\n'
                    else:
                        sb+="<td ><span style=\"cursor:hand\" onclick=\"javascript:trun('"+rightTable.getName()+"')\">"+rightTable.getName()+"</span>"+rightCompareStr+"</td>"+'\n'
                else:
                    sb+="<td >"+rightTable.getName()+"</td>"+'\n'
                sb+="</tr>"+'\n'
            #left>right 
            if cmp(leftTable.getName(),rightTable.getName())>0:
                rightindex+=1
                conflict="true";
                sb+="<tr  >"
                sb+="<td>&nbsp;</td>"
                sb+="<td>&nbsp;</td>"
                sb+="<td>"+moreTagStart+rightTable.getName()+moreTagEnd+"</td>"
                sb+="</tr>"+'\n'
            #left<right
            if cmp(leftTable.getName(),leftTable.getName())<0:
                leftindex+=1
                conflict="true";
                sb+="<tr  >"
                sb+="<td>"+moreTagStart+leftTable.getName()+moreTagEnd+"</td>"
                sb+="<td>&nbsp;</td>"
                sb+="<td>&nbsp;</td>"
                sb+="</tr>"+'\n'
        else:
            leftindex+=1
            conflict="true";
            sb+="<tr  >"
            sb+="<td>"+moreTagStart+leftTable.getName()+moreTagEnd+"</td>"
            sb+="<td>&nbsp;</td>"
            sb+="<td>&nbsp;</td>"
            sb+="</tr>"+'\n'
    sb+=getFootHtml()
    return sb

if __name__ == '__main__':
    #driver = dr.DriverManager(dbtype='mysql',dbname='avatar',host="127.0.0.1",port=3306,user="root",passwd="root",charset="utf8")  
    #left = driver.getDatabaseMeta()
    #right =left
    #print compare(left,right)
    print 'dbcompare....'
