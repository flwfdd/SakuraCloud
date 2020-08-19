import os
import json
from flask_cors import CORS
from flask import Flask,request

app=Flask(__name__)

#root=r"C:/Users/范滇东/OneDrive - vlity.ac.id/桌面/新建文件夹/"
root="/home/flwfdd/program/SakuraCloud/data/"

def get_list(args):
    # 基本参数处理
    if 'path' not in args: args['path']='.'
    if 'lim' not in args: args['lim']=20
    if 'off' not in args: args['off']=0
    if 'sort' not in args: args['sort']='dir_name_up'
    if 'search' not in args: args['search']=''
    path=os.path.join(root,args['path'])
    lim=int(args['lim'])
    off=int(args['off'])*lim #需要提前去掉的数量
    order=args['sort'].split('_')
    search=args['search']
    # 爬
    dic={}
    if os.path.exists(path)==False: return dic
    #如果是文件
    if os.path.isfile(path)==True:
        dic['type']='file'
        dic['path']=os.path.relpath(path,root).replace('\\','/')
        d={}
        d['type']='file'
        d['path']=os.path.relpath(path,root).replace('\\','/')
        d['name']=os.path.basename(path)
        d['size']=os.path.getsize(path)
        d['time']=int(os.path.getmtime(path))
        dic['data']=[d]
        return dic
    for rt,dirs,files in os.walk(path,topdown=False): pass
    
    dic['dir_num']=0
    dic['file_num']=0
    oril=[{'name':i,'type':'dir'} for i in dirs]+[{'name':i,'type':'file'} for i in files]
    l=[]
    for i in oril:
        if search in i['name']:
            l.append(i)
            dic[i['type']+'_num']+=1
    for i in l:
        i['size']=os.path.getsize(os.path.join(rt,i['name']))
        i['time']=int(os.path.getmtime(os.path.join(rt,i['name'])))
        i['path']=os.path.relpath(os.path.join(rt,i['name']),root).replace('\\','/')
    # 排序及裁剪
    l.sort(key=lambda x: x[order[1]],reverse=(order[2]=='down'))
    l.sort(key=lambda x: x['type']!=order[0])
    l=l[min(len(l),off):]
    l=l[:min(len(l),lim)]

    rt=os.path.relpath(rt,root)
    rt.replace('\\','/')
    dic['path']=rt
    dic['data']=l
    dic['type']='list'
    return dic

@app.route('/')
def api():
    args=request.args
    if 'cmd' in args:
        if args['cmd']=='list': #获取文件列表
            return get_list(dict(args))

@app.route('/music_search/') #MergeMusic搜索
def music_search():
    args=dict(request.args)
    with open("music.json",'r') as f: dic=json.loads(f.read())
    album=dic['album']
    music=dic['music']
    l=[]
    keyword=args['keyword']
    limit=int(args['limit'])
    offset=int(args['offset'])*limit
    if args['type']=='list':
        for i in album:
            i.pop('list')
            if keyword in i['name']: l.append(i)
    else:
        for i in music:
            if keyword in i['name']+i['album']['name']: l.append(i)
    l=l[min(len(l),offset):]
    l=l[:min(len(l),limit)]
    return json.dumps(l)

@app.route('/music_get/') #MergeMusic搜索
def music_get():
    args=dict(request.args)
    with open("music.json",'r') as f: dic=json.loads(f.read())
    album=dic['album']
    music=dic['music']
    mid=args['mid']
    if args['type']=='list':
        for i in album:
            if i['mid']==mid:
                l=i['list']
    else:
        for i in music:
            if i['mid']==mid:
                l=i
    return json.dumps(l)

CORS(app)
app.run(port=1111)
