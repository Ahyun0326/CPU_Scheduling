class RoundRobin_Scheduling:
    def __init__(self, p_list):
        self.queue = []
        self.p_num = 0
        self.time_slice = 0
        self.P_list = []
        self.P_state = []
        self.P_name = []
        self.P_arrive = []
        self.P_execute = []
        self.P_priority = []
        self.wait = []
        self.turn = []
        self.response = []
        self.response_time = 2
        self.curr_time = 0
        self.total_time = 0

        self.p_list = p_list

    def read_file(self):
        self.p_num = int(self.p_list[0])
        self.time_slice = int(self.p_list[-1])
        self.P_list = [item.split(' ') for item in self.p_list[1:-1]]

    def process_schedule(self): # CPU scheduling 작업을 수행하는 함수
        # 도착 시간을 기준으로 오름차순 정렬
        self.P_list.sort(key=lambda x: x[1]) # 도착 시간을 기준으로 오름차순 정렬

        for i in range(len(self.P_list)): # 프로세스 이름, 도착 시간, 실행 시간, 우선 순위를 각 리스트에 저장
            self.P_name.append(self.P_list[i][0])
            self.P_arrive.append(int(self.P_list[i][1]))
            self.P_execute.append(int(self.P_list[i][2]))
            self.P_priority.append(int(self.P_list[i][3]))

        self.P_state = [[0] for i in range(len(self.P_list))] # P_state 2차원 리스트를 프로세스의 개수만큼 생성한 후, 0으로 초기화
        self.wait = [[] for i in range(len(self.P_list))] # wait 2차원 리스트를 프로세스의 개수만큼 생성
        self.turn = [[] for i in range(len(self.P_list))] # turn 2차원 리스트를 프로세스의 개수만큼 생성
        self.total_time = sum(self.P_execute) # while문 실행을 위해 프로세스의 전체 작업 시간을 total_time에 저장
        pos = 0 # 프로세스 위치를 기억할 임시 변수

        while (self.curr_time < self.total_time): # curr_time이 total_time보다 작다면 반복

            # 가장 먼저 도착한 프로세스를 할당된 타임 슬라이스 만큼 실행
            for i in range(self.P_execute[0]):

                # 도착 시간이 0인 프로세스의 경우, 처음 대기 시간이 0
                if self.P_arrive[0] == self.curr_time:
                    self.wait[0] = [self.P_list[0][0], 0]
                    self.response.append(self.response_time) # 응답 시간이 response_time과 같으므로 response_time을 저장

                print('[', self.P_list[0][0], ']', end='') # 처음 도착한 프로세스 출력
                self.curr_time += 1  # 한 번 실행했으므로 curr_time 증가

                self.P_state[0] = [self.P_list[0][0], self.curr_time] # 프로세스의 이름과 현재까지의 진행 시간 저장

                if (self.curr_time != 0 and self.curr_time in self.P_arrive): # 프로세스 진행 도중 중간에 도착한 값이 있다면
                    pos = self.P_arrive.index(self.curr_time) # 프로세스의 인덱스 위치를 알기 위해 현재 도착한 프로세스의 위치를 pos에 저장
                    tmp = [self.P_list[pos][0], int(self.P_list[pos][1]), int(self.P_list[pos][2])]
                    self.queue.append(tmp) # 큐에 도착한 프로세스 저장

                # 타임 슬라이스만큼 실행을 완료하면 큐의 마지막에 삽입 후 반복문 빠져나오기
                if (self.curr_time == self.time_slice):
                    tmp = [self.P_list[0][0], int(self.P_list[0][1]), int(self.P_list[0][2]) - self.time_slice]
                    self.queue.append(tmp)
                    break

            curr_process = None
            while (len(self.queue) > 0): # 큐가 빌 때까지 반복

                curr_process = self.queue.pop(0) # 큐에서 프로세스 꺼내기

                if curr_process[0] in self.P_name: # 대기 시간 계산을 위해 프로세스의 인덱스 위치 확인
                    pos = self.P_name.index(curr_process[0])

                    if curr_process[2] == self.P_execute[pos]: # 처음 실행하는 프로세스라면
                        # 현재 시간에서 도착 시간을 뺀 값을 대기 시간으로 저장
                        self.wait[pos] = [curr_process[0], self.curr_time - curr_process[1]]
                        self.response.append(self.curr_time + self.response_time)
                    else: # 처음 실행하는 프로세스가 아니라면
                        # 현재 도착한 시간에서 자신이 이전에 실행을 완료했던 시점의 시간을 뺀 값을 더하여 대기 시간에 저장
                        tmp_wait = self.wait[pos][1] + self.curr_time - self.P_state[pos][1]
                        self.wait[pos] = [curr_process[0], tmp_wait]

                cnt = 0
                for i in range(curr_process[2]):    # 현재 프로세스의 실행 시간만큼 반복

                    print('[', curr_process[0], ']', end='') # 간트 차트 출력을 위해 프로세스 이름 출력
                    self.curr_time += 1  # curr_time 1 증가
                    curr_process[2] -= 1 # 한 번 실행했으므로 실행 시간 1 감소
                    cnt += 1 # 타임 슬라이스만큼 실행했는지 검사하기 위해 cnt 값 1 증가

                    # 프로세스 실행 도중에 도착한 값이 있다면 해당 프로세스 큐에 넣기
                    if (self.curr_time in self.P_arrive):
                        pos = self.P_arrive.index(self.curr_time)
                        tmp = [self.P_list[pos][0], int(self.P_list[pos][1]), int(self.P_list[pos][2])]
                        self.queue.append(tmp)

                    # 프로세스가 할당된 시간만큼 작업을 완료했다면 반복문 빠져나오기
                    if curr_process[2] == 0:
                        break

                    if cnt == self.time_slice: # 타임 슬라이스만큼 실행을 완료했다면
                        pos = self.P_name.index(curr_process[0]) # 해당 프로세스의 인덱스 위치 구하기
                        # 대기 시간을 구하기 위해 현재까지 실행된 프로세스의 시점 저장
                        self.P_state[pos] = [curr_process[0], self.curr_time]
                        tmp = [curr_process[0], curr_process[1], curr_process[2]]
                        self.queue.append(tmp) #큐의 마지막에 프로세스 삽입 후, 반복문 빠져나오기
                        break
            break

    def calculate_metrics(self): # 계산된 실행 시간, 응답 시간, 반환 시간을 출력하는 함수
        print(flush=True)

        ''' 대기 시간, 평균 대기 시간 출력 '''
        print("----" * 5)
        wait_sum = 0
        for i in range(len(self.wait)):
            print('[', self.wait[i][0], ']', "대기 시간: ", self.wait[i][1]) # 각 프로세스별 대기 시간 출력
            wait_sum += self.wait[i][1]
        avg_wait = round(wait_sum / len(self.wait), 2) # 평균 대기 시간 계산
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
        turn_sum = 0
        for i in range(len(self.turn)):
            self.turn[i] = [self.wait[i][0], self.wait[i][1] + self.P_execute[i]]
            print('[', self.turn[i][0], ']', "반환 시간: ", self.turn[i][1]) # 각 프로세스별 반환 시간 출력
            turn_sum += self.turn[i][1] # 평균 반환 시간 계산
        avg_turn = round(turn_sum / len(self.turn), 2)
        print("평균 반환 시간: ", avg_turn) # 평균 반환 시간 출력
        print("----" * 5)