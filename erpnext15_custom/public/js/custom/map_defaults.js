const map_settings = frappe.provide("frappe.utils.map_defaults");

// Center and zoomlevel can be copied from the URL of
// the map view at openstreetmap.org.

// New default location (37 Military Hospital).
map_settings.center = [5.5891435, -0.1899715];
// new zoomlevel: see the whole country, not just a single city
map_settings.zoom = 10;

// Use a different map: satellite instead of streets
// Examples can be found at https://leaflet-extras.github.io/leaflet-providers/preview/
map_settings.tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}";
map_settings.attribution = "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community";