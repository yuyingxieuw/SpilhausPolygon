# Splihaus Cordination Transform Tool

This tool is build on Proj4 package with which you can transform points from any coordinate system to a splihaus projection. But to transform polygon the errs occurs.

The function trace each points and find the points that touch the extreme of the boundary of the spilhaus project. It divides the polygon to lines and reconstruction these lines.

### Test log diary

#### Nov3 2025

- Test simpleUS4326.json -- >
