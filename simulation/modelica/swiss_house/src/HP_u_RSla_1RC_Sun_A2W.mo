within modelica.swiss_house.src;
model HP_u_RSla_1RC_Sun_A2W
  "Heat pump with Carnot HX connected to a simple room model with floor heating"
  extends Modelica.Icons.Example;
  replaceable package MediumA =
      Buildings.Media.Air "Medium model for air";
  replaceable package MediumW =
      Buildings.Media.Water "Medium model for water";

  ////////////////////////////
  // Parameter Specification
  ////////////////////////////

  // Heat Pump
  parameter Real COP_nominal = 3
    "Nominal COP";
  parameter Modelica.SIunits.Power P_nominal = 1000
    "Nominal compressor power (at y=1)";
  parameter Modelica.SIunits.HeatFlowRate Q_flow_nominal = 3000
    "Nominal heat flow rate of radiator";
  parameter Modelica.SIunits.MassFlowRate mHeaPum_flow_nominal = Q_flow_nominal/4200/5
    "Heat pump nominal mass flow rate";
  parameter Modelica.SIunits.TemperatureDifference dTEva_nominal = -10
    "Temperature difference evaporator outlet-inlet";
  parameter Modelica.SIunits.TemperatureDifference dTCon_nominal = 10
    "Temperature difference condenser outlet-inlet";
  parameter Modelica.SIunits.TemperatureDifference TCon_nominal = 273.15 + 30
    "Condenser Temperature used to compute COP_nominal";
  parameter Modelica.SIunits.TemperatureDifference TEva_nominal = 273.15 + 5
    "Evaporator Temperature used to compute COP_nominal";

  // Floor heating radiant slab
  parameter Modelica.SIunits.Area slab_surf = 200
    "Surface area of radiant slab (m^2)";

  // Building envelope
  parameter Modelica.SIunits.ThermalConductance therm_cond_G = 100
    "Envelope Thermal Conductance (W/K)";  // G=Qheat/max(Tin-Tout)
  parameter Modelica.SIunits.HeatCapacity heat_capa_C = 40e6
    "Envelope Heat Capacity (J/K)";  // C=0.2 MJ/m2K
  parameter Modelica.SIunits.Volume room_vol_V = 750
    "Room volume (m^3)";
  parameter Modelica.SIunits.MassFlowRate mA_flow_nominal = room_vol_V*6/3600
    "Air nominal mass flow rate (kg/s)";
  parameter Modelica.SIunits.HeatFlowRate QRooInt_flow = 0.0
    "Internal heat gains of the room (W)";

  // Sun effect on tilted surface
  parameter Real tilt_C = 90 "Surface tilt (°C)";
  parameter Real azimuth_C = 0 "Surface azimuth (°C)";
  parameter Real latitude_C = 47.14 "Latitude (°C)";
  parameter Real sun_heat_gain = 2.5 "Sun heat gain";

  // Weather data
  parameter String weafile = Modelica.Utilities.Files.loadResource(
        "modelica://modelica/simple_house/wf/Switzerland_CHE_Maur.mos")
    "Name of weather data file";

//===========================================================================//

  Buildings.Fluid.MixingVolumes.MixingVolume vol(
    redeclare package Medium = MediumA,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    m_flow_nominal=mA_flow_nominal,
    V=room_vol_V)
    annotation (Placement(transformation(extent={{40,-10},{60,10}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor theCon(G=therm_cond_G)
    "Thermal conductance with the ambient"
    annotation (Placement(transformation(extent={{-20,10},{0,30}})));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor heaCap(C=heat_capa_C)
    "Heat capacity for furniture and walls"
    annotation (Placement(transformation(extent={{40,20},{60,40}})));
  Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor temRoo
    "Room temperature" annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        origin={-100,0})));

//---------------------------------------------------------------------------//

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
    annotation (Placement(transformation(extent={{-46,-156},{-14,-124}})));

//---------------------------------------------------------------------------//

  Buildings.Fluid.Movers.FlowControlled_m_flow pumHeaPum(
    redeclare package Medium = MediumW,
    m_flow_nominal=mHeaPum_flow_nominal,
    y_start=1,
    m_flow_start=0.85,
    T_start=TCon_nominal,
    nominalValuesDefineDefaultPressureCurve=true,
    use_inputFilter=false,
    energyDynamics=Modelica.Fluid.Types.Dynamics.SteadyState)
    "Pump for radiator side" annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        rotation=90,
        origin={-80,-80})));
