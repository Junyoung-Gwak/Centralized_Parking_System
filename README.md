# 🚗 Centralized-Parking-System

Top-view 카메라 기반의 영상 처리 기술과 경로계획 알고리즘을 결합한 **실시간 자율 주차 시스템**입니다.  
C++와 Python을 활용하여 비정형 장애물을 회피하고 최적의 경로로 정밀 후방 주차를 수행합니다.

![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![TCP/IP](https://img.shields.io/badge/TCP%2FIP-Socket-green?style=flat)

---

## 🌟 Key Features: Obstacle Avoidance

본 프로젝트의 핵심 역량인 **실시간 장애물 회피 및 동적 경로 재계획** 시연 영상입니다.

| 정적 장애물 회피 주차 (Static) | 동적 장애물 실시간 회피 (Dynamic) |
|:---:|:---:|
| <video src="./assets/04_Static_Obstacle_Avoidance.mp4" width="400"></video> | <video src="./assets/05_Dynamic_Obstacle_Avoidance.mp4" width="400"></video> |
| **A* 알고리즘**을 통해 고정된 장애물을 우회하는 최적 주차 경로 생성 | 경로 상에 사람이나 물체 등 **동적 장애물 침범 시 즉각 제동 및 안전 확보** |

---

## 🏗️ System Configuration

중앙 서버(PC)가 모든 연산을 처리하고 RC카를 제어하는 **중앙 집중형 구조**입니다.

![System Configuration](./assets/system_configuration.png)

1. **Vision Node:** Top-view 영상을 분석하여 주차면 점유 상태 및 차량 마커 추적
2. **Planning Node:** 현재 위치에서 목표 주차 칸까지의 최적 궤적 생성
3. **Control Node:** TCP/IP 소켓을 통해 RC카에 조향 및 속도 명령 하사

---

## ⚙️ Core Algorithms

### 1. Custom A* Path Planning (Heuristic)
단순한 최단 거리가 아닌, **차량의 실제 회전 반경과 주차 가능 각도**를 고려한 커스텀 휴리스틱 함수를 적용했습니다.

![Heuristic Logic](./assets/Heuristic.png)
* *Weighting Strategy:* 목표 지점과의 거리 비용에 차량의 헤딩 방향(Heading) 페널티를 결합하여 후방 주차에 최적화된 경로를 산출합니다.

### 2. Pure Pursuit Control
생성된 경로를 부드럽게 추종하기 위해 전진과 후진 상황에 각각 최적화된 제어기를 구현했습니다.

| 전진 추종 (Forward) | 후방 주차 제어 (Backward) |
|:---:|:---:|
| ![Pure Pursuit Forward](./assets/pure_pursuit(forward).jpeg) | ![Pure Pursuit Backward](./assets/pure_pursuit(backward).png) |
| Look-ahead 거리를 조절하여 안정적인 조향 유지 | 후진 시 조향각 반전 및 후방 마커 기반의 정밀 제어 |

---

## 🎬 Basic Parking Scenarios

기본적인 환경에서의 전/후방 주차 알고리즘 검증 결과입니다.

| 전진 주차 | 후방 주차 (기본) | 후방 주차 (각도 심화) |
|:---:|:---:|:---:|
| <video src="./assets/01_Forward_Parking.mkv"></video> | <video src="./assets/02_Reverse_Parking_Basic.mkv"></video> | <video src="./assets/03_Reverse_Parking_Angle.mkv"></video> |

---

## 🛠 Tech Stack
- **Language:** C++, Python
- **Library:** OpenCV (Image Processing)
- **Protocol:** TCP/IP Socket Communication
- **Hardware:** RC Car, Raspberry Pi, Top-view Camera
