import os
import json

root='/home/flwfdd/program/SakuraCloud/data/music'
#root=r"C:/Users/范滇东/OneDrive - vlity.ac.id/桌面/新建文件夹/[160914] 映画「聲の形」オリジナルサウンドトラック a shape of light 320K"
url="http://cloud.flwfdd.xyz/data/music/"

def path2url(path):
    return url+os.path.relpath(path,root).replace('\\','/')

album=[]
songs=[]
mid=0
aid=0
for path,dirs,files in os.walk(root):
    l=[]
    imgurl=""
    nowdir=os.path.split(path)[1]
    files.sort()
    for i in files:
        x=os.path.splitext(i)
        if x[1] in ['.mp3']: l.append({'name':x[0],'src':path2url(os.path.join(path,i))})
        if i=='cover.png' or i=='cover.jpg': imgurl=path2url(os.path.join(path,i))
    if len(l)==0: continue
    for i in l:
        i['mid']="S"+str(mid)
        mid+=1
        i['type']='music'
        i['album']={'name':nowdir}
        i['artist']=[]
        i['img']=imgurl
        i['lrc']='[00:0.00]木有歌词哦'
    songs+=l
    album.append({'name':nowdir,'mid':"S"+str(aid),'type':'list','album':{'name':nowdir},'artist':[],'list':l})
    aid+=1

with open("music.json","w") as f: f.write(json.dumps({'music':songs,'album':album}))    
