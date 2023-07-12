class Piority_Scheduling:
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
        self.P_list.sort(key=lambda x: x[1]) # 도착 시간을 기준으로 오름차순 정렬

        for i in range(len(self.P_list)):   # 프로세스 이름, 도착 시간, 실행 시간, 우선 순위를 각 리스트에 저장
            self.P_name.append(self.P_list[i][0])
            self.P_arrive.append(int(self.P_list[i][1]))
            self.P_execute.append(int(self.P_list[i][2]))
            self.P_priority.append(int(self.P_list[i][3]))

        self.P_state = [[0] for i in range(len(self.P_list))] # P_state 2차원 리스트를 프로세스의 개수만큼 생성한 후, 0으로 초기화
        self.wait = [[0] for i in range(len(self.P_list))] # wait 2차원 리스트를 프로세스의 개수만큼 생성한 후, 0으로 초기화
        self.response = [[] for i in range(len(self.P_list))] # response 2차원 리스트를 프로세스의 개수만큼 생성한 후, 0으로 초기화
        self.turn = [[] for i in range(len(self.P_list))] # turn 2차원 리스트를 프로세스의 개수만큼 생성한 후, 0으로 초기화
        self.total_time = sum(self.P_execute) # while문 실행을 위해 프로세스의 전체 작업 시간을 total_time에 저장
        pos = 0 # 프로세스 위치를 기억할 임시 변수

        while (self.curr_time < self.total_time): # curr_time이 total_time보다 작다면 반복

            # 가장 먼저 도착한 프로세스 실행
            for i in range(self.P_execute[0]): # 프로세스의 실행 시간만큼 반복

                if self.P_arrive[0] == self.curr_time: # 도착 시간이 0인 프로세스의 경우, 처음 대기 시간이 0
                    self.wait[0] = [self.P_list[0][0], 0]
                    self.response[0] = self.response_time # 응답 시간이 response_time과 같으므로 response_time을 저장

                print('[', self.P_list[0][0], ']', end='') # 처음 도착한 프로세스 출력
                self.curr_time += 1  # 한 번 실행했으므로 curr_time 1 증가
                self.P_state[0] = [self.P_list[0][0], self.curr_time] # 프로세스의 이름과 현재까지의 진행 시간 저장

                if (self.curr_time != 0 and self.curr_time in self.P_arrive): # 프로세스 진행 도중 중간에 도착한 값이 있다면 우선 순위 비교
                    pos = self.P_arrive.index(self.curr_time) # 프로세스의 인덱스 위치를 알기 위해 현재 도착한 프로세스의 위치를 pos에 저장
                    # 도착한 프로세스의 우선순위가 현재 프로세스의 우선순위보다 크다면
                    if self.P_priority[0] > self.P_priority[pos]:
                        tmp = [self.P_list[0][0], int(self.P_list[0][1]), int(self.P_list[0][2]) - self.curr_time, self.P_priority[0]]
                        self.queue.append(tmp) # 큐에 현재까지 실행된 프로세스 상태 저장

                        tmp = [self.P_list[pos][0], int(self.P_list[pos][1]), int(self.P_list[pos][2]), self.P_priority[pos]]
                        self.queue.append(tmp)
                        break   # 현재 반복문 빠져나오기
                    # 도착한 프로세스의 우선순위가 현재 프로세스의 우선순위보다 작다면
                    else:
                        tmp = [self.P_list[pos][0], int(self.P_list[pos][1]), int(self.P_list[pos][2]), self.P_priority[pos]]
                        self.queue.append(tmp) # 큐에 도착한 프로세스 저장 후, 현재 실행 중인 프로세스 계속 실행

            while (self.curr_time <= max(self.P_arrive)): # 도착 시간이 가장 큰 프로세스가 도착할 때까지 반복
                # 우선순위대로 큐 정렬, 우선순위가 같은 프로세스가 있다면 먼저 도착한 프로세스 순서대로 정렬
                self.queue.sort(key=lambda x: (x[3], x[1]))

                # 큐에서 맨 앞에 있는 프로세스 꺼내기. 즉, 우선순위가 가장 높은 프로세스 꺼내기
                curr_process = self.queue.pop(0)
                self.wait[pos] = [curr_process[0], self.curr_time - curr_process[1]] # 큐에서 꺼낸 프로세스의 대기 시간 저장
                self.response[pos] = self.curr_time + self.response_time # 큐에서 꺼낸 프로세스의 응답 시간 저장   

                for i in range(curr_process[2]): # 프로세스의 실행시간만큼 반복
                    print('[', curr_process[0], ']', end='') # 간트차트 출력을 위해 프로세스 출력
                    self.curr_time += 1 # curr_time 1 증가
                    curr_process[2] -= 1 # 한 번 실행했으므로 실행 시간 1 감소

                    # 프로세스 진행 도중 중간에 도착한 값이 있다면 우선 순위 비교
                    if (self.curr_time != 0 and self.curr_time in self.P_arrive):
                        # 도착한 프로세스의 인덱스 위치를 알기 위해 현재 도착한 프로세스의 위치를 curr_pos에 저장
                        curr_pos = self.P_arrive.index(self.curr_time)
                        # 도착한 프로세스의 우선순위가 현재 실행 중인 프로세스의 우선순위보다 크다면
                        if self.P_priority[pos] > self.P_priority[curr_pos]:
                            tmp = [self.P_list[pos][0], int(self.P_list[pos][1]), curr_process[2], self.P_priority[pos]]
                            self.P_state[pos] = [curr_process[0], self.curr_time] # 프로세스 이름과 현재 진행 시간 저장
                            self.queue.append(tmp) # 큐에 현재까지 실행된 프로세스 상태 저장

                            tmp = [self.P_list[curr_pos][0], int(self.P_list[curr_pos][1]), self.P_execute[curr_pos],
                                   self.P_priority[curr_pos]]
                            self.queue.append(tmp) # 큐에 도착한 프로세스 저장
                            pos = curr_pos # pos 인덱스 값을 현재 도착한 프로세스의 인덱스 값으로 변경
                            break # 현재 반복문 빠져나오기
                        # 도착한 프로세스의 우선순위가 현재 실행 중인 프로세스의 우선순위보다 작다면
                        else:
                            tmp = [self.P_list[curr_pos][0], int(self.P_list[curr_pos][1]), int(self.P_list[curr_pos][2]),
                                   self.P_priority[curr_pos]]
                            self.queue.append(tmp)  # 현재 도착한 프로세스 큐에 저장

            self.P_state[pos] = [curr_process[0], self.curr_time] # 마지막으로 실행 완료한 프로세스 상태 저장
            # 큐에 저장된 프로세스를 우선순위 순서대로 정렬, 우선순위가 같으면 먼저 도착한 순서대로 정렬
            self.queue.sort(key=lambda x: (x[3], x[1]))
            while (len(self.queue) > 0):  # 큐가 빌 때까지 반복
                # 큐에 저장된 프로세스를 차례대로 꺼내서 실행
                curr_process = self.queue.pop(0)
                pos = self.P_name.index(curr_process[0]) # 꺼낸 프로세스의 인덱스 위치를 저장

                if self.wait[pos][0] == 0 and self.P_state[pos][0] == 0: # 한 번도 실행되지 않은 프로세스일 경우
                    self.response[pos] = self.curr_time + self.response_time # 응답 시간 저장
                    # 현재 시간에서 도착시간을 뺀 값을 대기 시간으로 저장
                    self.wait[pos] = [curr_process[0], self.curr_time - self.P_arrive[pos]]
                else: # 한 번 이상 실행된 프로세스일 경우
                    # 대기 시간 업데이트
                    self.wait[pos] = [curr_process[0], self.curr_time - self.P_state[pos][1] + self.wait[pos][1]]
                for i in range(curr_process[2]): # 프로세스 실행시간만큼 반복
                    print('[', curr_process[0], ']', end='') # 간트차트 출력을 위해 프로세스 이름 출력
                    self.curr_time += 1 # curr_time 1 증가
            break
    def calculate_metrics(self): # 계산된 실행 시간, 응답 시간, 반환 시간을 출력하는 함수
        print(flush=True)

        ''' 대기 시간, 평균 대기 시간 출력 '''
        wait_sum = 0
        print("----" * 5)
        for i in range(len(self.wait)):
            print('[', self.wait[i][0], ']', "대기 시간: ", self.wait[i][1]) # 각 프로세스별 대기 시간 출력
            wait_sum += self.wait[i][1]
        avg_wait = round(wait_sum / len(self.wait), 2) # 평균 대기 시간 계산
        print("평균 대기 시간: ", avg_wait) # 평균 대기 시간 출력
        print("----" * 5)

        ''' 응답 시간, 평균 응답 시간 출력 '''
        print("----" * 5)
        for i in range(len(self.response)):
            print('[', self.wait[i][0], ']', "응답 시간: ", self.response[i]) # 각 프로세스별 응답 시간 출력
        print("평균 응답 시간: ", round(sum(self.response) / len(self.response), 2)) # 평균 응답 시간 출력
        print("----" * 5)

        ''' 반환 시간, 평균 반환 시간 출력 '''
        turn_sum = 0
        print("----" * 5)
        for i in range(len(self.turn)):
            self.turn[i] = [self.wait[i][0], self.wait[i][1] + self.P_execute[i]]
            print('[', self.turn[i][0], ']', "반환 시간: ",  self.turn[i][1]) # 각 프로세스별 반환 시간 출력
            turn_sum += self.turn[i][1] # 평균 반환 시간 계산
        avg_turn = round(turn_sum / len(self.turn), 2)
        print("평균 반환 시간: ", avg_turn) # 평균 반환 시간 출력
        print("----" * 5)