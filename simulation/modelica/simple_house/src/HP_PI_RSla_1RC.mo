within modelica.simple_house.src;
model HP_PI_RSla_1RC
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
  parameter Real COP_nominal = 6
    "Nominal COP";
  parameter Modelica.SIunits.Power P_nominal = 10e3
    "Nominal compressor power (at y=1)";
  parameter Modelica.SIunits.HeatFlowRate Q_flow_nominal = 20e3
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
  parameter Modelica.SIunits.Area slab_surf = 100
    "Surface area of radiant slab (m^2)";

  // Building envelope
  parameter Modelica.SIunits.ThermalConductance therm_cond_G = 500
    "Envelope Thermal Conductance (W/K)";  // G=20000/40
  parameter Modelica.SIunits.HeatCapacity heat_capa_C = 5e5
    "Envelope Heat Capacity (J/K)";  // C=2*180*1.2*1006
  parameter Modelica.SIunits.Volume room_vol_V = 6*10*3
    "Room volume (m^3)";
  parameter Modelica.SIunits.MassFlowRate mA_flow_nominal = room_vol_V*6/3600
    "Air nominal mass flow rate (kg/s)";
  parameter Modelica.SIunits.HeatFlowRate QRooInt_flow = 4000
    "Internal heat gains of the room (W)";

//===========================================================================//

  Buildings.Fluid.MixingVolumes.MixingVolume vol(
    redeclare package Medium = MediumA,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    m_flow_nominal=mA_flow_nominal,
    V=room_vol_V)
    annotation (Placement(transformation(extent={{60,10},{80,30}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor theCon(G=therm_cond_G)
    "Thermal conductance with the ambient"
    annotation (Placement(transformation(extent={{20,40},{40,60}})));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor heaCap(C=heat_capa_C)
    "Heat capacity for furniture and walls"
    annotation (Placement(transformation(extent={{60,50},{80,70}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHea
    "Prescribed heat flow"
    annotation (Placement(transformation(extent={{20,70},{40,90}})));
  Modelica.Blocks.Sources.CombiTimeTable timTab(
      extrapolation=Modelica.Blocks.Types.Extrapolation.Periodic,
      smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
      table=[-6*3600, 0;
              8*3600, QRooInt_flow;
             18*3600, 0]) "Time table for internal heat gain"
    annotation (Placement(transformation(extent={{-20,70},{0,90}})));
  Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor temRoo
    "Room temperature" annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        origin={-80,20})));

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
    annotation (Placement(transformation(extent={{-26,-146},{6,-114}})));

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
        origin={-60,-70})));
//---------------------------------------------------------------------------//

  Buildings.Fluid.Sensors.TemperatureTwoPort temSup(
    redeclare package Medium = MediumW,
    m_flow_nominal=mHeaPum_flow_nominal,
    T_start=TCon_nominal)  "Supply water temperature"
      annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        rotation=0,
        origin={20,-30})));

  Buildings.Fluid.Sensors.TemperatureTwoPort temRet(
    redeclare package Medium = MediumW,
    m_flow_nominal=mHeaPum_flow_nominal,
    T_start=TCon_nominal)  "Return water temperature"
      annotation (Placement(transformation(
        extent={{10,-10},{-10,10}},
        rotation=0,
        origin={-40,-30})));

//---------------------------------------------------------------------------//

  Buildings.Controls.Continuous.LimPID conPID(
    controllerType=Modelica.Blocks.Types.SimpleController.PI,
    initType=Modelica.Blocks.Types.InitPID.InitialState,
    Ti=300,
    Td=60,
    k=0.1)
    annotation (Placement(transformation(extent={{-140,-80},{-120,-60}})));
  Buildings.ThermalZones.Detailed.Validation.BESTEST.BaseClasses.DaySchedule TSetHea(table=[
        0.0,273.15 + 20]) "Heating setpoint"
    annotation (Placement(transformation(extent={{-180,-80},{-160,-60}})));
  Modelica.Blocks.Math.Gain gaiHP(k=1) "Gain for Heat Pump"
    annotation (Placement(transformation(extent={{-86,-108},{-70,-92}})));

//---------------------------------------------------------------------------//

  Buildings.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(filNam=
        Modelica.Utilities.Files.loadResource(
        "modelica://modelica/simple_house/wf/Switzerland_CHE_Maur.mos"))
    "Weather data reader"
    annotation (Placement(transformation(extent={{-200,40},{-180,60}})));
  Buildings.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
    annotation (Placement(transformation(extent={{-140,40},{-120,60}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature TOut
    "Outside temperature"
    annotation (Placement(transformation(extent={{-20,40},{0,60}})));

//---------------------------------------------------------------------------//

  Buildings.Fluid.Storage.ExpansionVessel exp(redeclare package Medium =
        MediumW)
    annotation (Placement(transformation(extent={{50,-110},{70,-90}})));
  Buildings.Fluid.Sources.Boundary_pT hole(redeclare package Medium = MediumW,
      nPorts=1) annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=90,
        origin={-60,-180})));
  Buildings.Fluid.Sources.MassFlowSource_T mf_sou(
    redeclare package Medium = MediumW,
    m_flow=mHeaPum_flow_nominal,
    use_T_in=true,
    nPorts=1) annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=90,
        origin={40,-170})));
  Modelica.Blocks.Sources.Constant gnd_temp(k=10 + 273.15)
    annotation (Placement(transformation(extent={{0,-210},{20,-190}})));

