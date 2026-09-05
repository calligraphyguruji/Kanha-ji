"""
================================================================================
           DIVINE JANMASHTAMI 2026 - BAL KRISHNA CINEMATIC ANIMATION
                     Built with Python and Pygame
================================================================================
A complete, visually stunning, standalone night-time Vrindavan animation celebrating
Janmashtami 2026. Features an exquisitely illustrated Bal Krishna (Kanha Ji),
a loving baby calf, a majestic peacock, handcrafted terracotta matki overflowing
with butter, flowing Yamuna waters, glowing moon, flickering diyas, organic fireflies,
procedural Bansuri (flute) synthesizer, and cinematic atmospheric visual effects.

Controls:
  SPACE : Play / Pause animation (or Skip Intro)
  L     : Toggle Diyas and Lanterns
  M     : Toggle Bansuri (Flute) Music
  F     : Toggle Fullscreen
  B     : Toggle Sacred Blessing Card
  H     : Toggle Controls Overlay
  ESC   : Exit
================================================================================
"""

import sys
import os
import math
import random
import time
import datetime
from typing import List, Tuple, Optional

# Ensure pygame and numpy are available
try:
    import pygame
    import numpy as np
except ImportError as e:
    print(f"Error: Missing required dependency ({e}).")
    print("Please install requirements using: pip install pygame numpy")
    sys.exit(1)

# ==============================================================================
# CONSTANTS & CONFIGURATION
# ==============================================================================
# Virtual Canvas Resolution (All rendering occurs on this surface for crisp scaling)
V_WIDTH = 1920
V_HEIGHT = 1080
TARGET_FPS = 60
CURRENT_YEAR = datetime.datetime.now().year

# Palette Definitions
COLOR_SKY_TOP = (6, 8, 28)
COLOR_SKY_MID = (18, 14, 48)
COLOR_SKY_BOT = (36, 22, 68)

COLOR_GOLD_LIGHT = (255, 235, 140)
COLOR_GOLD_MAIN  = (245, 195, 35)
COLOR_GOLD_DARK  = (185, 130, 15)
COLOR_GOLD_SHINE = (255, 255, 210)

COLOR_KRISHNA_BASE  = (105, 168, 228)
COLOR_KRISHNA_LIGHT = (160, 210, 255)
COLOR_KRISHNA_DARK  = (72, 118, 185)
COLOR_KRISHNA_BLUSH = (150, 165, 225)
COLOR_KRISHNA_LIPS  = (228, 95, 112)

COLOR_BUTTER = (255, 253, 240)
COLOR_BUTTER_SHADOW = (235, 230, 205)

COLOR_CLAY_BODY = (184, 88, 54)
COLOR_CLAY_DARK = (130, 52, 28)
COLOR_CLAY_LIGHT = (215, 118, 78)

# ==============================================================================
# PROCEDURAL BANSURI (FLUTE) AUDIO SYNTHESIZER
# ==============================================================================
class BansuriSynthesizer:
    """
    Synthesizes an authentic, peaceful Indian classical Bansuri (bamboo flute)
    melody using pure NumPy mathematics and Pygame mixer sound generation.
    Features natural warm harmonics, gentle breath turbulence, expressive vibrato,
    and graceful meend (portamento / legato sliding between swaras).
    Plays a serene Raag Bhopali / Yaman melody.
    """
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.sound: Optional[pygame.mixer.Sound] = None
        self.channel: Optional[pygame.mixer.Channel] = None
        self.is_playing = False
        self.init_audio()

    def init_audio(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=2, buffer=1024)

            # Check if user provided an external custom bansuri audio file in current directory
            for custom_file in ["bansuri.mp3", "bansuri.wav", "bansuri.ogg", "flute.mp3", "flute.wav"]:
                if os.path.exists(custom_file):
                    self.sound = pygame.mixer.Sound(custom_file)
                    return

            # Otherwise, synthesize a serene Raag Bhopali Bansuri melody
            self.sound = self._generate_procedural_melody()
        except Exception as err:
            print(f"Audio notice: mixer initialized in silent mode ({err})")
            self.sound = None

    def _generate_procedural_melody(self) -> pygame.mixer.Sound:
        sr = self.sample_rate

        # Swara frequencies in Raag Bhopali (Base Sa = E4 ~ 329.63 Hz)
        sa = 329.63
        re = sa * (9/8)    # 370.8 Hz
        ga = sa * (5/4)    # 412.0 Hz
        pa = sa * (3/2)    # 494.4 Hz
        dha = sa * (5/3)   # 549.4 Hz
        sa_high = sa * 2   # 659.2 Hz
        re_high = re * 2   # 741.6 Hz

        # Peaceful Bansuri composition: (note_frequency, duration_in_seconds, target_frequency_for_slide)
        melody = [
            (sa, 1.8, re),
            (re, 1.2, ga),
            (ga, 2.0, ga),
            (pa, 1.5, dha),
            (dha, 1.2, sa_high),
            (sa_high, 2.2, sa_high),
            (dha, 1.2, pa),
            (pa, 1.6, ga),
            (ga, 1.8, re),
            (re, 1.2, sa),
            (sa, 2.5, sa)
        ]

        total_audio = []
        for note_freq, dur, next_freq in melody:
            n_samples = int(dur * sr)
            t = np.linspace(0, dur, n_samples, False)

            # Expressive Indian classical vibrato (5 Hz, gentle 0.8% pitch oscillation)
            vibrato = np.sin(2 * np.pi * 5.0 * t) * (note_freq * 0.008)

            # Meend (gentle graceful pitch glide toward next note near end of note)
            glide_ratio = np.clip((t - (dur - 0.35)) / 0.35, 0.0, 1.0)
            glide = (next_freq - note_freq) * (glide_ratio ** 2)

            freq_track = note_freq + vibrato + glide
            phase = 2 * np.pi * np.cumsum(freq_track) / sr

            # Bamboo flute acoustic harmonic spectrum: dominant fundamental, warm 2nd & 3rd harmonics
            wave = (
                0.62 * np.sin(phase) +
                0.24 * np.sin(2 * phase + 0.3) +
                0.10 * np.sin(3 * phase + 0.6) +
                0.04 * np.sin(4 * phase + 0.9)
            )

            # Soft airy breath noise (characteristic of authentic bamboo bansuri)
            breath = np.random.normal(0, 0.025, n_samples)
            wave += breath

            # Soft attack and expressive decay envelope
            attack_len = int(0.12 * sr)
            decay_len = int(0.18 * sr)
            env = np.ones(n_samples)
            if attack_len < n_samples:
                env[:attack_len] = np.sin(np.linspace(0, np.pi/2, attack_len))
            if decay_len < n_samples:
                env[-decay_len:] = np.cos(np.linspace(0, np.pi/2, decay_len))

            audio_note = wave * env
            total_audio.append(audio_note)

        full_melody = np.concatenate(total_audio)
        # Normalize and convert to 16-bit stereo PCM
        full_melody = full_melody / (np.max(np.abs(full_melody)) + 1e-6)
        pcm = (full_melody * 16000).astype(np.int16)
        stereo_pcm = np.column_stack((pcm, pcm))
        return pygame.sndarray.make_sound(stereo_pcm)

    def play(self):
        if self.sound:
            try:
                self.channel = self.sound.play(loops=-1)
                if self.channel:
                    self.channel.set_volume(0.65)
                self.is_playing = True
            except Exception:
                self.is_playing = False

    def stop(self):
        if self.sound:
            try:
                self.sound.stop()
            except Exception:
                pass
        self.is_playing = False

    def toggle(self) -> bool:
        if self.is_playing:
            self.stop()
        else:
            self.play()
        return self.is_playing


