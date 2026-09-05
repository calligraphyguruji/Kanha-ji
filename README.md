# ॥ जय श्री कृष्ण ॥ Janmashtami 2026 - Bal Krishna (Kanha Ji)

A complete, visually stunning devotional celebration of Janmashtami 2026 featuring Bal Krishna (Kanha Ji), an adorable baby calf, a majestic peacock, handcrafted clay matki, flowing Yamuna waters, and authentic Bansuri flute music.

---

## 🌟 Project Highlights

1. **Vercel-Ready Web App (`web/`)**:
   - **Cinematic Darshan Transition**: Sacred ॐ (Om) glowing reveal before Kanha Ji's divine darshan.
   - **Interactive Mandir Bell**: Tap the brass temple bell with physical swing animation and realistic synthesized chime.
   - **Interactive Aarti / Puja Mode**: Perform Aarti with a floating brass Diya Thali (orbital motion or manual drag/touch) and showering rose petals (Pushpa Vrishti).
   - **Dynamic Year**: Automatically updates to the current year every year (`new Date().getFullYear()`) without manual edits.
   - **Seamless 9:16 Looping Video**: Crisp animated devotional wallpaper.
   - **Procedural Web Audio Bansuri**: Synthesizes Raag Bhopali bansuri flute natively in the browser with zero external MP3 dependencies.
   - **Mobile-First & Fully Responsive**: Tested with `100dvh`, iOS/Android safe area insets, non-passive touch gesture support, and bottom dock controls.

2. **Desktop Pygame Interactive App (`main.py`)**:
   - 60 FPS frame-independent animation with dynamic year (`datetime.datetime.now().year`).
   - Built-in procedural Bansuri (bamboo flute) audio synthesizer in Raag Bhopali.
   - Interactive controls: Toggle Bansuri (`M`), Lights/Diyas (`L`), Fullscreen (`F`), Blessing Card (`B`), Pause (`SPACE`).

3. **9:16 Animated Mobile Wallpaper Renderer (`animate_krishna_wallpaper.py`)**:
   - Transforms artwork into a seamless looping 1080x1920 (9:16) 10-second 30 FPS MP4 video.
   - 12 layered animation effects: divine aura, volumetric rays, pulsing neon contours, twinkling stars, micro-shimmer eye catchlights, and diamond sparkles.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install pygame opencv-python numpy pillow imageio imageio-ffmpeg scipy tqdm
```

### 2. Run the Desktop Pygame Animation
```bash
python3 main.py
```

### 3. Generate the 9:16 Looping Video Wallpaper
```bash
python3 animate_krishna_wallpaper.py --input 8034.jpg --output web/krishna_animated.mp4
```

### 4. Run the Web App Locally
```bash
cd web
python3 -m http.server 8000
# Open http://localhost:8000 in your browser
```

### 5. Deploy to Vercel
```bash
cd web
npx vercel
```
Or import the repository on [Vercel](https://vercel.com) and set the **Root Directory** to `web`.

---

## 📜 Sacred Blessing
> *“May Lord Krishna bless you with happiness, peace, prosperity and success.”*  
> **Happy Janmashtami 2026 🌸**
