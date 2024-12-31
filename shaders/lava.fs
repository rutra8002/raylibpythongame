#version 330

in vec2 fragTexCoord;
out vec4 finalColor;

uniform float time;
uniform vec2 resolution;

void main()
{
    vec2 uv = fragTexCoord;
    uv.y += time * 0.1;
    vec3 color = vec3(0.5 + 0.5 * sin(uv.y * 10.0 + time), 0.5 + 0.5 * sin(uv.y * 20.0 + time), 0.0);
    finalColor = vec4(color, 1.0);
}