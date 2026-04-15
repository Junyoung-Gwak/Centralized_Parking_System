# 🚗 Centralized-Parking-System

Top-view 카메라 기반의 영상 처리 기술과 경로계획 알고리즘을 결합한 **중앙제어 자율 주차 시스템**입니다.  
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
    <td width="48%"><b>정적 장애물 회피 주차 (Static)</b></td>
    <td width="4%"></td>
    <td width="48%"><b>동적 장애물 감지 및 제동 (Dynamic)</b></td>
  </tr>
  <tr align="center">
    <td>
      <video src="https://github.com/user-attachments/assets/66b7f58e-1842-483c-9651-1d106fa4bdf8" width="100%" autoplay muted loop playsinline></video>
    </td>
    <td></td>
    <td>
      <video src="https://github.com/user-attachments/assets/90327edc-e0bb-49ec-8103-ac6fbda49e1d" width="100%" autoplay muted loop playsinline></video>
    </td>
  </tr>
  <tr>
    <td valign="top">주차 경로 상에 고정된 장애물이 탐지되면, $A^*$ 알고리즘이 실시간으로 장애물을 우회하는 <b>새로운 최적 경로를 즉시 재계산</b>하여 주차를 완료합니다.</td>
    <td></td>
    <td valign="top">차량 이동 중 갑작스러운 동적 장애물(보행자 등)이 침범할 경우, 위험을 직시하고 <b>즉각적인 비상 제동</b>을 실시하여 안전을 확보합니다.</td>
  </tr>
</table>

---

## 🏗️ System Configuration

중앙 서버(PC)가 모든 연산을 처리하고 RC카를 제어하는 **중앙 집중형 구조**입니다.

<p align="center">
  <img src="https://github.com/Junyoung-Gwak/Centralized_Parking_System/raw/main/assets/system_configuration.png" width="550">
</p>

1. **Vision Node:** Top-view 영상을 분석하여 주차면 점유 상태 및 차량 마커 추적
2. **Planning Node:** 현재 위치에서 목표 주차 칸까지의 최적 궤적 생성
3. **Control Node:** TCP/IP 소켓을 통해 RC카에 조향 및 속도 명령 전송

---

## ⚙️ Core Algorithms

### 1. Custom A* Path Planning (Heuristic)
차량모델의 **실제 회전 반경과 주차 가능 각도**를 고려한 커스텀 휴리스틱 함수를 적용했습니다.

<p align="center">
  <img src="https://github.com/Junyoung-Gwak/Centralized_Parking_System/raw/main/assets/Heuristic.png" width="400">
</p>

### 2. Pure-Pursuit Control
전진과 후진 상황에 각각 최적화된 제어기를 구현했습니다.

| 전진 추종 제어 (Forward) | 후진 추종 제어 (Backward) |
|:---:|:---:|
| <img src="https://github.com/Junyoung-Gwak/Centralized_Parking_System/raw/main/assets/pure_pursuit(forward).jpeg" width="350"> | <img src="https://github.com/Junyoung-Gwak/Centralized_Parking_System/raw/main/assets/pure_pursuit(backward).png" width="350"> |

---

## 🎬 Basic Parking Scenarios

기본 조건 환경에서의 경로 추종 및 주차 정밀도 검증 결과입니다.

<table align="center" border="0" cellspacing="0" cellpadding="0">
  <tr align="center">
    <td width="48%"><b>전진 주차 (Forward Parking)</b></td>
    <td width="4%"></td>
    <td width="48%"><b>후진 주차 (Reverse Parking)</b></td>
  </tr>
  <tr align="center">
    <td>
      <video src="https://github.com/user-attachments/assets/5c9b8ee5-7745-485f-a6bc-830cc5a02edc" width="100%" autoplay muted loop playsinline></video>
    </td>
    <td></td>
    <td>
      <video src="https://github.com/user-attachments/assets/a4c967df-8886-44e9-94cb-1bb9edb8e335" width="100%" autoplay muted loop playsinline></video>
    </td>
  </tr>
  <tr>
    <td valign="top">Pure-Pursuit의 Look-ahead 거리를 최적화하여 곡선 경로에서도 이탈 없이 안정적으로 목표 지점에 진입합니다.</td>
    <td></td>
    <td valign="top">실차 회전 반경과 진입 각도를 계산하여, 수정 조향을 최소화한 최적 궤적을 따라 정밀하게 후방 정렬합니다.</td>
  </tr>
</table>

---

## 🛠 Tech Stack
- **Language:** C++, Python
- **Library:** OpenCV (Image Processing)
- **Protocol:** TCP/IP Socket Communication
- **Hardware:** RC Car, Raspberry Pi, Top-view Camera
