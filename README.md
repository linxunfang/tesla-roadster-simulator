# 🚀 Tesla Roadster SpaceX Lateral Thruster Simulator

> **Interactive Web-Based Physics Simulator: 180° Inverted Semi-Circle Ramp Jump & SpaceX Cold-Gas Retro-Thruster Landing**

[![Play Online](https://img.shields.io/badge/🎮_Play_Online-GitHub_Pages-brightgreen?style=for-the-badge)](https://linxunfang.github.io/tesla-roadster-simulator/)
[![Buy Me A Coffee](https://img.shields.io/badge/☕_Buy_Me_a_Coffee-linxunfang-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/linxunfang)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

Inspired by the conceptual demonstration of the **Tesla Roadster equipped with the SpaceX Package**, this browser-based physics simulator lets you pilot an ultra-high performance electric supercar as it launches past 90° vertical into a full **180° inverted semi-circle mega ramp**. 

Inverted in mid-air, you must deploy **SpaceX Cold-Gas RCS Thrusters** to recover attitude via 180° roll, and balance pitch with **front and rear bottom thrusters** to achieve a soft, balanced touchdown on the runway!

👉 **Play Now in Your Browser**: [https://linxunfang.github.io/tesla-roadster-simulator/](https://linxunfang.github.io/tesla-roadster-simulator/)

![Tesla Roadster Web Simulator Preview](landing_sequence.png)

---

## 🎮 Key Features

1. **180° Inverted Semi-Circle Mega Ramp**:
   - The Roadster speeds through a curved neon loop and launches into the air completely upside down (180° inverted ceiling state).
2. **3D Perspective Roll & Pitch Physics**:
   - Simulated dynamic perspective rendering on HTML5 Canvas featuring real-time 180° lateral roll and nose-to-tail pitch leveling.
3. **SpaceX Dual Bottom Thrusters & Lateral RCS**:
   - Independent front bottom nozzle (pitch up) and rear bottom nozzle (tail up) paired with simultaneous dual firing for soft, cushioned landings.
4. **3 Interactive Simulation Modes**:
   - 🕹️ **Manual Landing**: Full manual control over 180° roll recovery and dual thruster balance.
   - 🤖 **AI Autopilot**: Real-time critically damped PD controller showcasing a 0.0° zero-error perfect touchdown.
   - ⚔️ **Human vs AI**: Compare your landing score and reaction time side-by-side against the autopilot!
5. **Slow-Motion Time Scale (0.35x ~ 1.0x)**:
   - Dial in your preferred reaction speed to admire mid-air cold-gas thruster plumes and suspension dynamics.

---

## 🕹️ Controls Guide

| Function | Keyboard Keys | On-Screen Button | Description |
| :--- | :--- | :--- | :--- |
| **🔄 180° Roll Recovery** | `W` / `S` or `▲` / `▼` | `180° Roll` | Recovers the upside-down (180°) inverted body upright |
| **🚀 Front Bottom Thruster** | `A` or `◀` | `Front Bottom` | Fires nozzle beneath front nose to raise pitch and level body |
| **🚀 Rear Bottom Thruster** | `D` or `▶` | `Rear Bottom` | Fires nozzle beneath rear bumper to raise tail and level body |
| **⚡ Soft Touchdown** | `A+D together` or `SPACE` | `Dual Thrusters` | Fires both thrusters simultaneously for level descent and shock absorption |
| **🔄 Restart Simulation** | `R` | `Restart (R)` | Restarts launch from beginning with full nitrogen tank |

---

## 🛠️ Tech Stack

* **HTML5 Canvas**: Pure 2D canvas rendering with smoke particle physics and glowing neon effects.
* **Vanilla JavaScript (ES6+)**: Custom numerical physics integrator, collision mechanics, and PD autopilot control algorithms.
* **Pure CSS3**: Glassmorphism cockpit HUD, telemetry overlays, and responsive mobile-ready layout.
* **Zero Dependencies**: 100% standalone code — loads in under 1 second with no external build tools or installations.

---
---

## 🇰🇷 한국어 소개 (Korean Version)

> **Tesla Roadster SpaceX 패키지 180° 반원 램프 점프 및 콜드가스 역추진 수평 착지 시뮬레이터**

Tesla Roadster 시연 동영상에서 영감을 받아 제작된 웹 기반 고성능 물리 시뮬레이터입니다.  
90도 수직을 넘어 180도 완전 반원(Semi-Circle) 궤도를 타고 거꾸로 뒤집힌 로드스터를 **SpaceX 콜드가스 RCS 스러스터**로 180도 롤 복원하고, **앞/뒤 하부 추진 노즐**로 수평을 맞추어 안전하게 터치다운시키는 실시간 물리 엔진 게임입니다.

👉 **웹에서 바로 플레이하기**: [https://linxunfang.github.io/tesla-roadster-simulator/](https://linxunfang.github.io/tesla-roadster-simulator/)

### 🎮 주요 특징
1. **완벽한 반원(Semi-Circle) 180° 메가 램프**: 차체가 수직을 지나 180도 완전히 거꾸로 뒤집힌 상태로 공중에 진입합니다.
2. **3D 원근 롤(Roll) & 피치(Pitch) 물리 엔진**: 2D Canvas 위에서 펼쳐지는 입체적인 차체 롤링과 쿼터뷰 투영.
3. **SpaceX 듀얼 하부 노즐 & 측면 RCS 시스템**: 앞머리 밑 분사, 뒷부분 밑 분사, 앞뒤 동시 분사로 피치 수평 평형 유지 및 소프트 터치다운.
4. **3가지 게임 모드**: 🕹️ 수동 착지(Manual), 🤖 AI 오토파일럿(Autopilot), ⚔️ 사람 vs AI 비교(VS Mode).
5. **유저 맞춤형 슬로우 모션**: 0.35x(추천)부터 1.0x(실시간)까지 자유롭게 조절 가능.

### 🕹️ 조작 방법
| 구분 | 키보드 키 | 온스크린 버튼 | 동작 설명 |
| :--- | :--- | :--- | :--- |
| **🔄 180° 롤 회전** | `W` / `S` 또는 `▲` / `▼` | `180° 회전` | 180도 뒤집힌 차체를 정자세로 롤 회전 복원 |
| **🚀 앞머리 상승** | `A` 또는 `◀` | `앞머리 밑 분사` | 앞부분 밑 노즐 분사로 앞머리를 들어올려 수평 조절 |
| **🚀 뒷부분 상승** | `D` 또는 `▶` | `뒷부분 밑 분사` | 뒷부분 밑 노즐 분사로 뒷부분을 들어올려 수평 조절 |
| **⚡ 소프트 착지** | `A+D 동시` 또는 `SPACE` | `앞뒤 동시 분사` | 수평 유지 및 완충 감속 역추진 |
| **🔄 재도약** | `R` | `재도약 (R)` | 시뮬레이션 처음부터 다시 시작 |

---

## ☕ Support / 후원

If you enjoyed this Tesla Roadster flight simulator, feel free to buy me a coffee!  
프로젝트가 마음에 드셨다면 개발자에게 따뜻한 커피 한 잔을 선물해 주세요! ☕💛

<a href="https://www.buymeacoffee.com/linxunfang" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 50px !important;width: 217px !important;" ></a>

---

## 📄 License
MIT License
