# 🚗 중앙제어 자동 주차 시스템

Top-view 카메라 기반의 영상 처리 기술과 경로계획 알고리즘을 결합한 **실시간 자율 주차 시스템**입니다.  
A* 경로탐색과 Pure Pursuit 추종 알고리즘으로 비정형 장애물을 회피하며 정밀 후방 주차를 구현합니다.

![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![TCP/IP](https://img.shields.io/badge/TCP%2FIP-Socket-green?style=flat)

| 항목 | 내용 |
|------|------|
| 참여 인원 | 2명 |
| 진행 기간 | 2022.12 – 2023.01 |
| 핵심 알고리즘 | A\* · Pure Pursuit |
| 사용 기술 | C++, Python, OpenCV, TCP/IP, RC Car |

---

## 📌 개요

중앙 서버가 Top-view 카메라 영상을 분석하여 주차 구역의 점유 상태와 장애물을 실시간으로 판별하고,
RC카에 부착된 마커 추적으로 차량의 위치 및 방향을 정밀하게 파악합니다.
산출된 정보를 기반으로 최적 주차 경로를 생성한 뒤, TCP/IP 통신을 통해 차량을 원격 제어하는 **중앙제어형 자율 주차 시스템**입니다.

---

## 🏗 시스템 구조

```
Top-view 카메라
    │
    ▼
영상 처리 (마커 추적 · 주차 점유 판별)
    │
    ▼
경로 생성 (A* + 커스텀 휴리스틱)
    │
    ▼
경로 추종 (Pure Pursuit)
    │
    ▼
RC Car 제어 (TCP/IP 소켓 통신)
```

---

## ⚙️ 구현 내용

- **실시간 환경 인식** — Top-view 카메라로 주차 구역 점유 상태 및 장애물을 프레임 단위로 판별
- **정밀 위치 추정** — RC카에 부착된 마커를 추적하여 현재 위치(x, y)와 방향각(θ)을 정밀 산출
- **커스텀 A\* 경로 탐색** — 차량 회전 반경 및 목표 지점까지의 거리 비용을 결합한 휴리스틱 함수를 적용하여 비정형 장애물을 회피하는 최적 경로 생성
- **Pure Pursuit 경로 추종** — 생성된 경로를 부드럽게 추종하며 후방 정밀 주차 실현
- **TCP/IP 실시간 통신** — 중앙 서버 ↔ RC Car 간 소켓 통신으로 제어 명령 실시간 전달

---

## 🎬 데모

### 시연 영상

https://github.com/user-attachments/assets/여기에-영상-ID를-붙여넣으세요

### 스크린샷

| Top-view 영상 처리 | 경로 생성 결과 | 주차 완료 |
|:---:|:---:|:---:|
| ![img1](./assets/topview.png) | ![img2](./assets/path.png) | ![img3](./assets/result.png) |

---

## 📂 프로젝트 구조

```
├── src/
│   ├── main.cpp          # 메인 제어 루프
│   ├── vision.cpp        # 영상 처리 (마커 추적, 점유 판별)
│   ├── pathplan.cpp      # A* 경로 탐색
│   ├── controller.cpp    # Pure Pursuit 제어기
│   └── comm.cpp          # TCP/IP 소켓 통신
├── assets/               # README용 이미지/영상
└── README.md
```
