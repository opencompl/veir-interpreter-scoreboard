#include "sqlite3.h"

int main(void) {
  return sqlite3_libversion_number() == SQLITE_VERSION_NUMBER ? 0 : 1;
}
