import SimpleTable
import click
import os
import matplotlib.pyplot as plt
from jinja2 import Template
import sys
#import database tools as well that has simple table definitions



@click.command()
@click.option('--dry_run', is_flag=True, default=False,
help="Dry run")

def tables(dry_run):
	if dry_run:
		cc.backend='fake'

	a = Table(table_schema="z", 
	short_table_name="table1", 
	date_column="date")

	final_table= SimpleTable(
	indices=['id'],
	table_schema='z',
	short_table_name='made_up_table',
	src_table=a,
	fixed = False,
	days_at_a_time=10,
	use_format_method=True,
	contents_sql= """
	Enter desired query (as an example we will use 3 variables)
	and from clause will look like this: FROM {self.input_table.table_name} a
	""",
	    
	on_clause= "existing.column_goes_here=incoming.column_goes_here AND existing.column_goes_here = incoming.column_goes_here",

	when_matched_clause = """update set 
	column_goes_here = incoming.column_goes_here""",

	when_not_matched_clause = """insert 
	(column_goes_here,column_goes_here,column_goes_here)
	        values 
	        (incoming.column_goes_here,incoming.column_goes_here,incoming.column_goes_here)""")

	final_table.substitutions = {"self": final_table}
	final_table.update_range(date_range = date() << 100, new=False, step_days=50)
