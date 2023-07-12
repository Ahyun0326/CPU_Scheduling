import queue

class Non_Preemptive_Priority_Scheduling:
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

    def process_schedule(self):  # CPU scheduling 작업을 수행하는 함수

        self.P_list.sort(key=lambda x: x[1]) # 도착 시간을 기준으로 오름차순 정렬

        for i in range(len(self.P_list)): # 만약 도착 시간이 0인 것이 있다면 해당 프로세스만 큐에 삽입
            if (self.P_list[i][1]) == '0':
                self.queue.put(self.P_list[i])

        # 우선순위가 높은 것을 기준으로 오름차순 정렬, 우선순위가 같을 경우 먼저 도착한 프로세스를 기준으로 정렬
        self.P_list.sort(key=lambda x: (x[3], x[1]))
        for i in range(len(self.P_list)):
            if (self.P_list[i][1] != '0'):
                self.queue.put(self.P_list[i]) # 정렬된 순서대로(우선순위가 높은 순으로) 큐에 삽입

        total = 0

        for i in range(len(self.P_list)):  # 저장된 프로세스 수만큼 반복
            process =  self.queue.get() # 큐에서 저장된 프로세스 꺼내 변수에 저장

            # 프로세스 아이디, 도착 시간, 실행 시간 순으로 각 변수에 저장
            p_id, arrive, execute = process[0], int(process[1]), int(process[2])

            '''응답 시간 계산'''
            if arrive == 0: # 비선점 우선순위의 경우, 도착 시간이 0인 프로세스는 도착 시간에 response_time을 더하여 응답시간 계산
                self.response.append(arrive + self.response_time)
            else: # 도착 시간이 0이 아닌 경우, 응답시간은 현재 프로세스가 작업을 시작하기 이전까지 진행된 total 변수에 response_time을 더한 값
                self.response.append(total + self.response_time)

            total += execute  # 다음 프로세스의 대기 시간 구하기 위해 현재까지의 프로세스 총 작업시간 저장
            self.P_state.append([p_id, arrive, execute, total]) #프로세스 상태를 저장하는 P_state 리스트에 프로세스 정보 추가


            ''' 간트 차트 출력 '''
            for j in range(execute):
                print('[', p_id, ']', end='')

            ''' 대기 시간 계산 '''
            if arrive == 0: # 현재 할당된 프로세스의 도착시간 0일 경우
                self.wait.append(arrive) # 대기 시간 0
            elif len(self.P_state) > 1: # 할당된 프로세스의 수가 2개 이상일 경우
                # 이전 프로세스가 실행을 마쳤을 때의 total 값에서 자신의 도착 시간을 뺀 값
                self.wait.append(self.P_state[i - 1][3] - self.P_state[i][1])

            ''' 반환 시간 계산 '''
            self.turn.append(self.wait[i] + execute) # 반환 시간은 구한 대기 시간에서 자신의 실행 시간을 더한 값

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
            print('[', self.P_state[i][0], ']', "반환 시간: ", self.turn[i])  # 각 프로세스별 반환 시간 출력
        avg_turn = round(sum(self.turn) / len(self.turn), 2) # 평균 반환 시간 계산
        print("평균 반환 시간: ", avg_turn) # 평균 반환 시간 출력
        print("----" * 5)
