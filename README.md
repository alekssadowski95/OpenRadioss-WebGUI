# OpenRadioss-WebGUI
Run and visualize dynamic FEM simulations from Abaqus/ Calculix *.inp files with the explicit open-source OpenRadioss solver.

![openradioss gui](openradioss-2.png)
*Figure 1: Impact of a debris particle onto the surface of the ISS*

## Overview
Quickly get started with OpenRadioss and open-source dynamic simulations. The OpenRadioss-WebGUI combines :
- OpenRadioss solver
- 3D WebWiewer VTK for unstructured meshes (based on three.js)
- Web-framework based on Flask (Webapp)
- Desktop-app deployment 
- Integrated dynamic, explicit simulation examples for teaching students
- Immediate results, while simulation is still running
- Compatible with a fully open-source workflow (FreeCAD + PrePoMax + OpenRadioss)
- Multi-core support out of the box (MPI)
  
## Getting started
1. Create CAD geometry in FreeCAD
2. Pre-Processing with PrePoMax
3. Solve and visualize with OpenRadioss-WebGUI

### 1. CAD Geometry in FreeCAD
![bullet-freecad](bullet-freecad.png)
*Figure 2: Creating the CAD geometry for the sperical particle and the simplified ISS hull model*
### 2. Pre-Processing with PrePoMax
![bullet-prepomax](bullet-prepomax.png)
*Figure 3: Setting up the impact simulation with non-linear material and fracture*
### 3. Solve and visualize with OpenRadioss-WebGUI
![bullet-openradioss-webgui](bullet-openradioss-webgui.png)
*Figure 4: Solving the case study and tracking the results with fracture while the simulations is still running in 3D*

## Applications of dynamic-explicit simulations using OpenRadioss
Applications of simulations performed using this software, specifically featuring plastic deformation and fracture. These case studies will be integrated into the OpenRadioss-WebGUI:
- EV platform EuroNCAP full-width crash simulation
- ISS space particle impact
- Mars Rover drop-off simulation on mars surface and suspension test
- EV Battery pack impact in a crash
- Deformation and stress of a compressed flat silicone gasket from a hydrogen fuel cell (PEMFC)
  
## Fully open-source workflow for crash simulations
The OpenRadioss-WebGUI simplifies the open-source workflow for crash simulations, that we have developed and validated by combining OpenRadioss with a Post-processing solution, reducing the number of software packages(FreeCAD + PrePoMax + OpenRadioss + ParaView) -> (FreeCAD + PrePoMax + OpenRadioss-WebGUI).
![Fully_open-source_workflow_for_crash_simulations](Fully_open-source_workflow_for_crash_simulations.png)
*Figure 5: Previous workflow overview comprised of FreeCAD, PrePoMax, OpenRadioss and ParaView*
![Fully_open-source_workflow_for_crash_simulations-diagram](Fully_open-source_workflow_for_crash_simulations-diagram.png)
*Figure 6: Block diagram of the previous workflow, including the interfaces and steps*

## Development of GUI 2.0
To make it even easier to get started, the GUI will be further simplified, while offering more information.
![new-ui-element-for-simulations-results](new-ui-element-for-simulations-results.jpeg)
*Figure 7: Hand drawing of a new user interface concept for the OpenRadioss-WebGUI with inspiration from a film reel*

## Requirements for development environment
Requires:
- Python 3.10

## Credits
- OpenRadioss solver: https://github.com/OpenRadioss/OpenRadioss
- OpenRadioss inp2rad: https://github.com/OpenRadioss/Tools/tree/main/input_converters/inp2rad
- three.js: https://github.com/mrdoob/three.js/
- Flask web-framework: https://github.com/pallets/flask
- FreeCAD: https://github.com/FreeCAD/FreeCAD
- PrePoMax: https://gitlab.com/MatejB/PrePoMax

