import queue

class HRN_Scheduling:
    def __init__(self, p_list):
        self.queue = queue.Queue()
        self.p_num = 0
        self.time_slice = 0
        self.P_list = []
        self.P_state = []
        self.wait = []
        self.turn = []
        self.response = []
        self.response_time = 2

        self.p_list = p_list

    def read_file(self):
        self.p_num = int(self.p_list[0])
        self.time_slice = int(self.p_list[-1])
        self.P_list = [item.split(' ') for item in self.p_list[1:-1]]

    def process_schedule(self): # CPU scheduling 작업을 수행하는 함수
        self.P_list.sort(key=lambda x: int(x[1])) # 도착 시간을 기준으로 오름차순 정렬

        self.queue.put(self.P_list[0]) # 큐에 가장 먼저 도착한 프로세스 삽입

        total = 0

        for i in range(len(self.P_list)): # 저장된 프로세스 수만큼 반복
            process = self.queue.get() # 큐에서 저장된 프로세스 꺼내 변수에 저장
            p_id, arrive, execute = process[0], int(process[1]), int(process[2]) # 프로세스 아이디, 도착 시간, 실행 시간 순으로 각 변수에 저장

            '''응답 시간 계산'''
            if arrive == 0: # HRN의 경우, 도착 시간이 0인 프로세스는 도착 시간에 response_time을 더하여 응답시간 계산
                self.response.append(arrive + self.response_time)
            else: # 도착 시간이 0이 아닌 경우, 응답시간은 현재 프로세스가 작업을 시작하기 이전까지 진행된 total 변수에 response_time을 더한 값
                self.response.append(total + self.response_time)

            total += execute # 응답 시간 계산이 끝났으므로 total 변수에 현재 도착한 프로세스의 실행 시간 누적

            self.P_state.append([p_id, arrive, execute, total]) # 프로세스 상태를 저장하는 P_state 리스트에 프로세스 정보 추가

            for j in range(execute): # 간트 차트 출력을 위해 도착한 프로세스 이름을 해당 프로세스의 실행시간 만큼 출력
                print('[', p_id, ']', end='')

            tmp_list = [] # 아직 실행되지 않은 프로세스들을 tmp_list에 저장
            priority = []
            self.queue = queue.Queue() # 큐 내용 초기화
            pos = []

            for j in range(len(self.P_list)): # 프로세스 수만큼 반복
                for k in range(len(self.P_state)): # 현재 실행된 프로세스 수만큼 반복
                    if self.P_list[j][0] in self.P_state[k]: # 이미 실행된 프로세스라면
                        pos.append(self.P_list.index(self.P_list[j])) # pos에 해당 프로세스의 인덱스 위치 저장
            
            for j in range(len(self.P_list)):   # 아직 실행되지 않은 프로세스 검사
                if j not in pos: # 아직 실행되지 않은 프로세스라면
                    tmp_list.append(self.P_list[j]) # tmp_list에 프로세스 정보 추가

            for j in range(len(tmp_list)): # tmp_list에 저장된 프로세스들의 우선순위 계산
                tmp_wait = total - int(tmp_list[j][1]) # 프로세스의 대기 시간 계산
                exe = int(tmp_list[j][2])
                if tmp_wait >= 0: # 구한 대기 시간을 바탕으로 priority 리스트에 현재 프로세스 정보 및 우선순위 추가
                    priority.append([tmp_list[j][0], tmp_list[j][1], exe, (tmp_wait + exe) / exe])

            priority.sort(key=lambda x: x[3], reverse=True) # priority에 저장된 값을 우선순위가 높은 순으로 정렬
            for j in range(len(priority)):
                self.queue.put(priority[j]) # 우선순위대로 정렬된 프로세스를 큐에 삽입

            if arrive == 0: # 도착시간이 0일 경우
                self.wait.append(arrive)
            elif len(self.P_state) > 1:     # 할당된 프로세스의 수가 2개 이상일 경우
                self.wait.append(self.P_state[i - 1][3] - self.P_state[i][1]) # 대기시간 계산하여 리스트에 추가

            self.turn.append(self.wait[i] + execute) # 계산된 대기시간을 바탕으로 반환 시간 계산하여 저장

    def calculate_metrics(self): # 계산된 실행 시간, 응답 시간, 반환 시간을 출력하는 함수
        print(flush=True)

        ''' 대기 시간, 평균 대기 시간 출력 '''
        print("----" * 5)
        for i in range(len(self.wait)):
            print('[', self.P_state[i][0], ']', "대기 시간: ", self.wait[i]) # 각 프로세스별 대기 시간 출력
        avg_wait = round(sum(self.wait) / len(self.wait), 2) # 평균 대기 시간 계산
        print("평균 대기 시간: ", avg_wait) # 평균 대기 시간 출력
        print("----" * 5)

        ''' 응답 시간, 평균 응답 시간 출력 '''
        print("----" * 5)
        for i in range(len(self.response)):
            print('[', self.P_state[i][0], ']', "응답 시간: ", self.response[i]) # 각 프로세스별 응답 시간 출력
        avg_response = round(sum(self.response) / len(self.response), 2) # 평균 응답 시간 계산
        print("평균 응답 시간: ", avg_response) # 평균 응답 시간 출력
        print("----" * 5)

        ''' 반환 시간, 평균 반환 시간 출력 '''
        print("----" * 5)
        for i in range(len(self.turn)):
            print('[', self.P_state[i][0], ']', "반환 시간: ", self.turn[i]) # 각 프로세스별 반환 시간 출력
        avg_turn = round(sum(self.turn) / len(self.turn), 2) # 평균 반환 시간 계산
        print("평균 반환 시간: ", avg_turn) # 평균 반환 시간 출력
        print("----" * 5)