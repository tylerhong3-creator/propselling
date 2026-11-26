import json,sys,math,collections
import statistics as st
from math import erf,sqrt
Phi=lambda x:0.5*(1+erf(x/sqrt(2)))
d=json.load(open(sys.argv[1]))
g=[]
bad=0
for r in d:
    try:
        hs,as_=float(r['home_final']),float(r['away_final'])
        sp=float(r['home_close_spread']); tot=float(r['close_over_under'])
        osp=float(r['home_open_spread']); otot=float(r['open_over_under'])
    except: bad+=1; continue
    if not(abs(sp)<=25 and 150<=tot<=280 and abs(osp)<=25 and 150<=otot<=280): bad+=1; continue
    hml,aml=r.get('home_close_ml'),r.get('away_close_ml')
    g.append(dict(s=r['season'],m=hs-as_,sp=sp,osp=osp,tot=tot,otot=otot,pts=hs+as_,hml=hml,aml=aml))
print('games',len(g),'dropped',bad, 'seasons',sorted(set(x['s'] for x in g)))
M=[x['m'] for x in g]
print('home margin mean %.2f sd %.2f'%(st.mean(M),st.pstdev(M)))
print('mean home close spread %.2f'%st.mean([x['sp'] for x in g]))
res=[x['m']+x['sp'] for x in g]  # >0 home covers
print('residual (margin - expected) mean %.2f sd %.2f'%(st.mean(res),st.pstdev(res)))
# normality: kurtosis, quantiles
mu=st.mean(res);sd=st.pstdev(res)
k=sum((r-mu)**4 for r in res)/len(res)/sd**4
print('excess kurtosis %.2f'%(k-3))
for q in [1,2]:
    print('frac |res|<= %d sd: %.3f (normal %.3f)'%(q,sum(abs(r-mu)<=q*sd for r in res)/len(res),2*Phi(q)-1))
# absolute margin frequency
am=collections.Counter(abs(int(x)) for x in M)
n=len(M)
print('Abs final margin freq (top 15):')
for v,c in sorted(am.items(),key=lambda t:-t[1])[:15]: print(v,c,'%.2f%%'%(100*c/n))
print('margins 1..15:',' '.join('%d:%.2f'%(v,100*am[v]/n) for v in range(1,16)))
# favorite margin frequency (signed from favorite perspective)
fm=collections.Counter()
nf=0
for x in g:
    if x['sp']==0: continue
    nf+=1
    f = x['m'] if x['sp']<0 else -x['m']
    fm[int(f)]+=1
print('fav-perspective margin 1..12 (fav wins by k):',' '.join('%d:%.2f'%(v,100*fm[v]/nf) for v in range(1,13)))
# push rates for integer spreads
print('Push rate by integer closing |spread|:')
bys=collections.defaultdict(list)
for x in g:
    bys[abs(x['sp'])].append(x)
for s in [1,2,3,4,5,6,7,8,9,10,11,12]:
    L=bys.get(float(s),[])
    if L:
        p=sum(1 for x in L if x['m']+x['sp']==0)/len(L)
        print(' %d: n=%d push=%.2f%%'%(s,len(L),100*p))
# overall prob residual==0 for integer spreads, and prob that final margin (fav persp) == k when spread in [k-1.5,k+1.5]
ints=[x for x in g if x['sp']==int(x['sp'])]
print('all integer spreads n=%d push %.2f%%'%(len(ints),100*sum(x['m']+x['sp']==0 for x in ints)/len(ints)))
# fit sigma: P(home cover) not needed; fit P(home win) vs spread via sd
# Empirical home win% by closing spread buckets and normal model
print('Home SU win% by closing home spread:')
for lo in [-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10]:
    L=[x for x in g if lo<=x['sp']<lo+2 and x['m']!=0]
    if len(L)<50: continue
    w=sum(x['m']>0 for x in L)/len(L); ms=st.mean([x['sp'] for x in L])
    print(' spread [%d,%d) n=%d mean %.2f win %.3f normal(sd=%.1f) %.3f'%(lo,lo+2,len(L),ms,w,sd,Phi(-ms/sd)))
# moneyline vs spread mapping
def imp(o): return 100/(o+100) if o>0 else -o/(-o+100)
print('No-vig home ML prob by closing spread (median):')
for s in [-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14]:
    L=[x for x in g if x['sp'] in (s,s+0.5) and isinstance(x['hml'],(int,float)) and isinstance(x['aml'],(int,float)) and abs(x['hml'])>=100 and abs(x['aml'])>=100]
    if len(L)<30: continue
    ps=[imp(x['hml'])/(imp(x['hml'])+imp(x['aml'])) for x in L]
    hold=[imp(x['hml'])+imp(x['aml'])-1 for x in L]
    emp=sum(x['m']>0 for x in L)/len(L)
    print(' %s/%s n=%d novig_p %.3f ML-hold %.3f empirical %.3f normal %.3f'%(s,s+0.5,len(L),st.median(ps),st.median(hold),emp,Phi(-(s+0.25)/sd)))
# SD of residual by total bucket
print('Residual SD by closing total:')
for lo in [180,190,200,210,220,230,240]:
    L=[x['m']+x['sp'] for x in g if lo<=x['tot']<lo+10]
    if len(L)>100: print(' [%d,%d) n=%d sd %.2f'%(lo,lo+10,len(L),st.pstdev(L)))