# ==============================================================================
# PARTICLE SYSTEMS & VISUAL FX
# ==============================================================================
class StarSystem:
    """Manages hundreds of twinkling stars and occasional shooting stars."""
    def __init__(self, count: int = 380):
        self.stars = []
        random.seed(108)  # Auspicious seed for beautiful consistent constellation
        for _ in range(count):
            x = random.uniform(0, V_WIDTH)
            y = random.uniform(0, V_HEIGHT * 0.55)
            radius = random.choice([0.9, 1.2, 1.5, 2.0, 2.6])
            # Star color palette: warm gold, diamond white, celestial cyan, soft violet
            color = random.choice([
                (255, 255, 255),
                (255, 245, 205),
                (210, 235, 255),
                (255, 225, 140),
                (220, 205, 255)
            ])
            twinkle_speed = random.uniform(1.2, 3.5)
            twinkle_phase = random.uniform(0, math.pi * 2)
            self.stars.append({
                "x": x, "y": y, "r": radius, "color": color,
                "speed": twinkle_speed, "phase": twinkle_phase
            })
        self.shooting_star = None
        self.next_shooting_star_time = random.uniform(4.0, 10.0)

    def update(self, dt: float, current_time: float):
        if self.shooting_star:
            self.shooting_star["x"] += self.shooting_star["vx"] * dt
            self.shooting_star["y"] += self.shooting_star["vy"] * dt
            self.shooting_star["life"] -= dt
            if self.shooting_star["life"] <= 0:
                self.shooting_star = None
                self.next_shooting_star_time = current_time + random.uniform(6.0, 14.0)
        elif current_time >= self.next_shooting_star_time:
            # Spawn a shooting star streaking across the sky
            start_x = random.uniform(100, V_WIDTH * 0.7)
            start_y = random.uniform(40, 220)
            angle = random.uniform(0.35, 0.65)
            speed = random.uniform(900, 1300)
            dur = random.uniform(0.7, 1.2)
            self.shooting_star = {
                "x": start_x, "y": start_y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": dur,
                "max_life": dur
            }

    def draw(self, surface: pygame.Surface, current_time: float, alpha_scale: float = 1.0):
        if alpha_scale <= 0:
            return
        for s in self.stars:
            brightness = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(current_time * s["speed"] + s["phase"]))
            final_alpha = int(255 * brightness * alpha_scale)
            if final_alpha <= 5:
                continue
            r, g, b = s["color"]
            col = (r, g, b)
            px, py = int(s["x"]), int(s["y"])

            if s["r"] > 1.8:
                # Soft cross-gleam for larger brightest stars
                gleam_len = int(s["r"] * 2.5)
                gleam_col = (r, g, b, min(140, final_alpha))
                glow_surf = pygame.Surface((gleam_len * 2 + 1, gleam_len * 2 + 1), pygame.SRCALPHA)
                pygame.draw.line(glow_surf, gleam_col, (gleam_len, 0), (gleam_len, gleam_len * 2), 1)
                pygame.draw.line(glow_surf, gleam_col, (0, gleam_len), (gleam_len * 2, gleam_len), 1)
                pygame.draw.circle(glow_surf, (255, 255, 255, final_alpha), (gleam_len, gleam_len), int(s["r"]))
                surface.blit(glow_surf, (px - gleam_len, py - gleam_len), special_flags=pygame.BLEND_ADD)
            else:
                pygame.draw.circle(surface, col, (px, py), int(s["r"]))

        # Draw shooting star if active
        if self.shooting_star and alpha_scale > 0.2:
            sx, sy = self.shooting_star["x"], self.shooting_star["y"]
            tail_x = sx - self.shooting_star["vx"] * 0.08
            tail_y = sy - self.shooting_star["vy"] * 0.08
            ratio = max(0.0, min(1.0, self.shooting_star["life"] / max(0.001, self.shooting_star["max_life"])))
            star_alpha = int(255 * ratio)
            streak_surf = pygame.Surface((V_WIDTH, V_HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(streak_surf, (255, 245, 210, star_alpha), (int(tail_x), int(tail_y)), (int(sx), int(sy)), 3)
            pygame.draw.circle(streak_surf, (255, 255, 255, star_alpha), (int(sx), int(sy)), 3)
            surface.blit(streak_surf, (0, 0), special_flags=pygame.BLEND_ADD)


class FireflySystem:
    """Simulates organic bioluminescent fireflies drifting around Vrindavan."""
    def __init__(self, count: int = 42):
        self.fireflies = []
        for _ in range(count):
            self.fireflies.append({
                "x": random.uniform(80, V_WIDTH - 80),
                "y": random.uniform(V_HEIGHT * 0.45, V_HEIGHT * 0.92),
                "vx": random.uniform(-18, 18),
                "vy": random.uniform(-15, 15),
                "size": random.uniform(2.0, 3.8),
                "pulse_speed": random.uniform(1.8, 3.8),
                "pulse_phase": random.uniform(0, math.pi * 2),
                "wander_seed": random.uniform(0, 100)
            })

    def update(self, dt: float, current_time: float):
        for f in self.fireflies:
            # Organic wander using multi-frequency sine wave turbulence
            seed = f["wander_seed"]
            ax = math.sin(current_time * 0.7 + seed) * 14 + math.cos(current_time * 1.5 + seed * 2) * 8
            ay = math.cos(current_time * 0.6 + seed) * 12 + math.sin(current_time * 1.3 + seed * 1.5) * 6
            f["vx"] += ax * dt
            f["vy"] += ay * dt
            # Damping to maintain smooth floating speed
            f["vx"] *= 0.96
            f["vy"] *= 0.96
            f["x"] += f["vx"] * dt
            f["y"] += f["vy"] * dt

            # Soft boundaries
            if f["x"] < 50: f["x"] = 50; f["vx"] *= -1
            if f["x"] > V_WIDTH - 50: f["x"] = V_WIDTH - 50; f["vx"] *= -1
            if f["y"] < V_HEIGHT * 0.40: f["y"] = V_HEIGHT * 0.40; f["vy"] *= -1
            if f["y"] > V_HEIGHT * 0.95: f["y"] = V_HEIGHT * 0.95; f["vy"] *= -1

    def draw(self, surface: pygame.Surface, current_time: float, alpha_scale: float = 1.0):
        if alpha_scale <= 0:
            return
        for f in self.fireflies:
            glow_intensity = 0.5 + 0.5 * math.sin(current_time * f["pulse_speed"] + f["pulse_phase"])
            glow_intensity = glow_intensity ** 1.8  # Sharpen pulse like real fireflies
            alpha = int(240 * glow_intensity * alpha_scale)
            if alpha <= 4:
                continue

            glow_radius = int(f["size"] * 5.5)
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)

            # Outer soft golden-green aura
            aura_color = (195, 255, 80, int(alpha * 0.35))
            pygame.draw.circle(glow_surf, aura_color, (glow_radius, glow_radius), glow_radius)

            # Mid warm glow
            mid_color = (235, 255, 140, int(alpha * 0.75))
            pygame.draw.circle(glow_surf, mid_color, (glow_radius, glow_radius), int(glow_radius * 0.5))

            # Bright intense core
            core_color = (255, 255, 220, alpha)
            pygame.draw.circle(glow_surf, core_color, (glow_radius, glow_radius), int(f["size"] * 0.8))

            surface.blit(glow_surf, (int(f["x"] - glow_radius), int(f["y"] - glow_radius)), special_flags=pygame.BLEND_ADD)


class ParticleSystem:
    """Manages divine floating golden aura particles around Kanha Ji and sacred dust."""
    def __init__(self):
        self.particles = []

    def update(self, dt: float, kanha_pos: Tuple[float, float]):
        # Continuously emit subtle golden aura particles around Kanha Ji
        if random.random() < 0.85:
            offset_x = random.gauss(0, 110)
            offset_y = random.gauss(0, 120)
            self.particles.append({
                "x": kanha_pos[0] + offset_x,
                "y": kanha_pos[1] + 60 + offset_y,
                "vx": random.uniform(-12, 12),
                "vy": random.uniform(-35, -15),
                "size": random.uniform(1.8, 3.6),
                "life": random.uniform(2.5, 4.2),
                "max_life": 4.0,
                "drift_seed": random.uniform(0, 10)
            })

        # Update existing particles
        for p in self.particles[:]:
            p["life"] -= dt
            if p["life"] <= 0:
                self.particles.remove(p)
                continue
            p["x"] += (p["vx"] + math.sin(p["life"] * 3.0 + p["drift_seed"]) * 15) * dt
            p["y"] += p["vy"] * dt

    def draw(self, surface: pygame.Surface, alpha_scale: float = 1.0):
        if alpha_scale <= 0:
            return
        for p in self.particles:
            ratio = p["life"] / p["max_life"]
            # Fade in then fade out smoothly
            alpha_factor = math.sin(ratio * math.pi)
            alpha = int(220 * alpha_factor * alpha_scale)
            if alpha <= 4:
                continue

            r = int(p["size"])
            glow_surf = pygame.Surface((r * 6, r * 6), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 215, 60, int(alpha * 0.35)), (r * 3, r * 3), r * 3)
            pygame.draw.circle(glow_surf, (255, 245, 180, alpha), (r * 3, r * 3), r)
            surface.blit(glow_surf, (int(p["x"] - r * 3), int(p["y"] - r * 3)), special_flags=pygame.BLEND_ADD)


