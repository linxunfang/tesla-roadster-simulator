"""
Tesla Roadster 공중 점프 & 착지 MuJoCo 시뮬레이터
- SpaceX Cold-Gas Thruster 기반 공중 수평 자세 제어 (RCS Attitude Control)
- 역추진 감속 착지 (Retro-Thruster Soft Landing)
- 4륜 독립 서스펜션 충격 흡수 역학
"""

import os
import sys
import time
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mujoco
try:
    import mujoco.viewer
except ImportError:
    pass

def quat_to_euler(quat):
    """MuJoCo 쿼터니언 [w, x, y, z]를 Roll, Pitch, Yaw (deg)로 변환"""
    w, x, y, z = quat
    # Roll (x-axis rotation)
    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    # Pitch (y-axis rotation)
    sinp = 2.0 * (w * y - z * x)
    if np.abs(sinp) >= 1:
        pitch = np.sign(sinp) * (np.pi / 2)
    else:
        pitch = np.arcsin(sinp)

    # Yaw (z-axis rotation)
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return np.degrees(roll), np.degrees(pitch), np.degrees(yaw)

def run_simulation(xml_path="roadster.xml", duration=3.0, enable_thrusters=True, view=False):
    model = mujoco.MjModel.from_xml_path(xml_path)
    data = mujoco.MjData(model)

    dt = model.opt.timestep
    total_steps = int(duration / dt)

    # 텔레메트리 기록용 버퍼
    history = {
        "time": [],
        "z_pos": [],
        "z_vel": [],
        "roll": [],
        "pitch": [],
        "thrust_total": [],
        "susp_fl": [],
        "susp_fr": [],
        "susp_rl": [],
        "susp_rr": []
    }

    # 서스펜션 조인트 Qpos 인덱스
    fl_idx = model.joint("susp_fl_joint").qposadr[0]
    fr_idx = model.joint("susp_fr_joint").qposadr[0]
    rl_idx = model.joint("susp_rl_joint").qposadr[0]
    rr_idx = model.joint("susp_rr_joint").qposadr[0]
    chassis_id = model.body("chassis").id

    # 자세 제어 PID 게인 (공중 RCS)
    # 질량 1800kg, 관성 모멘트 ~2500 kg*m^2 고려
    kp_att = 8000.0
    kd_att = 2200.0

    print("=" * 60)
    print("🚀 Tesla Roadster Landing Simulation 시작")
    print(f" - SpaceX 스러스터 활성화: {enable_thrusters}")
    print(f" - 시뮬레이션 시간: {duration}초 (총 {total_steps} 스텝)")
    print("=" * 60)

    # 3D 뷰어 모드
    if view:
        with mujoco.viewer.launch_passive(model, data) as viewer:
            # 카메라를 로드스터 추적 카메라로 전환
            viewer.cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
            viewer.cam.trackbodyid = chassis_id
            viewer.cam.distance = 7.5
            viewer.cam.elevation = -15
            viewer.cam.azimuth = 140

            step = 0
            while viewer.is_running():
                step_start = time.time()

                if step < total_steps:
                    apply_controls(model, data, enable_thrusters, chassis_id, kp_att, kd_att)
                    mujoco.mj_step(model, data)
                    record_telemetry(data, history, chassis_id, fl_idx, fr_idx, rl_idx, rr_idx)
                    step += 1

                viewer.sync()

                time_until_next_step = dt - (time.time() - step_start)
                if time_until_next_step > 0:
                    time.sleep(time_until_next_step)
    else:
        # 헤드리스 고속 시뮬레이션
        for step in range(total_steps):
            apply_controls(model, data, enable_thrusters, chassis_id, kp_att, kd_att)
            mujoco.mj_step(model, data)
            record_telemetry(data, history, chassis_id, fl_idx, fr_idx, rl_idx, rr_idx)

    print("✅ 시뮬레이션 완료!")
    return model, data, history

