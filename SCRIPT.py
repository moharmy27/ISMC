# Copyright: (c) 2021 Bentley Systems, Incorporated. All rights reserved.

import plxle
import math
from plxle.analysis_settings import *
from plxle.material import *
from plxle.model import *
from plxle.water import *

def create_model(uw,c,phi,deg,h):
    model_settings = ModelSettings2D(
        "BASIC",
        Units.Metric,
        SlipDirection.LeftToRight
    )
    
    con_set=ConvergenceSettings(min_slip_surface_depth=h*0.9)

    analysis_settings = AnalysisSettings(
        [CalculationMethod.GLE],convergence_settings =  con_set
    )
    analysis = SingleAnalysis2D(CuckooSearch(100), False)
    
    upper_soil = MohrCoulombMaterial("Upper Soil", uw, c, phi)
    lower_soil = MohrCoulombMaterial("Lower Soil", 18, 1000, 85)

    wit=h/(math.tan(math.radians(deg)))
    upper_region = Region2D(
        "Upper Soil",
        [
            (-20, 0),
            (-20, h),
            (5, h),
            (5+wit, 0)
        ]
    )

    lower_region = Region2D(
        "Lower Soil",
        [
            (-20, 0),
            (50, 0),
            (50, -20),
            (-20, -20)
        ]
    )

    pwp = WaterTablePWP2D(
        WaterTablePiezoLine(
            [
                (-20, h),
                (5, h),
                (5+wit, 0),
                (50, 0)
            ], 
            [
                upper_region,
                lower_region
            ]
        ),
        []
    )
    
    regions = [upper_region, lower_region]
    materials = [upper_soil, lower_soil]
    material_assignment = {
        upper_region: upper_soil,
        lower_region: lower_soil
    }

    model = Model2D(
        model_settings,
        analysis_settings,
        analysis,
        materials,
        regions,
        material_assignment,
        pwp
    )
    return model

#uw,c,phi,deg,h
ai=[10,15,20]
bi=[10,15,20]
ci=[10,20,30]
di=[10,20,30,40,50,60,70,80]
ei=[10,15,20,30,40]
hasil=[]
for a in ai:
    for b in bi:
        for c in ci:
            for d in di:
                for e in ei:
                    if __name__ == "__main__":
                        model = create_model(a,b,c,d,e)
                        version = plxle.get_version()
                        result = plxle.solve(model)
                        print(f"Solver version: {version}")
                        print(f"Model solved with FOS = {result.fos}")
                        print(f"Output to {result.output_path}")
                    fos_re=result.fos
                    uwu=result.model_info
                    ini=uwu.rfind('"Total Weight":')
                    tail=uwu.rfind('"Total Volume":')
                    wei=uwu[(ini+17):(tail-15)]
                    hasil.append([a,b,c,d,e,wei,fos_re])
                    