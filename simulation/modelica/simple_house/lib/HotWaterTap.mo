within modelica.simple_house.lib;
model HotWaterTap

   replaceable package medium =
      Buildings.Media.Water (T_min=250, T_max=500) "Medium in the component";

   parameter Real hw_cold_temp_c = 10;
  Buildings.Fluid.Sources.MassFlowSource_T HWflow(
    m_flow=0.001,
    use_m_flow_in=true,
    redeclare package Medium = medium,
    use_T_in=true,
    T=288.15,
    nPorts=1) "Inlet and flow rate for hot water draw" annotation (Placement(
        transformation(
        extent={{9,-9},{-9,9}},
        origin={69,9},
        rotation=90)));
   parameter Real table[:, :] = fill(0.0, 0, 2) "Flow scedule litres/s/person";
   parameter Real number_of_people = 4 "Number of people using hot water";

  Buildings.Fluid.Sensors.TemperatureTwoPort tem_out(
    T_start(displayUnit="K"),
    redeclare package Medium = medium,
    m_flow_nominal=0.1) "Temperature sensor" annotation (Placement(
        transformation(
        extent={{8,8},{-8,-8}},
        rotation=90,
        origin={70,-40})));
  Buildings.Fluid.Sources.Boundary_pT HWsink(
    redeclare package Medium = Buildings.Media.Water (T_min=250, T_max=500),
    use_T_in=false,
    nPorts=1) "Outlet for hot water draw" annotation (Placement(transformation(
        extent={{8,-8},{-8,8}},
        rotation=0,
        origin={0,10})));

  Modelica.Fluid.Interfaces.FluidPort_a hot_in(redeclare package Medium =
        medium) annotation (Placement(transformation(extent={{-90,0},{-70,20}}),
        iconTransformation(extent={{-90,0},{-70,20}})));
  Modelica.Fluid.Interfaces.FluidPort_b cold_out(redeclare package Medium =
        medium) annotation (Placement(transformation(extent={{60,-90},{80,-70}}),
        iconTransformation(extent={{60,-90},{80,-70}})));
  Buildings.Fluid.Sensors.TemperatureTwoPort tem_in(
    T_start(displayUnit="K"),
    redeclare package Medium = medium,
    m_flow_nominal=0.1) "Temperature sensor" annotation (Placement(
        transformation(
        extent={{8,8},{-8,-8}},
        rotation=180,
        origin={-40,10})));
  Modelica.Blocks.Sources.Constant Tcold(k=273.15 + hw_cold_temp_c) annotation (
     Placement(transformation(
        extent={{-8,-8},{8,8}},
        rotation=0,
        origin={32,80})));
  Modelica.Blocks.Interfaces.RealInput uFlowDHW annotation (Placement(
        transformation(extent={{-80,68},{-56,92}}), iconTransformation(extent={{-80,68},
            {-56,92}})));
equation
  connect(Tcold.y, HWflow.T_in) annotation (Line(points={{40.8,80},{66,80},{66,
          19.8},{65.4,19.8}},      color={0,0,127}));
  connect(uFlowDHW, HWflow.m_flow_in) annotation (Line(points={{-68,80},{0,80},
          {0,60},{61.8,60},{61.8,19.8}},     color={0,0,127}));
  connect(hot_in, tem_in.port_a)
    annotation (Line(points={{-80,10},{-48,10}},        color={0,127,255}));
  connect(tem_in.port_b, HWsink.ports[1])
    annotation (Line(points={{-32,10},{-8,10}},           color={0,127,255}));
  connect(HWflow.ports[1], tem_out.port_a)
    annotation (Line(points={{69,3.55271e-15},{70,3.55271e-15},{70,-32}},
                                                           color={0,127,255}));
  connect(tem_out.port_b, cold_out) annotation (Line(points={{70,-48},{70,-80}},
                      color={0,127,255}));
  annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
          Polygon(
          points={{78,-56},{54,-56},{56,-14},{52,-10},{38,-10},{24,-12},{14,-8},
              {-2,-12},{-22,-10},{-38,-10},{-50,-16},{-60,-14},{-60,36},{-46,34},
              {-34,30},{-26,30},{-20,32},{-16,38},{-16,40},{-16,44},{-18,46},{
              -16,48},{-14,50},{-12,56},{-10,62},{-8,66},{-8,74},{-32,76},{-34,
              80},{-28,90},{-14,88},{-4,86},{18,84},{30,84},{36,86},{46,84},{56,
              80},{52,78},{50,76},{42,74},{32,74},{14,74},{12,74},{14,70},{12,
              64},{14,60},{14,54},{18,44},{20,32},{36,26},{52,26},{60,24},{70,
              20},{78,12},{84,-2},{86,-20},{86,-38},{86,-48},{86,-56},{78,-56}},
          lineColor={238,46,47},
          fillColor={175,175,175},
          fillPattern=FillPattern.Solid)}), Diagram(coordinateSystem(
          preserveAspectRatio=false), graphics={
                                               Text(
          extent={{-148,136},{152,96}},
          textString="%name",
          lineColor={0,0,255})}));
end HotWaterTap;
