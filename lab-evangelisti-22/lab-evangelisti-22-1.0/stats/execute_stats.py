import sys
from datetime import datetime, timedelta

def create_date_obj(period):
    today = datetime.now()
    start_date = (today - timedelta(days=period, hours=today.hour, minutes=today.minute, seconds=today.second)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return start_date

def far_logs(conn, distance, delta_time, period):
    start_date = create_date_obj(period)
    cur = conn.cursor()
    sql_find = '''select *
                  from public.log_difference ld
                  where ld.dist_diff > (%s) and extract(epoch from ld.time_diff)/60 < (%s)
                        and ld.prec_time >= (%s)'''
    cur.execute(sql_find, (distance, delta_time, start_date))
    logs = cur.fetchall()
    return logs

def unlogged_user(conn, period):
    start_date = create_date_obj(period)
    cur = conn.cursor()
    sql_find = '''select u.user_id, u.givenname
                  from public.users u
                  left join public.logs l
	                on u.user_id = l.user_id and l.createdatetime > (%s)
                  where l.id is null'''
    cur.execute(sql_find, (start_date,))
    data = cur.fetchall()
    return data

def unused_devices(conn, period):
    start_date = create_date_obj(period)
    cur = conn.cursor()
    sql_find = '''SELECT d.device_id, d.displayname
                  FROM public.devices d
                  LEFT JOIN public.logs l
                    on d.device_id = l.device_id and l.createdatetime > (%s)
                  WHERE l.id is NULL'''
    cur.execute(sql_find, (start_date,))
    data = cur.fetchall()
    return data

def multilogs_devices(conn, period):
    start_date = create_date_obj(period)
    cur = conn.cursor()
    sql_find = '''select l2.device_id, l2.devicedisplayname, l2.user_id, l2.userdisplayname
                  from (
	                    select l.device_id
	                    from public.logs l
	                    group by l.device_id
	                    having 
		                count(distinct l.user_id) > 1
                        ) as MultiLog
                  inner join public.logs l2 
                    on MultiLog.device_id = l2.device_id
                  where l2.createdatetime >= (%s)
                  group by l2.device_id, l2.devicedisplayname, l2.user_id, l2.userdisplayname
                  order by l2.device_id, l2.user_id'''
    cur.execute(sql_find, (start_date,))
    data = cur.fetchall()
    return data

def user_ureg_devices(conn, period):
    start_date = create_date_obj(period)
    cur = conn.cursor()
    sql_find = '''with only_registered as (
	                    select l2.user_id  
	                    from public.logs l2
	                    where l2.device_id is not null)
                  select l.user_id, l.userdisplayname 
                  from public.users u
                  left join public.logs l
                    on u.user_id = l.user_id
                  where l.device_id is null and l.user_id not in (select user_id from only_registered)
                        and l.createdatetime >= (%s)
                  group by l.user_id, l.userdisplayname'''
    cur.execute(sql_find, (start_date,))
    data = cur.fetchall()
    return data