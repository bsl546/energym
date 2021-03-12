within modelica.simple_house.src;
model HP_u_Rad_1RC_Sun
  "Heat pump with Carnot HX connected to a simple room model with radiator"
  extends Modelica.Icons.Example;
  replaceable package MediumA =
      Buildings.Media.Air "Medium model for air";
  replaceable package MediumW =
      Buildings.Media.Water "Medium model for water";

  ////////////////////////////
  // Parameter Specification
  ////////////////////////////

  // Heat Pump
  parameter Real COP_nominal = 6
    "Nominal COP";
  parameter Modelica.SIunits.Power P_nominal = 10e3
    "Nominal compressor power (at y=1)";
  parameter Modelica.SIunits.TemperatureDifference dTEva_nominal = -10
    "Temperature difference evaporator outlet-inlet";
  parameter Modelica.SIunits.TemperatureDifference dTCon_nominal = 10
    "Temperature difference condenser outlet-inlet";
  parameter Modelica.SIunits.TemperatureDifference TCon_nominal = 273.15 + 30
    "Condenser Temperature used to compute COP_nominal";
  parameter Modelica.SIunits.TemperatureDifference TEva_nominal = 273.15 + 5
    "Evaporator Temperature used to compute COP_nominal";

  // Radiator
  parameter Modelica.SIunits.HeatFlowRate Q_flow_nominal = 20000
    "Nominal heat flow rate of radiator";
  parameter Modelica.SIunits.Temperature TRadSup_nominal = 273.15+50
    "Radiator nominal supply water temperature";
  parameter Modelica.SIunits.Temperature TRadRet_nominal = 273.15+45
    "Radiator nominal return water temperature";
  parameter Modelica.SIunits.MassFlowRate mHeaPum_flow_nominal = Q_flow_nominal/4200/5
    "Heat pump nominal mass flow rate";

  // Building envelope
  parameter Modelica.SIunits.ThermalConductance therm_cond_G = 500
    "Envelope Thermal Conductance (W/K)";  // G=20000/40
  parameter Modelica.SIunits.HeatCapacity heat_capa_C = 5e5
    "Envelope Heat Capacity (J/K)";  // C=2*180*1.2*1006
  parameter Modelica.SIunits.Volume room_vol_V=6*10*3
    "Room volume (m^3)";
  parameter Modelica.SIunits.MassFlowRate mA_flow_nominal = room_vol_V*6/3600
    "Air nominal mass flow rate (kg/s)";
  parameter Modelica.SIunits.HeatFlowRate QRooInt_flow = 1000
    "Internal heat gains of the room (W)";

  // Sun effect on tilted surface
  parameter Real tilt_C = 20 "Surface tilt (°C)";
  parameter Real azimuth_C = -45 "Surface azimuth (°C)";
  parameter Real latitude_C = 37.7 "Latitude (°C)";
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
    annotation (Placement(transformation(extent={{-20,30},{0,50}})));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor heaCap(C=heat_capa_C)
    "Heat capacity for furniture and walls"
    annotation (Placement(transformation(extent={{40,40},{60,60}})));
  Buildings.Fluid.HeatExchangers.Radiators.RadiatorEN442_2 rad(
    redeclare package Medium = MediumW,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    Q_flow_nominal=Q_flow_nominal,
    T_a_nominal=TRadSup_nominal,
    T_b_nominal=TRadRet_nominal,
    m_flow_nominal=mHeaPum_flow_nominal,
    T_start=TRadSup_nominal)     "Radiator"
    annotation (Placement(transformation(extent={{-20,-50},{-40,-30}})));
  Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor temRoo
    "Room temperature" annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        origin={-100,0})));