//---------------------------------------------------------------------------//

  Buildings.Fluid.Sensors.TemperatureTwoPort temSup(
    redeclare package Medium = MediumW,
    m_flow_nominal=mHeaPum_flow_nominal,
    T_start=TCon_nominal)  "Supply water temperature"
      annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        rotation=0,
        origin={0,-50})));

  Buildings.Fluid.Sensors.TemperatureTwoPort temRet(
    redeclare package Medium = MediumW,
    m_flow_nominal=mHeaPum_flow_nominal,
    T_start=TCon_nominal)  "Return water temperature"
      annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        rotation=0,
        origin={-60,-50})));

//---------------------------------------------------------------------------//

  Modelica.Blocks.Math.Gain gaiHP(k=1) "Gain for Heat Pump"
    annotation (Placement(transformation(extent={{-106,-118},{-90,-102}})));

//---------------------------------------------------------------------------//

  Buildings.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(
        filNam=weafile) "Weather data reader"
    annotation (Placement(transformation(extent={{-200,40},{-180,60}})));
  Buildings.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
    annotation (Placement(transformation(extent={{-140,40},{-120,60}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature TOut
    "Outside temperature"
    annotation (Placement(transformation(extent={{-60,10},{-40,30}})));

//---------------------------------------------------------------------------//

  Buildings.Fluid.Storage.ExpansionVessel exp(redeclare package Medium =
        MediumW)
    annotation (Placement(transformation(extent={{30,-120},{50,-100}})));
  Buildings.Fluid.Sources.Boundary_pT hole(redeclare package Medium = MediumA,
      nPorts=1) annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=90,
        origin={-80,-180})));
  Buildings.Fluid.Sources.MassFlowSource_T mf_sou(
    redeclare package Medium = MediumA,
    m_flow=mHeaPum_flow_nominal,
    use_T_in=true,
    nPorts=1) annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=180,
        origin={30,-156})));

