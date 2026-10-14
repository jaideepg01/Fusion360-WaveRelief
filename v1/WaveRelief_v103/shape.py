"""Dimensionless relief profile, shared by Fusion and portable generator."""
import math
WIDTH_MM = 200.0
HEIGHT_MM = 380.0
THICKNESS_MM = 11.0
DEPTH_MM = 4.0
CENTER_X = 0.43
CENTER_Y = 0.39
RADIUS_X = 0.48
RADIUS_Y = 0.21
WAVE_AMOUNT = 0.65
WAVE_COUNT = 3.0
WAVE_PHASE_DEG = 0.0
SECTIONS = 49
POINTS = 41

def depth_fraction(u, v):
    dx = (u-CENTER_X)/RADIUS_X
    dy = (v-CENTER_Y)/RADIUS_Y
    r = math.sqrt(dx*dx+dy*dy)
    a = max(0.0, min(1.0, (v-0.49)/0.32))
    a = a*a*(3.0-2.0*a)
    phase = r*WAVE_COUNT*RADIUS_Y/(1-CENTER_Y) + WAVE_AMOUNT*a*math.sin(2*math.pi*u+0.7) + WAVE_PHASE_DEG/360.0
    # Smooth crest and broad rounded valleys; no vertical walls or undercuts.
    return 0.5*(1.0-math.cos(2*math.pi*phase))
