-- SEMPLICE ELENCO DEI DEVICES UTILIZZATI DA PIU' USERS
-- select l.device_id
-- from public.logs l 
-- group by l.device_id
-- having 
-- 	count(distinct l.user_id) > 1

-- ELENCO LOGS SUI DEVICE CONDIVISI, RAGGRUPPATI PER device_id E user_id
select l2.device_id, l2.devicedisplayname, l2.user_id, l2.userdisplayname
from (
	select l.device_id
	from public.logs l
	group by l.device_id
	having 
		count(distinct l.user_id) > 1
) as MultiLog
inner join public.logs l2 on MultiLog.device_id = l2.device_id
group by l2.device_id, l2.devicedisplayname, l2.user_id, l2.userdisplayname
order by l2.device_id, l2.user_id

-- ELENCO DI TUTTI I LOGS EFFETTUATI SUI DEVICE CONDIVISI, ORDINATI PER device_id, user_id
-- select l2.device_id, l2.devicedisplayname, l2.user_id, l2.userdisplayname
-- from (
-- 	select l.device_id
-- 	from public.logs l
-- 	group by l.device_id
-- 	having 
-- 		count(distinct l.user_id) > 1
-- ) as MultiLog
-- inner join public.logs l2 on MultiLog.device_id = l2.device_id
-- order by l2.device_id, l2.user_id