//---------------------------------------------------------------------------//

  Modelica.Thermal.HeatTransfer.Components.ThermalResistor theSla(R=sla.R_c/sla.A_floor
        *sla.nDiscr) "Thermal conductance of the radiant slab" annotation (
      Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=0,
        origin={20,0})));
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
    annotation (Placement(transformation(extent={{0,-40},{-20,-20}})));
equation
  connect(theCon.port_b, vol.heatPort) annotation (Line(
      points={{40,50},{50,50},{50,20},{60,20}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(preHea.port, vol.heatPort) annotation (Line(
      points={{40,80},{50,80},{50,20},{60,20}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(heaCap.port, vol.heatPort) annotation (Line(
      points={{70,50},{50,50},{50,20},{60,20}},
      color={191,0,0},
      smooth=Smooth.None));
  connect(timTab.y[1], preHea.Q_flow) annotation (Line(
      points={{1,80},{20,80}},
      color={0,0,127},
      smooth=Smooth.None));
  connect(temRoo.port, vol.heatPort) annotation (Line(
      points={{-70,20},{60,20}},
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
      points={{-130,50},{-22,50}},
      color={255,204,51},
      thickness=0.5,
      smooth=Smooth.None), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(TOut.port, theCon.port_a) annotation (Line(
      points={{0,50},{20,50}},
      color={191,0,0},
      smooth=Smooth.None));

  connect(temRoo.T, conPID.u_m) annotation (Line(points={{-90,20},{-200,20},{
          -200,-100},{-130,-100},{-130,-82}},
                                            color={0,0,127}));
  connect(conPID.y, pumHeaPum.m_flow_in) annotation (Line(points={{-119,-70},{
          -72,-70}},                       color={0,0,127}));
  connect(TSetHea.y[1], conPID.u_s)
    annotation (Line(points={{-158,-70},{-142,-70}}, color={0,0,127}));
  connect(conPID.y, gaiHP.u)
    annotation (Line(points={{-119,-70},{-100,-70},{-100,-100},{-87.6,-100}},
                                                     color={0,0,127}));
  connect(gaiHP.y, heaPum.y) annotation (Line(points={{-69.2,-100},{-40,-100},{
          -40,-115.6},{-29.2,-115.6}},              color={0,0,127}));
  connect(heaPum.port_b2, hole.ports[1]) annotation (Line(points={{-26,-139.6},
          {-60,-139.6},{-60,-170}},
                                 color={0,127,255}));
  connect(mf_sou.ports[1], heaPum.port_a2) annotation (Line(points={{40,-160},{
          40,-139.6},{6,-139.6}},     color={0,127,255}));
  connect(gnd_temp.y, mf_sou.T_in) annotation (Line(points={{21,-200},{36,-200},
          {36,-182}},        color={0,0,127}));
  connect(heaPum.port_b1, temSup.port_a) annotation (Line(points={{6,-120.4},{
          40,-120.4},{40,-30},{30,-30}}, color={0,127,255}));
  connect(temRet.port_b, pumHeaPum.port_a) annotation (Line(points={{-50,-30},{
          -60,-30},{-60,-60}}, color={0,127,255}));
  connect(pumHeaPum.port_b, heaPum.port_a1) annotation (Line(points={{-60,-80},
          {-60,-120},{-26,-120},{-26,-120.4}}, color={0,127,255}));
  connect(heaPum.port_b1, exp.port_a) annotation (Line(points={{6,-120.4},{40,
          -120.4},{40,-120},{60,-120},{60,-110}},color={0,127,255}));
  connect(temSup.port_b, sla.port_a)
    annotation (Line(points={{10,-30},{0,-30}}, color={0,127,255}));
  connect(sla.port_b, temRet.port_a)
    annotation (Line(points={{-20,-30},{-30,-30}}, color={0,127,255}));
  connect(sla.heatPortEmb[1], theSla.port_a)
    annotation (Line(points={{-10,-20},{-10,0},{10,0}}, color={191,0,0}));
  connect(theSla.port_b, vol.heatPort)
    annotation (Line(points={{30,0},{50,0},{50,20},{60,20}}, color={191,0,0}));
  annotation (Documentation(info="<html>
<p>Example that simulates one room equipped with a radiator. Hot water is produced by a <i>24</i> kW nominal capacity heat pump. The source side water temperature to the heat pump is constant at <i>10</i>&deg;C.</p>
<p>The heat pump is activated through a PI controller to regulate the room temperature around 20&deg;C.</p>
</html>", revisions="<html>
<ul>
<li>April 2020, by Max Boegli:<br>Replaced the radiator by a radiant slab.</li>
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
end HP_PI_RSla_1RC;
