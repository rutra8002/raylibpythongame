#version 330

uniform float time;
uniform vec2 resolution;      // Screen resolution
uniform vec2 camera_offset;   // Camera position offset
uniform vec2 block_position;  // Position of the block
uniform vec2 block_size;      // Size of the block
uniform float camera_zoom;    // Camera zoom

const float PATTERN_SIZE = 50.0; // Fixed pattern size

float noise(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

float smoothNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    float a = noise(i);
    float b = noise(i + vec2(1.0, 0.0));
    float c = noise(i + vec2(0.0, 1.0));
    float d = noise(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

float fbm(vec2 p) {
    float value = 0.0;
    float scale = 0.5;
    for (int i = 0; i < 5; i++) {
        value += smoothNoise(p) * scale;
        p *= 2.0;
        scale *= 0.5;
    }
    return value;
}

void main() {
    vec2 uv = gl_FragCoord.xy / resolution.xy;

    // Scale UV by block dimensions
    vec2 local_uv = (gl_FragCoord.xy - block_position) / (block_size * camera_zoom);

    // Normalize to pattern grid
    vec2 pattern_uv = local_uv * (block_size / PATTERN_SIZE);

    // Offset pattern with camera
    vec2 pos = (pattern_uv + camera_offset / PATTERN_SIZE) * 3.0 * camera_zoom - vec2(1.5);
    float n = fbm(pos + time * 0.2);

    vec3 color = vec3(0.0);
    if (n > 0.6) {
        color = mix(vec3(1.0, 0.5, 0.0), vec3(1.0, 1.0, 0.0), smoothstep(0.6, 1.0, n));
    } else if (n > 0.4) {
        color = mix(vec3(0.5, 0.1, 0.0), vec3(1.0, 0.5, 0.0), smoothstep(0.4, 0.6, n));
    } else {
        color = vec3(0.2, 0.0, 0.0);
    }

    float glow = smoothstep(0.7, 1.0, n);
    color += glow * vec3(1.0, 0.3, 0.0);

    gl_FragColor = vec4(color, 1.0);
}
