from FCFS_class import FCFS_Scheduling
from SJF_class import SJF_Scheduling
from 비선점Priority_class import Non_Preemptive_Priority_Scheduling
from 선점Priority_class import Piority_Scheduling
from 라운드로빈_class import RoundRobin_Scheduling
from SRT_class import SRT_Scheduling
from HRN_class import HRN_Scheduling

def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines() # 파일에서 줄 단위로 읽어오기

    p_list = [line.strip() for line in lines] # 공백 문자를 제거하여 p_list에 저장
    return p_list # p_list 리턴

def run_scheduling(choice): # 입력한 번호에 따라 스케줄링을 실행하는 함수
    p_list = read_file("data.txt") # read_file 함수 호출
    if choice == 1: # FCFS 스케줄링 실행 위한 객체 생성
        scheduler = FCFS_Scheduling(p_list)
    elif choice == 2: # SJF 스케줄링 실행 위한 객체 생성
        scheduler = SJF_Scheduling(p_list)
    elif choice == 3: # 비선점 우선순위 스케줄링 실행 위한 객체 생성
        scheduler = Non_Preemptive_Priority_Scheduling(p_list)
    elif choice == 4: # 선점 우선순위 스케줄링 실행 위한 객체 생성
        scheduler = Piority_Scheduling(p_list)
    elif choice == 5: # 라운드로빈 스케줄링 실행 위한 객체 생성
        scheduler = RoundRobin_Scheduling(p_list)
    elif choice == 6: # SRT 스케줄링 실행 위한 객체 생성
        scheduler = SRT_Scheduling(p_list)
    elif choice == 7: # HRT 스케줄링 실행 위한 객체 생성
        scheduler = HRN_Scheduling(p_list)

    scheduler.read_file()           # 각 스케줄링에 따른 메소드 실행
    scheduler.process_schedule()
    scheduler.calculate_metrics()

if __name__ == '__main__': # 메인
    while True: # 0번을 입력할 때까지 무한 반복
        print("0:종료, 1:FCFS, 2:SJF, 3:비선점 우선순위, 4:선점 우선순위, 5:RR, 6:SRT, 7:HRN")
        choice = int(input("실행하고자 하는 스케줄링 번호를 입력하세요: "))
        if choice == 0: # 0번을 입력하였을 경우, 종료에 해당
            print("프로그램을 종료합니다.")
            break
        elif choice == 1: # 1번을 입력하였을 경우 FCFS 스케줄링 실행
            print("FCFS 스케줄링")
            run_scheduling(choice)
        elif choice == 2: # 2번을 입력하였을 경우 SJF 스케줄링 실행
            print("SJF 스케줄링")
            run_scheduling(choice)
        elif choice == 3: # 3번을 입력하였을 경우 비선점 우선순위 스케줄링 실행
            print("비선점 우선순위 스케줄링")
            run_scheduling(choice)
        elif choice == 4: # 4번을 입력하였을 경우 선점 우선순위 스케줄링 실행
            print("선점 우선순위 스케줄링")
            run_scheduling(choice)
        elif choice == 5: # 5번을 입력하였을 경우 RR 스케줄링 실행
            print("RR 스케줄링")
            run_scheduling(choice)
        elif choice == 6: # 6번을 입력하였을 경우 SRT 스케줄링 실행
            print("SRT 스케줄링")
            run_scheduling(choice)
        elif choice == 7: # 7번을 입력하였을 경우 HRN 스케줄링 실행
            print("HRN 스케줄링")
            run_scheduling(choice)
        else: # 잘못된 번호를 입력하였을 경우 반복문으로 되돌아가기
            print("잘못된 입력입니다.")
            continue