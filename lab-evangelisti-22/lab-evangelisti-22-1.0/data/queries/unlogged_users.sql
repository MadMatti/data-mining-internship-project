-- SELECT u.user_id, u.givenname 
-- FROM public.users u 
-- WHERE NOT EXISTS (SELECT l.user_id  
--                   FROM public.logs l
--                   WHERE u.user_id  = l.user_id)

-- SELECT u.user_id 
-- FROM public.users u  
-- EXCEPT 
-- SELECT l.user_id
-- FROM logs l

select u.user_id, u.givenname
from public.users u
left join public.logs l
    on u.user_id = l.user_id
where l.id is NULL
