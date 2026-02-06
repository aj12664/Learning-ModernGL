from math import tau
import moderngl
import glfw
import glm
import numpy as np

Width = 1600
Height = 800
Camera_pos = glm.vec3(0, 0, 50)
Camera_forward = glm.vec3(0, 0,-1)
Camera_up = glm.vec3(0, 1, 0)
Radius = 75
DeltaTheta = 0.05/Radius

if not glfw.init():
    raise RuntimeError("GLFW failed to intialise")

window = glfw.create_window(Width, Height,"Black Hole Simulator",None, None,)

glfw.make_context_current(window)

ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST)

vertex_shader_source = """
#version 330
in vec3 in_position;
uniform mat4 mvp;
void main(){
    gl_Position = mvp * vec4(in_position, 1.0);
}
"""
fragment_shader_source = """
#version 330
out vec4 fragColor;
void main(){
    fragColor = vec4(1.0, 0.64, 0.0, 1.0);
}
"""
prog = ctx.program(vertex_shader=vertex_shader_source, fragment_shader=fragment_shader_source)

vertices = [0.0, 0.0, 0.0]

segments = int(tau / DeltaTheta)
theta_values = np.linspace(0, tau, segments, endpoint=True)

for theta in theta_values:
    x = Radius * np.cos(theta)
    y = Radius * np.sin(theta)
    x_ndc = x / (Width / 2)
    y_ndc = y / (Height / 2)
    vertices.extend([x_ndc, y_ndc, 0.0])


vertices = np.array(vertices, dtype="f4")

vbo = ctx.buffer(vertices.tobytes())
vao = ctx.simple_vertex_array(prog, vbo, "in_position")

prog["mvp"].write(np.eye(4, dtype="f4").tobytes())

while not glfw.window_should_close(window):
    ctx.clear(0.02, 0.02, 0.05)
        
    vao.render(mode=moderngl.TRIANGLE_FAN)
    glfw.poll_events()
    glfw.swap_buffers(window)
    

glfw.terminate()
