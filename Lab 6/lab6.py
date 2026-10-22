import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, box
CRS = "EPSG:32643"

#--------Task 1-----------
rng = np.random.default_rng(42)
xy = rng.uniform(0, 5000, size=(8, 2))                       # 8 random points in a 5 km x 5 km area
pts = gpd.GeoDataFrame(geometry=[Point(x, y) for x, y in xy], crs=CRS)

fig, ax = plt.subplots(figsize=(8, 8))
for dist, col in [(1000, "#cfe3f5"), (500, "#8fbfe8"), (100, "#2f7fc1")]:   # big -> small so all stay visible
    b = pts.copy(); b["geometry"] = pts.buffer(dist)
    b.plot(ax=ax, color=col, edgecolor="k", alpha=0.6, linewidth=0.5, label=f"{dist} m buffer")
pts.plot(ax=ax, color="red", markersize=25, zorder=5, label="random points")
ax.set_title("Random points with 100 m, 500 m and 1 km buffers")
ax.set_xlabel("Easting (m)"); ax.set_ylabel("Northing (m)"); ax.set_aspect("equal"); ax.legend(loc="upper right")
plt.show()

#--------Task 2-----------
circle = gpd.GeoDataFrame({"shape": ["circle"]}, geometry=[Point(300, 300).buffer(200)], crs=CRS)
rect   = gpd.GeoDataFrame({"shape": ["rectangle"]}, geometry=[box(300, 250, 700, 550)], crs=CRS)

fig, axes = plt.subplots(1, 4, figsize=(20, 5))
panels = [("Inputs", None), ("Intersection", "intersection"), ("Union", "union"), ("Difference (circle - rect)", "difference")]
for ax, (title, how) in zip(axes, panels):
    if how is None:
        circle.plot(ax=ax, color="tab:blue", alpha=0.5, edgecolor="k")
        rect.plot(ax=ax, color="tab:orange", alpha=0.5, edgecolor="k")
    else:
        res = gpd.overlay(circle, rect, how=how)
        circle.boundary.plot(ax=ax, color="tab:blue"); rect.boundary.plot(ax=ax, color="tab:orange")
        res.plot(ax=ax, color="tab:green", alpha=0.7, edgecolor="k")
        print(f"{how:13s} area = {res.area.sum():10.1f} m2")
    ax.set_title(title); ax.set_aspect("equal")
plt.tight_layout(); plt.show()

#--------Task 3-----------

def load(path):
    g = gpd.read_file(path)
    return g.set_crs("EPSG:4326", allow_override=True).to_crs(CRS)

boundary = load(r"C:\Users\aldri\OneDrive - Indian Institute of Space Science and Technology\Studies\GIS\Lab\6\/nedumangad_boundary.shp")
b = load(r"C:\Users\aldri\OneDrive - Indian Institute of Space Science and Technology\Studies\GIS\Lab\6\/buildings/nedumangad_buildings.shp")
r = load(r"C:\Users\aldri\OneDrive - Indian Institute of Space Science and Technology\Studies\GIS\Lab\6\/roads/nedumangad_road.shp")
w = load(r"C:\Users\aldri\OneDrive - Indian Institute of Space Science and Technology\Studies\GIS\Lab\6\/waterways/nedumangad_waterways.shp")
p = load(r"C:\Users\aldri\OneDrive - Indian Institute of Space Science and Technology\Studies\GIS\Lab\6\/pois/nedumangad_pois.shp")
l = load(r"C:\Users\aldri\OneDrive - Indian Institute of Space Science and Technology\Studies\GIS\Lab\6\/landuse/nedumangad_landuse.shp")

for n, g in dict(boundary=boundary, buildings=b, roads=r, waterways=w, pois=p, landuse=l).items():
    print(f"{n:10s} {len(g):6d} features  {g.crs}")

area = boundary.area.sum()
print(f"Area of Nedumangad Taluk: {area/1e6:,.2f} km2  ({area/1e4:,.0f} ha)\n")

print("Forest polygons in LULC:", (l.fclass == "forest").sum())
print("Forest area: %.2f km2" % (l[l.fclass == "forest"].area.sum()/1e6))
print("\nLULC classes:\n", l.fclass.value_counts().to_string())

prim = sorted(r.loc[r.fclass == "primary", "name"].dropna().unique())
print(f"\nPrimary road names ({len(prim)}):", prim)
print("\nRoad length by class (km):\n", (r.assign(L=r.length).groupby("fclass").L.sum()/1000).round(1).sort_values(ascending=False).head(8).to_string())
print("\nWaterways:\n", w.fclass.value_counts().to_string())
print("\nTop POIs:\n", p.fclass.value_counts().head(8).to_string())
print("\nBuildings:", len(b), "| named:", b.name.notna().sum())

