with only_registered as (
	select l2.user_id  
	from public.logs l2
	where l2.device_id is not null)
select l.user_id, l.userdisplayname 
from public.users u
left join public.logs l
    on u.user_id = l.user_id
where l.device_id is null and l.user_id not in (select user_id from only_registered)
group by l.user_id, l.userdisplayname