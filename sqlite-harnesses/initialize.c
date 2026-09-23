#include "sqlite3.h"

int main(void) {
  if( sqlite3_initialize() != SQLITE_OK ) return 1;
  return sqlite3_shutdown() == SQLITE_OK ? 0 : 1;
}
