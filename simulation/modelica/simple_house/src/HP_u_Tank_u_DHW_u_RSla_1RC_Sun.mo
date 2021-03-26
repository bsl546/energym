within modelica.simple_house.src;
model HP_u_Tank_u_DHW_u_RSla_1RC_Sun
  "Heat pump connected to a tank storage, DHW and a simple room model with radiant slab"
  extends Modelica.Icons.Example;
  replaceable package MediumA =
      Buildings.Media.Air "Medium model for air";
  replaceable package MediumW =
      Buildings.Media.Water "Medium model for water";

  ////////////////////////////
  // Parameter Specification
  ////////////////////////////

  // Heat Pump
  parameter Modelica.SIunits.Power P_nominal = 10e3
    "Nominal compressor power (at y=1)";
  parameter Real COP_nominal = 4
    "Nominal COP";
  parameter Modelica.SIunits.MassFlowRate mHeaPum_flow_nominal = 1.0
    "Heat pump nominal mass flow rate";
  parameter Modelica.SIunits.TemperatureDifference dTEva_nominal = -10
    "Temperature difference evaporator outlet-inlet";
  parameter Modelica.SIunits.TemperatureDifference dTCon_nominal = 10
    "Temperature difference condenser outlet-inlet";
  parameter Modelica.SIunits.TemperatureDifference TCon_nominal = 273.15 + 30
    "Condenser Temperature used to compute COP_nominal";
  parameter Modelica.SIunits.TemperatureDifference TEva_nominal = 273.15 + 5
    "Evaporator Temperature used to compute COP_nominal";

  // Tank Storage
  parameter Modelica.SIunits.Volume SH_tank_vol_m3 = 1.0
    "Storage Tank Volume";
  parameter Modelica.SIunits.Length SH_tank_hei_m = 1.0
    "Storage Tank Height";
  parameter Modelica.SIunits.Length SH_hex_top_hei_m = 0.5
    "Top height of heat exchanger";
  parameter Modelica.SIunits.Length SH_hex_bottom_hei_m = 0.1
    "Bottom height of heat exchanger";
  parameter Modelica.SIunits.HeatFlowRate SH_nominal_hex_power_W = 0.278*4200*20
    "Nominal power of the heat exchanger";
  parameter Modelica.SIunits.Temperature TTan_nominal = 273.15 + 40
    "Temperature of fluid inside the tank at nominal heat transfer conditions";
  parameter Modelica.SIunits.Temperature THex_nominal = 273.15 + 50
    "Temperature of fluid inside the heat exchanger at nominal heat transfer conditions";

  // Floor heating radiant slab
  parameter Modelica.SIunits.Area slab_surf = 100
    "Surface area of radiant slab (m^2)";
  parameter Modelica.SIunits.MassFlowRate mSlab_flow_nominal = 1.0
    "Radiator nominal mass flow rate";

  // Building envelope
  parameter Modelica.SIunits.ThermalConductance therm_cond_G = 500
    "Envelope Thermal Conductance W/K";
  parameter Modelica.SIunits.HeatCapacity heat_capa_C = 5e5
    "Envelope Heat Capacity J/K";
  parameter Modelica.SIunits.Volume room_vol_V=6*10*3
    "Room volume";
  parameter Modelica.SIunits.MassFlowRate mA_flow_nominal = room_vol_V*6/3600
    "Air nominal mass flow rate";
  parameter Modelica.SIunits.HeatFlowRate QRooInt_flow = 1000
    "Internal heat gains of the room";

  // Sun effect on tilted surface 1
  parameter Real tilt1_C = 20 "Surface tilt (°C)";
  parameter Real azimuth1_C = -45 "Surface azimuth (°C)";
  parameter Real latitude1_C = 37.7 "Latitude (°C)";
  parameter Real sun_heat_gain1 = 2.5 "Sun heat gain";

