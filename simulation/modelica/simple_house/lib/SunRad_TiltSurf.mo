within modelica.simple_house.lib;
model SunRad_TiltSurf "Solar irradiance on tilted surface"
  extends Modelica.Blocks.Icons.PartialBooleanBlock;

  ////////////////////////////
  // Parameter Specification
  ////////////////////////////

  // PV orientation
  parameter Real tilt_C = 20 "Surface tilt (°C)";
  parameter Real azimuth_C = -45 "Surface azimuth (°C)";
  parameter Real latitude_C = 37.7 "Latitude (°C)";

  constant Real d2r = Modelica.Constants.pi/180 "Conversion degree to radian";

  parameter String weafile = ""
    "Name of weather data file";

  //===========================================================================

  Buildings.BoundaryConditions.SolarIrradiation.DiffusePerez HDifTil(
    til=tilt_C*d2r,
    lat=latitude_C*d2r,
    azi=azimuth_C*d2r) "Diffuse irradiation on tilted surface"
    annotation (Placement(transformation(extent={{14,50},{34,70}})));
  Buildings.BoundaryConditions.SolarIrradiation.DirectTiltedSurface HDirTil(
    til=tilt_C*d2r,
    lat=latitude_C*d2r,
    azi=azimuth_C*d2r) "Direct irradiation on tilted surface"
    annotation (Placement(transformation(extent={{14,10},{34,30}})));
  Buildings.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(
      computeWetBulbTemperature=false,
    HSou=Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HDifHor,
    filNam=weafile)
    annotation (Placement(transformation(extent={{-34,50},{-14,70}})));
  Modelica.Blocks.Math.Add G "Total irradiation on tilted surface"
    annotation (Placement(transformation(extent={{54,30},{74,50}})));
  Modelica.Blocks.Sources.CombiTimeTable sunwea(
    tableOnFile=true,
    tableName="tab1",
    fileName=weafile,
    columns=2:30,
    extrapolation=Modelica.Blocks.Types.Extrapolation.Periodic)
    annotation (Placement(transformation(extent={{-86,50},{-66,70}})));
  Modelica.Blocks.Interfaces.RealOutput y
    annotation (Placement(transformation(extent={{90,30},{110,50}})));
equation
  connect(weaDat.weaBus,HDifTil. weaBus) annotation (Line(
      points={{-14,60},{14,60}},
      color={255,204,51},
      thickness=0.5,
      smooth=Smooth.None));
  connect(weaDat.weaBus,HDirTil. weaBus) annotation (Line(
      points={{-14,60},{0,60},{0,20},{14,20}},
      color={255,204,51},
      thickness=0.5,
      smooth=Smooth.None));
  connect(HDifTil.H,G. u1) annotation (Line(
      points={{35,60},{42,60},{42,46},{52,46}},
      color={0,0,127},
      smooth=Smooth.None));
  connect(HDirTil.H,G. u2) annotation (Line(
      points={{35,20},{42,20},{42,34},{52,34}},
      color={0,0,127},
      smooth=Smooth.None));
  connect(sunwea.y[10], weaDat.HDifHor_in) annotation (Line(points={{-65,60},{
          -46,60},{-46,52.4},{-35,52.4}},    color={0,0,127}));
  connect(sunwea.y[9], weaDat.HDirNor_in) annotation (Line(points={{-65,60},{
          -54,60},{-54,49},{-35,49}},    color={0,0,127}));
  connect(G.y, y) annotation (Line(points={{75,40},{100,40}}, color={0,0,127}));
  annotation (experiment(StopTime=1.0, Tolerance=1e-6),
    __Dymola_Commands(file=
          "modelica://Buildings/Resources/Scripts/Dymola/Electrical/AC/OnePhase/Sources/Examples/PVPanels.mos"
        "Simulate and plot"),
    Documentation(revisions="<html>
<ul>
<li>
April 2020, by Max Boegli:<br/>
Submodule for Solar irradiance on tilted surface.
</li>
<li>
August 5, 2014, by Marco Bonvini:<br/>
Revised model and documentation.
</li>
</ul>
</html>", info="<html>
<p>Derived from the example of a simple PV model with orientation.<br/>
Orientation through tilt, azimuth, latitude.<br/>
GHI = DHI + DNI*cos(zenith angle)<br/>
</html>"),
    Icon(graphics={
        Text(
          extent={{-44,72},{44,30}},
          lineColor={28,108,200},
          textString="Solar"),
        Polygon(points={{-8,-20},{-8,-20}}, lineColor={28,108,200}),
        Polygon(points={{-26,-60},{6,-8},{52,-8},{24,-60},{-26,-60}}, lineColor
            ={28,108,200}),
        Ellipse(extent={{-42,4},{-4,-34}}, lineColor={28,108,200})}));
end SunRad_TiltSurf;
