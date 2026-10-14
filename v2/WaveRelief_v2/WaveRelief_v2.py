"""Autodesk Fusion native parametric relief. Run through Scripts and Add-Ins.
No external packages. A NEW document is created; existing designs are untouched.
"""
import adsk.core, adsk.fusion, traceback, math, os, importlib.util, time
HERE=os.path.dirname(os.path.abspath(__file__))
VERSION='2.0.0'
LOG_PATH=os.path.join(HERE,'wave_relief_build.log')

class BuildCancelled(Exception):
    pass

def log(message):
    try:
        with open(LOG_PATH,'a',encoding='utf-8') as f:
            f.write(time.strftime('%H:%M:%S ')+message+'\n')
    except OSError:
        pass

def update(progress, value, message):
    progress.progressValue=value
    progress.message=message+'\n%p% complete'
    adsk.doEvents()
    if progress.wasCancelled:
        raise BuildCancelled('Build cancelled by user')

def point(x,y,z=0):
    return adsk.core.Point3D.create(x,y,z)

def expression(u,v):
    # All styling inputs remain live user parameters in Fusion's timeline.
    a=max(0.,min(1.,(v-.49)/.32)); a=a*a*(3-2*a)
    radial='sqrt((({u:.10f}-CenterX)/OvalRadiusX)^2+(({v:.10f}-CenterY)/OvalRadiusY)^2)'.format(u=u,v=v)
    phase='({r}*WaveCount*OvalRadiusY/(1-CenterY)+WaveBend*{a:.10f}*sin({angle:.10f} deg)+WavePhase/(360 deg))'.format(r=radial,a=a,angle=(2*math.pi*u+.7)*180/math.pi)
    ridge='(sqrt(sin('+phase+'*180 deg)^2+(1/RidgeSharpness)^2)-1/RidgeSharpness)/(sqrt(1+(1/RidgeSharpness)^2)-1/RidgeSharpness)'
    return 'PanelThickness-CrestAllowance-(CarveDepth-CrestAllowance)*('+ridge+')'