fig, ax = plt.subplots(figsize=(8, 8))
boundary.plot(ax=ax, color="#f2efe6", edgecolor="k")
l[l.fclass == "forest"].plot(ax=ax, color="green", label="forest")
w[w.fclass == "river"].plot(ax=ax, color="blue", linewidth=1.2, label="rivers")
r[r.fclass.isin(["primary", "secondary"])].plot(ax=ax, color="red", linewidth=0.8, label="primary/secondary roads")
ax.legend(); ax.set_title(f"Nedumangad Taluk  ({area/1e6:,.0f} km2)"); plt.show()

#--------Task 4-----------
streams = w[w.fclass.isin(["river", "stream"])]
buf200 = gpd.GeoDataFrame(geometry=[streams.buffer(200).union_all()], crs=CRS)
near_b = gpd.sjoin(b, buf200, predicate="intersects", how="inner").drop(columns="index_right")

print("Total buildings:", len(b))
print("Within 200 m of river/stream:", len(near_b), f"({len(near_b)/len(b):.1%})")
named = near_b["name"].dropna()
print(f"Named buildings among them: {len(named)}\n\n10 names:")
for n in named.head(10): print("  -", n)

fig, ax = plt.subplots(figsize=(10, 10))
buf200.plot(ax=ax, color="lightblue", alpha=0.5)
b.plot(ax=ax, color="lightgrey")
near_b.plot(ax=ax, color="red")
streams.plot(ax=ax, color="blue", linewidth=0.5)
ax.set_title("Buildings within 200 m of rivers and streams (red)"); plt.show()

#--------Task 5-----------
hosp = p[p.fclass == "hospital"]
main_roads = r[r.fclass.isin(["primary", "primary_link", "trunk", "trunk_link"])]
print("Road classes used:", main_roads.fclass.value_counts().to_dict())

buf750 = gpd.GeoDataFrame(geometry=[main_roads.buffer(750).union_all()], crs=CRS)
near_h = gpd.sjoin(hosp, buf750, predicate="within", how="inner").drop(columns="index_right")
print(f"\nHospitals total: {len(hosp)} | within 750 m of primary/trunk: {len(near_h)}")
print("\n10 names:")
for n in near_h["name"].dropna().head(10): print("  -", n)

fig, ax = plt.subplots(figsize=(10, 10))
boundary.plot(ax=ax, color="#f7f5ee", edgecolor="k")
buf750.plot(ax=ax, color="khaki", alpha=0.5)
main_roads.plot(ax=ax, color="darkorange", linewidth=1)
hosp.plot(ax=ax, color="grey", markersize=15, label="other hospitals")
near_h.plot(ax=ax, color="red", markersize=35, label="within 750 m")
ax.legend(); ax.set_title("Hospitals within 750 m of primary/trunk roads"); plt.show()

#--------Task 6-----------  
bridges = r[r.bridge == "T"]
rivers = w[w.fclass.isin(["river", "canal"])]          # note: the class is 'canal' (singular) in this data

on_river = gpd.sjoin(bridges, rivers[["geometry"]], predicate="intersects", how="inner")
on_river = on_river[~on_river.index.duplicated()]       # one row per bridge segment

print("Total bridge segments in taluk:", len(bridges))
print("Bridge segments on top of rivers/canals:", len(on_river))
names = sorted(on_river["name"].dropna().unique())
print(f"Distinct bridge/road names ({len(names)}):")
for n in names: print("  -", n)
print("Unnamed bridge segments:", on_river["name"].isna().sum())

cross = gpd.overlay(rivers[["geometry"]], on_river[["geometry"]], how="intersection", keep_geom_type=False)
fig, ax = plt.subplots(figsize=(9, 9))
rivers.plot(ax=ax, color="blue", linewidth=1.5, alpha=0.6, label="rivers/canals")
on_river.plot(ax=ax, color="orange", linewidth=2, label="bridges")
cross.plot(ax=ax, color="red", markersize=25, label="crossing points")
ax.legend(); ax.set_title("Bridges on top of rivers"); plt.show()

#--------Task 7-----------
forest = l[l.fclass == "forest"]
pt = r[r.fclass.isin(["primary", "tertiary"])]
inside = gpd.overlay(pt, forest[["geometry"]], how="intersection")   # portions of the roads lying in forest
inside["len_m"] = inside.length

print("Road pieces inside forest:", len(inside), "| total length: %.1f km" % (inside.len_m.sum()/1000))
g = inside.groupby(["fclass", "name"], dropna=False).len_m.sum().div(1000).round(2).sort_values(ascending=False)
print("\nNames of primary/tertiary roads inside forest (km inside forest):")
print(g.to_string())
print("Unnamed pieces:", inside["name"].isna().sum())

fig, ax = plt.subplots(figsize=(10, 10))
boundary.plot(ax=ax, color="#f7f5ee", edgecolor="k")
forest.plot(ax=ax, color="#9fd79f")
pt.plot(ax=ax, color="grey", linewidth=0.6)
inside.plot(ax=ax, color="red", linewidth=2.5)
ax.set_title("Primary & tertiary roads inside forest (red)"); plt.show()