// Sun effect on tilted surface 2
  parameter Real tilt2_C = 20 "Surface tilt (°C)";
  parameter Real azimuth2_C = -45 "Surface azimuth (°C)";
  parameter Real latitude2_C = 47.3 "Latitude (°C)";
  parameter Real sun_heat_gain2 = 2.5 "Sun heat gain";

  // Weather data
  parameter String weafile = Modelica.Utilities.Files.loadResource(
        "modelica://modelica/simple_house/wf/Switzerland_CHE_Maur.mos")
    "Name of weather data file";

//------------------------------------------------------------------------------//

  Buildings.Fluid.MixingVolumes.MixingVolume vol(
    redeclare package Medium = MediumA,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    m_flow_nominal=mA_flow_nominal,
    V=room_vol_V)
    annotation (Placement(transformation(extent={{-10,-10},{10,10}},
        rotation=270,
        origin={240,-50})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor theCon(G=therm_cond_G)
    "Thermal conductance with the ambient"
    annotation (Placement(transformation(extent={{200,30},{220,50}})));

  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHea
    "Prescribed heat flow"
    annotation (Placement(transformation(extent={{280,70},{260,90}})));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor heaCap(C=heat_capa_C)
    "Heat capacity for furniture and walls"
    annotation (Placement(transformation(extent={{-10,-10},{10,10}},
        rotation=270,
        origin={270,40})));
  Modelica.Blocks.Sources.CombiTimeTable timTab(
      extrapolation=Modelica.Blocks.Types.Extrapolation.Periodic,
      smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
      table=[-6*3600, 0;
              8*3600, QRooInt_flow;
             18*3600, 0]) "Time table for internal heat gain"
    annotation (Placement(transformation(extent={{320,70},{300,90}})));
  Buildings.Fluid.Sensors.TemperatureTwoPort temTan2Sla(
    redeclare package Medium = MediumW,
    m_flow_nominal=mSlab_flow_nominal,
    T_start=TTan_nominal)
    "Supply water temperature from Tank to Radiant Slab"
    annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=0,
        origin={70,-80})));
  Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor temRoo
    "Room temperature" annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        origin={70,0})));

//----------------------------------------------------------------------------//

  Buildings.Fluid.Movers.FlowControlled_m_flow pumHP(
    redeclare package Medium = MediumW,
    m_flow_nominal=mHeaPum_flow_nominal,
    y_start=1,
    m_flow_start=0.85,
    T_start=THex_nominal,
    nominalValuesDefineDefaultPressureCurve=true,
    use_inputFilter=false,
    energyDynamics=Modelica.Fluid.Types.Dynamics.SteadyState)
    "Pump for HP condenser" annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        rotation=0,
        origin={-150,-180})));
//----------------------------------------------------------------------------//

  Buildings.Fluid.Sensors.TemperatureTwoPort temSla2Tan(
    redeclare package Medium = MediumW,
    m_flow_nominal=mSlab_flow_nominal,
    T_start=TTan_nominal)
    "Return water temperature from Radiant Slab to Tank"
    annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=0,
        origin={150,-80})));