def run(context):
    ui=None
    progress=None
    sk=None
    stage="Starting"
    try:
        app=adsk.core.Application.get();ui=app.userInterface
        try:
            with open(LOG_PATH,'w',encoding='utf-8') as f:
                f.write('WaveRelief '+VERSION+'\nScript: '+os.path.abspath(__file__)+'\n')
        except OSError:
            pass
        log('run(context) entered')
        progress=ui.createProgressDialog()
        progress.cancelButtonText='Cancel'
        progress.isCancelButtonShown=True
        progress.isBackgroundTranslucent=False
        progress.show('WaveRelief V'+VERSION,'Starting script...\n%p% complete',0,100,0)
        update(progress,0,'Loading profile definition')
        spec=importlib.util.spec_from_file_location('wave_relief_shape_v2',os.path.join(HERE,'shape.py'))
        shape=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(shape)
        stage='Create document'
        log(stage)
        # Rebuild the active V2 design into a NEW document while retaining
        # its edited user parameters. All defaults are created before restoring
        # expressions, so references between user parameters remain valid.
        previous=adsk.fusion.Design.cast(app.activeProduct)
        snapshot={}
        if previous and previous.userParameters.itemByName('RidgeSharpness') and previous.userParameters.itemByName('OvalRadiusX'):
            for k in range(previous.userParameters.count):
                q=previous.userParameters.item(k)
                snapshot[q.name]=q.expression
            log('Rebuilding from active V2 parameter values')
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design=adsk.fusion.Design.cast(app.activeProduct)
        design.designType=adsk.fusion.DesignTypes.ParametricDesignType
        # Fusion forbids assigning a name to the root component.
        # Name the design when saving; the resulting body is named below.
        root=design.rootComponent
        params=[
            ('PanelWidth','200 mm','mm','Panel X dimension'),
            ('PanelHeight','380 mm','mm','Panel Y dimension'),
            ('PanelThickness','11 mm','mm','Original stock height above flat back'),
            ('CarveDepth','4 mm','mm','Maximum nominal carving depth; keep below PanelThickness'),
            ('CrestAllowance','0.20 mm','mm','Small crest allowance to accommodate spline overshoot; keep below CarveDepth'),
            ('RidgeSharpness','12','','Larger = narrower crest; use 4 to 16; not a radius in mm'),
            ('WaveCount','3','','Nominal cycles from centre toward top; controls wave density'),
            ('WaveBend','0.65','','Top wave bend: 0 = concentric ovals, larger = flowing waves'),
            ('CenterX','0.43','','Centre X fraction of panel width; use 0.15 to 0.85'),
            ('CenterY','0.39','','Centre Y fraction of panel height; use 0.15 to 0.80'),
            ('OvalRadiusX','0.48','','Horizontal contour scale as fraction of panel width'),
            ('OvalRadiusY','0.21','','Vertical contour scale as fraction of panel height'),
            ('WavePhase','0 deg','deg','0 = raised centre; 180 deg = centre depression'),
        ]
        stage='Create user parameters'
        log(stage)
        update(progress,1,stage)
        for name,val,unit,comment in params:
            param=design.userParameters.add(name,adsk.core.ValueInput.createByString(val),unit,comment)
            param.isFavorite=True
        for name,val,unit,comment in params:
            if name in snapshot:
                design.userParameters.itemByName(name).expression=snapshot[name]
        # Adaptive anchors and the initial points use the restored styling.
        for field,name in [('CENTER_X','CenterX'),('CENTER_Y','CenterY'),('RADIUS_X','OvalRadiusX'),('RADIUS_Y','OvalRadiusY'),('WAVE_AMOUNT','WaveBend'),('WAVE_COUNT','WaveCount'),('RIDGE_SHARPNESS','RidgeSharpness')]:
            setattr(shape,field,design.userParameters.itemByName(name).value)
        shape.WAVE_PHASE_DEG=design.userParameters.itemByName('WavePhase').value*180/math.pi
        w=design.userParameters.itemByName('PanelWidth').value
        h=design.userParameters.itemByName('PanelHeight').value
        thick=design.userParameters.itemByName('PanelThickness').value
        depth=design.userParameters.itemByName('CarveDepth').value
        allowance=design.userParameters.itemByName('CrestAllowance').value
        if not (w>0 and h>0 and 0<allowance<depth<thick):
            raise ValueError('Require positive dimensions and 0 < CrestAllowance < CarveDepth < PanelThickness')
        if not (0<shape.CENTER_Y<1 and shape.RADIUS_X>0 and shape.RADIUS_Y>0 and shape.RIDGE_SHARPNESS>0):
            raise ValueError('Centre Y must be between 0 and 1; oval radii and RidgeSharpness must be positive')
        profiles=[]
        # Fusion internal lengths are centimetres. Construction plane normal
        # is queried so plane orientation is not assumed.
        normal_y=root.xZConstructionPlane.geometry.normal.y
        if abs(normal_y)<.9: raise RuntimeError('Unexpected XZ plane orientation')
        section_values=shape.section_vs()
        nsections=len(section_values)
        for j,v in enumerate(section_values):
            stage='Section {}/{}: create sketch'.format(j+1,nsections)
            log(stage)
            update(progress,2+int(86*j/nsections),stage)
            pin=root.constructionPlanes.createInput()
            pin.setByOffset(root.xZConstructionPlane,adsk.core.ValueInput.createByString('PanelHeight*{:.10f}'.format(v/normal_y)))
            plane=root.constructionPlanes.add(pin);plane.name='Section {:02d}'.format(j+1)
            sk=root.sketches.add(plane);sk.name='Relief section {:02d}'.format(j+1)
            sk.isComputeDeferred=True
            us=shape.section_us(v)
            pts=adsk.core.ObjectCollection.create()
            for u in us:
                z=thick-allowance-(depth-allowance)*shape.depth_fraction(u,v)
                pts.add(sk.modelToSketchSpace(point(w*u,h*v,z)))
            spline=sk.sketchCurves.sketchFittedSplines.add(pts)
            origin=sk.originPoint
            br=sk.sketchPoints.add(sk.modelToSketchSpace(point(w,h*v,0)))
            lines=sk.sketchCurves.sketchLines
            left=lines.addByTwoPoints(origin,spline.startSketchPoint)
            right=lines.addByTwoPoints(spline.endSketchPoint,br)
            bottom=lines.addByTwoPoints(br,origin)
            gc=sk.geometricConstraints
            gc.addVertical(left);gc.addVertical(right);gc.addHorizontal(bottom)
            # Position every fit point with expressions. Styling therefore
            # recomputes natively; this is not a frozen imported surface.
            for i in range(spline.fitPoints.count):
                if i%8==0:
                    stage='Section {}/{}: constrain point {}/{}'.format(j+1,nsections,i+1,len(us))
                    log(stage)
                    update(progress,2+int(86*(j+i/len(us))/nsections),stage)
                p=spline.fitPoints.item(i);u=us[i]
                g=p.geometry
                if i:
                    d=sk.sketchDimensions.addDistanceDimension(origin,p,adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,point(g.x,g.y+1))
                    d.parameter.expression='PanelWidth*{:.10f}'.format(u)
                d=sk.sketchDimensions.addDistanceDimension(origin,p,adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,point(g.x+1,g.y))
                d.parameter.expression=expression(u,v)
            stage='Section {}/{}: solve sketch'.format(j+1,nsections)
            log(stage)
            update(progress,2+int(86*(j+.95)/nsections),stage)
            sk.isComputeDeferred=False
            if sk.profiles.count!=1:
                raise RuntimeError('Section {} is not a single closed profile'.format(j+1))
            profiles.append(sk.profiles.item(0))
            sk.isLightBulbOn=False
            plane.isLightBulbOn=False
            log('Section {} complete: {} closed profile'.format(j+1,sk.profiles.count))
        stage='Build solid loft'
        log(stage)
        update(progress,90,stage+' — Fusion may pause during this operation')
        lofts=root.features.loftFeatures
        li=lofts.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        li.isSolid=True
        li.isClosed=False
        li.isTangentEdgesMerged=True
        for prof in profiles: li.loftSections.add(prof)
        loft=lofts.add(li);loft.name='Parametric wave relief'
        if loft.bodies.count!=1: raise RuntimeError('Expected one solid')
        loft.bodies.item(0).name='CNC Wave Panel'
        stage='Compute design and fit view'
        log(stage)
        update(progress,97,stage)
        design.computeAll()
        app.activeViewport.fit()
        update(progress,100,'Complete')
        progress.hide()
        log('COMPLETE: one solid created')
        ui.messageBox('WaveRelief V'+VERSION+'\nRelief created. Save as F3D.\nModify > Change Parameters controls size AND styling.\nRidgeSharpness controls crest sharpness. Rebuild after large styling edits to relocate crest samples.\nSTEP/STL companions have fixed geometry; use this design for parameter editing.','Wave Relief')
    except BuildCancelled:
        log('CANCELLED at '+stage)
        if progress: progress.hide()
        if sk:
            try: sk.isComputeDeferred=False
            except: pass
        if ui: ui.messageBox('Cancelled at '+stage+'\nThe new document may contain partial sketches.','WaveRelief V'+VERSION)
    except:
        detail=traceback.format_exc()
        log('FAILED at '+stage+'\n'+detail)
        if progress: progress.hide()
        if ui: ui.messageBox('WaveRelief V'+VERSION+'\nStage: '+stage+'\nScript: '+os.path.abspath(__file__)+'\nLog: '+LOG_PATH+'\n\n'+detail,'Wave Relief build error')
    finally:
        if progress:
            try: progress.hide()
            except: pass
