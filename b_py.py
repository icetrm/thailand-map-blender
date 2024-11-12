import bpy
import json
from urllib.request import urlopen

response = urlopen("https://www.thaiwater.net/json/boundary/thailand.json")
json_data = response.read().decode('utf-8', 'replace')
load_json = json.loads(json_data)

# thai_item = list(filter(lambda x: x['properties']['title_eng'] in ["bangkok"], load_json['features']))
thai_item = list(load_json['features'])

context = bpy.context

def create_circle(geometrys, name):
    faces = [tuple(map(lambda x: x, range(0, len(geometrys), 1)))]
    edges = []
    verts = list(map(lambda x: (x[0] - 100, x[1] - 13, 0), geometrys))
    # create a mesh from the vert, edge, and face data
    mesh_data = bpy.data.meshes.new(name)
    mesh_data.from_pydata(verts, edges, faces)
    
    # create a object using the mesh data
    mesh_obj = bpy.data.objects.new(name, mesh_data)
    
    context.collection.objects.link(mesh_obj)

for province in range(0, len(thai_item) , 1):
   
   item = thai_item[province]
   geometrys = item['geometry']['coordinates']
   
   if (item['geometry']['type'] == 'MultiPolygon'):
       for geo_a in geometrys:
           j = 0
           for geo_b in geo_a:
               create_circle(geo_b, item['properties']['title_eng'] + '_' + str(j))
               j = j + 1
   else:
       for geo_a in geometrys:
           create_circle(geo_a, item['properties']['title_eng'])


for province in bpy.context.scene.objects.values():
    bpy.ops.object.select_all(action='DESELECT')
    province.select_set(True) # Select the default Blender Cub
    bpy.context.view_layer.objects.active = province
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0.03)})
    bpy.ops.object.mode_set(mode='OBJECT')