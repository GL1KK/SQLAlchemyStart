from queries.core  import create_table_core, insert_data_core, select_workers_core, update_workers_core
from queries.orm  import create_table_orm, insert_table_orm, select_workers_orm, select_resumes_avg_compensation, join_cte_subquery_window_func #update_workers_orm
import asyncio

create_table_orm()
insert_table_orm()
# select_workers_core()
# update_workers_core()
select_workers_orm()
# update_workers_orm()
select_resumes_avg_compensation()
asyncio.run(join_cte_subquery_window_func())
