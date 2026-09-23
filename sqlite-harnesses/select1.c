#include "sqlite3.h"

int main(void) {
  sqlite3 *database = 0;
  sqlite3_stmt *statement = 0;
  int result = 1;

  if( sqlite3_open(":memory:", &database) != SQLITE_OK ) goto done;
  if( sqlite3_prepare_v2(database, "SELECT 1", -1, &statement, 0) != SQLITE_OK ) {
    goto done;
  }
  if( sqlite3_step(statement) == SQLITE_ROW && sqlite3_column_int(statement, 0) == 1 ) {
    result = 0;
  }

done:
  if( statement ) sqlite3_finalize(statement);
  if( database ) sqlite3_close(database);
  return result;
}
