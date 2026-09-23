volatile int answer_value;

__attribute__((noinline))
int answer(int value) {
  answer_value = value;
  return answer_value;
}

int main(void) {
  volatile int value = 42;
  return answer(value) == 42 ? 0 : 1;
}