def apply_controls(model, data, enable_thrusters, chassis_id, kp_att, kd_att):
    if not enable_thrusters:
        data.ctrl[:] = 0.0
        return

    # 회전 행렬 3x3 (차체 로컬축의 월드 좌표계 표현)
    xmat = data.xmat[chassis_id].reshape(3, 3)
    # xmat[:, 0] = 로컬 X축 (앞), xmat[:, 1] = 로컬 Y축 (좌), xmat[:, 2] = 로컬 Z축 (상)
    
    # 수평 오차: 로컬 Z축이 월드 Z축 [0,0,1]과 일치하도록 제어
    # Pitch error (X축의 월드 Z성분): 양수면 노즈 업 -> 앞쪽 내려야 함
    pitch_err = xmat[2, 0] 
    # Roll error (Y축의 월드 Z성분): 양수면 좌측 업 -> 좌측 내려야 함
    roll_err = xmat[2, 1]  

    # 각속도 (월드 좌표계)
    angvel = data.qvel[3:6]
    omega_x = angvel[0] # roll rate
    omega_y = angvel[1] # pitch rate

    # 자세 안정화 제어 토크 (PID)
    # pitch_err > 0 (앞이 들림) -> 앞 추력 감소(-), 뒤 추력 증가(+)
    # roll_err > 0 (좌측이 들림) -> 좌측 추력 감소(-), 우측 추력 증가(+)
    t_pitch = -(kp_att * pitch_err + kd_att * omega_y)
    t_roll  = -(kp_att * roll_err  + kd_att * omega_x)

    z_pos = data.qpos[2]
    z_vel = data.qvel[2]

    # 역추진 감속 (Retro-thrust)
    # 낙하 속도가 빠르고 착지 지점에 접근할 때 충격 완화
    thrust_base = 0.0
    if z_pos < 2.5 and z_vel < -0.8:
        # 목표 하강 속도를 -0.8 m/s 로 부드럽게 감속
        thrust_base = np.clip(1800 * 9.81 * 0.8 + 6000.0 * (-0.8 - z_vel), 0, 9000.0)

    # 지면에 착지(타이어가 지면에 닿은 높이) 시 스러스터 종료
    if z_pos < 0.52:
        thrust_base = 0.0
        t_pitch = 0.0
        t_roll = 0.0

    # 4개 스러스터에 힘 분배
    # FL (앞좌), FR (앞우), RL (뒤좌), RR (뒤우)
    f_fl = thrust_base + t_pitch + t_roll
    f_fr = thrust_base + t_pitch - t_roll
    f_rl = thrust_base - t_pitch + t_roll
    f_rr = thrust_base - t_pitch - t_roll

    data.ctrl[0] = np.clip(f_fl, 0, 12000.0)
    data.ctrl[1] = np.clip(f_fr, 0, 12000.0)
    data.ctrl[2] = np.clip(f_rl, 0, 12000.0)
    data.ctrl[3] = np.clip(f_rr, 0, 12000.0)

def record_telemetry(data, history, chassis_id, fl_idx, fr_idx, rl_idx, rr_idx):
    history["time"].append(data.time)
    history["z_pos"].append(data.qpos[2])
    history["z_vel"].append(data.qvel[2])

    quat = data.qpos[3:7]
    roll, pitch, _ = quat_to_euler(quat)
    history["roll"].append(roll)
    history["pitch"].append(pitch)

    history["thrust_total"].append(np.sum(data.ctrl))
    history["susp_fl"].append(data.qpos[fl_idx])
    history["susp_fr"].append(data.qpos[fr_idx])
    history["susp_rl"].append(data.qpos[rl_idx])
    history["susp_rr"].append(data.qpos[rr_idx])

def plot_telemetry(history, save_path="landing_telemetry.png"):
    t = np.array(history["time"])
    
    plt.style.use('dark_background')
    fig, axs = plt.subplots(3, 1, figsize=(10, 11), sharex=True)
    fig.patch.set_facecolor('#0d1117')

    for ax in axs:
        ax.set_facecolor('#161b22')
        ax.grid(True, linestyle='--', alpha=0.3, color='#8b949e')

    # 1. 고도 & 하강 속도
    axs[0].plot(t, history["z_pos"], color='#58a6ff', linewidth=2.2, label='Chassis Altitude (m)')
    axs[0].plot(t, history["z_vel"], color='#ff7b72', linewidth=1.8, linestyle=':', label='Vertical Velocity (m/s)')
    axs[0].axhline(y=0.48, color='#3fb950', linestyle='--', alpha=0.7, label='Target Ground Height')
    axs[0].set_ylabel('Height / Velocity')
    axs[0].set_title('Tesla Roadster Landing Dynamics: Altitude & Velocity', fontsize=12, fontweight='bold', color='#f0f6fc')
    axs[0].legend(loc='upper right', facecolor='#21262d', edgecolor='#30363d')

    # 2. 자세 각도 (Roll & Pitch)
    axs[1].plot(t, history["roll"], color='#d2a8ff', linewidth=2.0, label='Roll Angle (deg)')
    axs[1].plot(t, history["pitch"], color='#ffa657', linewidth=2.0, label='Pitch Angle (deg)')
    axs[1].axhline(y=0, color='#8b949e', linestyle='--', alpha=0.5)
    axs[1].set_ylabel('Angle (degrees)')
    axs[1].set_title('SpaceX RCS Attitude Correction (Airborne Levelling)', fontsize=12, fontweight='bold', color='#f0f6fc')
    axs[1].legend(loc='upper right', facecolor='#21262d', edgecolor='#30363d')

    # 3. 4륜 서스펜션 압축량 & 스러스터 추력
    ax_thrust = axs[2].twinx()
    ax_thrust.set_facecolor('none')
    ax_thrust.plot(t, np.array(history["thrust_total"]) / 1000.0, color='#7ee787', alpha=0.5, linewidth=1.5, label='Total Thrusters (kN)')
    ax_thrust.set_ylabel('Thrusters (kN)', color='#7ee787')
    ax_thrust.tick_params(axis='y', labelcolor='#7ee787')

    axs[2].plot(t, history["susp_fl"], color='#79c0ff', linewidth=1.5, label='Susp FL')
    axs[2].plot(t, history["susp_fr"], color='#56d364', linewidth=1.5, label='Susp FR')
    axs[2].plot(t, history["susp_rl"], color='#e3b341', linewidth=1.5, label='Susp RL')
    axs[2].plot(t, history["susp_rr"], color='#f78166', linewidth=1.5, label='Susp RR')
    axs[2].set_ylabel('Suspension Travel (m)')
    axs[2].set_xlabel('Time (seconds)', fontsize=11, color='#f0f6fc')
    axs[2].set_title('Suspension Compression & Touchdown Impact', fontsize=12, fontweight='bold', color='#f0f6fc')
    axs[2].legend(loc='upper left', facecolor='#21262d', edgecolor='#30363d')

    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()
    print(f"📊 텔레메트리 그래프 저장 완료: {save_path}")