//---------------------------------------------------------------------------//

  Buildings.Fluid.HeatPumps.Carnot_y heaPum(
    redeclare package Medium1 = MediumW,
    redeclare package Medium2 = MediumW,
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
    annotation (Placement(transformation(extent={{-46,-146},{-14,-114}})));

//---------------------------------------------------------------------------//

  Buildings.Fluid.Movers.FlowControlled_m_flow pumHeaPum(
    redeclare package Medium = MediumW,
    m_flow_nominal=mHeaPum_flow_nominal,
    y_start=1,
    m_flow_start=0.85,
    T_start=TRadSup_nominal,
    nominalValuesDefineDefaultPressureCurve=true,
    use_inputFilter=false,
    energyDynamics=Modelica.Fluid.Types.Dynamics.SteadyState)
    "Pump for radiator side" annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        rotation=90,
        origin={-80,-70})));
//---------------------------------------------------------------------------//

  Buildings.Fluid.Sensors.TemperatureTwoPort temSup(
    redeclare package Medium = MediumW,
    m_flow_nominal=mHeaPum_flow_nominal,
    T_start=TRadSup_nominal)  "Supply water temperature"
      annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        rotation=0,
        origin={0,-40})));

  Buildings.Fluid.Sensors.TemperatureTwoPort temRet(
    redeclare package Medium = MediumW,
    m_flow_nominal=mHeaPum_flow_nominal,
    T_start=TRadSup_nominal)  "Return water temperature"
      annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        rotation=0,
        origin={-60,-40})));

//---------------------------------------------------------------------------//

  Modelica.Blocks.Math.Gain gaiHP(k=1) "Gain for Heat Pump"
    annotation (Placement(transformation(extent={{-106,-108},{-90,-92}})));

//---------------------------------------------------------------------------//

  Buildings.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(
        filNam=weafile) "Weather data reader"
    annotation (Placement(transformation(extent={{-200,30},{-180,50}})));
  Buildings.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
    annotation (Placement(transformation(extent={{-140,30},{-120,50}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature TOut
    "Outside temperature"
    annotation (Placement(transformation(extent={{-60,30},{-40,50}})));

//---------------------------------------------------------------------------//

  Buildings.Fluid.Storage.ExpansionVessel exp(redeclare package Medium =
        MediumW)
    annotation (Placement(transformation(extent={{30,-110},{50,-90}})));
  Buildings.Fluid.Sources.Boundary_pT hole(redeclare package Medium = MediumW,
      nPorts=1) annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=90,
        origin={-80,-180})));
  Buildings.Fluid.Sources.MassFlowSource_T mf_sou(
    redeclare package Medium = MediumW,
    m_flow=mHeaPum_flow_nominal,
    use_T_in=true,
    nPorts=1) annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=90,
        origin={20,-170})));
  Modelica.Blocks.Sources.Constant gnd_temp(k=10 + 273.15)
    annotation (Placement(transformation(extent={{-20,-210},{0,-190}})));

