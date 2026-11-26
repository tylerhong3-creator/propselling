import json,sys,math,statistics as st
from statistics import NormalDist
N=NormalDist();Phi=N.cdf;inv=N.inv_cdf
def dec(a): return 1+100/abs(a) if a<0 else 1+a/100
def imp(a): return 1/dec(a)
print('== break-even ==')
for a in [-100,-102,-104,-105,-107,-108,-110,-112,-115,-120,-125,-130,+100,+105,+110]:
    print(a,'dec %.4f BE %.4f'%(dec(a),imp(a)))
print('== hold, two-way ==')
for a,b in [(-110,-110),(-105,-105),(-108,-108),(-115,-105),(-102,-102),(-120,+100),(-112,-108)]:
    p1,p2=imp(a),imp(b);B=p1+p2
    hold=1-1/B  # theoretical hold if action balanced proportional to fair (equalized liability)
    print(a,b,'booksum %.4f overround %.2f%% hold %.2f%%'%(B,100*(B-1),100*hold))
print('== devig example -150/+130 ==')
p1,p2=imp(-150),imp(130);B=p1+p2
mult=(p1/B,p2/B)
add=(p1-(B-1)/2,p2-(B-1)/2)
# power: find k s.t. p1^k+p2^k=1
lo,hi=1,2
for _ in range(100):
    k=(lo+hi)/2
    if p1**k+p2**k>1: lo=k
    else: hi=k
powr=(p1**k,p2**k)
# shin
def shin(pis):
    B=sum(pis)
    def probs(z): return [ (math.sqrt(z*z+4*(1-z)*pi*pi/B)-z)/(2*(1-z)) for pi in pis]
    lo,hi=0,0.4
    for _ in range(200):
        z=(lo+hi)/2
        if sum(probs(z))>1: lo=z
        else: hi=z
    return z,probs(z)
z,sh=shin([p1,p2])
print('raw %.4f %.4f booksum %.4f'%(p1,p2,B))
print('multiplicative %.4f %.4f'%mult)
print('additive %.4f %.4f'%add)
print('power k=%.4f %.4f %.4f'%(k,*powr))
print('shin z=%.4f %.4f %.4f'%(z,*sh))
# three way example
pis=[1/1.5,1/4.2,1/7.0];B=sum(pis);z,sh=shin(pis)
print('3-way 1.5/4.2/7.0 booksum %.4f mult'%B,[round(x/B,4) for x in pis],'shin z=%.4f'%z,[round(x,4) for x in sh])
print('== spread->win prob table ==')
for sig in [11.5,12.0,12.6,13.5]:
    print('sigma',sig,' '.join('%g:%.3f'%(s,Phi(s/sig)) for s in [1,2,3,4,5,6,7,8,9,10,12,14,16]))
def ml(p): return -100*p/(1-p) if p>=0.5 else 100*(1-p)/p
print('Fair ML for favorite at sigma=12.6 (no vig):',' '.join('%g:%+.0f'%(s,ml(Phi(s/12.6))) for s in [1,2,3,4,5,6,7,8,9,10,12,14]))
# implied sigma from market no-vig ML
d=json.load(open(sys.argv[1]))
g=[]
for r in d:
    try:
        sp=float(r['home_close_spread']);m=float(r['home_final'])-float(r['away_final']);h=float(r['home_close_ml']);a=float(r['away_close_ml']);tot=float(r['close_over_under'])
    except: continue
    if abs(sp)>25 or not(150<=tot<=280) or abs(h)<100 or abs(a)<100: continue
    g.append((sp,m,h,a,tot))
print('n ml games',len(g))
print('Market-implied sigma = |spread|/invPhi(novig fav prob):')
for s in [2,3,4,5,6,7,8,9,10,11,12,13,14]:
    L=[x for x in g if abs(x[0]) in (s,s-0.5)]
    sigs=[]
    for sp,m,h,a,t in L:
        ph,pa=imp(h),imp(a);pf=max(ph,pa)/(ph+pa)
        if pf>0.5: sigs.append(abs(sp)/inv(pf))
    print(' |s| %g-%g n=%d median sigma %.2f'%(s-0.5,s,len(sigs),st.median(sigs)))
