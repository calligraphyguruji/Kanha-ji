# ॥ जय श्री कृष्ण ॥ Janmashtami 2026 - Bal Krishna (Kanha Ji)

A complete, visually stunning devotional celebration of Janmashtami 2026 featuring Bal Krishna (Kanha Ji), an adorable baby calf, a majestic peacock, handcrafted clay matki, flowing Yamuna waters, and authentic Bansuri flute music.

---

## 🌟 Project Highlights

1. **Desktop Pygame Interactive App (`main.py`)**:
   - 60 FPS frame-independent animation.
   - Built-in procedural Bansuri (bamboo flute) audio synthesizer in Raag Bhopali.
   - Interactive controls: Toggle Bansuri (`M`), Lights/Diyas (`L`), Fullscreen (`F`), Blessing Card (`B`), Pause (`SPACE`).

2. **9:16 Animated Mobile Wallpaper Renderer (`animate_krishna_wallpaper.py`)**:
   - Transforms artwork into a seamless looping 1080x1920 (9:16) 10-second 30 FPS MP4 video.
   - 12 layered animation effects: divine aura, volumetric rays, pulsing neon contours, twinkling stars, micro-shimmer eye catchlights, and diamond sparkles.

3. **Vercel-Ready Web App (`web/`)**:
   - Mobile-first, glassmorphism web interface ready to deploy on Vercel.
   - Seamless looping video wallpaper background.
   - Web Audio API procedural bansuri synthesizer (no external MP3 required).
   - One-click "Save Wallpaper" download button and Fullscreen toggle.

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
