#version 330

in vec2 fragTexCoord;
in vec4 fragColor;
out vec4 finalColor;

uniform float time;
uniform vec2 resolution;

// Better noise function for detailed patterns
float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

vec2 random2(vec2 st) {
    st = vec2(dot(st,vec2(127.1,311.7)), dot(st,vec2(269.5,183.3)));
    return -1.0 + 2.0 * fract(sin(st)*43758.5453123);
}

// Improved value noise
float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(a, b, u.x) + (c - a)* u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

// Fractal Brownian Motion with more detail
float fbm(vec2 p) {
    float sum = 0.0;
    float amp = 0.5;
    float freq = 1.0;
    vec2 pos = p;
    // More octaves for finer detail
    for(int i = 0; i < 8; i++) {
        sum += noise(pos * freq) * amp;
        amp *= 0.5;
        freq *= 2.0;
        pos += vec2(1.3, 1.7); // Rotate for better patterns
    }
    return sum;
}

// Voronoi noise for bubble-like patterns
float voronoi(vec2 x) {
    vec2 n = floor(x);
    vec2 f = fract(x);

    float md = 8.0;

    for(int j = -1; j <= 1; j++) {
        for(int i = -1; i <= 1; i++) {
            vec2 g = vec2(float(i), float(j));
            vec2 o = random2(n + g);
            o = 0.5 + 0.5 * sin(time * 0.5 + 6.2831 * o); // Animate bubbles

            vec2 r = g + o - f;
            float d = dot(r, r);

            if(d < md) {
                md = d;
            }
        }
    }
    return md;
}

void main() {
    vec2 uv = fragTexCoord.xy;
    // Scale UV for more visible detail
    vec2 pos = uv * 8.0;

    // Multiple layers of flow
    float flow1 = fbm(pos + vec2(time * 0.2));
    float flow2 = fbm(pos * 1.5 - vec2(time * 0.1));
    float flow3 = fbm(pos * 0.5 + vec2(time * 0.15));

    // Bubble effect using voronoi
    float bubbles = voronoi(pos * 3.0 + vec2(time * 0.1));
    float bubblePattern = 1.0 - smoothstep(0.0, 0.4, bubbles);

    // Create cracks/details
    float cracks = fbm(pos * 4.0) * fbm(pos * 2.0 - vec2(time * 0.05));

    // Combine different layers
    float pattern = flow1 * 0.5 + flow2 * 0.3 + flow3 * 0.2;
    pattern = pattern + bubblePattern * 0.3;

    // Color palette
    vec3 baseColor = vec3(0.6, 0.0, 0.0);   // Dark base
    vec3 hotColor = vec3(1.0, 0.3, 0.0);    // Hot orange
    vec3 glowColor = vec3(1.0, 0.6, 0.0);   // Yellow-orange glow
    vec3 darkColor = vec3(0.3, 0.0, 0.0);   // Very dark for cracks

    // Mix colors based on patterns
    vec3 color = mix(baseColor, hotColor, pattern);
    color = mix(color, glowColor, bubblePattern * 0.8);
    color = mix(color, darkColor, cracks * 0.5);

    // Add bright spots for bubbles
    float bright = smoothstep(0.4, 0.45, bubblePattern);
    color += glowColor * bright * 0.5;

    // Edge darkening
    float edge = length(uv - 0.5) * 2.0;
    edge = 1.0 - smoothstep(0.4, 1.0, edge);
    color *= edge;

    // Pulsing glow
    float pulse = sin(time + pattern * 2.0) * 0.1 + 0.9;
    color *= pulse;

    // Add subtle variation based on position
    float posVariation = fbm(pos * 0.5) * 0.2;
    color *= (1.0 + posVariation);

    finalColor = vec4(color, edge);
}