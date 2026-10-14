"""V2 concave channel relief with narrow, rounded crests and adaptive samples."""
import math
WIDTH_MM=200.0
HEIGHT_MM=380.0
THICKNESS_MM=11.0
DEPTH_MM=4.0
CREST_ALLOWANCE_MM=0.20
CENTER_X=0.43
CENTER_Y=0.39
RADIUS_X=0.48
RADIUS_Y=0.21
WAVE_AMOUNT=0.65
WAVE_COUNT=3.0
WAVE_PHASE_DEG=0.0
RIDGE_SHARPNESS=12.0
SECTIONS=61
POINTS=41

def phase_at(u,v):
    r=math.sqrt(((u-CENTER_X)/RADIUS_X)**2+((v-CENTER_Y)/RADIUS_Y)**2)
    a=max(0.,min(1.,(v-.49)/.32));a=a*a*(3-2*a)
    return r*WAVE_COUNT*RADIUS_Y/(1-CENTER_Y)+WAVE_AMOUNT*a*math.sin(2*math.pi*u+.7)+WAVE_PHASE_DEG/360

def depth_fraction(u,v):
    e=1/RIDGE_SHARPNESS
    s=math.sin(math.pi*phase_at(u,v))
    return (math.sqrt(s*s+e*e)-e)/(math.sqrt(1+e*e)-e)

def section_us(v):
    """Anchor every crest and add points either side, in addition to base grid.
    Anchor locations are computed at creation. Large styling edits should be
    rebuilt so the adaptive anchors move to the new crests.
    """
    us={i/(POINTS-1) for i in range(POINTS)}
    scan=800
    for i in range(scan):
        a=i/scan;b=(i+1)/scan
        pa=phase_at(a,v);pb=phase_at(b,v)
        lo=math.ceil(min(pa,pb));hi=math.floor(max(pa,pb))
        for level in range(lo,hi+1):
            aa=a;bb=b;fa=pa-level
            for _ in range(28):
                mid=(aa+bb)/2;fm=phase_at(mid,v)-level
                if fa*fm<=0:bb=mid
                else:aa=mid;fa=fm
            root=(aa+bb)/2
            for delta in (-.025,-.012,-.005,0,.005,.012,.025):
                x=root+delta
                if 0<=x<=1:us.add(round(x,8))
    result=[]
    for x in sorted(us):
        if not result or x-result[-1]>0.0002:result.append(x)
    return result


def section_vs():
    return [j/(SECTIONS-1) for j in range(SECTIONS)]
