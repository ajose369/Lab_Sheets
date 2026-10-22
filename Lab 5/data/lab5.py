import os
import zipfile
import geopandas as gpd
import matplotlib.pyplot as plt

os.makedirs("output", exist_ok=True)

for z in ["NE_states.zip", "meghalaya.zip"]:
    zipfile.ZipFile(z).extractall("data")

ne  = gpd.read_file("data/NE_states.shp")
meg = gpd.read_file("data/meghalaya.shp")

print(ne)
print(meg)
# ---------------- Q1: Projection ----------------
print("===== Q1: Projection =====")
print("NE_states CRS :", ne.crs)
print("NE_states name:", ne.crs.name)
print("Meghalaya CRS :", meg.crs)
print("Meghalaya name:", meg.crs.name)
# ---------------- Q2: Missing attributes ----------------
print("\n===== Q2: Missing attributes =====")

print("NE_states - missing values per column:")
print(ne.isna().sum())

print("\nMeghalaya - missing values per column:")
print(meg.isna().sum())

print("\nNE_states - valid geometry?")
print(ne[["State_Name"]].assign(valid=ne.is_valid))
# ---------------- Q3: Reproject, plot, save ----------------
print("\n===== Q3: Reproject to EPSG:4326 =====")

# 1. Reproject
ne_4326  = ne.to_crs(epsg=4326)
meg_4326 = meg.to_crs(epsg=4326)
print("NE_states new CRS :", ne_4326.crs)
print("Meghalaya new CRS :", meg_4326.crs)

# 2. Plot
fig, ax = plt.subplots(figsize=(8, 8))
ne_4326.plot(ax=ax, column="State_Name", cmap="tab10",
             edgecolor="black", legend=True)

for i, row in ne_4326.iterrows():
    point = row.geometry.representative_point()
    ax.annotate(row["State_Name"], (point.x, point.y),
                ha="center", fontsize=8)

ax.set_title("North-Eastern States (EPSG:4326)")
ax.set_xlabel("Longitude (°E)")
ax.set_ylabel("Latitude (°N)")
plt.savefig("output/q3_NE_states.png", dpi=200)
plt.show()

# 3. Save as new shapefiles
ne_4326.to_file("output/NE_states_4326.shp")
meg_4326.to_file("output/meghalaya_4326.shp")
print("Saved reprojected shapefiles in output/")
# ---------------- Q4: Area of NE states ----------------
print("\n===== Q4: Area of NE states =====")

# 1. Project to an equal-area CRS
ne_ea = ne.to_crs("ESRI:102028")

# 2. Calculate area in km²
ne_ea["Area_km2"] = ne_ea.geometry.area / 1_000_000

# 3. Sort largest to smallest
ne_ea = ne_ea.sort_values("Area_km2", ascending=False)
print(ne_ea[["State_Name", "Area_km2"]].round(1))

# 4. Bar chart
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(ne_ea["State_Name"], ne_ea["Area_km2"], color="steelblue")
ax.bar_label(bars, fmt="%.0f")
ax.set_title("Area of North-Eastern States")
ax.set_xlabel("State")
ax.set_ylabel("Area (km²)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("output/q4_NE_areas.png", dpi=200)
plt.show()
# ---------------- Q5: My state from GADM ----------------
print("\n===== Q5: Kerala from GADM =====")

states = gpd.read_file("gadm/gadm41_IND_1.shp")
print("GADM CRS:", states.crs)
print(states["NAME_1"].unique())

kerala = states[states["NAME_1"] == "Kerala"]
print(kerala[["NAME_1"]])

fig, ax = plt.subplots(figsize=(6, 9))
kerala.plot(ax=ax, color="lightgreen", edgecolor="black")
ax.set_title("Kerala (GADM 4.1)")
ax.set_xlabel("Longitude (°E)")
ax.set_ylabel("Latitude (°N)")
plt.savefig("output/q5_kerala.png", dpi=200)
plt.show()
# ---------------- Q6: Favourite region -> EPSG:4326 ----------------
print("\n===== Q6: Favourite region =====")

districts = gpd.read_file("gadm/gadm41_IND_2.shp")
print(districts[districts["NAME_1"] == "Kerala"]["NAME_2"].tolist())

region = districts[(districts["NAME_1"] == "Kerala") &
                   (districts["NAME_2"] == "Ernakulam")]

region = region.to_crs(epsg=4326)
print("Region CRS:", region.crs)

region.to_file("output/ernakulam_4326.shp")
print("Saved output/ernakulam_4326.shp")

fig, ax = plt.subplots(figsize=(6, 6))
region.plot(ax=ax, color="orange", edgecolor="black")
ax.set_title("Ernakulam District (EPSG:4326)")
ax.set_xlabel("Longitude (°E)")
ax.set_ylabel("Latitude (°N)")
plt.tight_layout()
plt.savefig("output/q6_ernakulam.png", dpi=200)
plt.show()
# ---------------- Q7: District areas of Kerala ----------------
print("\n===== Q7: District areas of Kerala =====")

kerala_dist = districts[districts["NAME_1"] == "Kerala"]
kerala_dist = kerala_dist.to_crs("ESRI:102028")

kerala_dist["Area_km2"] = kerala_dist.geometry.area / 1_000_000
kerala_dist = kerala_dist.sort_values("Area_km2", ascending=False)

print(kerala_dist[["NAME_2", "Area_km2"]].round(1))
total = kerala_dist["Area_km2"].sum()
print(f"Total area of Kerala: {total:,.0f} km²")

fig, ax = plt.subplots(figsize=(11, 5))
bars = ax.bar(kerala_dist["NAME_2"], kerala_dist["Area_km2"], color="seagreen")
ax.bar_label(bars, fmt="%.0f", fontsize=8)
ax.set_title("District Areas of Kerala")
ax.set_xlabel("District")
ax.set_ylabel("Area (km²)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("output/q7_kerala_districts.png", dpi=200)
plt.show()