// Lava Shader
#version 330

uniform float time;
uniform vec2 resolution;

// Noise generation function
float noise(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

// Smooth noise
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

// Fractal Brownian Motion (fBm)
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
    uv.x *= resolution.x / resolution.y;

    // Lava turbulence
    vec2 pos = uv * 3.0 - vec2(1.5);
    float n = fbm(pos + time * 0.2);

    // Color gradient for lava
    vec3 color = vec3(0.0);
    if (n > 0.6) {
        color = mix(vec3(1.0, 0.5, 0.0), vec3(1.0, 1.0, 0.0), smoothstep(0.6, 1.0, n));
    } else if (n > 0.4) {
        color = mix(vec3(0.5, 0.1, 0.0), vec3(1.0, 0.5, 0.0), smoothstep(0.4, 0.6, n));
    } else {
        color = vec3(0.2, 0.0, 0.0);
    }

    // Add glow effect
    float glow = smoothstep(0.7, 1.0, n);
    color += glow * vec3(1.0, 0.3, 0.0);

    gl_FragColor = vec4(color, 1.0);
}
