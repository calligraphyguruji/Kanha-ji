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
// CINEMATIC DARSHAN INTRO REVEAL CONTROLLER
// ==============================================================================
function initDarshanReveal(bansuri) {
  const introOverlay = document.getElementById('introOverlay');
  const enterBtn = document.getElementById('enterDarshanBtn');
  const mediaContainer = document.getElementById('mediaContainer');
  const uiOverlay = document.getElementById('uiOverlay');
  const bgVideo = document.getElementById('bgVideo');
  const bansuriBtn = document.getElementById('bansuriBtn');

  let hasRevealed = false;

  const triggerReveal = (startAudio = false) => {
    if (hasRevealed) return;
    hasRevealed = true;

    // 1. Trigger transition on intro screen
    if (introOverlay) {
      introOverlay.classList.add('revealed');
    }

    // 2. Reveal Kanha Ji picture/video with cinematic bloom
    if (mediaContainer) {
      mediaContainer.classList.remove('darshan-hidden');
      mediaContainer.classList.add('darshan-revealed');
    }

    // 3. Ensure background video plays smoothly
    if (bgVideo) {
      bgVideo.play().catch(() => {});
    }

    // 4. Reveal UI Overlay smoothly
    setTimeout(() => {
      if (uiOverlay) {
        uiOverlay.classList.remove('darshan-hidden');
        uiOverlay.classList.add('darshan-revealed');
      }
    }, 500);

    // 5. Start bansuri music if user tapped
    if (startAudio && bansuri && !bansuri.isPlaying) {
      bansuri.startMelody();
      if (bansuriBtn) {
        bansuriBtn.classList.remove('pulse');
        bansuriBtn.innerHTML = '<span class="icon">⏸</span><span class="label">Pause Bansuri</span>';
      }
    }

    // Remove intro overlay from DOM after transition completes
    setTimeout(() => {
      if (introOverlay) {
        introOverlay.style.display = 'none';
      }
    }, 2200);
  };

  // User click on button or screen
  if (enterBtn) {
    enterBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      triggerReveal(true);
    });
  }

  if (introOverlay) {
    introOverlay.addEventListener('click', () => {
      triggerReveal(true);
    });
  }

  // Auto-reveal after 3.2 seconds if user hasn't clicked
  setTimeout(() => {
    triggerReveal(false);
  }, 3200);
}

// ==============================================================================
// TEMPLE AUDIO SYNTHESIZER (BELL & AARTI SOUNDS)
// ==============================================================================
class TempleAudio {
  constructor(sharedCtx = null) {
    this.ctx = sharedCtx;
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

  // Realistic temple brass bell (Mandir Ghanti) synthesis
  ringBell() {
    this.init();
    if (!this.ctx) return;
    const now = this.ctx.currentTime;

    // Authentic bronze temple bell partials
    const bellPartials = [
      { ratio: 1.0, gain: 0.55, decay: 3.2 },
      { ratio: 1.98, gain: 0.35, decay: 2.2 },
      { ratio: 2.96, gain: 0.22, decay: 1.6 },
      { ratio: 4.14, gain: 0.16, decay: 1.1 },
      { ratio: 5.43, gain: 0.10, decay: 0.7 },
      { ratio: 6.82, gain: 0.06, decay: 0.4 }
    ];

    const baseFreq = 1046.5; // C6 bell resonance

    bellPartials.forEach(p => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(baseFreq * p.ratio, now);

      gain.gain.setValueAtTime(0.001, now);
      // Fast strike transient
      gain.gain.linearRampToValueAtTime(p.gain, now + 0.006);
      // Exponential bronze decay
      gain.gain.exponentialRampToValueAtTime(0.0001, now + p.decay);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + p.decay + 0.1);
    });
  }
}