print('Residual SD by |spread|:')
for lo,hi in [(0,3),(3,6),(6,9),(9,12),(12,26)]:
    L=[x['m']+x['sp'] for x in g if lo<=abs(x['sp'])<hi]
    print(' [%d,%d) n=%d sd %.2f'%(lo,hi,len(L),st.pstdev(L)))
print('Residual SD by season:')
for s in sorted(set(x['s'] for x in g)):
    L=[x['m']+x['sp'] for x in g if x['s']==s]
    print(' ',s,len(L),'%.2f'%st.pstdev(L))
# total residual
tr=[x['pts']-x['tot'] for x in g]
print('Total residual mean %.2f sd %.2f'%(st.mean(tr),st.pstdev(tr)))
# correlation fav cover & over
fc=[];ov=[]
for x in g:
    if x['sp']==0: continue
    fres = (x['m']+x['sp']) if x['sp']<0 else -(x['m']+x['sp'])
    if fres==0 or x['pts']==x['tot']: continue
    fc.append(1 if fres>0 else 0); ov.append(1 if x['pts']>x['tot'] else 0)
def corr(a,b):
    ma,mb=st.mean(a),st.mean(b);return sum((i-ma)*(j-mb) for i,j in zip(a,b))/len(a)/st.pstdev(a)/st.pstdev(b)
print('n=%d fav cover %.3f over %.3f corr(favcover,over) %.3f'%(len(fc),st.mean(fc),st.mean(ov),corr(fc,ov)))
for name,cond in [('all',lambda x:True),('|sp|>=10',lambda x:abs(x['sp'])>=10),('|sp|<=3',lambda x:abs(x['sp'])<=3)]:
    a=[];b=[]
    for x in g:
        if x['sp']==0 or not cond(x):continue
        fres = (x['m']+x['sp']) if x['sp']<0 else -(x['m']+x['sp'])
        if fres==0 or x['pts']==x['tot']: continue
        a.append(fres>0);b.append(x['pts']>x['tot'])
    both=sum(i and j for i,j in zip(a,b))/len(a); un=sum((not i) and (not j) for i,j in zip(a,b))/len(a)
    pa,pb=st.mean(a),st.mean(b)
    print(' %s n=%d P(fav&over)=%.3f indep %.3f ; P(dog&under)=%.3f indep %.3f; corr %.3f'%(name,len(a),both,pa*pb,un,(1-pa)*(1-pb),corr([int(i) for i in a],[int(i) for i in b])))
# continuous correlation of residuals
fr=[];trr=[]
for x in g:
    if x['sp']==0: continue
    fr.append((x['m']+x['sp']) if x['sp']<0 else -(x['m']+x['sp'])); trr.append(x['pts']-x['tot'])
print('corr(fav margin residual, total residual) %.3f'%corr(fr,trr))
# ATS overall
hc=[x for x in g if x['m']+x['sp']!=0]
print('home cover rate %.3f n=%d'%(sum(x['m']+x['sp']>0 for x in hc)/len(hc),len(hc)))
fcv=[ (x['m']+x['sp']>0) if x['sp']<0 else (x['m']+x['sp']<0) for x in hc if x['sp']!=0]
print('fav cover rate %.3f'%st.mean(fcv))
# opening -> closing CLV test: bet side line moved toward at opening number
w=l=p=0
for x in g:
    mv=x['sp']-x['osp']
    if mv==0: continue
    # if mv<0 home became bigger fav => bet home at open spread osp
    r = (x['m']+x['osp']) if mv<0 else -(x['m']+x['osp'])
    if r>0:w+=1
    elif r<0:l+=1
    else:p+=1
print('Bet opening line in direction of move: W %d L %d P %d win%% %.3f'%(w,l,p,w/(w+l)))
for thr in [0.5,1,1.5,2,3]:
    w=l=0
    for x in g:
        mv=x['sp']-x['osp']
        if abs(mv)<thr: continue
        r = (x['m']+x['osp']) if mv<0 else -(x['m']+x['osp'])
        if r>0:w+=1
        elif r<0:l+=1
    print(' |move|>=%.1f n=%d win %.3f'%(thr,w+l,w/(w+l)))
# same with closing line (should be ~50%)
w=l=0
for x in g:
    mv=x['sp']-x['osp']
    if mv==0: continue
    r = (x['m']+x['sp']) if mv<0 else -(x['m']+x['sp'])
    if r>0:w+=1
    elif r<0:l+=1
print('Same side at CLOSING number: win %.3f n=%d'%(w/(w+l),w+l))
# teasers: 6-point teaser leg win rate (ties = push removed? count push as loss-out)
for t in [4,6,7]:
    W=L=P=0
    for x in g:
        if x['sp']==0: continue
        fav_home=x['sp']<0
        for side in ['fav','dog']:
            line = x['sp'] if fav_home else -x['sp']   # fav line negative
            m = x['m'] if fav_home else -x['m']        # fav margin
            if side=='fav': r = m + line + t
            else: r = -m - line + t
            if r>0:W+=1
            elif r<0:L+=1
            else:P+=1
    print('%d-pt teaser leg: win %.4f (excl push) n=%d'%(t,W/(W+L),W+L+P))
# half point values: prob residual exactly 0 from fav perspective at various spreads & P(fav margin==k)
print('P(fav final margin == k) for games with |spread| in [k-2,k+2]:')
for k in range(1,13):
    L=[x for x in g if x['sp']!=0 and k-2<=abs(x['sp'])<=k+2]
    c=sum(1 for x in L if (x['m'] if x['sp']<0 else -x['m'])==k)
    print(' k=%d n=%d %.2f%%'%(k,len(L),100*c/len(L)))
