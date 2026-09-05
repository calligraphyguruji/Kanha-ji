// ==============================================================================
// WEB AUDIO PROCEDURAL BANSURI (FLUTE) SYNTHESIZER
// ==============================================================================
class WebBansuri {
  constructor() {
    this.ctx = null;
    this.isPlaying = false;
    this.timerId = null;
  }

  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioContext();
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  // Plays a single traditional Bansuri swara with breath noise, vibrato and warm harmonics
  playNote(freq, durationSec) {
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    const masterGain = this.ctx.createGain();
    masterGain.gain.setValueAtTime(0.001, now);
    // Soft attack
    masterGain.gain.exponentialRampToValueAtTime(0.18, now + 0.12);
    // Gentle decay
    masterGain.gain.exponentialRampToValueAtTime(0.001, now + durationSec - 0.05);

    // Warm harmonics (Fundamental + 2nd & 3rd harmonics)
    const harmonics = [
      { ratio: 1.0, gain: 0.65 },
      { ratio: 2.0, gain: 0.22 },
      { ratio: 3.0, gain: 0.08 }
    ];

    harmonics.forEach(h => {
      const osc = this.ctx.createOscillator();
      const hGain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq * h.ratio, now);

      // Subtle vibrato (5 Hz, gentle pitch wobble)
      const vib = this.ctx.createOscillator();
      const vibGain = this.ctx.createGain();
      vib.frequency.setValueAtTime(5.2, now);
      vibGain.gain.setValueAtTime(freq * 0.008, now);
      vib.connect(osc.frequency);
      vib.start(now);
      vib.stop(now + durationSec);

      hGain.gain.value = h.gain;
      osc.connect(hGain);
      hGain.connect(masterGain);

      osc.start(now);
      osc.stop(now + durationSec);
    });

    masterGain.connect(this.ctx.destination);
  }

  startMelody() {
    this.init();
    this.isPlaying = true;

    // Peaceful Raag Bhopali bansuri swara loop (Base E4 = 329.6 Hz)
    const sa = 329.6;
    const re = sa * (9/8);
    const ga = sa * (5/4);
    const pa = sa * (3/2);
    const dha = sa * (5/3);
    const saHigh = sa * 2;

    const melody = [
      { f: sa, d: 2.0 },
      { f: re, d: 1.4 },
      { f: ga, d: 2.2 },
      { f: pa, d: 1.6 },
      { f: dha, d: 1.4 },
      { f: saHigh, d: 2.4 },
      { f: dha, d: 1.4 },
      { f: pa, d: 1.8 },
      { f: ga, d: 2.0 },
      { f: re, d: 1.4 },
      { f: sa, d: 2.8 }
    ];

    let noteIndex = 0;
    const playNext = () => {
      if (!this.isPlaying) return;
      const note = melody[noteIndex];
      this.playNote(note.f, note.d);
      noteIndex = (noteIndex + 1) % melody.length;
      this.timerId = setTimeout(playNext, note.d * 1000 - 80); // Legato overlap
    };

    playNext();
  }

  stop() {
    this.isPlaying = false;
    if (this.timerId) {
      clearTimeout(this.timerId);
      this.timerId = null;
    }
  }

  toggle() {
    if (this.isPlaying) {
      this.stop();
      return false;
    } else {
      this.startMelody();
      return true;
    }
  }
}

// ==============================================================================
// AMBIENT CELESTIAL CANVAS PARTICLES (FIREFLIES & GOLDEN DUST)
// ==============================================================================
class ParticleCanvas {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.particles = [];
    this.resize();
    this.initParticles(75);

    window.addEventListener('resize', () => this.resize());
    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  resize() {
    this.width = this.canvas.width = window.innerWidth;
    this.height = this.canvas.height = window.innerHeight;
  }

  initParticles(count) {
    this.particles = [];
    for (let i = 0; i < count; i++) {
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        r: Math.random() * 2.5 + 1.0,
        vx: (Math.random() - 0.5) * 0.4,
        vy: -Math.random() * 0.6 - 0.2, // Upward drift
        alpha: Math.random() * 0.8 + 0.2,
        pulseSpeed: Math.random() * 0.04 + 0.02,
        phase: Math.random() * Math.PI * 2,
        isGold: Math.random() > 0.4
      });
    }
  }

  animate() {
    this.ctx.clearRect(0, 0, this.width, this.height);

    for (let p of this.particles) {
      p.x += p.vx + Math.sin(p.phase) * 0.3;
      p.y += p.vy;
      p.phase += p.pulseSpeed;

      if (p.y < -10) {
        p.y = this.height + 10;
        p.x = Math.random() * this.width;
      }

      const pulseAlpha = p.alpha * (0.6 + 0.4 * Math.sin(p.phase));
      this.ctx.save();
      this.ctx.globalAlpha = Math.max(0.1, pulseAlpha);
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);

      if (p.isGold) {
        this.ctx.fillStyle = '#fce277';
        this.ctx.shadowColor = '#f5c323';
        this.ctx.shadowBlur = 8;
      } else {
        this.ctx.fillStyle = '#bceeff';
        this.ctx.shadowColor = '#80d8ff';
        this.ctx.shadowBlur = 6;
      }

      this.ctx.fill();
      this.ctx.restore();
    }

    requestAnimationFrame(this.animate);
  }
}

// ==============================================================================
// UI EVENT CONTROLLERS
// ==============================================================================
document.addEventListener('DOMContentLoaded', () => {
  const bansuri = new WebBansuri();
  new ParticleCanvas('fxCanvas');

  const bansuriBtn = document.getElementById('bansuriBtn');
  const fullscreenBtn = document.getElementById('fullscreenBtn');

  // Bansuri Audio Toggle
  bansuriBtn.addEventListener('click', () => {
    const isPlaying = bansuri.toggle();
    if (isPlaying) {
      bansuriBtn.classList.remove('pulse');
      bansuriBtn.innerHTML = '<span class="icon">⏸</span><span class="label">Pause Bansuri</span>';
    } else {
      bansuriBtn.classList.add('pulse');
      bansuriBtn.innerHTML = '<span class="icon">♪</span><span class="label">Play Bansuri</span>';
    }
  });

  // Fullscreen Toggle
  fullscreenBtn.addEventListener('click', () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
      fullscreenBtn.querySelector('.label').textContent = 'Exit Fullscreen';
    } else {
      document.exitFullscreen().catch(() => {});
      fullscreenBtn.querySelector('.label').textContent = 'Fullscreen';
    }
  });
});
