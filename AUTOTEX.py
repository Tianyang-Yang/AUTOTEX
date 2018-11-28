"""
This is a script to automate the cover letter generating.
Tianyang Yang
11/27/2018
"""
import datetime
import subprocess
import os
import io
import re
import shutil

def input():
    """
    read the information of letter type/ company / address / job title
    from input stream, as int / string / string[] / string
    """
    with open('info.txt',"r") as f:
        infos = f.readlines()
        which = int(infos[0])
        name = infos[1].replace('\n','')
        address = [infos[2].replace('\n',''),infos[3].replace('\n','')]
        title = infos[4].replace('\n','')
        return which, name, address, title

def geneText(tex,which,name,address,title):
    """
    write the information into .tex file and build a pdf as the company name
    move the pdf to ./letter_outfile.
        @tex: the tex of .tex file
        @name: The company's name
        @address: company address [ line 1, line 2 ]
        @title: the job title, e.g. Software Engineer Intern positions
    """
    if which == 0:
        os.chdir('../SE_letter')
    elif which == 1:
        os.chdir('../Data_letter')
    with open(tex+'.tex',"r") as f:
        lines = f.readlines()
    datepat = re.compile('[A-Z][a-z]+\s\d*,\s\d\d\d\d')
    firstpat = re.compile('I\sam\swriting\sto')
    lastpat = re.compile('Thank\syou\sfor')
    for i,line in enumerate(lines):
        if re.match(datepat,line):
            dateline, comline, addrline, cityline = i, i+1, i+2, i+3
        if re.match(firstpat,line):
            firstline = i
        if re.match(lastpat,line):
            lastline = i
    now = datetime.datetime.now()
    lines[dateline] = now.strftime("%B")+' '+now.strftime("%d")+', '+now.strftime("%Y")+'\\\\\n'
    lines[comline] = name+'\\\\\n'
    lines[addrline] = address[0]+'\\\\\n'
    lines[cityline] = address[1]+'\\\\\n'
    lines[firstline] = re.sub(
        'interest\sin\s.+\sat\s.+[.]\sI\sam\sa', 
        'interest in '+title+' at '+name+'. I am a', 
        lines[firstline])
    lines[lastline] = re.sub(
        'work\sfor\s.+,\sand\slook\s', 
        'work for '+name+', and look ', 
        lines[lastline])
    with open(tex+'.tex',"w") as f:
        f.writelines(lines)
    # finish modifying the tex file, then compile it.
    subprocess.run(['pdflatex',tex,'--jobname='+name])
    os.rename(tex+'.pdf','letter_outfile/'+name+'.pdf')
    


    



if __name__ == "__main__":
    which, name, address, title = input()
    tex = "Cover_Letter"
    geneText(tex,which,name,address,title)