// ==============================================================================
// INTERACTIVE TEMPLE BELL & AARTI / PUJA CONTROLLERS
// ==============================================================================
function initTempleInteractions(templeAudio, bansuri) {
  const bellBtn = document.getElementById('bellBtn');
  const bellContainer = document.getElementById('templeBellContainer');
  const bellBody = document.getElementById('bellBody');
  const bellGlow = document.getElementById('bellGlow');

  const aartiBtn = document.getElementById('aartiBtn');
  const aartiThali = document.getElementById('aartiThali');
  const petalContainer = document.getElementById('petalContainer');

  // Trigger Bell Ring
  const triggerBell = () => {
    templeAudio.ringBell();

    // Bell swing animation
    if (bellBody) {
      bellBody.classList.remove('ringing');
      void bellBody.offsetWidth; // Force reflow
      bellBody.classList.add('ringing');
    }

    // Bell golden shockwave glow
    if (bellGlow) {
      bellGlow.classList.remove('active');
      void bellGlow.offsetWidth;
      bellGlow.classList.add('active');
    }
  };

  if (bellBtn) {
    bellBtn.addEventListener('click', triggerBell);
  }

  if (bellContainer) {
    bellContainer.addEventListener('click', triggerBell);
  }

  // --- AARTI / PUJA SYSTEM ---
  let isAartiActive = false;
  let petalInterval = null;
  let aartiBellInterval = null;

  // Flower Petal Spawner (Pushpa Vrishti)
  const spawnPetal = () => {
    if (!petalContainer) return;
    const petal = document.createElement('div');
    petal.className = 'falling-petal';
    const petals = ['🌸', '🌼', '🌺', '🌹', '🪷'];
    petal.textContent = petals[Math.floor(Math.random() * petals.length)];
    petal.style.left = Math.random() * 95 + 'vw';
    const duration = Math.random() * 2.5 + 3.0; // 3.0 - 5.5s
    petal.style.animationDuration = duration + 's';
    petal.style.fontSize = Math.random() * 0.8 + 1.1 + 'rem';

    petalContainer.appendChild(petal);
    setTimeout(() => {
      if (petal.parentNode) {
        petal.parentNode.removeChild(petal);
      }
    }, duration * 1000);
  };

  const startAarti = () => {
    isAartiActive = true;
    if (aartiBtn) {
      aartiBtn.classList.add('active-puja');
      aartiBtn.innerHTML = '<span class="icon">🪔</span><span class="label">Stop Aarti</span>';
    }

    // Show Aarti Thali & start orbit
    if (aartiThali) {
      aartiThali.style.left = '50%';
      aartiThali.style.top = '50%';
      aartiThali.classList.remove('darshan-hidden');
      aartiThali.classList.add('aarti-orbiting');
    }

    // Auto-ring bell on Aarti start
    templeAudio.ringBell();

    // Periodic gentle Aarti bell chimes
    aartiBellInterval = setInterval(() => {
      templeAudio.ringBell();
    }, 2800);

    // Continuous Pushpa Vrishti (Flower shower)
    for (let i = 0; i < 8; i++) {
      setTimeout(spawnPetal, i * 200);
    }
    petalInterval = setInterval(spawnPetal, 450);

    // If bansuri isn't playing, start it for divine devotional ambience
    if (bansuri && !bansuri.isPlaying) {
      bansuri.startMelody();
      const bansuriBtn = document.getElementById('bansuriBtn');
      if (bansuriBtn) {
        bansuriBtn.classList.remove('pulse');
        bansuriBtn.innerHTML = '<span class="icon">⏸</span><span class="label">Pause Bansuri</span>';
      }
    }
  };

  const stopAarti = () => {
    isAartiActive = false;
    if (aartiBtn) {
      aartiBtn.classList.remove('active-puja');
      aartiBtn.innerHTML = '<span class="icon">🪔</span><span class="label">Aarti / Puja</span>';
    }

    if (aartiThali) {
      aartiThali.classList.remove('aarti-orbiting');
      aartiThali.classList.add('darshan-hidden');
    }

    if (petalInterval) {
      clearInterval(petalInterval);
      petalInterval = null;
    }
    if (aartiBellInterval) {
      clearInterval(aartiBellInterval);
      aartiBellInterval = null;
    }
  };

  if (aartiBtn) {
    aartiBtn.addEventListener('click', () => {
      if (isAartiActive) {
        stopAarti();
      } else {
        startAarti();
      }
    });
  }

  // --- DRAG / TOUCH INTERACTION FOR AARTI THALI ---
  // Allows the devotee to physically move the Thali around Kanha Ji
  let isDragging = false;

  const onDragStart = (e) => {
    if (!isAartiActive) return;
    isDragging = true;
    if (aartiThali) {
      aartiThali.classList.remove('aarti-orbiting');
    }
  };

  const onDragMove = (e) => {
    if (!isDragging || !aartiThali) return;
    if (e.cancelable) e.preventDefault();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    aartiThali.style.left = `${clientX}px`;
    aartiThali.style.top = `${clientY}px`;
    aartiThali.style.transform = 'translate(-50%, -50%)';

    if (Math.random() > 0.6) {
      spawnPetal();
    }
  };

  const onDragEnd = () => {
    if (!isDragging) return;
    isDragging = false;
    if (isAartiActive && aartiThali) {
      aartiThali.style.left = '50%';
      aartiThali.style.top = '50%';
      aartiThali.classList.add('aarti-orbiting');
    }
  };

  if (aartiThali) {
    aartiThali.addEventListener('mousedown', onDragStart);
    window.addEventListener('mousemove', onDragMove);
    window.addEventListener('mouseup', onDragEnd);

    aartiThali.addEventListener('touchstart', onDragStart, { passive: true });
    window.addEventListener('touchmove', onDragMove, { passive: false });
    window.addEventListener('touchend', onDragEnd);
  }
}

// ==============================================================================
// DYNAMIC YEAR CONTROLLER
// ==============================================================================
function updateDynamicYear() {
  const currentYear = new Date().getFullYear();
  document.title = `॥ जय श्री कृष्ण ॥ Happy Janmashtami ${currentYear}`;
  document.querySelectorAll('.current-year').forEach(el => {
    el.textContent = currentYear;
  });
}

// ==============================================================================
// UI EVENT CONTROLLERS
// ==============================================================================
document.addEventListener('DOMContentLoaded', () => {
  updateDynamicYear();

  const bansuri = new WebBansuri();
  const templeAudio = new TempleAudio(bansuri.ctx);

  new ParticleCanvas('fxCanvas');

  initDarshanReveal(bansuri);
  initTempleInteractions(templeAudio, bansuri);

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