def render_snapshots(xml_path="roadster.xml", save_path="landing_sequence.png"):
    """시뮬레이션 중 4단계(공중 도약 -> 자세 제어 -> 착지 직전 -> 서스펜션 접지) 스냅샷 생성"""
    model = mujoco.MjModel.from_xml_path(xml_path)
    data = mujoco.MjData(model)
    renderer = mujoco.Renderer(model, width=640, height=360)

    snapshots = []
    capture_times = [0.05, 0.40, 0.75, 1.20]
    labels = ["1. Airborne (Tilted Jump)", "2. SpaceX RCS Levelling", "3. Retro-Thrust Braking", "4. Suspension Touchdown"]
    curr_idx = 0

    chassis_id = model.body("chassis").id
    dt = model.opt.timestep
    total_steps = int(1.5 / dt)

    for step in range(total_steps):
        apply_controls(model, data, enable_thrusters=True, chassis_id=chassis_id, kp_att=8000.0, kd_att=2200.0)
        mujoco.mj_step(model, data)

        if curr_idx < len(capture_times) and data.time >= capture_times[curr_idx]:
            # 사이드/추적 앵글 렌더링
            camera_id = model.camera("tracking").id
            renderer.update_scene(data, camera=camera_id)
            img = renderer.render()
            snapshots.append((labels[curr_idx], img))
            curr_idx += 1

    # 4개 샷 합치기
    fig, axs = plt.subplots(2, 2, figsize=(12, 7.5))
    fig.patch.set_facecolor('#0d1117')
    for ax, (label, img) in zip(axs.flat, snapshots):
        ax.imshow(img)
        ax.set_title(label, color='#f0f6fc', fontsize=12, fontweight='bold', pad=8)
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()
    print(f"📸 착지 시퀀스 스냅샷 저장 완료: {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tesla Roadster Landing Simulator")
    parser.add_argument("--view", action="store_true", help="3D 대화형 뷰어 실행")
    parser.add_argument("--no-thrusters", action="store_true", help="스러스터 끄고 단순 자유낙하 비교")
    parser.add_argument("--duration", type=float, default=2.5, help="시뮬레이션 시간(초)")
    args = parser.parse_args()

    # macOS에서 3D 뷰어 실행 시 Cocoa 메인 스레드 바인딩을 위해 mjpython으로 자동 전환
    if sys.platform == "darwin" and args.view and "MJPYTHON_BIN" not in os.environ and "MJPYTHON_RUNNING" not in os.environ:
        os.environ["DEVELOPER_DIR"] = "/Library/Developer/CommandLineTools"
        os.environ["MJPYTHON_RUNNING"] = "1"
        bin_dir = os.path.expanduser("~/Library/Python/3.11/bin")
        if bin_dir not in os.environ.get("PATH", ""):
            os.environ["PATH"] = f"{bin_dir}:{os.environ.get('PATH', '')}"

        mjpython_candidates = [
            os.path.join(bin_dir, "mjpython"),
            "/Library/Frameworks/Python.framework/Versions/3.11/bin/mjpython",
            "mjpython"
        ]
        for candidate in mjpython_candidates:
            if os.path.exists(candidate):
                os.execv(candidate, [candidate] + sys.argv)

    enable_thrust = not args.no_thrusters
    model, data, history = run_simulation(duration=args.duration, enable_thrusters=enable_thrust, view=args.view)
    plot_telemetry(history, "landing_telemetry.png")
    render_snapshots("roadster.xml", "landing_sequence.png")
