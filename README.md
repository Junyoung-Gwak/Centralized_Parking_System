# 🚗 Centralized-Parking-System

Top-view 카메라 기반의 영상 처리 기술과 경로계획 알고리즘을 결합한 **실시간 자율 주차 시스템**입니다.  
C++와 Python을 활용하여 비정형 장애물을 회피하고 최적의 경로로 정밀 후방 주차를 수행합니다.

![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![TCP/IP](https://img.shields.io/badge/TCP%2FIP-Socket-green?style=flat)

---

## 🌟 Key Features: Obstacle Avoidance

본 프로젝트의 핵심 역량인 **실시간 장애물 회피** 시연 영상입니다.

<table align="center" border="0" cellspacing="0" cellpadding="0">
  <tr align="center">
    <td>
      <video src="https://github.com/user-attachments/assets/54b0201d-5367-4e86-ab49-4a7f12f370fe" width="100%" autoplay muted loop playsinline></video>
    </td>
    <td>
      <video src="https://github.com/user-attachments/assets/349d29d8-b020-4e66-b665-0bdf086a5ef7" width="100%" autoplay muted loop playsinline></video>
    </td>
  </tr>
</table>

> 경로 내 장애물(사람, 물체) 침범 시 **즉각 제동 및 안전을 확보**하며, A* 알고리즘을 통해 최적의 주차 경로를 재생성합니다.

---

## 🏗️ System Configuration

중앙 서버(PC)가 모든 연산을 처리하고 RC카를 제어하는 **중앙 집중형 구조**입니다.

<p align="center">
  <img src="https://github.com/Junyoung-Gwak/Centralized_Parking_System/raw/main/assets/system_configuration.png" width="600">
</p>

1. **Vision Node:** Top-view 영상을 분석하여 주차면 점유 상태 및 차량 마커 추적
2. **Planning Node:** 현재 위치에서 목표 주차 칸까지의 최적 궤적 생성
3. **Control Node:** TCP/IP 소켓을 통해 RC카에 조향 및 속도 명령 전송

---

## ⚙️ Core Algorithms

### 1. Custom A* Path Planning (Heuristic)
차량의 **실제 회전 반경과 주차 가능 각도**를 고려한 커스텀 휴리스틱 함수를 적용했습니다.

<p align="center">
  <img src="https://github.com/Junyoung-Gwak/Centralized_Parking_System/raw/main/assets/Heuristic.png" width="400">
</p>

* *Weighting Strategy:* 목표 지점과의 거리 비용에 차량의 헤딩 방향(Heading) 페널티를 결합하여 후방 주차에 최적화된 경로를 산출합니다.

### 2. Pure Pursuit Control
전진과 후진 상황에 각각 최적화된 제어기를 구현하여 경로 추종 성능을 높였습니다.

| 전진 추종 (Forward) | 후방 주차 제어 (Backward) |
|:---:|:---:|
| <img src="https://github.com/Junyoung-Gwak/Centralized_Parking_System/raw/main/assets/pure_pursuit(forward).jpeg" height="250"> | <img src="https://github.com/Junyoung-Gwak/Centralized_Parking_System/raw/main/assets/pure_pursuit(backward).png" height="250"> |
| Look-ahead 거리를 조절하여 조향 안정성 유지 | 후진 시 조향각 반전 및 정밀 제어 구현 |

---

## 🎬 Basic Parking Scenarios

기본 환경에서의 알고리즘 검증 결과입니다.

<table align="center" border="0" cellspacing="0" cellpadding="0">
  <tr align="center">
    <td><video src="https://github.com/user-attachments/assets/cecbfe7f-d09c-4f40-b27f-a315e26f3635" width="100%" muted autoplay loop playsinline></video></td>
    <td><video src="https://github.com/user-attachments/assets/9ccaab7f-233f-45c6-9a10-53be63675920" width="100%" muted autoplay loop playsinline></video></td>
    <td><video src="https://github.com/user-attachments/assets/1a8dc87f-ec85-409e-bba7-dffdc5509ab3" width="100%" muted autoplay loop playsinline></video></td>
  </tr>
</table>

---

## 🛠 Tech Stack
- **Language:** C++, Python
- **Library:** OpenCV (Image Processing)
- **Protocol:** TCP/IP Socket Communication
- **Hardware:** RC Car, Raspberry Pi, Top-view Camera
