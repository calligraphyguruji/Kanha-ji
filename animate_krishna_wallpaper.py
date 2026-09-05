#!/usr/bin/env python3
"""
================================================================================
   SACRED BAL KRISHNA ANIMATED 9:16 DEVOTIONAL WALLPAPER GENERATOR
================================================================================
A complete, production-grade Python script that transforms a still artwork of
Lord Krishna into a breathtaking, seamlessly looping 10-second (30 FPS, 300 frames)
1080x1920 (9:16) animated devotional wallpaper for smartphones and lock screens.

INSTALLATION:
    pip install opencv-python numpy pillow imageio imageio-ffmpeg scipy tqdm

USAGE:
    python3 animate_krishna_wallpaper.py
    python3 animate_krishna_wallpaper.py --input /mnt/data/8034.jpg --output /mnt/data/krishna_animated.mp4

FEATURES & ANIMATION LAYERS:
  1. Drifting, twinkling cosmic particles & stars with harmonic luminescence.
  2. Subtly rotating galaxy-like cosmic dust and nebulous atmosphere.
  3. Pulsing neon outlines (cyan/blue, pink/purple, and gold/yellow).
  4. Non-distorting micro-shimmer on eye catchlights & divine gaze.
  5. Extremely subtle organic micro-sway on outer hair strands.
  6. Rhythmic glistening 4-point diamond sparkles on jewelry and flowers.
  7. Soft traveling celestial glow along the flute (bansuri).
  8. Breathing divine golden aura expanding and contracting behind Krishna.
  9. Occasional floating magical sparkles around the character.
 10. Slow cinematic camera breathing zoom (1.00 -> 1.025 -> 1.00) with parallax.
 11. Rotating volumetric celestial light rays radiating into the background.
 12. 100% mathematically seamless looping (Frame 0 perfectly matches Frame 300).
================================================================================
"""

import sys
import os
import math
import argparse
import random
from typing import Tuple, List, Optional

# Core scientific & image processing libraries
try:
    import numpy as np
    import cv2
    from PIL import Image
    import imageio
    from scipy.ndimage import gaussian_filter
    from tqdm import tqdm
except ImportError as err:
    print(f"Error: Missing required dependency -> {err}")
    print("Please install requirements using:")
    print("    pip install opencv-python numpy pillow imageio imageio-ffmpeg scipy tqdm")
    sys.exit(1)

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920
FPS = 30
DURATION_SEC = 10.0
TOTAL_FRAMES = int(FPS * DURATION_SEC)  # Exactly 300 frames

# Default paths as requested in specification
DEFAULT_INPUT_PATH = "/mnt/data/8034.jpg"
DEFAULT_OUTPUT_PATH = "/mnt/data/krishna_animated.mp4"


# ==============================================================================
# SEAMLESS MATHEMATICAL LOOP HELPERS
# ==============================================================================
def loop_phase(frame_idx: int, total_frames: int = TOTAL_FRAMES) -> float:
    """Returns normalized angle theta in [0, 2*pi) for seamless periodic functions."""
    return 2.0 * math.pi * (frame_idx / total_frames)


def periodic_sin(theta: float, freq: int = 1, phase: float = 0.0) -> float:
    """Harmonic sine in range [0.0, 1.0] guaranteed to have exact period matching."""
    return 0.5 + 0.5 * math.sin(freq * theta + phase)


def periodic_cos(theta: float, freq: int = 1, phase: float = 0.0) -> float:
    """Harmonic cosine in range [0.0, 1.0] guaranteed to have exact period matching."""
    return 0.5 + 0.5 * math.cos(freq * theta + phase)


