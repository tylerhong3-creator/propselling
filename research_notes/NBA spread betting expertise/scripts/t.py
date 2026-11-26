import json,sys,collections
d=json.load(open(sys.argv[1]));G=[]
for r in d:
    try: sp=float(r['home_close_spread']);m=float(r['home_final'])-float(r['away_final']);t=float(r['close_over_under'])
    except: continue
    if abs(sp)<=25 and 150<=t<=280 and sp!=0: G.append((sp,m,t))
def leg(side,lo,hi,T):
    W=L=0
    for sp,m,t in G:
        fl=-abs(sp); fm = m if sp<0 else -m
        if not(lo<=abs(sp)<=hi): continue
        r = fm+fl+T if side=='fav' else -fm-fl+T
        if r>0:W+=1
        elif r<0:L+=1
    return W/(W+L),W+L
for T in [6]:
  for side,lo,hi in [('fav',1,3),('fav',3.5,6),('fav',6.5,9),('fav',9.5,25),('dog',1,3),('dog',3.5,6),('dog',6.5,9),('dog',9.5,25)]:
    p,n=leg(side,lo,hi,T);print(T,side,lo,hi,'n=%d win %.3f'%(n,p))
# overtime share: games where margin small; check quarter scores sum vs final for OT
ot=0;n=0
for r in d:
    try:
        q=sum(float(r['home_%sQtr'%k])-float(r['away_%sQtr'%k]) for k in ['1st','2nd','3rd','4th'])
        n+=1; ot+= (q==0)
    except: pass
print('OT share (tied after 4Q) %.3f n=%d'%(ot/n,n))