//---------------------------------------------------------------------------//

  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHea
    "Prescribed heat flow"
    annotation (Placement(transformation(extent={{58,70},{38,90}})));
  Modelica.Blocks.Sources.CombiTimeTable timTab(
    extrapolation=Modelica.Blocks.Types.Extrapolation.Periodic,
    smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
    table=[-6*3600,0; 8*3600,QRooInt_flow; 18*3600,0])
                          "Time table for internal heat gain"
    annotation (Placement(transformation(extent={{100,70},{80,90}})));
  simple_house.lib.SunRad_TiltSurf sunRad(
    weafile=weafile,
    tilt_C=tilt_C,
    azimuth_C=azimuth_C,
    latitude_C=latitude_C)
    "Solar irradiance on tilted surface"
    annotation (Placement(transformation(extent={{-100,66},{-80,86}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow sunHea
    "Solar heat flow"
    annotation (Placement(transformation(extent={{-18,70},{2,90}})));
  Modelica.Blocks.Math.Gain gaiSun(k=sun_heat_gain)
    "Heat gain from solar irradiance"
    annotation (Placement(transformation(extent={{-58,72},{-42,88}})));
  IDEAS.Fluid.HeatExchangers.RadiantSlab.EmbeddedPipe sla(
    redeclare package Medium = MediumW,
    redeclare
      IDEAS.Fluid.HeatExchangers.RadiantSlab.BaseClasses.FH_ValidationEmpa4_6
      RadSlaCha,
    m_flow_nominal=mHeaPum_flow_nominal,
    A_floor=slab_surf,
    nParCir=10,
    computeFlowResistance=true,
    m_flowMin=mHeaPum_flow_nominal/5,
    nDiscr=1,
    R_c=0.05,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial) "Radiant slab"
    annotation (Placement(transformation(extent={{-20,-60},{-40,-40}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalResistor theSla(R=sla.R_c/sla.A_floor
        *sla.nDiscr) "Thermal conductance of the radiant slab" annotation (
      Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=0,
        origin={-10,-20})));
  Modelica.Blocks.Interfaces.RealOutput y
    annotation (Placement(transformation(extent={{-150,-10},{-170,10}})));
  Modelica.Blocks.Interfaces.RealInput u
    annotation (Placement(transformation(extent={{-172,-92},{-148,-68}})));
equation
  connect(theCon.port_b, vol.heatPort) annotation (Line(
      points={{0,20},{20,20},{20,0},{40,0}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(heaCap.port, vol.heatPort) annotation (Line(
      points={{50,20},{20,20},{20,0},{40,0}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(temRoo.port, vol.heatPort) annotation (Line(
      points={{-90,0},{40,0}},
      color={191,0,0},
      smooth=Smooth.None));

  connect(weaDat.weaBus, weaBus) annotation (Line(
      points={{-180,50},{-130,50}},
      color={255,204,51},
      thickness=0.5,
      smooth=Smooth.None), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaBus.TDryBul, TOut.T) annotation (Line(
      points={{-130,50},{-80,50},{-80,20},{-62,20}},
      color={255,204,51},
      thickness=0.5,
      smooth=Smooth.None), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(TOut.port, theCon.port_a) annotation (Line(
      points={{-40,20},{-20,20}},
      color={191,0,0},
      smooth=Smooth.None));

  connect(gaiHP.y, heaPum.y) annotation (Line(points={{-89.2,-110},{-60,-110},{
          -60,-125.6},{-49.2,-125.6}},              color={0,0,127}));
  connect(heaPum.port_b2, hole.ports[1]) annotation (Line(points={{-46,-149.6},
          {-80,-149.6},{-80,-170}},
                                 color={0,127,255}));
  connect(mf_sou.ports[1], heaPum.port_a2) annotation (Line(points={{20,-156},{
          20,-149.6},{-14,-149.6}},   color={0,127,255}));
  connect(heaPum.port_b1, temSup.port_a) annotation (Line(points={{-14,-130.4},
          {20,-130.4},{20,-50},{10,-50}},color={0,127,255}));
  connect(temRet.port_b, pumHeaPum.port_a) annotation (Line(points={{-70,-50},{
          -80,-50},{-80,-70}}, color={0,127,255}));
  connect(pumHeaPum.port_b, heaPum.port_a1) annotation (Line(points={{-80,-90},
          {-80,-130},{-46,-130},{-46,-130.4}}, color={0,127,255}));
  connect(heaPum.port_b1, exp.port_a) annotation (Line(points={{-14,-130.4},{20,
          -130.4},{20,-130},{40,-130},{40,-120}},color={0,127,255}));
  connect(timTab.y[1],preHea. Q_flow) annotation (Line(
      points={{79,80},{58,80}},
      color={0,0,127},
      smooth=Smooth.None));
  connect(sunRad.y,gaiSun. u)
    annotation (Line(points={{-80,80},{-59.6,80}},  color={0,0,127}));
  connect(gaiSun.y,sunHea. Q_flow)
    annotation (Line(points={{-41.2,80},{-18,80}}, color={0,0,127}));
  connect(sunHea.port, vol.heatPort)
    annotation (Line(points={{2,80},{20,80},{20,0},{40,0}}, color={191,0,0}));
  connect(preHea.port, vol.heatPort)
    annotation (Line(points={{38,80},{20,80},{20,0},{40,0}}, color={191,0,0}));
  connect(temSup.port_b, sla.port_a)
    annotation (Line(points={{-10,-50},{-20,-50}}, color={0,127,255}));
  connect(sla.port_b, temRet.port_a)
    annotation (Line(points={{-40,-50},{-50,-50}}, color={0,127,255}));
  connect(sla.heatPortEmb[1], theSla.port_a)
    annotation (Line(points={{-30,-40},{-30,-20},{-20,-20}}, color={191,0,0}));
  connect(theSla.port_b, vol.heatPort) annotation (Line(points={{0,-20},{20,-20},
          {20,0},{40,0}},      color={191,0,0}));
  connect(temRoo.T, y)
    annotation (Line(points={{-110,0},{-160,0}}, color={0,0,127}));
  connect(u, gaiHP.u)
    annotation (Line(points={{-160,-80},{-120,-80},{-120,-110},{-107.6,-110}},
                                                         color={0,0,127}));
  connect(u, pumHeaPum.m_flow_in)
    annotation (Line(points={{-160,-80},{-92,-80}}, color={0,0,127}));
  connect(weaBus.TDryBul, mf_sou.T_in) annotation (Line(
      points={{-130,50},{80,50},{80,-160},{42,-160}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{6,3},{6,3}},
      horizontalAlignment=TextAlignment.Left));
  annotation (Documentation(info="<html>
<p>Example that simulates one room equipped with a air-to-water heat pump.</p>
<p>The heat pump is activated via an external controller.</p>
</html>", revisions="<html>
<ul>
<li>April 2020, by Max Boegli:<br>Replaced the radiator by a radiant slab.</li>
<li>March 2020, by Max Boegli:<br>Replaced the feedback controller by an input u for external activation.</li>
<li>Sometime in 2019, by Max Boegli:<br>Replaced the hysteresis loop by a PI controller.</li>
<li>March 3, 2017, by Michael Wetter:<br>Changed mass flow test to use a hysteresis as a threshold test can cause chattering. </li>
<li>January 27, 2017, by Massimo Cimmino:<br>First implementation. </li>
</ul>
</html>"),
    Diagram(coordinateSystem(preserveAspectRatio=false,extent={{-240,-220},{100,
            100}})),
    __Dymola_Commands(file=
     "modelica://Buildings/Resources/Scripts/Dymola/Fluid/HeatPumps/Examples/ScrollWaterToWater_OneRoomRadiator.mos"
        "Simulate and plot"),
    experiment(
      StopTime=172800,
      Tolerance=1e-08));
end HP_u_RSla_1RC_Sun_A2W;