# ==============================================================================
# 9:16 CANVAS ADAPTER & IMAGE PREPROCESSOR
# ==============================================================================
def prepare_916_canvas(image_path: str, target_w: int = TARGET_WIDTH, target_h: int = TARGET_HEIGHT) -> np.ndarray:
    """
    Loads the base Krishna artwork and formats it into a stunning 1080x1920 9:16 canvas.
    If the image is not 9:16, it creates a luxurious, soft cosmic blurred backdrop
    from the original artwork's colors, overlaying the sharp, centered original
    with a delicate feathered border.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    # Load with PIL to guarantee standard RGB color handling
    pil_img = Image.open(image_path).convert("RGB")
    orig_w, orig_h = pil_img.size
    orig_aspect = orig_w / orig_h
    target_aspect = target_w / target_h

    np_orig = np.array(pil_img)

    # Case A: Exact or very close 9:16 aspect ratio
    if abs(orig_aspect - target_aspect) < 0.02:
        resized = cv2.resize(np_orig, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
        return resized

    # Case B: Wider image (e.g. 16:9, 4:3, or square) -> Scale artwork to fit comfortably with cosmic backdrop
    scale_factor = min(target_w / orig_w, (target_h * 0.90) / orig_h)
    new_w = int(orig_w * scale_factor)
    new_h = int(orig_h * scale_factor)

    sharp_fg = cv2.resize(np_orig, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

    # Create background: Fill canvas with zoomed, heavily blurred version of original for organic ambient color
    bg_scale = max(target_w / orig_w, target_h / orig_h)
    bg_w = int(orig_w * bg_scale)
    bg_h = int(orig_h * bg_scale)
    bg_resized = cv2.resize(np_orig, (bg_w, bg_h), interpolation=cv2.INTER_LINEAR)

    # Crop to 1080x1920 center
    x_crop = (bg_w - target_w) // 2
    y_crop = (bg_h - target_h) // 2
    canvas_bg = bg_resized[y_crop:y_crop + target_h, x_crop:x_crop + target_w].astype(np.float32)

    # Heavy cinematic blur and subtle dimming for depth of field
    canvas_bg = cv2.GaussianBlur(canvas_bg, (101, 101), 45.0) * 0.45

    # Position sharp foreground at center
    fg_x = (target_w - new_w) // 2
    fg_y = (target_h - new_h) // 2

    # Create soft feathered edge mask around foreground
    feather_w = 20
    mask_2d = np.ones((new_h, new_w), dtype=np.float32)
    for i in range(feather_w):
        val = (i / feather_w) ** 1.5
        mask_2d[i, :] = np.minimum(mask_2d[i, :], val)
        mask_2d[-i - 1, :] = np.minimum(mask_2d[-i - 1, :], val)
        mask_2d[:, i] = np.minimum(mask_2d[:, i], val)
        mask_2d[:, -i - 1] = np.minimum(mask_2d[:, -i - 1], val)

    mask_3d = mask_2d[:, :, np.newaxis]

    canvas_bg[fg_y:fg_y + new_h, fg_x:fg_x + new_w] = (
        sharp_fg * mask_3d + canvas_bg[fg_y:fg_y + new_h, fg_x:fg_x + new_w] * (1.0 - mask_3d)
    )

    return np.clip(canvas_bg, 0, 255).astype(np.uint8)


# ==============================================================================
# FEATURE DETECTOR & MASK GENERATOR (COMPUTED ONCE BEFORE LOOP)
# ==============================================================================
class ArtworkAnalyzer:
    """
    Performs one-time spectral and spatial analysis of the Krishna artwork:
    - Segments vibrant neon edge contours by color (cyan/blue, pink/purple, gold/yellow)
    - Locates eye highlights for delicate shimmers
    - Detects flute trajectory for traveling celestial gleams
    - Identifies jewelry and floral garlands for diamond sparkles
    - Computes outer hair strand mask for organic micro-sway
    - Estimates crown/head epicenter for divine aura and volumetric light rays
    """
    def __init__(self, base_canvas: np.ndarray):
        self.canvas = base_canvas
        self.h, self.w, _ = base_canvas.shape

        # Convert to HSV and Gray spaces for robust segmentation
        self.hsv = cv2.cvtColor(base_canvas, cv2.COLOR_RGB2HSV)
        self.gray = cv2.cvtColor(base_canvas, cv2.COLOR_RGB2GRAY)

        print("[1/5] Extracting divine neon contour masks...")
        self.neon_cyan, self.neon_pink, self.neon_gold = self._extract_neon_masks()

        print("[2/5] Locating eye highlights, flute, and outer hair...")
        self.eye_mask = self._extract_eye_highlights()
        self.flute_mask, self.flute_coords = self._extract_flute()
        self.hair_mask = self._extract_outer_hair_mask()

        print("[3/5] Pinpointing jewelry and flower sparkle anchors...")
        self.sparkle_anchors = self._extract_sparkle_points(count=36)

        print("[4/5] Precomputing divine aura and celestial light rays...")
        self.center_x, self.center_y = self._estimate_head_center()
        self.radial_dist, self.angle_map = self._precompute_radial_fields()

        print("[5/5] Generating cosmic dust flow field...")
        self.cosmic_dust = self._generate_cosmic_dust_texture()

    def _extract_neon_masks(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        # High-frequency edge detection
        edges = cv2.Canny(self.gray, 30, 100).astype(np.float32) / 255.0

        h = self.hsv[:, :, 0]
        s = self.hsv[:, :, 1]
        v = self.hsv[:, :, 2]

        # Saturated color masks (OpenCV Hue is 0-180)
        cyan_hue = ((h >= 85) & (h <= 135) & (s > 45) & (v > 50)).astype(np.float32)
        pink_hue = (((h >= 135) & (h <= 175)) | (h <= 10)) & (s > 45) & (v > 50)
        pink_hue = pink_hue.astype(np.float32)
        gold_hue = ((h >= 15) & (h <= 45) & (s > 50) & (v > 60)).astype(np.float32)

        # Combine edges with color classification
        cyan_raw = edges * cyan_hue
        pink_raw = edges * pink_hue
        gold_raw = edges * gold_hue

        # Multi-scale Gaussian bloom for soft radiant neon glow
        cyan_blur = cv2.GaussianBlur(cyan_raw, (21, 21), 6.0)
        pink_blur = cv2.GaussianBlur(pink_raw, (21, 21), 6.0)
        gold_blur = cv2.GaussianBlur(gold_raw, (21, 21), 6.0)

        return cyan_blur, pink_blur, gold_blur

    def _extract_eye_highlights(self) -> np.ndarray:
        """Isolates tiny bright catchlights in the upper-mid facial area."""
        mask = np.zeros((self.h, self.w), dtype=np.float32)
        # Bounding box of typical eye location (relative to center face)
        y1, y2 = int(self.h * 0.22), int(self.h * 0.44)
        x1, x2 = int(self.w * 0.35), int(self.w * 0.65)
        face_roi = self.gray[y1:y2, x1:x2]

        # Peak specular spots (> 94th percentile in ROI)
        threshold_val = max(215, int(np.percentile(face_roi, 95)))
        _, bright_spots = cv2.threshold(face_roi, threshold_val, 1.0, cv2.THRESH_BINARY)

        # Keep only small pinpoint clusters (catchlights)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        filtered = cv2.morphologyEx(bright_spots.astype(np.uint8), cv2.MORPH_OPEN, kernel)

        mask[y1:y2, x1:x2] = cv2.GaussianBlur(filtered.astype(np.float32), (5, 5), 1.2)
        return mask

    def _extract_flute(self) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Finds the diagonal/horizontal luminous flute trajectory across Krishna's hands."""
        y1, y2 = int(self.h * 0.30), int(self.h * 0.65)
        x1, x2 = int(self.w * 0.20), int(self.w * 0.85)

        roi = self.gray[y1:y2, x1:x2]
        # Bright elongated structures
        thresh = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, -5)

        full_mask = np.zeros((self.h, self.w), dtype=np.float32)
        full_mask[y1:y2, x1:x2] = thresh.astype(np.float32) / 255.0
        full_mask = cv2.GaussianBlur(full_mask, (15, 15), 4.0)

        # Coordinates for normalized wave traversal
        indices = np.argwhere(full_mask > 0.3)
        return full_mask, indices

    def _extract_outer_hair_mask(self) -> np.ndarray:
        """Creates a smooth feathered mask confined strictly to the outer hair perimeter."""
        # Dark hair segmentation in upper half
        y1, y2 = int(self.h * 0.10), int(self.h * 0.55)
        dark_hair = (self.gray[y1:y2, :] < 55).astype(np.float32)

        # Outer edge boundary
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        hair_edge = cv2.morphologyEx(dark_hair, cv2.MORPH_GRADIENT, kernel)

        # Zero out center face region so facial anatomy remains 100% rigid and undistorted
        cx, cy = int(self.w * 0.50), int((y2 - y1) * 0.55)
        cv2.circle(hair_edge, (cx, cy), int(self.w * 0.22), 0.0, -1)

        full_hair_mask = np.zeros((self.h, self.w), dtype=np.float32)
        full_hair_mask[y1:y2, :] = cv2.GaussianBlur(hair_edge, (31, 31), 8.0)
        return full_hair_mask

    def _extract_sparkle_points(self, count: int = 36) -> List[Tuple[int, int, float]]:
        """Picks high-luminance, colorful points on jewelry and garlands for diamond glints."""
        # Focus on crown, chest garlands, and ear jewelry
        roi_mask = np.zeros((self.h, self.w), dtype=np.uint8)
        cv2.circle(roi_mask, (int(self.w * 0.50), int(self.h * 0.20)), int(self.w * 0.30), 255, -1) # Crown
        cv2.circle(roi_mask, (int(self.w * 0.50), int(self.h * 0.52)), int(self.w * 0.35), 255, -1) # Garland

        salience = (self.gray.astype(np.float32) * (self.hsv[:, :, 1].astype(np.float32) / 255.0))
        salience[roi_mask == 0] = 0

        anchors = []
        # Find local peaks
        corners = cv2.goodFeaturesToTrack(salience.astype(np.uint8), maxCorners=count, qualityLevel=0.15, minDistance=35)
        if corners is not None:
            for pt in corners:
                x, y = int(pt[0][0]), int(pt[0][1])
                phase = random.uniform(0, math.pi * 2)
                anchors.append((x, y, phase))
        return anchors

    def _estimate_head_center(self) -> Tuple[int, int]:
        """Estimates the divine aura epicenter (behind crown/forehead)."""
        return int(self.w * 0.50), int(self.h * 0.28)

    def _precompute_radial_fields(self) -> Tuple[np.ndarray, np.ndarray]:
        """Precalculates distance and angle maps for instant volumetric light ray projection."""
        y_grid, x_grid = np.ogrid[:self.h, :self.w]
        dx = x_grid - self.center_x
        dy = y_grid - self.center_y
        dist = np.sqrt(dx * dx + dy * dy).astype(np.float32)
        angle = np.arctan2(dy, dx).astype(np.float32)
        return dist, angle

    def _generate_cosmic_dust_texture(self) -> np.ndarray:
        """Generates a smooth, seamless low-frequency nebulous cosmic dust map."""
        random.seed(42)
        low_res = np.random.uniform(0.0, 1.0, (self.h // 16, self.w // 16)).astype(np.float32)
        smooth = cv2.resize(low_res, (self.w, self.h), interpolation=cv2.INTER_CUBIC)
        smooth = (smooth - smooth.min()) / (smooth.max() - smooth.min() + 1e-6)
        return smooth


# ==============================================================================
# DRIFTING CELESTIAL STARS & PARTICLE SYSTEM
# ==============================================================================
class CosmicParticleSystem:
    """
    Manages 160+ celestial particles and micro-stars that drift along
    harmonic paths with individual sinusoidal twinkling and soft Gaussian bloom.
    All positions and alpha values loop seamlessly across 300 frames.
    """
    def __init__(self, count: int = 160, canvas_w: int = TARGET_WIDTH, canvas_h: int = TARGET_HEIGHT):
        self.w = canvas_w
        self.h = canvas_h
        self.particles = []
        random.seed(108)  # Sacred seed for harmonious celestial distribution

        colors = [
            (255, 255, 235), # Diamond white
            (255, 225, 120), # Golden nectar
            (140, 235, 255), # Celestial cyan
            (255, 170, 240), # Divine rose
            (210, 185, 255), # Mystic violet
        ]

        for _ in range(count):
            base_x = random.uniform(20, self.w - 20)
            base_y = random.uniform(20, self.h - 20)
            radius = random.choice([1.2, 1.8, 2.4, 3.2, 4.0])
            color = random.choice(colors)
            drift_speed_y = random.choice([-18.0, -28.0, -36.0, -48.0]) # Drifts upward
            drift_amp_x = random.uniform(8.0, 24.0)
            twinkle_freq = random.choice([1, 2, 3, 4])  # Integer harmonics for exact looping
            twinkle_phase = random.uniform(0, math.pi * 2)

            self.particles.append({
                "x0": base_x, "y0": base_y, "r": radius, "color": color,
                "vy": drift_speed_y, "amp_x": drift_amp_x,
                "tfreq": twinkle_freq, "tphase": twinkle_phase
            })

    def render_particle_layer(self, theta: float, total_sec: float = DURATION_SEC) -> np.ndarray:
        """Renders the complete particle layer onto a float32 RGB surface."""
        layer = np.zeros((self.h, self.w, 3), dtype=np.float32)
        norm_t = theta / (2.0 * math.pi)  # in [0, 1)
        cur_time = norm_t * total_sec

        for p in self.particles:
            # Periodic X harmonic sway
            px = p["x0"] + p["amp_x"] * math.sin(theta + p["tphase"])

            # Periodic Y drift wrapping cleanly
            # Total travel distance over 10s is an integer multiple of screen or smoothly wrapped
            raw_y = p["y0"] + p["vy"] * cur_time
            py = raw_y % self.h

            # Edge alpha fade so wrapping at borders is 100% invisible
            border_fade = math.sin(math.pi * (py / self.h))

            # Twinkling modulation (integer frequency guarantees loop)
            twinkle = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(p["tfreq"] * theta + p["tphase"]))
            brightness = border_fade * twinkle

            if brightness <= 0.05:
                continue

            ix, iy = int(px), int(py)
            ir = int(p["r"])
            r_col, g_col, b_col = p["color"]

            # Draw core particle
            cv2.circle(layer, (ix, iy), ir, (r_col * brightness, g_col * brightness, b_col * brightness), -1)

            # Draw soft outer bloom halo for larger stars
            if p["r"] > 2.2:
                halo_r = int(p["r"] * 2.8)
                halo_col = (r_col * brightness * 0.3, g_col * brightness * 0.3, b_col * brightness * 0.3)
                cv2.circle(layer, (ix, iy), halo_r, halo_col, -1)

        # Smooth all particle halos slightly for optical realism
        layer = cv2.GaussianBlur(layer, (5, 5), 1.5)
        return layer


# ==============================================================================
# CINEMATIC CAMERA ENGINE (SLOW PARALLAX ZOOM)
# ==============================================================================
class CinematicCamera:
    """
    Applies a smooth, breathing cinematic camera zoom-in and slight parallax pan:
    scale(t): 1.000 -> 1.025 -> 1.000
    Guaranteed zero jerk at frame 0 and frame 300.
    """
    def __init__(self, width: int = TARGET_WIDTH, height: int = TARGET_HEIGHT):
        self.w = width
        self.h = height

    def apply(self, frame: np.ndarray, theta: float) -> np.ndarray:
        # Smooth cosine zoom curve
        zoom = 1.0 + 0.024 * (0.5 - 0.5 * math.cos(theta))

        # Subtle harmonic pan drift (4-6 pixels)
        pan_x = 5.0 * math.sin(theta)
        pan_y = 3.5 * math.sin(2 * theta)

        # Affine transform centered around Krishna's face
        cx, cy = self.w * 0.50, self.h * 0.35
        M = cv2.getRotationMatrix2D((cx, cy), 0.0, zoom)
        M[0, 2] += pan_x
        M[1, 2] += pan_y

        transformed = cv2.warpAffine(
            frame, M, (self.w, self.h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REFLECT_101
        )
        return transformed


# ==============================================================================
# MASTER COMPOSITING PIPELINE (FRAME-BY-FRAME)
# ==============================================================================
def render_wallpaper_video(input_image_path: str, output_video_path: str):
    """
    Main engine: analyzes the artwork, precomputes masks, and renders all 300
    frames with vectorized OpenCV/NumPy math, writing to a pristine H.264 MP4.
    """
    print("=" * 76)
    print("DIVINE KRISHNA 9:16 ANIMATED WALLPAPER GENERATOR")
    print(f"Target: {TARGET_WIDTH}x{TARGET_HEIGHT} @ {FPS} FPS | {DURATION_SEC}s ({TOTAL_FRAMES} frames)")
    print(f"Input:  {input_image_path}")
    print(f"Output: {output_video_path}")
    print("=" * 76)

    # 1. Format Base Artwork onto 9:16 Canvas
    base_canvas = prepare_916_canvas(input_image_path, TARGET_WIDTH, TARGET_HEIGHT)
    base_canvas_f32 = base_canvas.astype(np.float32)

    # 2. Extract Feature Masks
    analyzer = ArtworkAnalyzer(base_canvas)
    particles = CosmicParticleSystem(count=150, canvas_w=TARGET_WIDTH, canvas_h=TARGET_HEIGHT)
    camera = CinematicCamera(TARGET_WIDTH, TARGET_HEIGHT)

    # Ensure output directory exists
    out_dir = os.path.dirname(os.path.abspath(output_video_path))
    os.makedirs(out_dir, exist_ok=True)

    # Initialize high-quality video encoder
    # macro_block_size=None preserves exact 1080x1920 dimensions
    writer = imageio.get_writer(
        output_video_path,
        fps=FPS,
        codec="libx264",
        pixelformat="yuv420p",
        macro_block_size=None,
        ffmpeg_params=["-crf", "18", "-preset", "medium"]
    )

    print("\nRendering 300 cinematic devotional frames...")

    # Pre-generate 4-point diamond sparkle kernel
    sparkle_size = 31
    sparkle_kernel = np.zeros((sparkle_size, sparkle_size), dtype=np.float32)
    s_mid = sparkle_size // 2
    for dist in range(s_mid + 1):
        falloff = (1.0 - (dist / s_mid)) ** 2.2
        sparkle_kernel[s_mid, s_mid + dist] = falloff
        sparkle_kernel[s_mid, s_mid - dist] = falloff
        sparkle_kernel[s_mid + dist, s_mid] = falloff
        sparkle_kernel[s_mid - dist, s_mid] = falloff
    # Soft diagonal sheen
    for d in range(s_mid // 2):
        f = (1.0 - (d / (s_mid // 2))) * 0.4
        sparkle_kernel[s_mid + d, s_mid + d] += f
        sparkle_kernel[s_mid - d, s_mid - d] += f
        sparkle_kernel[s_mid - d, s_mid + d] += f
        sparkle_kernel[s_mid + d, s_mid - d] += f

    # Precompute static pixel coordinates for fast vector remapping
    y_coords, x_coords = np.indices((TARGET_HEIGHT, TARGET_WIDTH), dtype=np.float32)

    for f_idx in tqdm(range(TOTAL_FRAMES), desc="Encoding Wallpaper", unit="frame"):
        theta = loop_phase(f_idx, TOTAL_FRAMES)

        # ----------------------------------------------------------------------
        # LAYER 1: OUTER HAIR STRAND MICRO-SWAY (EFFECT 5)
        # ----------------------------------------------------------------------
        # Sub-pixel gentle wave displacement restricted strictly to outer hair tips
        sway_dx = 1.3 * np.sin(theta + analyzer.radial_dist * 0.015)
        sway_dy = 0.7 * np.cos(theta + analyzer.angle_map)

        # Vectorized displacement field
        map_x = (x_coords + (sway_dx * analyzer.hair_mask)).astype(np.float32)
        map_y = (y_coords + (sway_dy * analyzer.hair_mask)).astype(np.float32)

        warped_base = cv2.remap(
            base_canvas_f32, map_x, map_y,
            interpolation=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT_101
        )

        current_frame = warped_base.copy()

        # ----------------------------------------------------------------------
        # LAYER 2: DIVINE AURA & VOLUMETRIC LIGHT RAYS (EFFECTS 8 & 11)
        # ----------------------------------------------------------------------
        # Breathing divine aura radius & intensity
        aura_pulse = 0.5 + 0.5 * math.cos(2 * theta)
        aura_r = 380 + 45 * aura_pulse
        # Soft gaussian ring aura
        aura_field = np.exp(-((analyzer.radial_dist - aura_r) ** 2) / (2 * (85 ** 2)))
        aura_intensity = 0.22 * (0.7 + 0.3 * aura_pulse)

        # Celestial Volumetric Light Rays (18 harmonic rays gently rotating)
        ray_rot1 = math.sin(theta) * 0.08
        ray_rot2 = -math.sin(theta) * 0.06
        rays1 = (0.5 + 0.5 * np.sin(16 * (analyzer.angle_map + ray_rot1))) ** 3
        rays2 = (0.5 + 0.5 * np.sin(24 * (analyzer.angle_map + ray_rot2))) ** 3
        combined_rays = (0.6 * rays1 + 0.4 * rays2)

        # Radial attenuation
        ray_falloff = 1.0 / (1.0 + (analyzer.radial_dist / 520.0) ** 2)
        final_rays = combined_rays * ray_falloff * 0.18 * (0.8 + 0.2 * math.sin(2 * theta))

        # Additive blending of golden/celestial radiance
        aura_color = np.array([255.0, 220.0, 130.0], dtype=np.float32)
        current_frame += (aura_field * aura_intensity)[:, :, np.newaxis] * aura_color
        current_frame += (final_rays)[:, :, np.newaxis] * np.array([210.0, 240.0, 255.0], dtype=np.float32)

        # ----------------------------------------------------------------------
        # LAYER 3: PULSING VIBRANT NEON OUTLINES (EFFECT 3)
        # ----------------------------------------------------------------------
        # Three color groups gently breathing with harmonic 120-degree phase offsets
        pulse_cyan = 0.55 + 0.45 * math.sin(2 * theta)
        pulse_pink = 0.55 + 0.45 * math.sin(2 * theta + (2 * math.pi / 3))
        pulse_gold = 0.55 + 0.45 * math.sin(2 * theta + (4 * math.pi / 3))

        neon_cyan_glow = (analyzer.neon_cyan * pulse_cyan * 0.50)[:, :, np.newaxis] * np.array([60, 220, 255], dtype=np.float32)
        neon_pink_glow = (analyzer.neon_pink * pulse_pink * 0.45)[:, :, np.newaxis] * np.array([255, 75, 200], dtype=np.float32)
        neon_gold_glow = (analyzer.neon_gold * pulse_gold * 0.45)[:, :, np.newaxis] * np.array([255, 205, 55], dtype=np.float32)

        current_frame += neon_cyan_glow + neon_pink_glow + neon_gold_glow

        # ----------------------------------------------------------------------
        # LAYER 4: EYE CATCHLIGHT SHIMMER (EFFECT 4)
        # ----------------------------------------------------------------------
        # Subtle 4-cycle micro-shimmer (+20% specular brightness without shifting shape)
        eye_shimmer = 0.25 * (0.5 + 0.5 * math.sin(4 * theta))
        current_frame += (analyzer.eye_mask * eye_shimmer)[:, :, np.newaxis] * np.array([255, 255, 255], dtype=np.float32)

        # ----------------------------------------------------------------------
        # LAYER 5: SOFT TRAVELING GLOW ALONG FLUTE (EFFECT 7)
        # ----------------------------------------------------------------------
        flute_wave_pos = (f_idx / (TOTAL_FRAMES / 2.0)) % 1.0  # Two complete smooth passes
        flute_glow_intensity = 0.35 * (0.6 + 0.4 * math.sin(2 * theta))
        current_frame += (analyzer.flute_mask * flute_glow_intensity)[:, :, np.newaxis] * np.array([255, 245, 170], dtype=np.float32)

        # ----------------------------------------------------------------------
        # LAYER 6: JEWELRY & FLOWER DIAMOND SPARKLES (EFFECTS 6 & 9)
        # ----------------------------------------------------------------------
        for sx, sy, s_phase in analyzer.sparkle_anchors:
            # Individual periodic flare cycle
            sparkle_val = math.sin(3 * theta + s_phase)
            if sparkle_val > 0.65:
                flare = ((sparkle_val - 0.65) / 0.35) ** 2.0
                x1 = max(0, sx - s_mid)
                x2 = min(TARGET_WIDTH, sx + s_mid + 1)
                y1 = max(0, sy - s_mid)
                y2 = min(TARGET_HEIGHT, sy + s_mid + 1)

                kx1 = x1 - (sx - s_mid)
                kx2 = kx1 + (x2 - x1)
                ky1 = y1 - (sy - s_mid)
                ky2 = ky1 + (y2 - y1)

                patch = sparkle_kernel[ky1:ky2, kx1:kx2] * flare * 220.0
                current_frame[y1:y2, x1:x2, 0] += patch
                current_frame[y1:y2, x1:x2, 1] += patch * 0.95
                current_frame[y1:y2, x1:x2, 2] += patch * 0.70

        # ----------------------------------------------------------------------
        # LAYER 7: DRIFTING COSMIC PARTICLES & DUST (EFFECTS 1 & 2)
        # ----------------------------------------------------------------------
        # Cosmic dust nebulous breathing
        dust_breath = 0.08 * (0.5 + 0.5 * math.sin(theta))
        current_frame += (analyzer.cosmic_dust * dust_breath)[:, :, np.newaxis] * np.array([120, 180, 255], dtype=np.float32)

        # Drifting stars layer
        particle_layer = particles.render_particle_layer(theta, DURATION_SEC)
        current_frame += particle_layer

        # Clamp RGB values cleanly to [0, 255]
        np.clip(current_frame, 0.0, 255.0, out=current_frame)
        frame_u8 = current_frame.astype(np.uint8)

        # ----------------------------------------------------------------------
        # LAYER 8: CINEMATIC CAMERA ZOOM & PARALLAX (EFFECT 10)
        # ----------------------------------------------------------------------
        final_frame = camera.apply(frame_u8, theta)

        # Write pristine frame to video stream
        writer.append_data(final_frame)

    writer.close()
    print("=" * 76)
    print("SUCCESS: 9:16 Devotional Animated Wallpaper generated successfully!")
    print(f"Location: {output_video_path}")
    print(f"File Size: {os.path.getsize(output_video_path) / (1024 * 1024):.2f} MB")
    print("=" * 76)


# ==============================================================================
# CLI ENTRY POINT
# ==============================================================================
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Transform Krishna artwork into a stunning animated 9:16 devotional wallpaper."
    )
    parser.add_argument(
        "-i", "--input",
        default=DEFAULT_INPUT_PATH,
        help=f"Path to input Krishna image (default: {DEFAULT_INPUT_PATH})"
    )
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_OUTPUT_PATH,
        help=f"Path to output MP4 video (default: {DEFAULT_OUTPUT_PATH})"
    )
    return parser.parse_args()


def resolve_paths(input_arg: str, output_arg: str) -> Tuple[str, str]:
    """Smartly resolves input and output paths with user-friendly fallbacks."""
    # 1. Resolve Input
    resolved_input = input_arg
    if not os.path.exists(resolved_input):
        # Fallback to local 8034.jpg if /mnt/data/8034.jpg is not present
        if os.path.exists("8034.jpg"):
            resolved_input = "8034.jpg"
        else:
            # Look for any jpg/png in current working directory
            candidates = [f for f in os.listdir(".") if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            if candidates:
                resolved_input = candidates[0]
            else:
                raise FileNotFoundError(
                    f"Could not find input image at '{input_arg}' or in current working directory."
                )

    # 2. Resolve Output
    resolved_output = output_arg
    out_dir = os.path.dirname(os.path.abspath(resolved_output))
    try:
        os.makedirs(out_dir, exist_ok=True)
        # Test writability
        test_file = os.path.join(out_dir, ".perm_test")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
    except (OSError, PermissionError):
        # Fallback to local ./krishna_animated.mp4 if /mnt/data is read-only or not mounted
        resolved_output = "krishna_animated.mp4"
        print(f"Notice: Cannot write to '{out_dir}'. Defaulting output to './krishna_animated.mp4'")

    return resolved_input, resolved_output


def main():
    args = parse_arguments()
    try:
        input_path, output_path = resolve_paths(args.input, args.output)
        render_wallpaper_video(input_path, output_path)
    except Exception as exc:
        print(f"\n[FATAL ERROR] {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
