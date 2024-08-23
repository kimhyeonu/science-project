# science-project
guitar - 기타 각 줄의 개방현, 6번줄의 7, 12, 19번 프렛과 6번줄 12, 7, 5번 프렛 하모닉스 소리

guitar_har - 기타 각 줄의 12번 프렛과 12번 프렛 하모닉스 소리

sound - 0~13.wav는 각각 "피아노 순서"에 있는 순서대로 녹음한 전자 피아노 소리, 14.wav는 피아노 화음 소리, 나머지는 테스트용 소리

test - test0-14.wav 는 sound의 0-14.wav를 generatewave.py에 넣어 얻어낸 소리, test111.wav는 테스트용

fourier.py - 함수의 기본음과 배음의 주파수, 각 주파수별 위상차이, 평균적인 세기를 구해 그래프로 보여주는 코드

fourier_gen.py - fourier.py와 generatewave.py를 합쳐서 분석 후 바로 소리를 만들어주는 코드

generatewave.py - 기본음과 배음, 위상, 평균 세기를 입력하면 이를 이용해 sin함수를 합성하여 소리를 만들어주는 코드

guitar.py - guitar와 guitar_har에 있는 wav파일에 대해 fourier.py코드 실행

결과분석.py - 장력과 줄의 종류에 따른 주파수 실험 결과와 이론값을 비교하여 그래프로 나타내는 코드