//---------------------------------------------------------------------------//

  Modelica.Blocks.Interfaces.RealInput u
    annotation (Placement(transformation(extent={{-172,-82},{-148,-58}})));
  Modelica.Blocks.Interfaces.RealOutput y
    annotation (Placement(transformation(extent={{-150,-10},{-170,10}})));
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
    annotation (Placement(transformation(extent={{-140,66},{-120,86}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow sunHea
    "Solar heat flow"
    annotation (Placement(transformation(extent={{-18,70},{2,90}})));
  Modelica.Blocks.Math.Gain gaiSun(k=sun_heat_gain)
    "Heat gain from solar irradiance"
    annotation (Placement(transformation(extent={{-80,72},{-64,88}})));
equation
  connect(theCon.port_b, vol.heatPort) annotation (Line(
      points={{0,40},{20,40},{20,0},{40,0}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(heaCap.port, vol.heatPort) annotation (Line(
      points={{50,40},{20,40},{20,0},{40,0}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(temRoo.port, vol.heatPort) annotation (Line(
      points={{-90,0},{40,0}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(rad.heatPortCon, vol.heatPort) annotation (Line(
      points={{-28,-32.8},{-28,0},{40,0}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(rad.heatPortRad, vol.heatPort) annotation (Line(
      points={{-32,-32.8},{-32,0},{40,0}},
      color={191,0,0},
      smooth=Smooth.None));

  connect(weaDat.weaBus, weaBus) annotation (Line(
      points={{-180,40},{-130,40}},
      color={255,204,51},
      thickness=0.5,
      smooth=Smooth.None), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaBus.TDryBul, TOut.T) annotation (Line(
      points={{-130,40},{-62,40}},
      color={255,204,51},
      thickness=0.5,
      smooth=Smooth.None), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(TOut.port, theCon.port_a) annotation (Line(
      points={{-40,40},{-20,40}},
      color={191,0,0},
      smooth=Smooth.None));

  connect(gaiHP.y, heaPum.y) annotation (Line(points={{-89.2,-100},{-60,-100},{
          -60,-115.6},{-49.2,-115.6}},              color={0,0,127}));
  connect(heaPum.port_b2, hole.ports[1]) annotation (Line(points={{-46,-139.6},
          {-80,-139.6},{-80,-170}},
                                 color={0,127,255}));
  connect(mf_sou.ports[1], heaPum.port_a2) annotation (Line(points={{20,-160},{
          20,-139.6},{-14,-139.6}},   color={0,127,255}));
  connect(gnd_temp.y, mf_sou.T_in) annotation (Line(points={{1,-200},{16,-200},
          {16,-182}},        color={0,0,127}));
  connect(heaPum.port_b1, temSup.port_a) annotation (Line(points={{-14,-120.4},
          {20,-120.4},{20,-40},{10,-40}},color={0,127,255}));
  connect(temSup.port_b, rad.port_a)
    annotation (Line(points={{-10,-40},{-20,-40}},
                                                color={0,127,255}));
  connect(rad.port_b, temRet.port_a)
    annotation (Line(points={{-40,-40},{-50,-40}}, color={0,127,255}));
  connect(temRet.port_b, pumHeaPum.port_a) annotation (Line(points={{-70,-40},{
          -80,-40},{-80,-60}}, color={0,127,255}));
  connect(pumHeaPum.port_b, heaPum.port_a1) annotation (Line(points={{-80,-80},
          {-80,-120},{-46,-120},{-46,-120.4}}, color={0,127,255}));
  connect(heaPum.port_b1, exp.port_a) annotation (Line(points={{-14,-120.4},{20,
          -120.4},{20,-120},{40,-120},{40,-110}},color={0,127,255}));
  connect(u, pumHeaPum.m_flow_in)
    annotation (Line(points={{-160,-70},{-92,-70}}, color={0,0,127}));
  connect(u, gaiHP.u) annotation (Line(points={{-160,-70},{-120,-70},{-120,-100},
          {-107.6,-100}},
                        color={0,0,127}));
  connect(temRoo.T, y)
    annotation (Line(points={{-110,0},{-160,0}},  color={0,0,127}));
  connect(timTab.y[1],preHea. Q_flow) annotation (Line(
      points={{79,80},{58,80}},
      color={0,0,127},
      smooth=Smooth.None));
  connect(sunRad.y,gaiSun. u)
    annotation (Line(points={{-120,80},{-81.6,80}}, color={0,0,127}));
  connect(gaiSun.y,sunHea. Q_flow)
    annotation (Line(points={{-63.2,80},{-18,80}}, color={0,0,127}));
  connect(sunHea.port, vol.heatPort)
    annotation (Line(points={{2,80},{20,80},{20,0},{40,0}}, color={191,0,0}));
  connect(preHea.port, vol.heatPort)
    annotation (Line(points={{38,80},{20,80},{20,0},{40,0}}, color={191,0,0}));
  annotation (Documentation(info="<html>
<p>Example that simulates one room equipped with a radiator. Hot water is produced by a <i>24</i> kW nominal capacity heat pump. The source side water temperature to the heat pump is constant at <i>10</i>&deg;C.</p>
<p>The heat pump is activated with an external controller connected to the input u.</p>
</html>", revisions="<html>
<ul>
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
end HP_u_Rad_1RC_Sun;
