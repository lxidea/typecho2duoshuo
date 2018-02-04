#!/usr/bin/env python
#coding=utf-8

import string, json, datetime, time

utc=False

def LineParser(line, useInt=False):
    result=[]
    quote=False
    ss=''
    for s in line:
        if s==',':
            if quote:
                ss+=s
            else:
                if ss.isdigit() and useInt:
                    result.append(int(ss))
                else:
                    result.append(ss)
                ss=''
        elif s==' ':
            if quote:
                ss+=s
        elif s=="'":
            quote=not quote
        else:
            ss+=s
    if len(ss)>0:
        if ss.isdigit() and useInt:
            result.append(int(ss))
        else:
            result.append(ss)
    return result

print '************************************'
print '*Program Typecho sql 2 duoshuo JSON*'
print '************************************'

sql=raw_input('type the sql file name:')
if (len(sql)==0):
    raise Exception('File name is empty')

fsql=open(sql, 'r')
if not fsql:
    raise Exception('File does not exist')

dic=dict()

flag='INSERT INTO `typecho_comments` VALUES ('
flag2='INSERT INTO `typecho_contents` VALUES ('
post_container=[]
thread_container=[]

Fflag=False
for line in fsql:
    if line.startswith(flag):
        post=dict()
        nline=LineParser(line[len(flag):].strip(");\n"))
        post['post_key']=nline[0]
        post['thread_key']=nline[1]
        if utc:
            post['created_at']=time.strftime("%Y-%m-%dT%H:%M:%S+08:00", time.gmtime(int(nline[2])))
        else:
            post['created_at']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(nline[2])))
        post['author_name']=nline[3]
        if int(nline[4])!=0:
            post['author_key']=nline[4]
        if not "NULL" in nline[6]:
            post['author_email']=nline[6]
        if not "NULL" in nline[7]:
            post['author_url']=nline[7]
        post['ip']=nline[8]
        post['agent']=nline[9]
        post['message']=unicode(nline[10],'utf-8')
        if int(nline[13])!=0:
            post['parent_key']=nline[13]
        post_container.append(post)
        #raw_input()
        continue
    elif line.startswith(flag2):
        Fflag=True
        thread=dict()
        nline=LineParser(line[len(flag):].strip(");\n"))
        thread['thread_key']=nline[0]
        thread['title']=nline[1]
        thread['content']=unicode(nline[5],'utf-8')
        thread['author_key']=nline[7]
        if nline[13]=='1':
            thread['comment_status']='open'
        else:
            thread['comment_status']='close'
        thread['url']='http://lxidea.org/archives/'+nline[0]+'.html'
        #thread['excerpt']=thread['content'][:200]
        thread_container.append(thread)
        #raw_input()
        continue
    elif Fflag:
        break

dic['threads']=thread_container
dic['posts']=post_container
dic['version']='0.1'
dic['generator']='python'
fsql.close()

of=raw_input('type the output file:')
fof=open(of,'w')
fof.writelines(json.dumps(dic))
fof.close()
    
