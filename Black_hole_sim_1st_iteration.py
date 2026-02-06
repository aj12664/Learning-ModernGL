from math import tau
import moderngl
import glfw
import glm
import numpy as np
import time

Width = 1600
Height = 800

Camera_pos = glm.vec3(0, 0, 50)
Camera_side = glm.vec3(1, 0, 0)
Camera_up = glm.vec3(0, 1, 0)
Camera_Speed = 0.01

Radius = 3
DeltaTheta = 0.05/Radius

if not glfw.init():
    raise RuntimeError("GLFW failed to intialise")

window = glfw.create_window(Width, Height,"Black Hole Simulator",None, None)

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
    vertices.extend([x, y, 0.0])


vertices = np.array(vertices, dtype="f4")

vbo = ctx.buffer(vertices.tobytes())
vao = ctx.simple_vertex_array(prog, vbo, "in_position")

def Camera_Movement(window, Camera_side, Camera_up, Camera_pos, speed, dt):
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        Camera_pos += Camera_up * speed * dt
        
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        Camera_pos -= Camera_up * speed * dt
        
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        Camera_pos += Camera_side * speed * dt
        
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        Camera_pos -= Camera_side * speed * dt
        
    return Camera_pos
projection = glm.perspective(glm.radians(45), Width / Height, 0.1, 1000.0)


last_time = time.time()
        
while not glfw.window_should_close(window):
    current_time = time.time()
    dt = current_time - last_time
    ctx.clear(0.02, 0.02, 0.05)
    
    Camera_pos = Camera_Movement(window, Camera_side, Camera_up, Camera_pos, Camera_Speed, dt)
    view = glm.lookAt(Camera_pos, Camera_pos + glm.vec3(0, 0, -1), Camera_up)
    
    mvp = projection * view * glm.mat4(1.0)
    prog["mvp"].write(np.array(mvp.to_list(), dtype="f4").tobytes())

    vao.render(mode=moderngl.TRIANGLE_FAN)
    glfw.poll_events()
    glfw.swap_buffers(window)
    

glfw.terminate()