# probit MLE sigma for SU outcome
best=None
for sig10 in range(90,170):
    sig=sig10/10;ll=0
    for sp,m,h,a,t in g:
        if m==0: continue
        p=Phi(-sp/sig);p=min(max(p,1e-9),1-1e-9)
        ll+= math.log(p) if m>0 else math.log(1-p)
    if best is None or ll>best[1]: best=(sig,ll)
print('MLE sigma for SU win given closing spread: %.1f'%best[0])
print('== buying half points (fair line at integer k, landing prob h) ==')
for h in [0.02,0.03,0.04,0.045,0.05,0.06,0.09,0.15]:
    ev_off=(1-h)/2*(1/1.1)-(1+h)/2   # -k.5 at -110
    ev_on=(1-h)/2*(100/120)-(1-h)/2  # -k at -120
    ev_on2=(1-h)/2*(100/115)-(1-h)/2
    print(' h=%.3f EV -k.5@-110 %.4f | -k@-120 %.4f | -k@-115 %.4f'%(h,ev_off,ev_on,ev_on2))
# break-even landing prob for 10-cent and 5-cent buys
for price in [-115,-120,-125]:
    w=100/abs(price)
    lo,hi=0,0.5
    for _ in range(100):
        h=(lo+hi)/2
        if (1-h)/2*w-(1-h)/2 > (1-h)/2/1.1-(1+h)/2: hi=h
        else: lo=h
    print(' buy half-point onto number to %d worthwhile if P(land)>%.3f'%(price,h))
print('== Kelly ==')
for p in [0.5238,0.53,0.54,0.55,0.56,0.58,0.60]:
    for a in [-110,-105]:
        b=dec(a)-1;q=1-p
        f=(b*p-q)/b; ev=p*b-q
        G=lambda f: p*math.log(1+b*f)+q*math.log(1-f)
        print(' p=%.4f %d EV/bet %.4f full Kelly %.4f; growth/bet full %.6f half %.6f (ratio %.3f) 2x %.6f'%(p,a,ev,f,G(f),G(f/2),G(f/2)/G(f) if f>0 else 0,G(2*f) if f>0 else 0))
print('P(double before halve) c*Kelly = 1/(1+2^-(2-c)/c); P(ever hit x of bankroll)= x^(2/c-1):')
for c in [0.25,0.5,0.75,1,1.5,2]:
    print(' c=%.2f Pdouble-before-halve %.3f ; P(ever drop to 50%%) %.4f ; P(ever drop to 25%%) %.4f ; growth rel %.3f'%(c,1/(1+2**(-(2-c)/c)),0.5**(2/c-1),0.25**(2/c-1),c*(2-c)))
print('== sample size / luck ==')
be=1/1.90909
for p in [0.53,0.54,0.55]:
    for n in [100,250,500,1000,2500,5000]:
        sd=math.sqrt(p*(1-p)/n)
        z=(p-be)/math.sqrt(be*(1-be)/n)
        roi=p*(10/11)-(1-p)
        units_sd=math.sqrt(n)*math.sqrt(p*(10/11)**2+(1-p)-(p*10/11-(1-p))**2)
        P_losing=Phi(-(roi*n)/units_sd)
        print(' p=%.2f n=%5d win%% SD %.3f z vs 52.38%% %.2f ROI %.2f%% E[units] %+.1f SD units %.1f P(net loss) %.3f'%(p,n,sd,z,100*roi,roi*n,units_sd,P_losing))
for p in [0.53,0.54,0.55]:
    for zc in [1.645,1.96,2.576]:
        n=(zc*math.sqrt(be*(1-be))/(p-be))**2
        print(' bets needed for true %.2f to show z=%.2f vs BE (expected): %d'%(p,zc,math.ceil(n)))
# P coinflip bettor >=55% over n
for n in [100,250,500,1000]:
    print(' P(50%% bettor hits >=55%% over %d) = %.4f; P(52.38%%-bettor... ) '%(n,1-Phi((0.55-0.5)/math.sqrt(.25/n))))
print('== teasers ==')
for legs,price in [(2,-110),(2,-120),(3,160),(3,140),(4,250)]:
    D=dec(price);print(' %d-team at %+d break-even per leg %.4f'%(legs,price,(1/D)**(1/legs)))