# ==============================================================================
# ENVIRONMENT: BACKGROUND, MOON, TEMPLES, YAMUNA, TREES
# ==============================================================================
class Background:
    """
    Renders the night-time Vrindavan setting:
    - Celestial gradient sky
    - Radiant full moon with soft multi-layered volumetric halos
    - Drifting moonlit clouds
    - Distant illuminated Vrindavan temple silhouettes and spires
    - Framing ancient Kadamba trees with swaying leaves
    """
    def __init__(self):
        self._static_sky = self._precompute_sky()
        self._distant_temples = self._precompute_temples()
        self.clouds = [
            {"x": 200, "y": 140, "speed": 12, "scale": 1.1, "alpha": 75},
            {"x": 750, "y": 190, "speed": 18, "scale": 1.4, "alpha": 95},
            {"x": 1350, "y": 160, "speed": 14, "scale": 1.25, "alpha": 85},
            {"x": 1850, "y": 120, "speed": 10, "scale": 1.0, "alpha": 65},
        ]
        # Pre-cache soft moon glow surfaces
        self.moon_x = 1280
        self.moon_y = 210
        self.moon_r = 68
        self._moon_halo = self._create_moon_halo()

    def _precompute_sky(self) -> pygame.Surface:
        surf = pygame.Surface((V_WIDTH, V_HEIGHT))
        for y in range(V_HEIGHT):
            t = y / V_HEIGHT
            if t < 0.5:
                sub_t = t / 0.5
                r = int(COLOR_SKY_TOP[0] * (1 - sub_t) + COLOR_SKY_MID[0] * sub_t)
                g = int(COLOR_SKY_TOP[1] * (1 - sub_t) + COLOR_SKY_MID[1] * sub_t)
                b = int(COLOR_SKY_TOP[2] * (1 - sub_t) + COLOR_SKY_MID[2] * sub_t)
            else:
                sub_t = (t - 0.5) / 0.5
                r = int(COLOR_SKY_MID[0] * (1 - sub_t) + COLOR_SKY_BOT[0] * sub_t)
                g = int(COLOR_SKY_MID[1] * (1 - sub_t) + COLOR_SKY_BOT[1] * sub_t)
                b = int(COLOR_SKY_MID[2] * (1 - sub_t) + COLOR_SKY_BOT[2] * sub_t)
            pygame.draw.line(surf, (r, g, b), (0, y), (V_WIDTH, y))
        return surf

    def _create_moon_halo(self) -> pygame.Surface:
        halo_size = 600
        surf = pygame.Surface((halo_size, halo_size), pygame.SRCALPHA)
        center = (halo_size // 2, halo_size // 2)
        # Multi-stage radial bloom falloff
        for r in range(halo_size // 2, 0, -6):
            ratio = 1.0 - (r / (halo_size // 2))
            alpha = int(70 * (ratio ** 2.5))
            pygame.draw.circle(surf, (230, 240, 255, alpha), center, r)
        return surf

    def _precompute_temples(self) -> pygame.Surface:
        surf = pygame.Surface((V_WIDTH, V_HEIGHT), pygame.SRCALPHA)
        # Horizon base at y=560
        base_y = 560

        # Temple silhouettes: Nagara style shikharas, domes, and ghat pavilions
        temple_profiles = [
            (280, base_y, 90, 190),
            (380, base_y, 110, 240),
            (500, base_y, 70, 150),
            (1450, base_y, 80, 170),
            (1560, base_y, 120, 250),
            (1700, base_y, 95, 200),
        ]

        temple_col = (18, 20, 48, 230)
        rim_col = (130, 160, 210, 180)
        window_col = (255, 210, 100, 220)

        for cx, cy, w, h in temple_profiles:
            half_w = w // 2
            # Curved shikhara spire points
            points = [
                (cx - half_w, cy),
                (cx - half_w * 0.9, cy - h * 0.4),
                (cx - half_w * 0.6, cy - h * 0.75),
                (cx - half_w * 0.25, cy - h * 0.92),
                (cx, cy - h), # Pinnacle (Kalash)
                (cx + half_w * 0.25, cy - h * 0.92),
                (cx + half_w * 0.6, cy - h * 0.75),
                (cx + half_w * 0.9, cy - h * 0.4),
                (cx + half_w, cy),
            ]
            pygame.draw.polygon(surf, temple_col, points)
            # Kalash finial
            pygame.draw.circle(surf, rim_col, (cx, int(cy - h)), 5)
            pygame.draw.line(surf, rim_col, (cx, int(cy - h - 12)), (cx, int(cy - h)), 2)

            # Moonlit rim highlight on upper shikhara
            pygame.draw.lines(surf, rim_col, False, points[3:6], 2)

            # Warm glowing temple window (darshan deepak)
            win_y = int(cy - h * 0.35)
            pygame.draw.rect(surf, window_col, (cx - 5, win_y, 10, 14), border_radius=4)

        return surf

    def update(self, dt: float):
        # Update clouds drifting across sky
        for c in self.clouds:
            c["x"] += c["speed"] * dt
            if c["x"] > V_WIDTH + 250:
                c["x"] = -250

    def draw_sky_and_moon(self, surface: pygame.Surface, current_time: float, intro_progress: float = 1.0):
        # Base sky
        surface.blit(self._static_sky, (0, 0))

        # Moon elevation during intro
        moon_rise_offset = (1.0 - min(1.0, intro_progress * 1.3)) * 220
        actual_moon_y = self.moon_y + moon_rise_offset

        # Soft volumetric moon halo bloom
        halo_pos = (int(self.moon_x - 300), int(actual_moon_y - 300))
        surface.blit(self._moon_halo, halo_pos, special_flags=pygame.BLEND_ADD)

        # Draw Moon disc
        moon_surf = pygame.Surface((self.moon_r * 2 + 10, self.moon_r * 2 + 10), pygame.SRCALPHA)
        center = (self.moon_r + 5, self.moon_r + 5)
        # Smooth antialiased bright disc
        pygame.draw.circle(moon_surf, (255, 255, 245), center, self.moon_r)
        # Soft moon surface craters (mare textures)
        craters = [
            (-18, -12, 16), (15, -22, 14), (22, 10, 18),
            (-8, 20, 20), (5, 5, 12), (-24, 8, 10)
        ]
        for ox, oy, cr in craters:
            pygame.draw.circle(moon_surf, (230, 232, 240, 75), (center[0] + ox, center[1] + oy), cr)

        # Moon rim illumination
        pygame.draw.circle(moon_surf, (255, 255, 255), center, self.moon_r, width=2)
        surface.blit(moon_surf, (int(self.moon_x - self.moon_r - 5), int(actual_moon_y - self.moon_r - 5)))

        # Drifting soft moonlit clouds
        for c in self.clouds:
            self._draw_cloud(surface, c["x"], c["y"] + moon_rise_offset * 0.4, c["scale"], c["alpha"])

        # Distant temples
        surface.blit(self._distant_temples, (0, 0))

    def _draw_cloud(self, surface: pygame.Surface, cx: float, cy: float, scale: float, base_alpha: int):
        cloud_surf = pygame.Surface((int(320 * scale), int(120 * scale)), pygame.SRCALPHA)
        color = (200, 215, 245, base_alpha)
        # Composition of multiple overlapping soft puffs
        puffs = [
            (60, 60, 45), (110, 45, 55), (170, 40, 60),
            (230, 55, 50), (140, 75, 45)
        ]
        for px, py, pr in puffs:
            pygame.draw.circle(
                cloud_surf, color,
                (int(px * scale), int(py * scale)),
                int(pr * scale)
            )
        surface.blit(cloud_surf, (int(cx - 160 * scale), int(cy - 60 * scale)))

    def draw_framing_trees(self, surface: pygame.Surface, current_time: float):
        """Draws magnificent Kadamba trees on the left and right framing Vrindavan."""
        sway = math.sin(current_time * 1.2) * 5

        # --- LEFT KADAMBA TREE ---
        # Trunk
        trunk_left = [
            (-60, V_HEIGHT), (120, V_HEIGHT),
            (160, 780), (130, 560), (70, 320),
            (0, 150), (-120, 150), (-60, 500)
        ]
        pygame.draw.polygon(surface, (18, 14, 26), trunk_left)
        # Bark highlight
        pygame.draw.lines(surface, (38, 28, 48), False, [(120, V_HEIGHT), (160, 780), (130, 560), (70, 320)], 4)

        # Foliage Clusters (Left)
        leaf_clusters_left = [
            (-20, 120, 220), (110 + sway, 160, 170),
            (60 + sway * 0.8, 300, 190), (180 + sway * 0.7, 360, 150),
            (90, 480, 140), (-30, 380, 180)
        ]
        for lx, ly, lr in leaf_clusters_left:
            self._draw_leaf_puff(surface, lx, ly, lr, (22, 34, 32), (36, 58, 50))

        # --- RIGHT KADAMBA TREE ---
        trunk_right = [
            (V_WIDTH + 60, V_HEIGHT), (V_WIDTH - 120, V_HEIGHT),
            (V_WIDTH - 150, 780), (V_WIDTH - 130, 550), (V_WIDTH - 80, 330),
            (V_WIDTH + 20, 140), (V_WIDTH + 140, 140)
        ]
        pygame.draw.polygon(surface, (18, 14, 26), trunk_right)
        pygame.draw.lines(surface, (38, 28, 48), False, [(V_WIDTH - 120, V_HEIGHT), (V_WIDTH - 150, 780), (V_WIDTH - 130, 550)], 4)

        leaf_clusters_right = [
            (V_WIDTH - 40 - sway, 130, 230), (V_WIDTH - 160 - sway, 200, 180),
            (V_WIDTH - 110 - sway * 0.8, 330, 190), (V_WIDTH - 190 - sway * 0.7, 400, 150),
            (V_WIDTH - 80, 500, 140)
        ]
        for rx, ry, rr in leaf_clusters_right:
            self._draw_leaf_puff(surface, rx, ry, rr, (22, 34, 32), (36, 58, 50))

    def _draw_leaf_puff(self, surface: pygame.Surface, cx: float, cy: float, r: int,
                        col_dark: Tuple[int, int, int], col_light: Tuple[int, int, int]):
        pygame.draw.circle(surface, col_dark, (int(cx), int(cy)), r)
        # Moonlit top highlight
        pygame.draw.circle(surface, col_light, (int(cx + 8), int(cy - 12)), int(r * 0.75))


# ==============================================================================
# SACRED YAMUNA RIVER & WATER FLOW
# ==============================================================================
class Yamuna:
    """
    Renders the sacred Yamuna River:
    - Deep reflective water with continuous flowing ripple waves
    - Dynamic moonlight reflection dancing directly beneath the moon
    - Floating sacred lotus flowers gently bobbing on the waves
    """
    def __init__(self):
        self.top_y = 530
        self.bot_y = 750
        # Floating lotus flowers on the river
        self.lotuses = [
            {"x": 620, "y": 640, "scale": 0.85, "phase": 0.0},
            {"x": 830, "y": 680, "scale": 1.1, "phase": 1.7},
            {"x": 1050, "y": 650, "scale": 0.95, "phase": 3.2},
            {"x": 1390, "y": 670, "scale": 1.05, "phase": 4.8},
            {"x": 480, "y": 700, "scale": 0.9, "phase": 2.5},
        ]

    def draw(self, surface: pygame.Surface, current_time: float, moon_x: float):
        # Water base background
        water_rect = pygame.Rect(0, self.top_y, V_WIDTH, self.bot_y - self.top_y)
        pygame.draw.rect(surface, (14, 24, 52), water_rect)

        # Flowing water bands with sinusoidal ripples
        for i in range(16):
            band_y = self.top_y + (i / 16) * (self.bot_y - self.top_y)
            depth_ratio = i / 16
            alpha = int(40 + 70 * depth_ratio)
            col = (30, 55, 95, alpha)

            line_surf = pygame.Surface((V_WIDTH, 6), pygame.SRCALPHA)
            offset = math.sin(current_time * 2.2 + i * 0.8) * 8
            for x_seg in range(0, V_WIDTH, 40):
                wave_h = math.sin((x_seg + offset) * 0.03 + current_time * 1.8) * 2.5
                pygame.draw.line(line_surf, col, (x_seg, int(3 + wave_h)), (x_seg + 28, int(3 + wave_h)), 2)
            surface.blit(line_surf, (0, int(band_y)))

        # Dynamic Moonlight Reflection Shimmer (directly beneath the moon)
        ref_surf = pygame.Surface((V_WIDTH, self.bot_y - self.top_y), pygame.SRCALPHA)
        for i in range(24):
            y_rel = (i / 24) * (self.bot_y - self.top_y)
            depth_ratio = i / 24
            # Reflection broadens as it gets closer to viewer
            refl_width = 35 + depth_ratio * 160
            wave_drift = math.sin(current_time * 2.5 + i * 0.6) * (14 + depth_ratio * 20)
            center_x = moon_x + wave_drift

            refl_alpha = int((140 - depth_ratio * 70) * (0.6 + 0.4 * math.sin(current_time * 3.5 + i * 1.2)))
            if refl_alpha > 0:
                bar_rect = pygame.Rect(
                    int(center_x - refl_width / 2),
                    int(y_rel),
                    int(refl_width),
                    3
                )
                pygame.draw.ellipse(ref_surf, (240, 248, 255, refl_alpha), bar_rect)
        surface.blit(ref_surf, (0, self.top_y), special_flags=pygame.BLEND_ADD)

        # Riverbank Stone Ghats (foreground threshold)
        self._draw_stone_ghat(surface)

        # Floating Lotus Flowers
        for lot in self.lotuses:
            bob = math.sin(current_time * 2.0 + lot["phase"]) * 3.5
            self._draw_lotus(surface, lot["x"], lot["y"] + bob, lot["scale"])

    def _draw_stone_ghat(self, surface: pygame.Surface):
        # Ancient stepped stone ghat where Kanha Ji sits peacefully
        ghat_poly = [
            (0, V_HEIGHT), (V_WIDTH, V_HEIGHT),
            (V_WIDTH, 730), (1400, 720), (960, 715),
            (500, 725), (0, 735)
        ]
        pygame.draw.polygon(surface, (28, 26, 36), ghat_poly)
        # Step top edge highlight
        pygame.draw.lines(surface, (55, 50, 70), False, [(0, 735), (500, 725), (960, 715), (1400, 720), (V_WIDTH, 730)], 4)

        # Soft grassy layer with tufts
        grass_poly = [
            (100, V_HEIGHT), (V_WIDTH - 100, V_HEIGHT),
            (V_WIDTH - 180, 770), (960, 755), (200, 775)
        ]
        pygame.draw.polygon(surface, (18, 28, 24), grass_poly)

    def _draw_lotus(self, surface: pygame.Surface, x: float, y: float, scale: float):
        # Lotus Pad
        pad_r = int(22 * scale)
        pygame.draw.ellipse(surface, (28, 64, 48), (int(x - pad_r), int(y + 2), pad_r * 2, int(pad_r * 0.6)))

        # Lotus Petals (soft sacred pink)
        petal_col = (255, 140, 185)
        petal_core = (255, 230, 110)
        # Central cup
        pygame.draw.circle(surface, petal_core, (int(x), int(y - 4 * scale)), int(4 * scale))
        for angle_deg in [-50, -25, 0, 25, 50]:
            rad = math.radians(angle_deg)
            px = x + math.sin(rad) * (14 * scale)
            py = y - 4 * scale - math.cos(rad) * (14 * scale)
            pygame.draw.ellipse(
                surface, petal_col,
                (int(px - 5 * scale), int(py - 10 * scale), int(10 * scale), int(16 * scale))
            )


# ==============================================================================
# DIYAS (TRADITIONAL OIL LAMPS) & HANGING LANTERNS
# ==============================================================================
class Diyas:
    """
    Simulates traditional terracotta oil lamps with realistic multi-harmonic
    flickering flame dynamics, molten wick core, and pulsating warm ambient bloom.
    """
    def __init__(self):
        self.diyas = [
            {"x": 240, "y": 780, "scale": 1.1},
            {"x": 490, "y": 745, "scale": 0.85},
            {"x": 680, "y": 800, "scale": 1.15},
            {"x": 1250, "y": 810, "scale": 1.15},
            {"x": 1420, "y": 750, "scale": 0.9},
            {"x": 1680, "y": 790, "scale": 1.2},
            {"x": 840, "y": 710, "scale": 0.75}, # Floating diya on river
            {"x": 1110, "y": 690, "scale": 0.7},  # Floating diya on river
        ]

    def draw(self, surface: pygame.Surface, current_time: float, active: bool = True, alpha_scale: float = 1.0):
        if not active or alpha_scale <= 0:
            return

        for idx, d in enumerate(self.diyas):
            x, y, s = d["x"], d["y"], d["scale"]

            # Multi-octave natural flame flicker
            flicker = (
                math.sin(current_time * 16.0 + idx * 2.3) * 0.4 +
                math.sin(current_time * 29.0 + idx * 4.7) * 0.3 +
                math.sin(current_time * 7.5 + idx) * 0.3
            )
            flame_h = (22 + flicker * 7) * s
            flame_w = (11 + flicker * 3) * s

            # 1. Warm Ambient Diya Glow (Bloom)
            glow_r = int(55 * s + flicker * 8)
            glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
            halo_alpha = int(120 * alpha_scale)
            pygame.draw.circle(glow_surf, (255, 145, 30, int(halo_alpha * 0.4)), (glow_r, glow_r), glow_r)
            pygame.draw.circle(glow_surf, (255, 205, 75, int(halo_alpha * 0.7)), (glow_r, glow_r), int(glow_r * 0.5))
            surface.blit(glow_surf, (int(x - glow_r), int(y - flame_h - glow_r + 10)), special_flags=pygame.BLEND_ADD)

            # 2. Terracotta Clay Bowl
            bowl_w = int(32 * s)
            bowl_h = int(14 * s)
            pygame.draw.ellipse(surface, (145, 62, 34), (int(x - bowl_w / 2), int(y), bowl_w, bowl_h))
            pygame.draw.ellipse(surface, (185, 88, 48), (int(x - bowl_w / 2 + 2), int(y + 1), bowl_w - 4, bowl_h - 4))
            # Glistening golden oil surface
            pygame.draw.ellipse(surface, (195, 140, 30), (int(x - bowl_w / 2 + 5), int(y + 3), bowl_w - 10, int(bowl_h * 0.55)))

            # 3. Flame Shape (Outer vibrant saffron-gold, inner pure white-hot core)
            flame_pts = [
                (x - flame_w / 2, y + 2),
                (x + flame_w / 2, y + 2),
                (x + flame_w * 0.3 + flicker * 1.5, y - flame_h * 0.6),
                (x + flicker * 2.5, y - flame_h), # Dancing flame tip
                (x - flame_w * 0.3 + flicker * 1.5, y - flame_h * 0.6),
            ]
            pygame.draw.polygon(surface, (255, 140, 20), flame_pts)

            # Inner white flame core
            core_pts = [
                (x - flame_w * 0.25, y + 2),
                (x + flame_w * 0.25, y + 2),
                (x + flicker, y - flame_h * 0.65),
            ]
            pygame.draw.polygon(surface, (255, 255, 230), core_pts)


class Lantern:
    """Hanging traditional brass filigree lanterns with warm glowing light."""
    def __init__(self):
        self.lanterns = [
            {"x": 160, "y": 380, "chain_len": 180},
            {"x": V_WIDTH - 160, "y": 420, "chain_len": 210},
        ]

    def draw(self, surface: pygame.Surface, current_time: float, active: bool = True, alpha_scale: float = 1.0):
        if not active or alpha_scale <= 0:
            return

        for idx, l in enumerate(self.lanterns):
            x, y = l["x"], l["y"]
            chain = l["chain_len"]
            sway = math.sin(current_time * 1.4 + idx * 3.14) * 4

            # Hanging brass chain
            pygame.draw.line(surface, (140, 110, 45), (x, y - chain), (int(x + sway), int(y)), 2)

            lx = int(x + sway)
            ly = int(y)

            # Warm glowing lantern bloom
            glow_r = 90
            glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
            pulse = 0.85 + 0.15 * math.sin(current_time * 5.0 + idx)
            halo_alpha = int(140 * pulse * alpha_scale)
            pygame.draw.circle(glow_surf, (255, 175, 50, int(halo_alpha * 0.3)), (glow_r, glow_r), glow_r)
            pygame.draw.circle(glow_surf, (255, 220, 100, int(halo_alpha * 0.65)), (glow_r, glow_r), int(glow_r * 0.5))
            surface.blit(glow_surf, (lx - glow_r, ly - glow_r), special_flags=pygame.BLEND_ADD)

            # Brass Lantern Cap and Frame
            pygame.draw.polygon(surface, (180, 135, 35), [(lx - 22, ly - 15), (lx + 22, ly - 15), (lx, ly - 35)])
            # Glass body
            pygame.draw.rect(surface, (255, 235, 160), (lx - 18, ly - 15, 36, 42), border_radius=4)
            # Brass cage bars
            pygame.draw.rect(surface, (120, 85, 20), (lx - 18, ly - 15, 36, 42), width=3, border_radius=4)
            pygame.draw.line(surface, (120, 85, 20), (lx, ly - 15), (lx, ly + 27), 2)
            pygame.draw.line(surface, (120, 85, 20), (lx - 18, ly + 6), (lx + 18, ly + 6), 2)
            # Hanging bottom bell
            pygame.draw.circle(surface, (180, 135, 35), (lx, ly + 33), 5)


# ==============================================================================
# TRADITIONAL CLAY MATKI (MAKHAN HANDI)
# ==============================================================================
class Matki:
    """
    Renders the handcrafted terracotta clay pot overflowing with fresh whipped
    white butter (Makhan). Includes ethnic folk art engravings, rope ties,
    thick creamy butter drips, and glistening highlights.
    """
    def __init__(self, x: float = 750, y: float = 800):
        self.x = x
        self.y = y

    def draw(self, surface: pygame.Surface, current_time: float, alpha_scale: float = 1.0):
        if alpha_scale <= 0:
            return

        x, y = int(self.x), int(self.y)

        # 1. Cast Shadow on Ground
        shadow_surf = pygame.Surface((180, 45), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (10, 10, 18, int(150 * alpha_scale)), (0, 0, 180, 45))
        surface.blit(shadow_surf, (x - 90, y + 25))

        # 2. Terracotta Clay Pot Body (Spherical earthen pot)
        pot_surf = pygame.Surface((180, 180), pygame.SRCALPHA)
        center = (90, 100)
        # Base round belly
        pygame.draw.circle(pot_surf, COLOR_CLAY_BODY, center, 65)
        # Deep shade contour on bottom/right
        pygame.draw.circle(pot_surf, COLOR_CLAY_DARK, (center[0] + 10, center[1] + 12), 62)
        # Warm highlight contour on upper left
        pygame.draw.circle(pot_surf, COLOR_CLAY_LIGHT, (center[0] - 12, center[1] - 10), 50)
        # Smooth blended core
        pygame.draw.circle(pot_surf, COLOR_CLAY_BODY, (center[0] - 4, center[1] - 2), 48)

        # Traditional White Folk Art Painted Bands (Geometrical patterns)
        for ring_y in [90, 115]:
            pygame.draw.arc(pot_surf, (245, 240, 230, 180), (35, ring_y - 20, 110, 45), 0.3, 2.8, 3)

        # Neck and Flared Rim
        neck_rect = pygame.Rect(55, 38, 70, 22)
        pygame.draw.rect(pot_surf, COLOR_CLAY_DARK, neck_rect, border_radius=6)
        rim_ellipse = pygame.Rect(45, 28, 90, 24)
        pygame.draw.ellipse(pot_surf, COLOR_CLAY_LIGHT, rim_ellipse)
        pygame.draw.ellipse(pot_surf, COLOR_CLAY_DARK, rim_ellipse, width=3)

        # Sacred Jute Rope (Sutli) tied around neck
        pygame.draw.arc(pot_surf, (210, 175, 110), (52, 42, 76, 16), 0.2, 3.0, 3)

        # 3. Fresh White Butter (Makhan) Overflowing
        # Billowy cloud-like mounds of fresh churned white butter
        butter_puffs = [
            (90, 32, 28), (72, 36, 22), (108, 35, 24),
            (82, 22, 20), (100, 20, 19)
        ]
        for bx, by, br in butter_puffs:
            pygame.draw.circle(pot_surf, COLOR_BUTTER_SHADOW, (bx, by + 2), br)
            pygame.draw.circle(pot_surf, COLOR_BUTTER, (bx, by), br)

        # Luscious Creamy Butter Drip cascading down the pot front
        drip_poly = [
            (82, 44), (98, 44),
            (96, 75), (93, 90), (89, 94), (85, 90), (84, 72)
        ]
        pygame.draw.polygon(pot_surf, COLOR_BUTTER, drip_poly)
        pygame.draw.circle(pot_surf, COLOR_BUTTER, (89, 93), 5)

        # Subtle dynamic Butter Glisten / Shine
        shine_pulse = 0.5 + 0.5 * math.sin(current_time * 3.0)
        shine_alpha = int(220 * shine_pulse)
        pygame.draw.circle(pot_surf, (255, 255, 255, shine_alpha), (82, 22), 4)
        pygame.draw.circle(pot_surf, (255, 255, 255, shine_alpha), (87, 85), 2)

        surface.blit(pot_surf, (x - 90, y - 90))


# ==============================================================================
# SACRED COMPANIONS: CALF (SURABHI) & PEACOCK (MAYUR)
# ==============================================================================
class Calf:
    """
    Renders the adorable divine white baby calf (Gau-Vatsa) resting peacefully
    beside Kanha Ji. Animates gentle ear twitches, soulful eyes looking lovingly
    at Krishna, and a swishing tail.
    """
    def __init__(self, x: float = 1240, y: float = 780):
        self.x = x
        self.y = y

    def draw(self, surface: pygame.Surface, current_time: float, alpha_scale: float = 1.0):
        if alpha_scale <= 0:
            return

        x, y = self.x, self.y

        # Gentle breathing and animations
        breathe = math.sin(current_time * 2.0) * 2.5
        ear_twitch = math.sin(current_time * 3.5) * 6 if (math.sin(current_time * 0.8) > 0.4) else 0
        tail_swish = math.sin(current_time * 2.5) * 14

        # 1. Ground Shadow
        shadow_surf = pygame.Surface((240, 60), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (10, 10, 18, int(140 * alpha_scale)), (0, 0, 240, 60))
        surface.blit(shadow_surf, (x - 120, y + 35))

        # 2. Swishing Tail (Right side)
        tail_start = (x + 85, y + 10)
        tail_end = (x + 115 + tail_swish, y + 35)
        pygame.draw.line(surface, (235, 235, 240), tail_start, tail_end, 5)
        # Tail hair tuft
        pygame.draw.circle(surface, (215, 215, 220), (int(tail_end[0]), int(tail_end[1])), 8)

        # 3. Folded Calf Body (Velvety white with soft warm ivory shading)
        body_rect = pygame.Rect(x - 80, y - 40 + breathe, 175, 85)
        pygame.draw.ellipse(surface, (220, 222, 230), (body_rect.x, body_rect.y + 6, body_rect.w, body_rect.h))
        pygame.draw.ellipse(surface, (250, 250, 255), body_rect)

        # Folded hooves
        pygame.draw.ellipse(surface, (70, 70, 80), (x - 70, y + 36, 26, 15))
        pygame.draw.ellipse(surface, (70, 70, 80), (x + 35, y + 38, 26, 15))

        # 4. Festive Red & Gold Bell Necklace around neck
        neck_pt1 = (x - 45, y - 20 + breathe)
        neck_pt2 = (x - 15, y + 5 + breathe)
        pygame.draw.line(surface, (200, 35, 45), neck_pt1, neck_pt2, 6)
        # Golden tinkling bells
        pygame.draw.circle(surface, COLOR_GOLD_MAIN, (int(x - 30), int(y - 5 + breathe)), 6)

        # 5. Cute Calf Head turned lovingly toward Krishna (facing left)
        head_x = x - 65
        head_y = y - 55 + breathe * 0.7
        # Head base
        head_rect = pygame.Rect(head_x - 30, head_y - 25, 65, 55)
        pygame.draw.ellipse(surface, (250, 250, 255), head_rect)

        # Soft Pink Muzzle / Snout
        muzzle_rect = pygame.Rect(head_x - 48, head_y - 8, 36, 28)
        pygame.draw.ellipse(surface, (245, 195, 205), muzzle_rect)
        # Dark nostrils
        pygame.draw.ellipse(surface, (110, 70, 80), (head_x - 44, head_y + 2, 7, 5))
        pygame.draw.ellipse(surface, (110, 70, 80), (head_x - 34, head_y + 2, 7, 5))

        # 6. Soulful Calf Eye looking at Krishna
        eye_x = int(head_x - 10)
        eye_y = int(head_y - 10)
        pygame.draw.ellipse(surface, (30, 25, 30), (eye_x - 9, eye_y - 7, 18, 14))
        # Loving catchlight
        pygame.draw.circle(surface, (255, 255, 255), (eye_x - 3, eye_y - 3), 3)

        # 7. Twitching Soft Calf Ears
        # Left ear
        ear_angle = math.radians(25 + ear_twitch)
        ex = head_x + 8
        ey = head_y - 18
        ear_poly = [
            (ex, ey),
            (ex + math.cos(ear_angle) * 32, ey - math.sin(ear_angle) * 22),
            (ex + 18, ey - 6)
        ]
        pygame.draw.polygon(surface, (245, 245, 250), ear_poly)
        # Soft pink inner ear
        pygame.draw.polygon(surface, (245, 190, 200), [
            (ex + 3, ey - 2),
            (ex + math.cos(ear_angle) * 25, ey - math.sin(ear_angle) * 16),
            (ex + 12, ey - 4)
        ])


class Peacock:
    """
    Renders the majestic royal Indian Peacock (Mayur) perched gracefully
    on a mossy riverside rock. Animates regal head tilt, breathing, and
    detailed iridescent tail feathers with multiple radiant eyespots (*chandrika*).
    """
    def __init__(self, x: float = 420, y: float = 750):
        self.x = x
        self.y = y

    def draw(self, surface: pygame.Surface, current_time: float, alpha_scale: float = 1.0):
        if alpha_scale <= 0:
            return

        x, y = self.x, self.y
        head_tilt = math.sin(current_time * 1.5) * 3.5
        tail_shimmer = math.sin(current_time * 2.2) * 5

        # 1. Mossy Riverside Perching Rock
        rock_poly = [
            (x - 90, y + 80), (x + 85, y + 80),
            (x + 70, y + 25), (x + 10, y + 10),
            (x - 70, y + 20)
        ]
        pygame.draw.polygon(surface, (34, 38, 42), rock_poly)
        pygame.draw.polygon(surface, (45, 68, 52), [(x - 65, y + 22), (x + 10, y + 12), (x + 65, y + 26), (x + 50, y + 42), (x - 50, y + 40)])

        # 2. Majestic Cascading Tail Train with multiple Peacock Eyespots
        for row in range(5):
            row_y = y + 15 + row * 14
            for col in range(-2, 3):
                px = x - 30 + col * 20 + tail_shimmer * 0.4
                py = row_y + abs(col) * 6
                # Feathery green wing barbs
                pygame.draw.ellipse(surface, (25, 85, 55), (int(px - 14), int(py - 10), 28, 20))
                # Outer gold ring
                pygame.draw.ellipse(surface, COLOR_GOLD_MAIN, (int(px - 9), int(py - 7), 18, 14))
                # Turquoise blue ring
                pygame.draw.ellipse(surface, (20, 145, 185), (int(px - 6), int(py - 5), 12, 10))
                # Royal purple-black iris
                pygame.draw.circle(surface, (25, 15, 65), (int(px), int(py)), 4)

        # 3. Royal Blue Body and Breast
        body_rect = pygame.Rect(x - 25, y - 25, 55, 45)
        pygame.draw.ellipse(surface, (15, 45, 125), body_rect)

        # 4. Regal S-Curved Iridescent Blue Neck
        neck_pts = [
            (x + 5, y - 10),
            (x + 18, y - 35),
            (x + 12, y - 65 + head_tilt),
            (x - 2, y - 60 + head_tilt),
            (x + 2, y - 20)
        ]
        pygame.draw.polygon(surface, (22, 75, 185), neck_pts)

        # 5. Graceful Head with Golden Beak and Crest (Kalgi)
        hx = int(x + 12)
        hy = int(y - 65 + head_tilt)
        pygame.draw.circle(surface, (25, 85, 215), (hx, hy), 12)

        # Eye
        pygame.draw.circle(surface, (255, 255, 255), (hx + 4, hy - 2), 4)
        pygame.draw.circle(surface, (20, 20, 30), (hx + 5, hy - 2), 2)

        # Curved Beak
        beak_pts = [(hx + 8, hy - 3), (hx + 20, hy + 1), (hx + 8, hy + 4)]
        pygame.draw.polygon(surface, (215, 175, 75), beak_pts)

        # Royal Head Crest (3 fan plumes)
        for offset_angle in [-0.35, 0.0, 0.35]:
            plume_x = hx + math.sin(offset_angle) * 16
            plume_y = hy - 12 - math.cos(offset_angle) * 16
            pygame.draw.line(surface, (30, 95, 215), (hx, hy - 10), (int(plume_x), int(plume_y)), 2)
            pygame.draw.circle(surface, (20, 185, 160), (int(plume_x), int(plume_y)), 3)


# ==============================================================================
# MAIN CHARACTER: BAL KRISHNA (KANHA JI)
# ==============================================================================
class Krishna:
    """
    Renders Bal Krishna (Kanha Ji) in an exquisite, respectful, polished
    Indian mythological art style with cute child-like proportions:
    - Soft celestial blue complexion with layered smooth shading
    - Big expressive lotus eyes with natural blinking and gentle gaze shifts
    - Innocent sweet smile with a dab of fresh butter on his lips
    - Glossy midnight-black curls framing his face
    - Sacred Chandan/Kasturi Tilak with vermillion red bindu
    - Regal Golden Mukut (Crown) with ruby accents and an animated peacock feather
    - Flowing golden silk Pitambari dhoti with realistic folds and zari embroidery
    - Pearl necklaces, Kaustubha jewel, golden bangles, armlets, and tinkling anklets
    - One hand enjoying fresh butter from the clay matki
    - Seated gracefully on a royal crimson-and-gold asana
    """
    def __init__(self, x: float = 960, y: float = 690):
        self.x = x
        self.y = y
        self.blink_timer = random.uniform(3.0, 5.0)
        self.is_blinking = False
        self.blink_progress = 0.0
        self.gaze_angle = 0.0  # Gaze shift toward viewer or butter

    def update(self, dt: float):
        # Update blinking state
        self.blink_timer -= dt
        if self.blink_timer <= 0:
            self.is_blinking = True
            self.blink_progress += dt * 8.0  # Fast, natural blink
            if self.blink_progress >= 1.0:
                self.is_blinking = False
                self.blink_progress = 0.0
                self.blink_timer = random.uniform(3.5, 6.0)

    def draw(self, surface: pygame.Surface, current_time: float, alpha_scale: float = 1.0):
        if alpha_scale <= 0:
            return

        x, y = self.x, self.y

        # Gentle breathing motion (expands chest and shoulders smoothly)
        breathe = math.sin(current_time * 1.8) * 3.2
        # Dynamic peacock feather sway
        feather_sway = math.sin(current_time * 1.5) * 6.5

        # ----------------------------------------------------------------------
        # 1. ROYAL EMBROIDERED ASANA (SEATING CARPET)
        # ----------------------------------------------------------------------
        asana_w, asana_h = 320, 65
        asana_rect = pygame.Rect(x - asana_w / 2, y + 105, asana_w, asana_h)
        # Deep royal crimson velvet with gold zari border
        pygame.draw.ellipse(surface, (140, 20, 35), asana_rect)
        pygame.draw.ellipse(surface, COLOR_GOLD_MAIN, asana_rect, width=5)
        # Golden tassel fringes
        for tx in range(int(x - asana_w / 2 + 25), int(x + asana_w / 2 - 20), 20):
            pygame.draw.circle(surface, COLOR_GOLD_SHINE, (tx, int(y + 135)), 3)

        # ----------------------------------------------------------------------
        # 2. SEATED LEGS & PITAMBARI (GOLDEN SILK DHOTI)
        # ----------------------------------------------------------------------
        # Sitting naturally in sukhasana / royal ease
        dhoti_base_rect = pygame.Rect(x - 110, y + 55, 220, 75)
        pygame.draw.ellipse(surface, (215, 150, 20), dhoti_base_rect) # Shadow
        pygame.draw.ellipse(surface, COLOR_GOLD_MAIN, (dhoti_base_rect.x, dhoti_base_rect.y - 4, dhoti_base_rect.w, dhoti_base_rect.h))

        # Silk Fabric Folds
        for fx in [-65, -25, 15, 55]:
            pygame.draw.arc(surface, (190, 125, 15), (x + fx - 25, y + 60, 50, 55), 0.2, 2.9, 3)

        # Red & Gold Embroidered Border (Zari) along dhoti hem
        pygame.draw.arc(surface, (185, 30, 45), (x - 100, y + 70, 200, 55), 3.2, 6.2, 4)

        # Cute chubby left foot peeking out from dhoti with golden anklet
        foot_x, foot_y = int(x + 75), int(y + 98)
        pygame.draw.ellipse(surface, COLOR_KRISHNA_BASE, (foot_x - 18, foot_y - 12, 36, 24))
        # Rounded toes
        for toe_i in range(5):
            tx = foot_x + 10 + toe_i * 3
            ty = foot_y - 8 + toe_i * 3
            pygame.draw.circle(surface, COLOR_KRISHNA_LIGHT, (tx, ty), 4 - int(toe_i * 0.5))

        # Golden Payal (Anklet) with tinkling bells
        pygame.draw.ellipse(surface, COLOR_GOLD_MAIN, (foot_x - 16, foot_y - 10, 28, 12), width=3)
        pygame.draw.circle(surface, COLOR_GOLD_SHINE, (foot_x - 6, foot_y + 2), 3)

        # ----------------------------------------------------------------------
        # 3. CHUBBY TORSO & ARMS
        # ----------------------------------------------------------------------
        torso_y = y - 10 + breathe
        # Soft blue torso
        torso_rect = pygame.Rect(x - 48, torso_y - 10, 96, 85)
        pygame.draw.ellipse(surface, COLOR_KRISHNA_DARK, (torso_rect.x, torso_rect.y + 4, torso_rect.w, torso_rect.h))
        pygame.draw.ellipse(surface, COLOR_KRISHNA_BASE, torso_rect)
        # Soft celestial chest highlight
        pygame.draw.ellipse(surface, COLOR_KRISHNA_LIGHT, (x - 30, torso_y - 6, 60, 42))

        # Cute toddler tummy & navel
        pygame.draw.ellipse(surface, COLOR_KRISHNA_BASE, (x - 35, torso_y + 25, 70, 40))
        pygame.draw.circle(surface, COLOR_KRISHNA_DARK, (int(x), int(torso_y + 44)), 3)

        # Jeweled Waistband (Kamarbandh)
        pygame.draw.arc(surface, COLOR_GOLD_MAIN, (x - 46, torso_y + 48, 92, 24), 0.1, 3.1, 5)
        pygame.draw.circle(surface, (215, 30, 45), (int(x), int(torso_y + 60)), 5) # Ruby central buckle

        # --- LEFT ARM: Resting gently toward Matki ---
        arm_l_pts = [
            (x - 42, torso_y + 5),
            (x - 78, torso_y + 35),
            (x - 110, torso_y + 65),
            (x - 90, torso_y + 78),
            (x - 30, torso_y + 25)
        ]
        pygame.draw.polygon(surface, COLOR_KRISHNA_BASE, arm_l_pts)
        # Left Hand resting playfully
        pygame.draw.circle(surface, COLOR_KRISHNA_BASE, (int(x - 105), int(torso_y + 72)), 12)
        # Golden Bajuband (Armlet) & Kangan (Bangle)
        pygame.draw.ellipse(surface, COLOR_GOLD_MAIN, (x - 68, torso_y + 24, 18, 10), width=3)
        pygame.draw.circle(surface, COLOR_GOLD_MAIN, (int(x - 98), int(torso_y + 68)), 6)

        # --- RIGHT ARM: Bent upward, holding fresh butter near mouth ---
        arm_r_pts = [
            (x + 40, torso_y + 5),
            (x + 75, torso_y + 25),
            (x + 55, torso_y - 25),
            (x + 35, torso_y - 20),
            (x + 30, torso_y + 20)
        ]
        pygame.draw.polygon(surface, COLOR_KRISHNA_BASE, arm_r_pts)
        # Right hand with fingers holding butter
        hand_r_pos = (int(x + 45), int(torso_y - 28))
        pygame.draw.circle(surface, COLOR_KRISHNA_BASE, hand_r_pos, 11)

        # Dollop of fresh white butter in his tiny fingers!
        pygame.draw.circle(surface, COLOR_BUTTER, (hand_r_pos[0] - 2, hand_r_pos[1] - 4), 7)
        pygame.draw.circle(surface, (255, 255, 255), (hand_r_pos[0] - 3, hand_r_pos[1] - 5), 3)

        # Golden Jewelry on Right Arm
        pygame.draw.ellipse(surface, COLOR_GOLD_MAIN, (x + 55, torso_y + 14, 18, 10), width=3)
        pygame.draw.circle(surface, COLOR_GOLD_MAIN, (hand_r_pos[0] + 4, hand_r_pos[1] + 6), 6)

        # ----------------------------------------------------------------------
        # 4. GOLDEN NECKLACES & SACRED KAUSTUBHA JEWEL
        # ----------------------------------------------------------------------
        # Layered Pearl Necklace (Moti Mala)
        for p_i, p_off in enumerate([-28, -18, -8, 0, 8, 18, 28]):
            py_off = abs(p_off) * 0.35
            pygame.draw.circle(surface, (255, 255, 255), (int(x + p_off), int(torso_y + 8 + py_off)), 4)

        # Long Golden Garland with radiant Kaustubha Gem
        pygame.draw.arc(surface, COLOR_GOLD_MAIN, (x - 26, torso_y + 6, 52, 45), 3.2, 6.2, 3)
        # Kaustubha Ruby Pendant
        pendant_y = int(torso_y + 35)
        pygame.draw.circle(surface, COLOR_GOLD_MAIN, (int(x), pendant_y), 7)
        pygame.draw.circle(surface, (220, 25, 45), (int(x), pendant_y), 5) # Radiant ruby
        pygame.draw.circle(surface, (255, 255, 255), (int(x - 2), pendant_y - 2), 2) # Sparkle

        # ----------------------------------------------------------------------
        # 5. ADORABLE HEAD & CHUBBY FACE
        # ----------------------------------------------------------------------
        head_cx = x
        head_cy = y - 65 + breathe * 0.7

        # Curly Midnight-Black Hair Locks (Back Volume)
        for hx_off, hy_off, hr in [
            (-45, -20, 26), (45, -20, 26),
            (-50, 10, 24), (50, 10, 24),
            (-35, 30, 22), (35, 30, 22),
            (-55, -5, 20), (55, -5, 20)
        ]:
            pygame.draw.circle(surface, (18, 16, 24), (int(head_cx + hx_off), int(head_cy + hy_off)), hr)

        # Rounded Chubby Baby Face
        face_rect = pygame.Rect(head_cx - 45, head_cy - 40, 90, 85)
        pygame.draw.ellipse(surface, COLOR_KRISHNA_DARK, (face_rect.x, face_rect.y + 4, face_rect.w, face_rect.h))
        pygame.draw.ellipse(surface, COLOR_KRISHNA_BASE, face_rect)
        # Soft celestial forehead highlight
        pygame.draw.ellipse(surface, COLOR_KRISHNA_LIGHT, (head_cx - 30, head_cy - 36, 60, 45))

        # Soft Rosy Peach Blush on Chubby Cheeks
        cheek_surf = pygame.Surface((34, 24), pygame.SRCALPHA)
        pygame.draw.ellipse(cheek_surf, (240, 130, 150, 85), (0, 0, 34, 24))
        surface.blit(cheek_surf, (int(head_cx - 42), int(head_cy + 5)))
        surface.blit(cheek_surf, (int(head_cx + 8), int(head_cy + 5)))

        # Forehead Hair Curls (Front fringe)
        for fx, fy, fr in [(-28, -35, 14), (28, -35, 14), (-12, -40, 15), (12, -40, 15)]:
            pygame.draw.circle(surface, (22, 18, 28), (int(head_cx + fx), int(head_cy + fy)), fr)
            # Hair luster highlight
            pygame.draw.arc(surface, (70, 75, 100), (int(head_cx + fx - 8), int(head_cy + fy - 8), 16, 16), 0.5, 2.2, 2)

        # ----------------------------------------------------------------------
        # 6. SACRED TILAK (URDHVA PUNDRA & VERMILLION BINDU)
        # ----------------------------------------------------------------------
        tilak_y = head_cy - 32
        # White/Yellow Chandan U-shape
        pygame.draw.line(surface, (255, 245, 205), (head_cx - 5, tilak_y), (head_cx - 2, tilak_y + 16), 2)
        pygame.draw.line(surface, (255, 245, 205), (head_cx + 5, tilak_y), (head_cx + 2, tilak_y + 16), 2)
        pygame.draw.line(surface, (255, 245, 205), (head_cx - 2, tilak_y + 16), (head_cx + 2, tilak_y + 16), 2)
        # Radiant Kumkum / Vermillion Red Bindu in center
        pygame.draw.ellipse(surface, (225, 25, 35), (head_cx - 2, tilak_y + 4, 4, 9))

        # ----------------------------------------------------------------------
        # 7. SOULFUL EYES & INNOCENT SMILE
        # ----------------------------------------------------------------------
        # Gaze tracking calculation
        gaze_x = math.sin(current_time * 0.8) * 1.5

        # --- EYES ---
        eye_y = head_cy - 4
        for eye_side in [-1, 1]:
            ecx = head_cx + eye_side * 22

            if self.is_blinking:
                # Eyelids smoothly closed during blink
                blink_h = (1.0 - math.sin(self.blink_progress * math.pi)) * 6
                pygame.draw.arc(surface, (30, 25, 35), (ecx - 11, eye_y - 4, 22, 10), 0.2, 2.9, 3)
            else:
                # Beautiful almond-shaped eyes with subtle kajal outline
                eye_w, eye_h = 22, 13
                # Sclera (eye white)
                pygame.draw.ellipse(surface, (255, 255, 255), (ecx - eye_w / 2, eye_y - eye_h / 2, eye_w, eye_h))
                # Soft kajal frame
                pygame.draw.ellipse(surface, (30, 25, 35), (ecx - eye_w / 2, eye_y - eye_h / 2, eye_w, eye_h), width=2)
                # Delicate curved eyebrow
                pygame.draw.arc(surface, (30, 25, 35), (ecx - 12, eye_y - 14, 24, 10), 0.3, 2.8, 2)

                # Soulful dark brown iris & pupil
                iris_x = ecx + gaze_x
                pygame.draw.circle(surface, (55, 35, 25), (int(iris_x), int(eye_y)), 5)
                pygame.draw.circle(surface, (10, 10, 15), (int(iris_x), int(eye_y)), 3)

                # Brilliant white catchlights (brings Krishna alive!)
                pygame.draw.circle(surface, (255, 255, 255), (int(iris_x - 2), int(eye_y - 2)), 2)
                pygame.draw.circle(surface, (255, 255, 255), (int(iris_x + 1), int(eye_y + 1)), 1)

        # --- SWEET INNOCENT SMILE ---
        mouth_y = head_cy + 22
        # Soft pink lips
        pygame.draw.arc(surface, COLOR_KRISHNA_LIPS, (head_cx - 12, mouth_y - 6, 24, 14), 3.4, 6.0, 3)
        # Upper lip bow
        pygame.draw.arc(surface, (215, 80, 100), (head_cx - 8, mouth_y - 4, 16, 8), 0.2, 2.9, 2)

        # Tiny dollop of delicious white butter at corner of his smile!
        pygame.draw.circle(surface, COLOR_BUTTER, (int(head_cx + 10), int(mouth_y - 1)), 3)
        pygame.draw.circle(surface, (255, 255, 255), (int(head_cx + 10), int(mouth_y - 1)), 1)

        # Golden Kundal (Earrings)
        pygame.draw.circle(surface, COLOR_GOLD_MAIN, (int(head_cx - 48), int(head_cy + 10)), 6)
        pygame.draw.circle(surface, (255, 255, 255), (int(head_cx - 48), int(head_cy + 18)), 3) # Pearl drop
        pygame.draw.circle(surface, COLOR_GOLD_MAIN, (int(head_cx + 48), int(head_cy + 10)), 6)
        pygame.draw.circle(surface, (255, 255, 255), (int(head_cx + 48), int(head_cy + 18)), 3)

        # ----------------------------------------------------------------------
        # 8. GOLDEN MUKUT (CROWN) & SWAYING PEACOCK FEATHER
        # ----------------------------------------------------------------------
        crown_base_y = head_cy - 44

        # --- PEACOCK FEATHER (MOR PANKH) ---
        # Gracefully mounted behind crown, swaying in breeze
        feather_rad = math.radians(-15 + feather_sway)
        feather_len = 85
        feather_end_x = head_cx - 15 + math.sin(feather_rad) * feather_len
        feather_end_y = crown_base_y - math.cos(feather_rad) * feather_len

        # Quill spine
        pygame.draw.line(surface, (215, 210, 160), (head_cx - 15, crown_base_y), (int(feather_end_x), int(feather_end_y)), 3)

        # Iridescent eye of the peacock feather (Chandrika)
        eye_cx, eye_cy = int(feather_end_x), int(feather_end_y)
        # Outer emerald green barbs
        pygame.draw.ellipse(surface, (22, 135, 80), (eye_cx - 24, eye_cy - 18, 48, 36))
        # Concentric golden-bronze ring
        pygame.draw.ellipse(surface, COLOR_GOLD_MAIN, (eye_cx - 17, eye_cy - 13, 34, 26))
        # Turquoise radiant ring
        pygame.draw.ellipse(surface, (18, 175, 215), (eye_cx - 12, eye_cy - 9, 24, 18))
        # Deep royal midnight-violet pupil
        pygame.draw.circle(surface, (35, 15, 75), (eye_cx, eye_cy), 6)

        # --- GOLDEN MUKUT (CROWN) ---
        crown_pts = [
            (head_cx - 46, crown_base_y + 4),
            (head_cx - 40, crown_base_y - 20),
            (head_cx - 22, crown_base_y - 12),
            (head_cx, crown_base_y - 45),     # Central high peak
            (head_cx + 22, crown_base_y - 12),
            (head_cx + 40, crown_base_y - 20),
            (head_cx + 46, crown_base_y + 4),
        ]
        pygame.draw.polygon(surface, COLOR_GOLD_MAIN, crown_pts)
        pygame.draw.polygon(surface, COLOR_GOLD_DARK, crown_pts, width=3)

        # Embossed temple filigree & ruby gem insets on crown
        pygame.draw.circle(surface, (220, 25, 45), (int(head_cx), int(crown_base_y - 20)), 6) # Central ruby
        pygame.draw.circle(surface, (255, 255, 255), (int(head_cx - 2), int(crown_base_y - 22)), 2)
        pygame.draw.circle(surface, (25, 145, 85), (int(head_cx - 24), int(crown_base_y - 6)), 4) # Emerald
        pygame.draw.circle(surface, (25, 145, 85), (int(head_cx + 24), int(crown_base_y - 6)), 4)

        # Pearl bead band along forehead
        for px_off in range(-38, 40, 8):
            pygame.draw.circle(surface, (255, 255, 255), (head_cx + px_off, int(crown_base_y + 3)), 3)


# ==============================================================================
# CINEMATIC INTRO CONTROLLER & TYPOGRAPHY
# ==============================================================================
class IntroSequence:
    """
    Orchestrates the elegant startup sequence:
    0.0 - 1.5s: Dark screen, stars appear & begin to twinkle
    1.5 - 3.2s: Full moon rises, illuminating Yamuna and clouds
    3.2 - 4.8s: Diyas and lanterns flicker to life
    4.8 - 6.2s: Bal Krishna and companions fade in with golden aura
    6.2 - 7.5s: Golden titles fade in and glow
    7.5s+: Full interactive celebration mode!
    """
    def __init__(self, duration: float = 7.5):
        self.duration = duration
        self.timer = 0.0
        self.finished = False

    def update(self, dt: float):
        if not self.finished:
            self.timer += dt
            if self.timer >= self.duration:
                self.finished = True

    def skip(self):
        self.finished = True
        self.timer = self.duration

    @property
    def star_alpha(self) -> float:
        if self.finished: return 1.0
        return min(1.0, self.timer / 1.5)

    @property
    def moon_progress(self) -> float:
        if self.finished: return 1.0
        if self.timer < 1.5: return 0.0
        return min(1.0, (self.timer - 1.5) / 1.7)

    @property
    def lights_alpha(self) -> float:
        if self.finished: return 1.0
        if self.timer < 3.2: return 0.0
        return min(1.0, (self.timer - 3.2) / 1.6)

    @property
    def krishna_alpha(self) -> float:
        if self.finished: return 1.0
        if self.timer < 4.8: return 0.0
        return min(1.0, (self.timer - 4.8) / 1.4)

    @property
    def title_alpha(self) -> float:
        if self.finished: return 1.0
        if self.timer < 6.2: return 0.0
        return min(1.0, (self.timer - 6.2) / 1.3)


class Typography:
    """Renders the glowing golden English & Sanskrit/Devanagari titles and blessings."""
    def __init__(self):
        # Find best available Devanagari and Serif fonts on the system
        self.font_devanagari = self._load_devanagari_font(46)
        self.font_title = self._load_serif_font(52, bold=True)
        self.font_subtitle = self._load_serif_font(28, bold=False)
        self.font_ui = pygame.font.SysFont("helvetica", 18, bold=True)

    def _load_devanagari_font(self, size: int) -> pygame.font.Font:
        candidates = [
            "/System/Library/Fonts/Supplemental/DevanagariMT.ttc",
            "/System/Library/Fonts/Kohinoor.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/Library/Fonts/Nirmala.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    return pygame.font.Font(path, size)
                except Exception:
                    pass
        # Fallback to system font
        return pygame.font.SysFont("devanagari", size)

    def _load_serif_font(self, size: int, bold: bool = False) -> pygame.font.Font:
        candidates = [
            "/System/Library/Fonts/Supplemental/Baskerville.ttc",
            "/System/Library/Fonts/Supplemental/Georgia.ttf",
            "/System/Library/Fonts/Times.ttc"
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    return pygame.font.Font(path, size)
                except Exception:
                    pass
        return pygame.font.SysFont("georgia", size, bold=bold)

    def draw_golden_text(self, surface: pygame.Surface, text: str, font: pygame.font.Font,
                         center_pos: Tuple[int, int], alpha: float = 1.0):
        if alpha <= 0:
            return

        cx, cy = center_pos

        # 1. Soft Golden Bloom Glow behind text
        glow_surf = font.render(text, True, (255, 215, 60))
        gw, gh = glow_surf.get_size()
        bloom_surf = pygame.Surface((gw + 20, gh + 20), pygame.SRCALPHA)
        bloom_alpha = int(120 * alpha)
        bloom_text = font.render(text, True, (255, 215, 60))
        bloom_text.set_alpha(bloom_alpha)
        # Multi-pass offset blit for soft bloom
        for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2)]:
            bloom_surf.blit(bloom_text, (10 + ox, 10 + oy))
        surface.blit(bloom_surf, (cx - gw // 2 - 10, cy - gh // 2 - 10), special_flags=pygame.BLEND_ADD)

        # 2. Deep Drop Shadow for legibility
        shadow_surf = font.render(text, True, (10, 8, 18))
        shadow_surf.set_alpha(int(220 * alpha))
        surface.blit(shadow_surf, (cx - gw // 2 + 2, cy - gh // 2 + 2))

        # 3. Main Radiant Golden Text
        main_surf = font.render(text, True, (255, 235, 140))
        main_surf.set_alpha(int(255 * alpha))
        surface.blit(main_surf, (cx - gw // 2, cy - gh // 2))

    def draw_titles(self, surface: pygame.Surface, current_time: float, alpha: float = 1.0):
        if alpha <= 0:
            return

        # Pulsing golden aura factor
        pulse = 0.85 + 0.15 * math.sin(current_time * 2.0)
        final_alpha = alpha * pulse

        # Top title: Dynamic "HAPPY JANMASHTAMI <YEAR>"
        self.draw_golden_text(
            surface, f"HAPPY JANMASHTAMI {CURRENT_YEAR}",
            self.font_title, (V_WIDTH // 2, 70), final_alpha
        )

        # Sanskrit sacred chant: "॥ जय श्री कृष्ण ॥"
        self.draw_golden_text(
            surface, "॥ जय श्री कृष्ण ॥",
            self.font_devanagari, (V_WIDTH // 2, 135), final_alpha
        )

    def draw_blessing_card(self, surface: pygame.Surface, alpha: float = 1.0):
        if alpha <= 0:
            return

        card_w, card_h = 960, 110
        cx, cy = V_WIDTH // 2, V_HEIGHT - 75

        # Frosted glass card surface
        card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        pygame.draw.rect(card_surf, (15, 12, 28, int(200 * alpha)), (0, 0, card_w, card_h), border_radius=18)
        pygame.draw.rect(card_surf, (245, 195, 35, int(180 * alpha)), (0, 0, card_w, card_h), width=2, border_radius=18)
        surface.blit(card_surf, (cx - card_w // 2, cy - card_h // 2))

        # Sacred Blessing Text
        self.draw_golden_text(
            surface, "“May Lord Krishna bless you with happiness, peace, prosperity and success.”",
            self.font_subtitle, (cx, cy - 18), alpha
        )
        self.draw_golden_text(
            surface, f"Happy Janmashtami {CURRENT_YEAR} 🌸",
            self.font_subtitle, (cx, cy + 22), alpha
        )


# ==============================================================================
# INTERACTIVE UI BUTTONS
# ==============================================================================
class Button:
    """Polished frosted glass UI button with golden trim, hover states and click events."""
    def __init__(self, rect: pygame.Rect, label: str, shortcut: str):
        self.rect = rect
        self.label = label
        self.shortcut = shortcut
        self.is_hovered = False
        self.is_active = False

    def handle_event(self, event, mouse_canvas_pos: Tuple[int, int]) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(mouse_canvas_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_canvas_pos):
                return True
        return False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        # Button background
        bg_alpha = 220 if self.is_hovered else 160
        border_col = (255, 235, 140) if self.is_hovered else (210, 165, 45)
        text_col = (255, 255, 220) if self.is_hovered else (240, 220, 150)

        btn_surf = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, (20, 16, 35, bg_alpha), (0, 0, self.rect.w, self.rect.h), border_radius=10)
        pygame.draw.rect(btn_surf, border_col, (0, 0, self.rect.w, self.rect.h), width=2, border_radius=10)
        surface.blit(btn_surf, (self.rect.x, self.rect.y))

        # Render Label
        full_text = f"{self.label} [{self.shortcut}]"
        lbl_surf = font.render(full_text, True, text_col)
        lx = self.rect.x + (self.rect.w - lbl_surf.get_width()) // 2
        ly = self.rect.y + (self.rect.h - lbl_surf.get_height()) // 2
        surface.blit(lbl_surf, (lx, ly))


# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================
class JanmashtamiApp:
    """Master application controlling rendering loop, responsive scaling and user inputs."""
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(f"Janmashtami {CURRENT_YEAR} - Bal Krishna (Kanha Ji)")

        # Initial window resolution (responsive: 1280x720 default window, scales to 1920x1080 or fullscreen)
        self.win_width = 1280
        self.win_height = 720
        self.screen = pygame.display.set_mode((self.win_width, self.win_height), pygame.RESIZABLE)
        self.canvas = pygame.Surface((V_WIDTH, V_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_paused = False
        self.is_fullscreen = False
        self.show_blessing = True
        self.lights_active = True
        self.show_help = False

        # Instantiate Scene Systems
        self.bansuri = BansuriSynthesizer()
        self.background = Background()
        self.yamuna = Yamuna()
        self.stars = StarSystem(count=380)
        self.fireflies = FireflySystem(count=42)
        self.particles = ParticleSystem()
        self.diyas = Diyas()
        self.lanterns = Lantern()
        self.matki = Matki(x=760, y=810)
        self.calf = Calf(x=1240, y=780)
        self.peacock = Peacock(x=420, y=750)
        self.krishna = Krishna(x=960, y=690)
        self.intro = IntroSequence(duration=7.5)
        self.typography = Typography()

        # UI Control Buttons (positioned at top right)
        self.buttons = [
            Button(pygame.Rect(V_WIDTH - 660, 25, 145, 42), "♪ Bansuri", "M"),
            Button(pygame.Rect(V_WIDTH - 500, 25, 130, 42), "✦ Lights", "L"),
            Button(pygame.Rect(V_WIDTH - 355, 25, 145, 42), "❀ Blessing", "B"),
            Button(pygame.Rect(V_WIDTH - 195, 25, 165, 42), "[ ] Fullscreen", "F"),
        ]

        # Auto-play soothing bansuri flute melody
        self.bansuri.play()

        # Precompute cinematic vignette
        self._vignette = self._create_vignette()

    def _create_vignette(self) -> pygame.Surface:
        vig = pygame.Surface((V_WIDTH, V_HEIGHT), pygame.SRCALPHA)
        for i in range(18):
            alpha = int(110 * ((18 - i) / 18.0) ** 2)
            inset_x = i * 26
            inset_y = i * 16
            rect = pygame.Rect(inset_x, inset_y, V_WIDTH - inset_x * 2, V_HEIGHT - inset_y * 2)
            pygame.draw.rect(vig, (2, 2, 10, alpha), rect, width=28)
        return vig

    def get_canvas_mouse_pos(self) -> Tuple[int, int]:
        """Converts window mouse coordinates to 1920x1080 virtual canvas coordinates."""
        mx, my = pygame.mouse.get_pos()
        scale_x = V_WIDTH / self.win_width
        scale_y = V_HEIGHT / self.win_height
        return int(mx * scale_x), int(my * scale_y)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.win_width, self.win_height = self.screen.get_size()

    def handle_events(self):
        mouse_canvas_pos = self.get_canvas_mouse_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                if not self.is_fullscreen:
                    self.win_width = max(640, event.w)
                    self.win_height = max(360, event.h)
                    self.screen = pygame.display.set_mode((self.win_width, self.win_height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if not self.intro.finished:
                        self.intro.skip()
                    else:
                        self.is_paused = not self.is_paused
                elif event.key == pygame.K_m:
                    self.bansuri.toggle()
                elif event.key == pygame.K_l:
                    self.lights_active = not self.lights_active
                elif event.key == pygame.K_f:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_b:
                    self.show_blessing = not self.show_blessing
                elif event.key == pygame.K_h:
                    self.show_help = not self.show_help

            # Check Button clicks
            for btn in self.buttons:
                if btn.handle_event(event, mouse_canvas_pos):
                    if btn.shortcut == "M":
                        self.bansuri.toggle()
                    elif btn.shortcut == "L":
                        self.lights_active = not self.lights_active
                    elif btn.shortcut == "B":
                        self.show_blessing = not self.show_blessing
                    elif btn.shortcut == "F":
                        self.toggle_fullscreen()

    def update(self, dt: float, current_time: float):
        if self.is_paused:
            return

        self.intro.update(dt)
        self.background.update(dt)
        self.stars.update(dt, current_time)
        self.fireflies.update(dt, current_time)
        self.particles.update(dt, (self.krishna.x, self.krishna.y))
        self.krishna.update(dt)

    def draw(self, current_time: float):
        # 1. Sky & Full Moon (animated elevation during intro)
        self.background.draw_sky_and_moon(self.canvas, current_time, self.intro.moon_progress)

        # 2. Twinkling Stars
        self.stars.draw(self.canvas, current_time, self.intro.star_alpha)

        # 3. Sacred Yamuna River & Moon Reflections
        self.yamuna.draw(self.canvas, current_time, self.background.moon_x)

        # 4. Framing Kadamba Trees
        self.background.draw_framing_trees(self.canvas, current_time)

        # 5. Hanging Brass Lanterns & Terracotta Diyas
        lantern_alpha = self.intro.lights_alpha if self.lights_active else 0.0
        self.lanterns.draw(self.canvas, current_time, self.lights_active, lantern_alpha)
        self.diyas.draw(self.canvas, current_time, self.lights_active, lantern_alpha)

        # 6. Characters: Peacock, Calf, Clay Matki & Bal Krishna
        char_alpha = self.intro.krishna_alpha
        self.peacock.draw(self.canvas, current_time, char_alpha)
        self.calf.draw(self.canvas, current_time, char_alpha)
        self.matki.draw(self.canvas, current_time, char_alpha)
        self.krishna.draw(self.canvas, current_time, char_alpha)

        # 7. Particle Systems (Fireflies & Divine Golden Aura)
        self.particles.draw(self.canvas, char_alpha)
        self.fireflies.draw(self.canvas, current_time, self.intro.lights_alpha)

        # 8. Titles & Glowing Typography
        self.typography.draw_titles(self.canvas, current_time, self.intro.title_alpha)

        # 9. Sacred Blessing Card (Bottom)
        if self.show_blessing and self.intro.finished:
            self.typography.draw_blessing_card(self.canvas, 1.0)

        # 10. Cinematic Vignette
        self.canvas.blit(self._vignette, (0, 0))

        # 11. UI Buttons
        for btn in self.buttons:
            btn.draw(self.canvas, self.typography.font_ui)

        # 12. Skip Intro hint
        if not self.intro.finished:
            hint_surf = self.typography.font_ui.render("Press SPACE or Click to Skip Intro", True, (210, 210, 235))
            self.canvas.blit(hint_surf, (V_WIDTH // 2 - hint_surf.get_width() // 2, V_HEIGHT - 45))

        # 13. Paused Overlay
        if self.is_paused:
            pause_overlay = pygame.Surface((V_WIDTH, V_HEIGHT), pygame.SRCALPHA)
            pause_overlay.fill((8, 6, 16, 140))
            self.canvas.blit(pause_overlay, (0, 0))
            self.typography.draw_golden_text(self.canvas, "PAUSED", self.typography.font_title, (V_WIDTH // 2, V_HEIGHT // 2), 1.0)

        # ----------------------------------------------------------------------
        # Final Presentation: Scale Virtual Canvas to Window / Screen
        # ----------------------------------------------------------------------
        scaled_view = pygame.transform.smoothscale(self.canvas, (self.win_width, self.win_height))
        self.screen.blit(scaled_view, (0, 0))
        pygame.display.flip()

    def run(self):
        start_time = time.time()
        while self.running:
            dt = self.clock.tick(TARGET_FPS) / 1000.0
            dt = min(dt, 0.05)  # Guard against large lag spikes
            current_time = time.time() - start_time

            self.handle_events()
            self.update(dt, current_time)
            self.draw(current_time)

        # Clean shutdown
        self.bansuri.stop()
        pygame.quit()


# ==============================================================================
# ENTRY POINT
# ==============================================================================
def main():
    app = JanmashtamiApp()
    app.run()


if __name__ == "__main__":
    main()
