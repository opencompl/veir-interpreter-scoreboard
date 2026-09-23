#include "sqlite3.h"

int main(void) {
  sqlite3 *database = 0;
  if( sqlite3_open(":memory:", &database) != SQLITE_OK ) {
    if( database ) sqlite3_close(database);
    return 1;
  }
  return sqlite3_close(database) == SQLITE_OK ? 0 : 1;
}