//------------------------------------------------------------------------------------//

  Buildings.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(
    filNam=weafile) "Weather data reader"
    annotation (Placement(transformation(extent={{60,30},{80,50}})));
  Buildings.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
    annotation (Placement(transformation(extent={{110,30},{130,50}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature TOut
    "Outside temperature"
    annotation (Placement(transformation(extent={{160,30},{180,50}})));

//--------------------------------------------------------------------------------------//

  Buildings.Fluid.HeatPumps.Carnot_y heaPum(
    redeclare package Medium1 = MediumW,
    redeclare package Medium2 = MediumA,
    P_nominal=P_nominal,
    dTEva_nominal=dTEva_nominal,
    dTCon_nominal=dTCon_nominal,
    dp1_nominal=2000,
    dp2_nominal=2000,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    show_T=true,
    use_eta_Carnot_nominal=false,
    COP_nominal=COP_nominal,
    TCon_nominal=TCon_nominal,
    TEva_nominal=TEva_nominal) "Heat pump model"
    annotation (Placement(transformation(extent={{16,-16},{-16,16}},
        rotation=270,
        origin={-230,-120})));

  Modelica.Blocks.Math.Gain gaiHP(k=1) "Gain for Heat Pump"
    annotation (Placement(transformation(extent={{-176,-156},{-192,-140}})));
  Buildings.Fluid.Storage.ExpansionVessel expHP(redeclare package Medium =
        MediumW)
    annotation (Placement(transformation(extent={{-110,-162},{-90,-142}})));
  Buildings.Fluid.Sources.Boundary_pT hole(redeclare package Medium = MediumA,
      nPorts=1) annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=0,
        origin={-270,-180})));
  Buildings.Fluid.Sources.MassFlowSource_T mf_sou(
    redeclare package Medium = MediumA,
    m_flow=mHeaPum_flow_nominal,
    use_T_in=true,
    nPorts=1) annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=90,
        origin={-296,-110})));
  Buildings.Fluid.Storage.StratifiedEnhancedInternalHex tanSH(
    redeclare package Medium = MediumW,
    m_flow_nominal=mSlab_flow_nominal,
    VTan=SH_tank_vol_m3,
    dIns=0.07,
    redeclare package MediumHex = MediumW,
    CHex=40,
    Q_flow_nominal=SH_nominal_hex_power_W,
    hTan=SH_tank_hei_m,
    hHex_a=SH_hex_top_hei_m,
    hHex_b=SH_hex_bottom_hei_m,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    allowFlowReversal=false,
    allowFlowReversalHex=false,
    mHex_flow_nominal=mHeaPum_flow_nominal,
    energyDynamicsHex=Modelica.Fluid.Types.Dynamics.FixedInitial,
    TTan_nominal=TTan_nominal,
    THex_nominal=THex_nominal) "Tank with heat exchanger configured as dynamic"
    annotation (Placement(transformation(extent={{-60,-130},{-26,-98}})));
  Buildings.Fluid.Movers.FlowControlled_m_flow pumSla(
    redeclare package Medium = MediumW,
    m_flow_nominal=mSlab_flow_nominal,
    y_start=1,
    m_flow_start=0.85,
    T_start=TTan_nominal,
    nominalValuesDefineDefaultPressureCurve=true,
    use_inputFilter=false,
    energyDynamics=Modelica.Fluid.Types.Dynamics.SteadyState)
    "Pump for radiator" annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        rotation=0,
        origin={20,-180})));
  Buildings.Fluid.Storage.ExpansionVessel expRad(redeclare package Medium =
        MediumW)
    annotation (Placement(transformation(extent={{210,-162},{230,-142}})));
  Buildings.Fluid.Sensors.TemperatureTwoPort temHP2Hex(
    redeclare package Medium = MediumW,
    m_flow_nominal=mHeaPum_flow_nominal,
    T_start=THex_nominal) "Supply water temperature from HP to Tank"
    annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=0,
        origin={-190,-80})));
  Buildings.Fluid.Sensors.TemperatureTwoPort temHex2HP(
    redeclare package Medium = MediumW,
    m_flow_nominal=mHeaPum_flow_nominal,
    T_start=THex_nominal) "Return water temperature from Tank to HP"
    annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        rotation=0,
        origin={-190,-180})));
  simple_house.lib.SunRad_TiltSurf sunRad2(
    weafile=weafile,
    tilt_C=tilt2_C,
    azimuth_C=azimuth2_C,
    latitude_C=latitude2_C) "Solar irradiance on tilted surface"
    annotation (Placement(transformation(extent={{120,66},{140,86}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow sunHea2
    "Solar heat flow"
    annotation (Placement(transformation(extent={{202,70},{222,90}})));
  Modelica.Blocks.Math.Gain gaiSun2(k=sun_heat_gain2)
    "Heat gain from solar irradiance"
    annotation (Placement(transformation(extent={{164,72},{180,88}})));
  simple_house.lib.SunRad_TiltSurf sunRad1(
    weafile=weafile,
    tilt_C=tilt1_C,
    azimuth_C=azimuth1_C,
    latitude_C=latitude1_C) "Solar irradiance on tilted surface"
    annotation (Placement(transformation(extent={{120,106},{140,126}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow sunHea1
    "Solar heat flow"
    annotation (Placement(transformation(extent={{202,110},{222,130}})));
  Modelica.Blocks.Math.Gain gaiSun1(k=sun_heat_gain1)
    "Heat gain from solar irradiance"
    annotation (Placement(transformation(extent={{164,112},{180,128}})));
  Modelica.Blocks.Interfaces.RealInput uHP
    annotation (Placement(transformation(extent={{-192,-12},{-168,12}})));
  Modelica.Blocks.Interfaces.RealInput uRSla
    annotation (Placement(transformation(extent={{-32,-52},{-8,-28}})));
  Modelica.Blocks.Interfaces.RealOutput temHP
    annotation (Placement(transformation(extent={{-210,-50},{-230,-30}})));
  Modelica.Blocks.Interfaces.RealOutput temRoom
    annotation (Placement(transformation(extent={{30,-10},{10,10}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalResistor thermalResistor(R=
        embPipe.R_c/embPipe.A_floor*embPipe.nDiscr) annotation (Placement(
        transformation(
        extent={{-10,-10},{10,10}},
        rotation=90,
        origin={112,-40})));
  IDEAS.Fluid.HeatExchangers.RadiantSlab.EmbeddedPipe embPipe(
    redeclare package Medium = MediumW,
    redeclare
      IDEAS.Fluid.HeatExchangers.RadiantSlab.BaseClasses.FH_ValidationEmpa4_6
      RadSlaCha,
    m_flow_nominal=mSlab_flow_nominal,
    A_floor=slab_surf,
    nParCir=10,
    computeFlowResistance=true,
    m_flowMin=mSlab_flow_nominal/5,
    nDiscr=1,
    R_c=0.05,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial)
    annotation (Placement(transformation(extent={{102,-90},{122,-70}})));
  Buildings.Fluid.Storage.StratifiedEnhancedInternalHex tanDHW(
    redeclare package Medium = MediumW,
    m_flow_nominal=mSlab_flow_nominal,
    VTan=SH_tank_vol_m3,
    dIns=0.07,
    redeclare package MediumHex = MediumW,
    CHex=40,
    Q_flow_nominal=SH_nominal_hex_power_W,
    hTan=SH_tank_hei_m,
    hHex_a=SH_hex_top_hei_m,
    hHex_b=SH_hex_bottom_hei_m,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    allowFlowReversal=true,
    allowFlowReversalHex=false,
    mHex_flow_nominal=mHeaPum_flow_nominal,
    energyDynamicsHex=Modelica.Fluid.Types.Dynamics.FixedInitial,
    TTan_nominal=TTan_nominal,
    THex_nominal=THex_nominal) "Tank with heat exchanger configured as dynamic"
    annotation (Placement(transformation(extent={{-60,30},{-26,62}})));
  Buildings.Fluid.Actuators.Valves.ThreeWayLinear valve(redeclare package
      Medium = MediumW, m_flow_nominal=mHeaPum_flow_nominal,
    dpValve_nominal=4000)
    annotation (Placement(transformation(extent={{-110,-90},{-130,-70}})));
  Modelica.Blocks.Interfaces.RealInput uValveDHW
    annotation (Placement(transformation(extent={{-192,28},{-168,52}})));
  simple_house.lib.HotWaterTap hotWaterTap
    annotation (Placement(transformation(extent={{-22,66},{4,92}})));
  Modelica.Blocks.Interfaces.RealInput uFlowDHW
    annotation (Placement(transformation(extent={{-192,78},{-168,102}})));
equation
  connect(theCon.port_b, vol.heatPort) annotation (Line(
      points={{220,40},{240,40},{240,-40}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(preHea.port, vol.heatPort) annotation (Line(
      points={{260,80},{240,80},{240,-40}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(heaCap.port, vol.heatPort) annotation (Line(
      points={{260,40},{240,40},{240,-40}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(timTab.y[1], preHea.Q_flow) annotation (Line(
      points={{299,80},{280,80}},
      color={0,0,127},
      smooth=Smooth.None));
  connect(temRoo.port, vol.heatPort) annotation (Line(
      points={{80,0},{240,0},{240,-40}},
      color={191,0,0},
      smooth=Smooth.None));

  connect(weaDat.weaBus, weaBus) annotation (Line(
      points={{80,40},{120,40}},
      color={255,204,51},
      thickness=0.5,
      smooth=Smooth.None), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaBus.TDryBul, TOut.T) annotation (Line(
      points={{120,40},{158,40}},
      color={255,204,51},
      thickness=0.5,
      smooth=Smooth.None), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(TOut.port, theCon.port_a) annotation (Line(
      points={{180,40},{200,40}},
      color={191,0,0},
      smooth=Smooth.None));

  connect(heaPum.port_b2, hole.ports[1]) annotation (Line(points={{-239.6,-136},
          {-240,-136},{-240,-180},{-260,-180}},
                                 color={0,127,255}));
  connect(mf_sou.ports[1], heaPum.port_a2) annotation (Line(points={{-296,-100},
          {-296,-80},{-240,-80},{-240,-104},{-239.6,-104}},
                                      color={0,127,255}));
  connect(temHex2HP.port_b, heaPum.port_a1) annotation (Line(points={{-200,-180},
          {-220,-180},{-220,-136},{-220.4,-136}}, color={0,127,255}));
  connect(heaPum.port_b1,temHP2Hex. port_a) annotation (Line(points={{-220.4,
          -104},{-220.4,-80},{-200,-80}}, color={0,127,255}));
  connect(temSla2Tan.port_b, pumSla.port_a) annotation (Line(points={{160,-80},
          {200,-80},{200,-180},{30,-180}}, color={0,127,255}));
  connect(pumHP.port_b,temHex2HP. port_a)
    annotation (Line(points={{-160,-180},{-180,-180}}, color={0,127,255}));
  connect(tanSH.portHex_b, pumHP.port_a) annotation (Line(points={{-60,-126.8},
          {-80,-126.8},{-80,-180},{-140,-180}},   color={0,127,255}));
  connect(expHP.port_a, pumHP.port_a) annotation (Line(points={{-100,-162},{
          -100,-180},{-140,-180}}, color={0,127,255}));
  connect(expRad.port_a, pumSla.port_a) annotation (Line(points={{220,-162},{
          220,-180},{30,-180}}, color={0,127,255}));
  connect(pumSla.port_b, tanSH.port_a) annotation (Line(points={{10,-180},{-70,
          -180},{-70,-114},{-60,-114}}, color={0,127,255}));
  connect(tanSH.port_b,temTan2Sla. port_a) annotation (Line(points={{-26,-114},
          {-10,-114},{-10,-80},{60,-80}}, color={0,127,255}));
  connect(gaiHP.y, heaPum.y) annotation (Line(points={{-192.8,-148},{-215.6,
          -148},{-215.6,-139.2}}, color={0,0,127}));
  connect(sunRad2.y,gaiSun2. u)
    annotation (Line(points={{140,80},{162.4,80}},   color={0,0,127}));
  connect(gaiSun2.y,sunHea2. Q_flow)
    annotation (Line(points={{180.8,80},{202,80}}, color={0,0,127}));
  connect(sunHea2.port, vol.heatPort) annotation (Line(points={{222,80},{240,80},
          {240,-40}},                 color={191,0,0}));
  connect(sunRad1.y,gaiSun1. u)
    annotation (Line(points={{140,120},{162.4,120}}, color={0,0,127}));
  connect(gaiSun1.y,sunHea1. Q_flow) annotation (Line(points={{180.8,120},{202,
          120}},                  color={0,0,127}));
  connect(sunHea1.port, vol.heatPort) annotation (Line(points={{222,120},{240,
          120},{240,-40}},            color={191,0,0}));
  connect(weaBus.TDryBul, mf_sou.T_in) annotation (Line(
      points={{120,40},{140,40},{140,20},{282,20},{282,-220},{-300,-220},{-300,
          -122}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-3,-6},{-3,-6}},
      horizontalAlignment=TextAlignment.Right));
  connect(uHP, pumHP.m_flow_in)
    annotation (Line(points={{-180,0},{-150,0},{-150,-168}}, color={0,0,127}));
  connect(uRSla, pumSla.m_flow_in)
    annotation (Line(points={{-20,-40},{20,-40},{20,-168}}, color={0,0,127}));
  connect(temHP2Hex.T, temHP) annotation (Line(points={{-190,-69},{-190,-40},{-220,
          -40}}, color={0,0,127}));
  connect(temRoo.T, temRoom)
    annotation (Line(points={{60,0},{20,0}}, color={0,0,127}));
  connect(uHP, gaiHP.u) annotation (Line(points={{-180,0},{-150,0},{-150,-148},
          {-174.4,-148}}, color={0,0,127}));
  connect(temTan2Sla.port_b, embPipe.port_a)
    annotation (Line(points={{80,-80},{102,-80}}, color={0,127,255}));
  connect(embPipe.port_b, temSla2Tan.port_a)
    annotation (Line(points={{122,-80},{140,-80}}, color={0,127,255}));
  connect(embPipe.heatPortEmb[1], thermalResistor.port_a)
    annotation (Line(points={{112,-70},{112,-50}}, color={191,0,0}));
  connect(thermalResistor.port_b, vol.heatPort) annotation (Line(points={{112,
          -30},{112,0},{240,0},{240,-40}}, color={191,0,0}));
  connect(temHP2Hex.port_b, valve.port_2)
    annotation (Line(points={{-180,-80},{-130,-80}}, color={0,127,255}));
  connect(valve.port_1, tanDHW.portHex_a) annotation (Line(points={{-110,-80},{
          -100,-80},{-100,40},{-70,40},{-70,39.92},{-60,39.92}}, color={0,127,
          255}));
  connect(valve.port_3, tanSH.portHex_a) annotation (Line(points={{-120,-90},{
          -120,-120},{-60,-120},{-60,-120.08}}, color={0,127,255}));
  connect(tanDHW.portHex_b, pumHP.port_a) annotation (Line(points={{-60,33.2},{
          -80,33.2},{-80,-180},{-140,-180}}, color={0,127,255}));
  connect(uValveDHW, valve.y) annotation (Line(points={{-180,40},{-120,40},{-120,
          -68}}, color={0,0,127}));
  connect(tanDHW.port_a, hotWaterTap.hot_in) annotation (Line(points={{-60,46},
          {-80,46},{-80,80.3},{-19.4,80.3}}, color={0,127,255}));
  connect(hotWaterTap.cold_out, tanDHW.port_b) annotation (Line(points={{0.1,
          68.6},{0.1,46},{-26,46}}, color={0,127,255}));
  connect(uFlowDHW, hotWaterTap.uFlowDHW) annotation (Line(points={{-180,90},{
          -18,90},{-18,89.4},{-17.84,89.4}}, color={0,0,127}));
  annotation (Documentation(info="<html>
<p>Example that simulates one room equipped with a radiant slab connected to a water storage tank supplied by a heat pump.</p>
<p>Two feedback controllers regulate the HP-Tank and Tank-Slab loops.</p>
</html>", revisions="<html>
<ul>
<li>April 2020, by Max Boegli:<br>Replaced the radiator by a radiant slab.</li>
<li>March 2020, by Max Boegli:<br>Adaptation of Heat pump, Tank storage and Radiator with basic building envelope.</li>
</ul>
</html>"),
    Diagram(coordinateSystem(preserveAspectRatio=false,extent={{-360,-240},{360,
            240}})),
    __Dymola_Commands(file=
     "modelica://Buildings/Resources/Scripts/Dymola/Fluid/HeatPumps/Examples/ScrollWaterToWater_OneRoomRadiator.mos"
        "Simulate and plot"),
    experiment(
      StopTime=172800,
      Tolerance=1e-08));
end HP_u_Tank_u_DHW_u_RSla_1RC_Sun;
