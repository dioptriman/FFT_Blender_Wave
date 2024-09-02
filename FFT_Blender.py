import bpy
import numpy as np

def create_plane(name, width, depth, resolution):
    """
    Create a plane with specified dimensions and resolution.

    Parameters:
    - name: Name of the plane object.
    - width: Width of the plane.
    - depth: Depth of the plane.
    - resolution: Number of subdivisions in each direction.
    """
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    plane = bpy.context.object
    plane.name = name
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=resolution - 1)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Scale the plane
    plane.scale[0] = width / 2
    plane.scale[1] = depth / 2
    plane.scale[2] = 1
    return plane

def generate_ocean_wave(plane, width, depth, resolution, frequency, amplitude, time):
    """
    Apply FFT-based ocean wave simulation to a mesh plane.

    Parameters:
    - plane: The Blender mesh object to modify.
    - width: Width of the plane.
    - depth: Depth of the plane.
    - resolution: Number of subdivisions in each direction.
    - frequency: Base frequency of the waves.
    - amplitude: Amplitude of the waves.
    - time: Current time to animate the waves.
    """
    # Access the mesh data
    mesh = plane.data
    for vertex in mesh.vertices:
        x, y, z = vertex.co
        # Convert coordinates to texture space
        u = x / width * resolution
        v = y / depth * resolution
        # Apply FFT-based wave pattern
        wave = amplitude * np.sin(frequency * (u + v) - time)
        vertex.co.z = wave

def main():
    # Settings
    plane_name = 'OceanPlane'
    width = 10
    depth = 10
    resolution = 50
    frequency = 1.0
    amplitude = 1.0

    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create and setup the plane
    plane = create_plane(plane_name, width, depth, resolution)

    # Animation setup
    for frame in range(1, 250):
        time = frame * 0.1
        bpy.context.scene.frame_set(frame)
        generate_ocean_wave(plane, width, depth, resolution, frequency, amplitude, time)
        plane.data.update()
        # Insert keyframe for vertex positions
        for vertex in plane.data.vertices:
            vertex.keyframe_insert(data_path="co", frame=frame)

# Run the script
main()
