* Some words are prohibited and can't be used is the query in anyways, even in
  a select query:
  - delete
  - drop
  - insert
  - alter
  - truncate
  - execute
  - create
  - update

See biocell_modelo_consultas_sql module to fix this issue.

* checking SQL request by execution and rollback is disabled in this module
  since variables features has been introduced. This can be fixed by
  overloading _prepare_request_check_execution() function.

* Move modules biocell_modelo_consultas_sql and biocell_descarga_consultas_sql to oca/reporting-engine for version 15
